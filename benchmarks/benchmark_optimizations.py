#!/usr/bin/env python3
"""Benchmark script to measure performance gains from optimizations.

Tests:
1. Cold run (first analysis, no cache)
2. Warm run (repeated analysis, with ASTRegistry + IncrementalAnalyzer)
3. Per-component timings (file collection, parsing, export)
"""

import gc
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from code2llm.core.config import Config
from code2llm.core.analyzer import ProjectAnalyzer
from code2llm.core.ast_registry import ASTRegistry
from code2llm.core.incremental import IncrementalAnalyzer


def clear_caches(project_path: Path) -> None:
    """Clear all caches for clean benchmark."""
    ASTRegistry.get_global().clear()
    
    # Remove incremental cache
    inc_cache = project_path / ".code2llm_incremental.json"
    if inc_cache.exists():
        inc_cache.unlink()
    
    # Remove file cache
    cache_dir = project_path / ".code2llm_cache"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    
    gc.collect()


def run_analysis(project_path: Path, config: Config) -> Tuple[float, int]:
    """Run analysis and return (time_seconds, file_count)."""
    analyzer = ProjectAnalyzer(config)
    
    start = time.perf_counter()
    result = analyzer.analyze_project(str(project_path))
    elapsed = time.perf_counter() - start
    
    file_count = len(result.functions) + len(result.classes)
    return elapsed, file_count


def benchmark_cold_vs_warm(project_path: Path, runs: int = 3) -> Dict:
    """Compare cold (no cache) vs warm (cached) runs."""
    config = Config()
    
    results = {
        "cold_runs": [],
        "warm_runs": [],
        "incremental_runs": [],
    }
    
    # Cold runs (clear cache each time)
    print("\n📊 Cold runs (no cache)...")
    for i in range(runs):
        clear_caches(project_path)
        elapsed, count = run_analysis(project_path, config)
        results["cold_runs"].append(elapsed)
        print(f"  Run {i+1}: {elapsed:.3f}s ({count} items)")
    
    # Warm runs (use existing cache)
    print("\n🔥 Warm runs (ASTRegistry cached)...")
    clear_caches(project_path)
    # First run populates cache
    run_analysis(project_path, config)
    
    for i in range(runs):
        elapsed, count = run_analysis(project_path, config)
        results["warm_runs"].append(elapsed)
        print(f"  Run {i+1}: {elapsed:.3f}s ({count} items)")
    
    # Incremental runs (simulating no changes)
    print("\n⚡ Incremental runs (IncrementalAnalyzer)...")
    inc = IncrementalAnalyzer(str(project_path))
    
    # First run: populate incremental cache
    analyzer = ProjectAnalyzer(config)
    result = analyzer.analyze_project(str(project_path))
    
    # Store results for each file
    for fname, finfo in result.functions.items():
        inc.update(finfo.file, {"cached": True})
    inc.save()
    
    for i in range(runs):
        start = time.perf_counter()
        # Simulate incremental check
        skipped = 0
        for fname, finfo in result.functions.items():
            if not inc.needs_analysis(finfo.file):
                skipped += 1
        elapsed = time.perf_counter() - start
        results["incremental_runs"].append(elapsed)
        print(f"  Run {i+1}: {elapsed:.4f}s (skipped {skipped} files)")
    
    return results


def print_summary(results: Dict) -> None:
    """Print benchmark summary with speedup calculations."""
    cold_avg = sum(results["cold_runs"]) / len(results["cold_runs"])
    warm_avg = sum(results["warm_runs"]) / len(results["warm_runs"])
    inc_avg = sum(results["incremental_runs"]) / len(results["incremental_runs"])
    
    print("\n" + "=" * 60)
    print("📈 BENCHMARK SUMMARY")
    print("=" * 60)
    
    print(f"\n{'Scenario':<25} {'Avg Time':<12} {'Speedup':<10}")
    print("-" * 47)
    print(f"{'Cold (no cache)':<25} {cold_avg:>8.3f}s {'(baseline)':<10}")
    print(f"{'Warm (ASTRegistry)':<25} {warm_avg:>8.3f}s {cold_avg/warm_avg:>6.1f}×")
    print(f"{'Incremental (no changes)':<25} {inc_avg:>8.4f}s {cold_avg/inc_avg:>6.0f}×")
    
    # Calculate estimated savings
    warm_savings = ((cold_avg - warm_avg) / cold_avg) * 100
    inc_savings = ((cold_avg - inc_avg) / cold_avg) * 100
    
    print(f"\n💰 Savings:")
    print(f"  - ASTRegistry cache: {warm_savings:.1f}% reduction")
    print(f"  - Incremental (unchanged): {inc_savings:.1f}% reduction")
    print()


def main():
    # Default to analyzing code2llm itself
    project_path = Path(__file__).parent.parent
    
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1])
    
    if not project_path.exists():
        print(f"Error: {project_path} does not exist")
        sys.exit(1)
    
    print(f"🔬 Benchmarking code2llm performance on: {project_path}")
    print(f"   Python files: ~{len(list(project_path.rglob('*.py')))}")
    
    results = benchmark_cold_vs_warm(project_path, runs=3)
    print_summary(results)


if __name__ == "__main__":
    main()
