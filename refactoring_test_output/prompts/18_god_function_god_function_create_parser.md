## Cel refaktoryzacji
Extract logic from `create_parser` to a new method/function.

## Powód (z analizy DFG)
- Function 'create_parser' has high complexity: fan-out=2, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 394-414)

## Kod źródłowy do refaktoryzacji
```python
def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="llm-flow-generator",
        description="Generate compact LLM-friendly app flow summary from code2flow analysis.yaml",
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji create_parser. Skup się na wydzieleniu operacji o największej liczbie mutacji.