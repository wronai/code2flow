## Cel refaktoryzacji
Extract logic from `generate_pngs` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'generate_pngs' is highly complex: CC=6, fan-out=7, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/mermaid_generator.py (linie 260+)

## Kod źródłowy do refaktoryzacji
```python
def generate_pngs(input_dir: Path, output_dir: Path, timeout: int = 60) -> int:
    """Generate PNG files from all .mmd files in input_dir."""
    mmd_files = list(input_dir.glob('*.mmd'))
    
    if not mmd_files:
        return 0
    
    success_count = 0
    
    for mmd_file in mmd_files:
        output_file = output_dir / f"{mmd_file.stem}.png"
        
        # Validate first
        errors = validate_mermaid_file(mmd_file)
        if errors:
            print(f"  Fixing {mmd_file.name}: {len(errors)} issues")
            fix_mermaid_file(mmd_file)
            
            # Re-validate
            errors = validate_mermaid_file(mmd_file)
            if errors:
                print(f"    Still has errors: {errors[:3]}")  # Show first 3 errors
                continue
        
        # Try to generate PNG
        if generate_single_png(mmd_file, output_file, timeout):
            success_count += 1
    
    return success_count


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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji generate_pngs. Skup się na wydzieleniu operacji o największej liczbie mutacji.