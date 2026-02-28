## Cel refaktoryzacji
Extract logic from `fix_mermaid_file` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'fix_mermaid_file' is highly complex: CC=25, fan-out=29, mutations=46.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/mermaid_generator.py (linie 135+)

## Kod źródłowy do refaktoryzacji
```python
def fix_mermaid_file(mmd_path: Path) -> bool:
    """Attempt to fix common Mermaid syntax errors."""
    try:
        content = mmd_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        fixed_lines = []

        import re

        def sanitize_label_text(txt: str) -> str:
            # Mermaid labels frequently break parsing when they contain Mermaid syntax chars.
            # Replace with HTML entities.
            return (
                txt.replace('&', '&amp;')
                .replace('"', '&quot;')
                .replace('[', '&#91;')
                .replace(']', '&#93;')
                .replace('(', '&#40;')
                .replace(')', '&#41;')
                .replace('{', '&#123;')
                .replace('}', '&#125;')
                .replace('|', '&#124;')
            )

        def sanitize_node_id(node_id: str) -> str:
            """Make a Mermaid-safe node identifier.

            Mermaid node IDs should avoid characters like '[', ']', '(', ')', '{', '}', '"', '|'.
            For call-graph exports, we only need stable-ish identifiers.
            """
            node_id = (node_id or '').strip()
            # Cut off at first clearly dangerous Mermaid syntax char.
            node_id = re.split(r"[\[\]\(\)\{\}\"\|\s]", node_id, maxsplit=1)[0]
            # Replace remaining non-word chars just in case.
            node_id = re.sub(r"[^A-Za-z0-9_]", "_", node_id)
            return node_id or "N"
        
        for line in lines:
            original_line = line
            
            # 2. Fix edge labels that might have pipe issues
            if '-->' in line and '|' in line:
                # Handle edge labels like: N1 -->|"label"| N2
                if '-->|' in line:
                    parts = line.split('-->|', 1)
                    if len(parts) == 2:
                        label_and_target = parts[1]
                        # Find the closing |
                        if '|' in label_and_target:
                            parts2 = label_and_target.split('|', 1)
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji fix_mermaid_file. Skup się na wydzieleniu operacji o największej liczbie mutacji.