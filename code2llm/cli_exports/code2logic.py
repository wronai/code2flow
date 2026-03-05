"""Code2logic integration — external tool invocation and output normalization."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def _export_code2logic(args, source_path: Path, output_dir: Path, formats: list[str]) -> None:
    """Generate project.toon using external code2logic tool."""
    if not _should_run_code2logic(formats):
        return

    _check_code2logic_installed()
    cmd = _build_code2logic_cmd(args, source_path, output_dir)
    res = _run_code2logic(cmd, args.verbose)

    if res.returncode != 0:
        _handle_code2logic_error(res, cmd)

    found = _find_code2logic_output(output_dir, res)
    target = output_dir / 'project.toon'
    final_files = _normalize_code2logic_output(found, target, args)

    if args.verbose:
        if len(final_files) == 1:
            print(f"  - CODE2LOGIC (project logic): {final_files[0]}")
        else:
            print(f"  - CODE2LOGIC (project logic): {len(final_files)} parts")
            for f in final_files:
                size_kb = os.path.getsize(f) / 1024
                print(f"    → {f.name}: {size_kb:.1f}KB")


def _should_run_code2logic(formats: list[str]) -> bool:
    """Check if code2logic format is requested."""
    return 'code2logic' in formats or 'all' in formats


def _check_code2logic_installed() -> None:
    """Verify code2logic is available in PATH."""
    if shutil.which('code2logic') is None:
        print("Error: requested format 'code2logic' but 'code2logic' executable was not found in PATH.", file=sys.stderr)
        print("Install it with: pip install code2logic --upgrade", file=sys.stderr)
        sys.exit(1)


def _build_code2logic_cmd(args, source_path: Path, output_dir: Path) -> list[str]:
    """Build command for code2logic execution."""
    cmd = [
        'code2logic', str(source_path),
        '-f', 'toon',
        '--compact',
        '--name', 'project',
        '-o', str(output_dir),
    ]
    if not args.verbose:
        cmd.append('-q')
    return cmd


def _run_code2logic(cmd: list[str], verbose: bool):
    """Execute code2logic command."""
    try:
        if verbose:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
    except Exception as e:
        print(f"Error running code2logic: {e}", file=sys.stderr)
        sys.exit(1)


def _handle_code2logic_error(res, cmd: list[str]) -> None:
    """Handle code2logic execution error."""
    if not res.stdout and not res.stderr:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
        except Exception as e:
            print(f"Error running code2logic: {e}", file=sys.stderr)
            sys.exit(1)

    if res.stdout:
        print(res.stdout, file=sys.stderr)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    print(f"Error: code2logic failed (exit code {res.returncode}).", file=sys.stderr)
    sys.exit(res.returncode)


def _find_code2logic_output(output_dir: Path, res) -> Path:
    """Find code2logic output file in possible locations."""
    candidate_paths = [
        output_dir / 'project.toon',
        output_dir / 'project' / 'project.toon',
        output_dir / 'project.toon.txt',
    ]
    found = next((p for p in candidate_paths if p.exists()), None)

    if found is None:
        if res.stdout:
            print(res.stdout, file=sys.stderr)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        print("Error: code2logic completed but project.toon was not found in the output directory.", file=sys.stderr)
        sys.exit(1)

    return found


def _normalize_code2logic_output(found: Path, target: Path, args) -> List[Path]:
    """Normalize output location to target path and check size limits."""
    if found != target:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(found, target)
        found = target

    from ..core.toon_size_manager import manage_toon_size
    return manage_toon_size(
        found,
        target.parent,
        max_kb=256,
        prefix="project",
        verbose=getattr(args, 'verbose', False)
    )
