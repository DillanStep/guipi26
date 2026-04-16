# Benchmarks

Honest, reproducible head-to-head between **GUIpi26** and **Tkinter** on identical workloads.

## Run it

```
python benchmarks/run_all.py
```

Common options:

```
python benchmarks/run_all.py --controls 400 --paints 200 --runs 5
```

The runner spawns each benchmark in a fresh Python process (so cold-start times are real), takes the **median** across `--runs`, and writes raw results to `benchmarks/results.json`.

## Plots

After running the benchmarks, render PNG charts (used in the project README) with:

```
python benchmarks/plot_results.py
```

Output lands in `benchmarks/plots/`:

- `summary.png` — 2x2 grid of all four metrics
- `speedup.png` — relative speedup factor over Tkinter
- `cold_start.png`, `create_controls.png`, `paint_time.png`, `fps.png` — individual charts

## What's measured

The same logical UI is built in each library: a header label and `--controls` "card" widgets in a 10-wide grid (each card is a bordered surface with a small caption and a large value).

| Metric | What it measures |
| --- | --- |
| `cold_start_ms` | Time from process launch to first complete paint of a populated window. |
| `create_ms` | Time to instantiate the window + every control. |
| `paint_ms_avg` / `p50` / `p95` | Wall-clock time per forced repaint cycle (averaged over `--paints` cycles, after a warmup paint is discarded). |
| `fps_estimate` | `1000 / paint_ms_avg`. Indicative ceiling for "what could this UI sustain if it painted continuously?" |

## How a paint is measured

- **GUIpi26** wraps `Window._paint` with a high-resolution timer. Each WM_PAINT cycle (clear background → composite all controls into the back buffer → BitBlt to screen) is one sample.
- **Tkinter** mutates every card's value `Label`, then calls `root.update()` — that's the unit of work a Tk app actually pays per refresh. Tk doesn't expose a "redraw everything" hook; this is the closest fair equivalent (and arguably _favors_ Tk because it only redraws dirty regions).

After the first sample lands, it's discarded as warmup so JIT-style first-call costs (font handles, brush caches) don't skew the average.

## Sample results (April 2026)

Windows 11, Python 3.9.13, 200 controls, 80 paints, 2 runs (median):

```
GUIpi26 0.1.0a1    vs    Tkinter tcl/tk 8.6

  metric                  GUIpi26         Tkinter         winner
  --------------------------------------------------------------------
  cold start             101.59 ms      1429.53 ms        14.07x  GUIpi26
  create N controls       48.82 ms       204.54 ms         4.19x  GUIpi26
  paint avg               20.98 ms        32.35 ms         1.54x  GUIpi26
  paint p50               20.78 ms        31.82 ms         1.53x  GUIpi26
  paint p95               22.79 ms        35.43 ms         1.55x  GUIpi26
  fps estimate            47.65 fps       30.90 fps        1.54x  GUIpi26
```

Cold start is the most dramatic win — Tk pays for `tcl.dll` / `tk86.dll` initialization, font system bring-up, and the X-style geometry manager before the first frame. GUIpi26 boots straight into a Win32 message loop with one GDI surface.

## Honesty notes

- **Tkinter is doing dirty-region painting**, GUIpi26 redraws the whole back buffer every frame. The "paint" comparison is thus tougher on GUIpi26 than on Tk, and GUIpi26 still wins.
- **Both libraries are single-threaded.** Numbers do not include threaded work.
- **`fps_estimate` is a ceiling**, not a measured frame rate. Real apps repaint on input/state changes, not in a tight loop.
- **Results vary** by hardware, theme, GPU compositor activity, and Python interpreter. Run it on your own machine to see your numbers.
- **Different abstraction levels.** Tk is cross-platform with native widgets. GUIpi26 is Windows-only with custom-drawn widgets. The right comparison is "for a modern Windows app, which gets you on screen faster and keeps the frame budget low?" — that's what these numbers answer.

## Files

- [bench_guipi26.py](bench_guipi26.py) — GUIpi26 self-timer, prints one JSON line.
- [bench_tkinter.py](bench_tkinter.py) — Tkinter self-timer, prints one JSON line.
- [run_all.py](run_all.py) — Spawns both as subprocesses, prints the table, writes `results.json`.
