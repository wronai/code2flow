## Cel refaktoryzacji
Extract logic from `main` to a new method/function.

## Powód (z analizy DFG)
- Function 'main' has high complexity: fan-out=14, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 422-442)

## Kod źródłowy do refaktoryzacji
```python
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji main. Skup się na wydzieleniu operacji o największej liczbie mutacji.