#!/usr/bin/env python3
"""
Auto-benchmark: before/after CC metrics for code2llm refactoring.

Usage:
    python benchmarks/benchmark_evolution.py [project_path]

Runs code2llm evolution analysis and prints before→after comparison.
"""

import json
import subprocess
import sys
import tempfile
import re
from pathlib import Path


def parse_evolution_metrics(toon_content: str) -> dict:
    """Extract metrics from evolution.toon content."""
    metrics = {}
    for line in toon_content.splitlines():
        line = line.strip()
        if line.startswith("CC̄:"):
            m = re.search(r"([\d.]+)\s*→", line)
            if m:
                metrics["cc_avg"] = float(m.group(1))
        elif line.startswith("max-CC:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["max_cc"] = int(m.group(1))
        elif line.startswith("god-modules:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["god_modules"] = int(m.group(1))
        elif line.startswith("high-CC"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["high_cc"] = int(m.group(1))
        elif line.startswith("hub-types:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["hub_types"] = int(m.group(1))

    # Also extract func count from header
    m = re.search(r"\| (\d+) func \|", toon_content)
    if m:
        metrics["total_funcs"] = int(m.group(1))

    return metrics


def load_previous(history_file: Path) -> dict:
    """Load previous metrics from history file if present."""
    if history_file.exists():
        try:
            return json.loads(history_file.read_text())
        except Exception:
            pass
    return {}


def save_current(history_file: Path, metrics: dict):
    """Save current metrics for next comparison."""
    history_file.parent.mkdir(parents=True, exist_ok=True)
    history_file.write_text(json.dumps(metrics, indent=2))


def run_benchmark(project_path: str):
    """Run evolution analysis and print before/after table."""
    history_file = Path(project_path) / ".code2llm_metrics.json"
    before = load_previous(history_file)

    # Run evolution analysis
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable, "-m", "code2llm",
            project_path, "-f", "evolution", "-o", tmpdir, "--no-png"
        ]
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            sys.exit(1)

        toon_path = Path(tmpdir) / "evolution.toon"
        if not toon_path.exists():
            print("ERROR: evolution.toon not generated")
            sys.exit(1)

        content = toon_path.read_text()
        after = parse_evolution_metrics(content)

    # Print comparison
    print("\n" + "=" * 60)
    print("  CODE2LLM EVOLUTION BENCHMARK")
    print("=" * 60)

    metrics_labels = {
        "cc_avg": "CC̄ (average)",
        "max_cc": "max-CC",
        "high_cc": "high-CC (≥15)",
        "god_modules": "god-modules",
        "hub_types": "hub-types",
        "total_funcs": "total functions",
    }

    print(f"\n  {'Metric':<22} {'Before':>10} {'After':>10} {'Delta':>10}")
    print(f"  {'-' * 22} {'-' * 10} {'-' * 10} {'-' * 10}")

    for key, label in metrics_labels.items():
        b = before.get(key, "—")
        a = after.get(key, "—")
        if isinstance(b, (int, float)) and isinstance(a, (int, float)):
            delta = a - b
            sign = "+" if delta > 0 else ""
            arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
            print(f"  {label:<22} {b:>10} {a:>10} {sign}{delta:>8} {arrow}")
        else:
            print(f"  {label:<22} {str(b):>10} {str(a):>10} {'—':>10}")

    print()

    # Save current for next run
    save_current(history_file, after)
    print(f"  Metrics saved → {history_file}")
    print(f"  Run again after refactoring to see delta!\n")

    # Show evolution.toon content
    print("-" * 60)
    print(content)


if __name__ == "__main__":
    project = sys.argv[1] if len(sys.argv) > 1 else "."
    run_benchmark(project)
