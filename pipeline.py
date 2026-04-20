#!/usr/bin/env python3
"""Unified single-process pipeline for code2llm ecosystem.

Eliminates ~3-5s of subprocess cold-start overhead by running all tools
in a single Python process with shared imports and cached analysis results.

Fixes:
- Fix 1: PIP_DISABLE_PIP_VERSION_CHECK handled at orchestrator level
- Fix 2: code2docs consumes code2llm result (no double scan)
- Fix 3: redup skipped for non-Python projects
- Fix 4: Single process eliminates 5× cold start (~750ms each = ~3.75s)

Usage:
    python pipeline.py [PROJECT_DIR] [OUTPUT_DIR]
    python pipeline.py ./ ./project

Or via orchestrator:
    ./orchestrator.sh ./ ./project  # falls back to subprocess if pipeline.py unavailable
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any

# Performance: disable pip version check for any subprocess we might spawn
os.environ.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")


def _detect_primary_language(project_dir: Path) -> str:
    """Detect primary language by file count."""
    ext_counts: Dict[str, int] = {
        ".py": 0,
        ".ts": 0,
        ".tsx": 0,
        ".js": 0,
        ".jsx": 0,
        ".go": 0,
        ".rs": 0,
        ".java": 0,
    }

    for root, _dirs, files in os.walk(project_dir):
        # Skip common non-source dirs
        if any(skip in root for skip in [".git", "venv", ".venv", "node_modules", "__pycache__"]):
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ext_counts:
                ext_counts[ext] += 1

    # Aggregate JS/TS
    js_ts = ext_counts[".ts"] + ext_counts[".tsx"] + ext_counts[".js"] + ext_counts[".jsx"]
    if js_ts > 0:
        ext_counts["js_ts"] = js_ts

    primary = max(ext_counts, key=ext_counts.get)
    return "python" if primary == ".py" else primary


def run_pipeline(project_dir: str = ".", output_dir: str = "./project") -> Dict[str, Any]:
    """Run unified pipeline in single process.

    Returns dict with timings and status for each stage.
    """
    project_path = Path(project_dir).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    timings: Dict[str, float] = {}
    results: Dict[str, Any] = {"status": {}, "timings": timings}
    start_total = time.perf_counter()

    print("=== Unified Pipeline (single-process) ===")
    print(f"Project: {project_path}")
    print(f"Output:  {out_path}")
    print()

    # Stage 1: code2llm analysis (core)
    t0 = time.perf_counter()
    try:
        from code2llm.api import analyze
        from code2llm.core.config import Config

        config = Config(mode="hybrid")
        config.output_dir = str(out_path)
        analysis_result = analyze(str(project_path), config)

        # Get stats for later decisions
        languages = getattr(analysis_result, "languages", {})
        py_count = languages.get("python", 0)

        timings["code2llm_analysis"] = time.perf_counter() - t0
        results["status"]["code2llm"] = "ok"
        results["analysis"] = analysis_result
        results["python_count"] = py_count
        print(f"✓ code2llm analysis: {timings['code2llm_analysis']:.2f}s ({py_count} Python files)")
    except Exception as e:
        timings["code2llm_analysis"] = time.perf_counter() - t0
        results["status"]["code2llm"] = f"error: {e}"
        print(f"✗ code2llm analysis failed: {e}")
        return results

    # Stage 2: code2docs (reuse analysis result)
    t0 = time.perf_counter()
    try:
        # Try to use code2docs with our analysis result
        import code2docs
        from code2docs import generate_docs

        # code2docs can consume code2llm result directly
        generate_docs(
            result=results["analysis"],
            output=str(out_path / "docs"),
            readme_only=True,
        )
        timings["code2docs"] = time.perf_counter() - t0
        results["status"]["code2docs"] = "ok"
        print(f"✓ code2docs: {timings['code2docs']:.2f}s (from cached analysis)")
    except ImportError:
        timings["code2docs"] = time.perf_counter() - t0
        results["status"]["code2docs"] = "skipped (not installed)"
        print("⚠ code2docs not installed, skipping")
    except Exception as e:
        timings["code2docs"] = time.perf_counter() - t0
        results["status"]["code2docs"] = f"error: {e}"
        print(f"✗ code2docs error: {e}")

    # Stage 3: redup (only for Python projects with >0 .py files)
    t0 = time.perf_counter()
    py_count = results.get("python_count", 0)
    if py_count > 0:
        try:
            from redup import scan_project

            scan_project(
                str(project_path),
                output=str(out_path / "duplication.toon.yaml"),
            )
            timings["redup"] = time.perf_counter() - t0
            results["status"]["redup"] = "ok"
            print(f"✓ redup: {timings['redup']:.2f}s ({py_count} Python files)")
        except ImportError:
            timings["redup"] = time.perf_counter() - t0
            results["status"]["redup"] = "skipped (not installed)"
            print("⚠ redup not installed, skipping")
        except Exception as e:
            timings["redup"] = time.perf_counter() - t0
            results["status"]["redup"] = f"error: {e}"
            print(f"✗ redup error: {e}")
    else:
        # Create placeholder for non-Python projects
        placeholder = out_path / "duplication.toon.yaml"
        placeholder.write_text("# redup/duplication | 0 groups | skip (non-python project)\n")
        timings["redup"] = time.perf_counter() - t0
        results["status"]["redup"] = "skipped (non-python)"
        print(f"⚠ redup: skipped (no Python files found)")

    # Stage 4: vallm validation
    t0 = time.perf_counter()
    try:
        from vallm import batch_validate

        batch_validate(
            str(project_path),
            output=str(out_path / "validation.toon.yaml"),
            compact=True,
        )
        timings["vallm"] = time.perf_counter() - t0
        results["status"]["vallm"] = "ok"
        print(f"✓ vallm: {timings['vallm']:.2f}s")
    except ImportError:
        timings["vallm"] = time.perf_counter() - t0
        results["status"]["vallm"] = "skipped (not installed)"
        print("⚠ vallm not installed, skipping")
    except Exception as e:
        timings["vallm"] = time.perf_counter() - t0
        results["status"]["vallm"] = f"error: {e}"
        print(f"✗ vallm error: {e}")

    # Summary
    timings["total"] = time.perf_counter() - start_total
    print()
    print("=== Summary ===")
    print(f"Total time: {timings['total']:.2f}s")
    print(f"  Analysis:  {timings.get('code2llm_analysis', 0):.2f}s")
    print(f"  Docs:      {timings.get('code2docs', 0):.2f}s")
    print(f"  Redup:     {timings.get('redup', 0):.2f}s")
    print(f"  Vallm:     {timings.get('vallm', 0):.2f}s")
    print()

    # Estimate savings
    estimated_subprocess_overhead = 3.75  # 5 tools × ~750ms
    print(f"Estimated savings vs subprocess: ~{estimated_subprocess_overhead:.1f}s")

    return results


if __name__ == "__main__":
    proj_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./project"
    run_pipeline(proj_dir, out_dir)
