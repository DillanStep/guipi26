"""UI safety linter for GUIpi26.

Scans engine + examples for common UI safety issues. Designed to run in CI as
part of the Guardian bot. Exits non-zero when any issues are found.

Checks:
  E001  use of eval()/exec() in widget code
  E002  bare 'except:' in event/callback handlers (swallows crashes silently)
  E003  while True without a sleep / break in a callback (UI freeze risk)
  E004  Window.run() without prior set_min_size() (resize crash risk)
  E005  TextInput / TextArea without max_length (unbounded input)
  E006  enable_scrolling(True) without any pinned status/footer
        (likely user can scroll their status bar away)
  E007  hard-coded absolute file paths in examples
  E008  ctypes.windll calls in examples (should go through engine)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Finding:
    __slots__ = ("code", "path", "line", "msg")

    def __init__(self, code: str, path: Path, line: int, msg: str):
        self.code = code
        self.path = path
        self.line = line
        self.msg = msg

    def format(self) -> str:
        rel = self.path.relative_to(ROOT).as_posix()
        return f"{rel}:{self.line}: {self.code} {self.msg}"


def iter_py(folder: Path):
    for p in folder.rglob("*.py"):
        if any(part in {".venv", "build", "dist", "__pycache__"} for part in p.parts):
            continue
        yield p


def check_file(path: Path) -> list[Finding]:
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError as exc:
        return [Finding("E000", path, exc.lineno or 1, f"syntax error: {exc.msg}")]

    findings: list[Finding] = []
    is_example = "examples" in path.parts

    enable_scrolling_seen = False
    pinned_seen = False
    set_min_size_seen = False
    run_call_line: int | None = None

    for node in ast.walk(tree):
        # E001 eval/exec
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"eval", "exec"}:
                findings.append(Finding("E001", path, node.lineno,
                    f"avoid {node.func.id}() in UI code"))

        # E002 bare except
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding("E002", path, node.lineno,
                "bare 'except:' swallows errors; use 'except Exception:'"))

        # E003 while True without break/sleep
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                has_break = any(isinstance(c, ast.Break) for c in ast.walk(node))
                has_sleep = any(
                    isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute)
                    and c.func.attr == "sleep"
                    for c in ast.walk(node)
                )
                # Allow message loops in engine (they call PeekMessage etc).
                if is_example and not (has_break or has_sleep):
                    findings.append(Finding("E003", path, node.lineno,
                        "while True without break/sleep can freeze the UI"))

        # Track Window.set_min_size / .run / enable_scrolling / pinned in examples
        if is_example and isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                if func.attr == "set_min_size":
                    set_min_size_seen = True
                elif func.attr == "run":
                    run_call_line = node.lineno
                elif func.attr == "enable_scrolling":
                    enable_scrolling_seen = True

        # pinned attribute assignment in examples
        if is_example and isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Attribute) and tgt.attr == "pinned":
                    pinned_seen = True

        # E005 TextInput/TextArea without max_length kwarg
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"TextInput", "TextArea"}:
                kwargs = {kw.arg for kw in node.keywords}
                if "max_length" not in kwargs:
                    findings.append(Finding("E005", path, node.lineno,
                        f"{node.func.attr}(...) without max_length is unbounded"))

        # E007 absolute paths in examples
        if is_example and isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if (len(v) >= 3 and v[1:3] == ":\\") or v.startswith("/home/") or v.startswith("/Users/"):
                findings.append(Finding("E007", path, node.lineno,
                    "hard-coded absolute path; use pathlib relative to __file__"))

        # E008 ctypes.windll in examples
        if is_example and isinstance(node, ast.Attribute) and node.attr == "windll":
            findings.append(Finding("E008", path, node.lineno,
                "examples should use guipi26 APIs, not raw ctypes.windll"))

    # E004 Window.run() without prior set_min_size()
    if is_example and run_call_line is not None and not set_min_size_seen:
        findings.append(Finding("E004", path, run_call_line,
            "Window.run() without set_min_size() — small windows can crash layout"))

    # E006 scrolling enabled but nothing pinned
    if is_example and enable_scrolling_seen and not pinned_seen:
        findings.append(Finding("E006", path, 1,
            "enable_scrolling(True) but no control marked .pinned = True "
            "(status bars/headers may scroll away)"))

    return findings


def main() -> int:
    targets = [ROOT / "guipi26", ROOT / "examples"]
    all_findings: list[Finding] = []
    for folder in targets:
        if not folder.exists():
            continue
        for p in iter_py(folder):
            all_findings.extend(check_file(p))

    if not all_findings:
        print("ui_safety_check: 0 issues found")
        return 0

    for f in all_findings:
        print(f.format())
    print(f"\nui_safety_check: {len(all_findings)} issue(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
