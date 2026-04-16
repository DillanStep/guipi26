"""GUIpi26 benchmark.

Measures:
  - cold_start_ms : time from process launch to first complete paint
  - paint_ms_avg  : average time per repaint with `--controls` controls visible
  - create_ms     : time to instantiate `--controls` controls

Outputs a single JSON object on stdout. Designed to be run as a subprocess by
benchmarks/run_all.py for a fair side-by-side comparison with Tkinter.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import sys
import threading
import time

import guipi26
from guipi26 import create_window, create_label, create_card
from guipi26.window import Window

WM_CLOSE = 0x0010
PROCESS_START = time.perf_counter()


def _patch_paint_timer(window: Window) -> list[float]:
    samples: list[float] = []
    original = window._paint

    def timed_paint() -> None:
        t0 = time.perf_counter()
        original()
        samples.append((time.perf_counter() - t0) * 1000.0)

    window._paint = timed_paint  # type: ignore[assignment]
    return samples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--paints", type=int, default=120)
    args = parser.parse_args()

    create_t0 = time.perf_counter()
    app = create_window("GUIpi26 Benchmark", 1200, 800)
    create_label(app, "Benchmark", x=24, y=12, width=400, height=40, style="title")
    cols, cw, ch, gap = 10, 110, 70, 8
    for i in range(args.controls):
        col = i % cols
        row = i // cols
        create_card(
            app, f"C{i:03d}", str(i),
            x=24 + col * (cw + gap),
            y=60 + row * (ch + gap),
            width=cw, height=ch,
            collision_safety=False,
        )
    create_ms = (time.perf_counter() - create_t0) * 1000.0

    paint_samples = _patch_paint_timer(app)
    cold = {"ms": 0.0}
    user32 = ctypes.windll.user32

    def driver() -> None:
        while not paint_samples:
            time.sleep(0.001)
        cold["ms"] = (time.perf_counter() - PROCESS_START) * 1000.0
        paint_samples.clear()  # drop warmup

        for _ in range(args.paints):
            target = len(paint_samples) + 1
            user32.InvalidateRect(app.hwnd, None, True)
            deadline = time.perf_counter() + 0.5
            while len(paint_samples) < target and time.perf_counter() < deadline:
                time.sleep(0.0005)

        user32.PostMessageW(app.hwnd, WM_CLOSE, 0, 0)

    threading.Thread(target=driver, daemon=True).start()
    app.mainloop()

    if paint_samples:
        avg = sum(paint_samples) / len(paint_samples)
        s = sorted(paint_samples)
        p50 = s[len(s) // 2]
        p95 = s[min(int(len(s) * 0.95), len(s) - 1)]
    else:
        avg = p50 = p95 = 0.0

    print(json.dumps({
        "library": "guipi26",
        "version": guipi26.__version__,
        "controls": args.controls,
        "cold_start_ms": round(cold["ms"], 2),
        "create_ms": round(create_ms, 2),
        "paint_count": len(paint_samples),
        "paint_ms_avg": round(avg, 3),
        "paint_ms_p50": round(p50, 3),
        "paint_ms_p95": round(p95, 3),
        "fps_estimate": round(1000.0 / avg, 1) if avg > 0 else 0.0,
    }))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
