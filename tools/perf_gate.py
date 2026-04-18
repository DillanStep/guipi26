"""Performance gate for GUIpi26.

Runs the GUIpi26 micro-benchmark and fails if results regress past the
configured thresholds. Designed for CI; prints a one-line summary plus a
JSON blob the Guardian bot picks up for the PR comment.

Thresholds are intentionally conservative so that genuine regressions trip
the gate but normal CI noise doesn't. Tune in PERF_THRESHOLDS below.
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "bench_guipi26.py"

# CI runners are shared, virtualised and ~3-5x slower than typical dev boxes.
# Thresholds reflect that — they catch order-of-magnitude regressions, not noise.
PERF_THRESHOLDS = {
    "cold_start_ms_max": 3000.0,    # cold-start a Window
    "create_ms_max":     3000.0,    # create N controls
    "paint_ms_p95_max":   80.0,     # 95th-percentile paint
    "fps_estimate_min":   25.0,     # minimum sustained fps
}


def run_once(controls: int, paints: int) -> dict:
    proc = subprocess.run(
        [sys.executable, str(BENCH),
         "--controls", str(controls),
         "--paints", str(paints)],
        capture_output=True, text=True, check=True,
    )
    last_line = proc.stdout.strip().splitlines()[-1]
    return json.loads(last_line)


def median_run(runs: list[dict]) -> dict:
    keys = ["cold_start_ms", "create_ms", "paint_ms_avg",
            "paint_ms_p50", "paint_ms_p95", "fps_estimate"]
    return {k: round(statistics.median(r[k] for r in runs), 2) for k in keys}


def evaluate(result: dict) -> list[str]:
    failures: list[str] = []
    if result["cold_start_ms"] > PERF_THRESHOLDS["cold_start_ms_max"]:
        failures.append(
            f"cold_start_ms={result['cold_start_ms']} > "
            f"{PERF_THRESHOLDS['cold_start_ms_max']}"
        )
    if result["create_ms"] > PERF_THRESHOLDS["create_ms_max"]:
        failures.append(
            f"create_ms={result['create_ms']} > "
            f"{PERF_THRESHOLDS['create_ms_max']}"
        )
    if result["paint_ms_p95"] > PERF_THRESHOLDS["paint_ms_p95_max"]:
        failures.append(
            f"paint_ms_p95={result['paint_ms_p95']} > "
            f"{PERF_THRESHOLDS['paint_ms_p95_max']}"
        )
    if result["fps_estimate"] < PERF_THRESHOLDS["fps_estimate_min"]:
        failures.append(
            f"fps_estimate={result['fps_estimate']} < "
            f"{PERF_THRESHOLDS['fps_estimate_min']}"
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=int, default=200)
    parser.add_argument("--paints", type=int, default=80)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--report", type=Path, default=ROOT / "perf_report.json")
    args = parser.parse_args()

    runs = [run_once(args.controls, args.paints) for _ in range(args.runs)]
    result = median_run(runs)
    failures = evaluate(result)

    report = {
        "result": result,
        "thresholds": PERF_THRESHOLDS,
        "failures": failures,
        "controls": args.controls,
        "paints": args.paints,
        "runs": args.runs,
    }
    args.report.write_text(json.dumps(report, indent=2))

    print("perf_gate result:", json.dumps(result))
    if failures:
        print("perf_gate FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("perf_gate PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
