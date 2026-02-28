## Cel refaktoryzacji
Extract logic from `main` to a new method/function.

## Powód (z analizy DFG)
- Function 'main' has high complexity: fan-out=11, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_task_generator.py (linie 237-257)

## Kod źródłowy do refaktoryzacji
```python
def main(argv: Optional[List[str]] = None) -> int:
    args = create_parser().parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 2

    data = load_input(input_path)

    if "task" not in data:
        data = {"task": data}

    normalized = normalize_llm_task(data)

    if args.validate_only:
        sys.stdout.write(dump_yaml(normalized))
        return 0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dump_yaml(normalized), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji main. Skup się na wydzieleniu operacji o największej liczbie mutacji.