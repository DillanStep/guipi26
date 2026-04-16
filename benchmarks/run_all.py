"""Run both benchmarks and print a comparison table.

Usage:
    python benchmarks/run_all.py
    python benchmarks/run_all.py --controls 400 --paints 200 --runs 3
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, controls: int, paints: int) -> dict:
    proc = subprocess.run(
        [sys.executable, str(HERE / script),
         "--controls", str(controls),
         "--paints", str(paints)],
        capture_output=True, text=True, check=True,
    )
    last_line = proc.stdout.strip().splitlines()[-1]
    return json.loads(last_line)


def aggregate(runs: list[dict]) -> dict:
    keys = ["cold_start_ms", "create_ms", "paint_ms_avg", "paint_ms_p50", "paint_ms_p95", "fps_estimate"]
    out = {k: round(statistics.median(r[k] for r in runs), 2) for k in keys}
    out["library"] = runs[0]["library"]
    out["version"] = runs[0]["version"]
    out["controls"] = runs[0]["controls"]
    out["paint_count"] = runs[0]["paint_count"]
    return out


def fmt_row(label: str, a: float, b: float, unit: str = "ms", lower_is_better: bool = True) -> str:
    if a > 0 and b > 0:
        ratio = b / a if lower_is_better else a / b
        winner = "GUIpi26" if (a < b) == lower_is_better else "Tkinter"
        diff = f"{ratio:.2f}x faster ({winner})"
    else:
        diff = "-"
    return f"  {label:<22} {a:>10.2f} {unit}   {b:>10.2f} {unit}   {diff}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--paints", type=int, default=120)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    print(f"Running {args.runs} run(s) per library  "
          f"(controls={args.controls}, paints={args.paints})\n")

    g_runs, t_runs = [], []
    for i in range(args.runs):
        print(f"  run {i+1}/{args.runs} guipi26 ...", end=" ", flush=True)
        g_runs.append(run("bench_guipi26.py", args.controls, args.paints))
        print("ok")
        print(f"  run {i+1}/{args.runs} tkinter ...", end=" ", flush=True)
        t_runs.append(run("bench_tkinter.py", args.controls, args.paints))
        print("ok")

    g = aggregate(g_runs)
    t = aggregate(t_runs)

    print()
    print(f"GUIpi26 {g['version']}    vs    Tkinter {t['version']}")
    print(f"controls={g['controls']}  paints={g['paint_count']}  runs={args.runs}  (median)\n")
    print(f"  {'metric':<22} {'GUIpi26':>13}   {'Tkinter':>13}   winner")
    print("  " + "-" * 72)
    print(fmt_row("cold start",      g["cold_start_ms"],  t["cold_start_ms"]))
    print(fmt_row("create N controls", g["create_ms"],   t["create_ms"]))
    print(fmt_row("paint avg",        g["paint_ms_avg"], t["paint_ms_avg"]))
    print(fmt_row("paint p50",        g["paint_ms_p50"], t["paint_ms_p50"]))
    print(fmt_row("paint p95",        g["paint_ms_p95"], t["paint_ms_p95"]))
    print(fmt_row("fps estimate",     g["fps_estimate"], t["fps_estimate"], unit="fps", lower_is_better=False))
    print()

    out_path = HERE / "results.json"
    out_path.write_text(json.dumps({"guipi26": g, "tkinter": t}, indent=2))
    print(f"raw results -> {out_path}")


if __name__ == "__main__":
    main()
