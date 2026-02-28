## Cel refaktoryzacji
Extract logic from `create_parser` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'create_parser' is highly complex: CC=1, fan-out=4, mutations=21.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/cli.py (linie 18+)

## Kod źródłowy do refaktoryzacji
```python
def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog='code2flow',
        description='Analyze Python code control flow, data flow, and call graphs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  code2flow /path/to/project
  code2flow /path/to/project -m static -o ./analysis
  code2flow /path/to/project --format yaml,json,mermaid
  code2flow llm-flow  # Generate LLM flow summary
        '''
    )
    
    # Add backward compatibility source argument first
    parser.add_argument(
        'source',
        nargs='?',
        help='Path to Python source file or directory'
    )
    
    parser.add_argument(
        '-m', '--mode',
        choices=list(ANALYSIS_MODES.keys()),
        default='hybrid',
        help=f'Analysis mode (default: hybrid)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='./code2flow_output',
        help='Output directory (default: ./code2flow_output)'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='yaml,mermaid,png',
        help='Output formats: yaml,json,mermaid,png (comma-separated)'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Include all fields in output (including empty/null values)'
    )
    
    parser.add_argument(
        '--no-patterns',
        action='store_true',
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji create_parser. Skup się na wydzieleniu operacji o największej liczbie mutacji.