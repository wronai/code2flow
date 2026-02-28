## Cel refaktoryzacji
Extract logic from `generate_single_png` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'generate_single_png' is highly complex: CC=13, fan-out=12, mutations=9.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/mermaid_generator.py (linie 291+)

## Kod źródłowy do refaktoryzacji
```python
def generate_single_png(mmd_file: Path, output_file: Path, timeout: int = 60) -> bool:
    """Generate PNG from single Mermaid file using available renderers."""
    
    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Mermaid's default maxTextSize is often too low for large projects,
    # resulting in placeholder PNGs that say "Maximum text size in diagram exceeded".
    # Provide a temporary config with a higher limit.
    try:
        max_text_size = int(os.getenv('CODE2FLOW_MERMAID_MAX_TEXT_SIZE', '2000000'))
    except Exception:
        max_text_size = 2000000

    try:
        max_edges = int(os.getenv('CODE2FLOW_MERMAID_MAX_EDGES', '20000'))
    except Exception:
        max_edges = 20000

    cfg_path: Optional[str] = None
    try:
        cfg = {
            "maxTextSize": max_text_size,
            "maxEdges": max_edges,
            "theme": "default",
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_cfg:
            tmp_cfg.write(json.dumps(cfg))
            cfg_path = tmp_cfg.name

        # Try different renderers in order of preference
        renderers = [
            (
                'mmdc',
                [
                    'mmdc',
                    '-i',
                    str(mmd_file),
                    '-o',
                    str(output_file),
                    '-t',
                    'default',
                    '-b',
                    'white',
                    '-c',
                    cfg_path,
                ],
            ),
            (
                'npx',
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji generate_single_png. Skup się na wydzieleniu operacji o największej liczbie mutacji.