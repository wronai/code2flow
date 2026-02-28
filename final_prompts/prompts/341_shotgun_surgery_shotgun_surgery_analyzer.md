## Cel refaktoryzacji
Extract logic from `analyzer` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'analyzer' spans 7 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/cli.py (linie 161+)

## Kod źródłowy do refaktoryzacji
```python
def main():
    """Main CLI entry point."""
    # Handle special cases first
    if len(sys.argv) > 1 and sys.argv[1] == 'llm-flow':
        from .llm_flow_generator import main as llm_flow_main
        return llm_flow_main(sys.argv[2:])
    
    if len(sys.argv) > 1 and sys.argv[1] == 'llm-context':
        # Quick LLM context generation
        return generate_llm_context(sys.argv[2:])
    
    # For all other cases, use the regular parser
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle analysis (default behavior)
    if not args.source:
        print("Error: missing required argument: source", file=sys.stderr)
        print("Usage: code2flow <source> [options]", file=sys.stderr)
        print("   or: code2flow llm-flow [options]", file=sys.stderr)
        sys.exit(2)

    # Validate source path
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}", file=sys.stderr)
        sys.exit(1)
        
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure analysis
    config = Config(
        mode=args.mode,
        max_depth_enumeration=args.max_depth,
        detect_state_machines=not args.no_patterns,
        detect_recursion=not args.no_patterns,
        output_dir=str(output_dir)
    )
    
    if args.verbose:
        print(f"Analyzing: {source_path}")
        print(f"Mode: {args.mode}")
        print(f"Output: {output_dir}")
        
    # Run analysis
    try:
        if args.streaming or args.strategy in ['quick', 'deep']:
            # Use optimized streaming analyzer
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.