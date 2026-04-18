"""Render benchmark plots for the GUIpi26 README.

Reads ``benchmarks/results.json`` and writes four PNG charts into
``benchmarks/plots/``:

* ``cold_start.png`` — startup latency (ms, lower is better)
* ``create_controls.png`` — time to instantiate 200 controls (ms, lower is better)
* ``paint_time.png`` — paint pass average (ms, lower is better)
* ``fps.png`` — sustained frames per second (higher is better)
* ``summary.png`` — 2x2 grid of all four
* ``speedup.png`` — relative speedup of GUIpi26 over Tkinter

Run::

    python benchmarks/plot_results.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.json"
OUT = HERE / "plots"

GUI_COLOR = "#005fb8"
TK_COLOR = "#9aa0a6"
GUI_LABEL = "GUIpi26"
TK_LABEL = "Tkinter"


def _bar(ax, values, *, ylabel, title, lower_is_better=True, fmt="{:.0f}"):
    bars = ax.bar([GUI_LABEL, TK_LABEL], values, color=[GUI_COLOR, TK_COLOR], width=0.55, edgecolor="white", linewidth=1.5)
    ax.set_ylabel(ylabel)
    direction = "lower is better" if lower_is_better else "higher is better"
    ax.set_title(f"{title}\n({direction})", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle="--", alpha=0.35)

    top = max(values) if values else 1.0
    ax.set_ylim(0, top * 1.18 if top > 0 else 1.0)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + top * 0.02,
            fmt.format(value),
            ha="center", va="bottom", fontsize=10, fontweight="bold",
        )


def _save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(HERE.parent)}")


def main():
    data = json.loads(RESULTS.read_text())
    g = data["guipi26"]
    t = data["tkinter"]

    plt.rcParams.update({
        "font.family": "Segoe UI",
        "font.size": 10,
        "axes.titleweight": "bold",
    })

    # --- Individual charts ---------------------------------------------
    fig, ax = plt.subplots(figsize=(5, 3.5))
    _bar(ax, [g["cold_start_ms"], t["cold_start_ms"]],
         ylabel="milliseconds", title="Cold start", fmt="{:.0f} ms")
    _save(fig, "cold_start.png")

    fig, ax = plt.subplots(figsize=(5, 3.5))
    _bar(ax, [g["create_ms"], t["create_ms"]],
         ylabel="milliseconds", title=f"Create {g['controls']} controls", fmt="{:.1f} ms")
    _save(fig, "create_controls.png")

    fig, ax = plt.subplots(figsize=(5, 3.5))
    _bar(ax, [g["paint_ms_avg"], t["paint_ms_avg"]],
         ylabel="milliseconds", title="Paint pass (avg)", fmt="{:.1f} ms")
    _save(fig, "paint_time.png")

    fig, ax = plt.subplots(figsize=(5, 3.5))
    _bar(ax, [g["fps_estimate"], t["fps_estimate"]],
         ylabel="frames per second", title="Sustained FPS",
         lower_is_better=False, fmt="{:.1f}")
    _save(fig, "fps.png")

    # --- 2x2 summary ---------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    _bar(axes[0, 0], [g["cold_start_ms"], t["cold_start_ms"]],
         ylabel="ms", title="Cold start", fmt="{:.0f} ms")
    _bar(axes[0, 1], [g["create_ms"], t["create_ms"]],
         ylabel="ms", title=f"Create {g['controls']} controls", fmt="{:.1f} ms")
    _bar(axes[1, 0], [g["paint_ms_avg"], t["paint_ms_avg"]],
         ylabel="ms", title="Paint pass (avg)", fmt="{:.1f} ms")
    _bar(axes[1, 1], [g["fps_estimate"], t["fps_estimate"]],
         ylabel="fps", title="Sustained FPS",
         lower_is_better=False, fmt="{:.1f}")
    fig.suptitle("GUIpi26 vs Tkinter — 200 controls, Windows 11", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _save(fig, "summary.png")

    # --- Speedup chart -------------------------------------------------
    speedups = {
        "Cold start": t["cold_start_ms"] / g["cold_start_ms"],
        "Create 200 controls": t["create_ms"] / g["create_ms"],
        "Paint pass": t["paint_ms_avg"] / g["paint_ms_avg"],
        "Sustained FPS": g["fps_estimate"] / t["fps_estimate"],
    }
    fig, ax = plt.subplots(figsize=(7, 4))
    names = list(speedups.keys())
    values = list(speedups.values())
    bars = ax.barh(names, values, color=GUI_COLOR, edgecolor="white", linewidth=1.5)
    ax.axvline(1.0, color="#9aa0a6", linestyle="--", linewidth=1, label="Tkinter baseline (1.0×)")
    ax.set_xlabel("speedup factor (×)")
    ax.set_title("How much faster is GUIpi26?\n(higher is better)", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, linestyle="--", alpha=0.35)
    ax.invert_yaxis()
    top = max(values)
    ax.set_xlim(0, top * 1.18)
    for bar, value in zip(bars, values):
        ax.text(value + top * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{value:.2f}×", va="center", fontsize=10, fontweight="bold")
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    _save(fig, "speedup.png")


if __name__ == "__main__":
    main()
