"""Tkinter benchmark (apples-to-apples with bench_guipi26.py).

Builds an equivalent visual: a Toplevel window with a header Label and
`--controls` Frame "cards" laid out in a 10-wide grid, each containing a
title Label and a value Label. Times window-up, control creation, and
forced repaints.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
import tkinter as tk

PROCESS_START = time.perf_counter()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--paints", type=int, default=120)
    args = parser.parse_args()

    create_t0 = time.perf_counter()
    root = tk.Tk()
    root.title("Tkinter Benchmark")
    root.geometry("1200x800")
    root.configure(bg="#f3f3f3")

    tk.Label(
        root, text="Benchmark",
        font=("Segoe UI Semibold", 18),
        bg="#f3f3f3", fg="#1f1f1f",
    ).place(x=24, y=12, width=400, height=40)

    cols, cw, ch, gap = 10, 110, 70, 8
    cards: list[tk.Frame] = []
    for i in range(args.controls):
        col = i % cols
        row = i // cols
        x = 24 + col * (cw + gap)
        y = 60 + row * (ch + gap)
        card = tk.Frame(root, bg="#ffffff", highlightthickness=1, highlightbackground="#dcdcdc")
        card.place(x=x, y=y, width=cw, height=ch)
        tk.Label(card, text=f"C{i:03d}", bg="#ffffff", fg="#616161",
                 font=("Segoe UI", 9), anchor="w").place(x=8, y=6, width=cw - 16, height=16)
        tk.Label(card, text=str(i), bg="#ffffff", fg="#1f1f1f",
                 font=("Segoe UI Semibold", 16), anchor="w").place(x=8, y=24, width=cw - 16, height=28)
        cards.append(card)
    root.update_idletasks()
    create_ms = (time.perf_counter() - create_t0) * 1000.0

    # Cold start: time until the window is mapped + first idle drain.
    root.update()
    cold_ms = (time.perf_counter() - PROCESS_START) * 1000.0

    # Forced repaints. Tk doesn't expose a direct "repaint everything" hook
    # the way GDI's WM_PAINT does, so we mutate every card's value label and
    # call update() — that's the unit of work a Tk app pays per refresh.
    samples: list[float] = []
    value_labels = [card.winfo_children()[1] for card in cards]
    for n in range(args.paints):
        text = str(n)
        t0 = time.perf_counter()
        for lbl in value_labels:
            lbl.config(text=text)
        root.update()
        samples.append((time.perf_counter() - t0) * 1000.0)

    root.destroy()

    if samples:
        avg = sum(samples) / len(samples)
        s = sorted(samples)
        p50 = s[len(s) // 2]
        p95 = s[min(int(len(s) * 0.95), len(s) - 1)]
    else:
        avg = p50 = p95 = 0.0

    print(json.dumps({
        "library": "tkinter",
        "version": f"tcl/tk {tk.TkVersion} (Python {platform.python_version()})",
        "controls": args.controls,
        "cold_start_ms": round(cold_ms, 2),
        "create_ms": round(create_ms, 2),
        "paint_count": len(samples),
        "paint_ms_avg": round(avg, 3),
        "paint_ms_p50": round(p50, 3),
        "paint_ms_p95": round(p95, 3),
        "fps_estimate": round(1000.0 / avg, 1) if avg > 0 else 0.0,
    }))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
