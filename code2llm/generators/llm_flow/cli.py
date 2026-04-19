"""LLM Flow CLI — command-line interface for generating flow summaries."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .._utils import dump_yaml
from .utils import _safe_read_yaml
from .generator import generate_llm_flow, render_llm_flow_md


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="llm-flow-generator",
        description="Generate compact LLM-friendly app flow summary from code2llm analysis.yaml",
    )
    p.add_argument(
        "-i",
        "--input",
        default="./output/analysis.yaml",
        help="Path to analysis.yaml (default: ./output/analysis.yaml)",
    )
    p.add_argument(
        "-o",
        "--output",
        default="./output/llm_flow.yaml",
        help="Output llm_flow.yaml path (default: ./output/llm_flow.yaml)",
    )
    p.add_argument(
        "--md",
        default=None,
        help="Optional output Markdown summary path (e.g. ./output/llm_flow.md)",
    )
    p.add_argument("--max-functions", type=int, default=40)
    p.add_argument("--limit-decisions", type=int, default=8)
    p.add_argument("--limit-calls", type=int, default=12)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = create_parser().parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 2

    analysis = _safe_read_yaml(input_path)
    flow = generate_llm_flow(
        analysis,
        max_functions=max(1, args.max_functions),
        limit_decisions=max(0, args.limit_decisions),
        limit_calls=max(0, args.limit_calls),
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dump_yaml(flow), encoding="utf-8")

    if args.md:
        md_path = Path(args.md)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_llm_flow_md(flow), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    'create_parser',
    'main',
]
