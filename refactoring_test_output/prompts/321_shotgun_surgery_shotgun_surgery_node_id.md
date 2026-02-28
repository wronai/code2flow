## Cel refaktoryzacji
Extract logic from `node_id` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'node_id' spans 9 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/mermaid_generator.py (linie 15-35)

## Kod źródłowy do refaktoryzacji
```python
def validate_mermaid_file(mmd_path: Path) -> List[str]:
    """Validate Mermaid file and return list of errors."""
    errors = []
    
    if not mmd_path.exists():
        return [f"File not found: {mmd_path}"]
    
    try:
        content = mmd_path.read_text(encoding='utf-8')
        
        # Basic syntax checks
        lines = content.strip().split('\n')
        
        # Check for proper graph declaration
        if not lines or not any(line.strip().startswith(('graph', 'flowchart')) for line in lines):
            errors.append("Missing graph declaration (should start with 'graph' or 'flowchart')")
        
        def strip_label_segments(s: str) -> str:
            """Remove label segments that frequently contain Mermaid syntax chars.

            We ignore bracket/paren balancing inside:
            - edge labels: -->|...|
            - node labels: N1["..."] or N1[/'...'/] etc.
            """
            import re

            # Remove edge labels |...|
            s = re.sub(r"\|[^|]*\|", "||", s)

            # Remove common node label forms: ["..."], ("..."), {"..."}
            s = re.sub(r"\[\"[^\"]*\"\]", "[]", s)
            s = re.sub(r"\(\"[^\"]*\"\)", "()", s)
            s = re.sub(r"\{\"[^\"]*\"\}", "{}", s)

            # Remove Mermaid special bracket label variants like [/'...'/]
            s = re.sub(r"\[/[^\]]*?/\]", "[]", s)
            s = re.sub(r"\(/[^)]*?/\)", "()", s)

            return s

        # Check for unmatched brackets/parentheses (outside label segments)
        bracket_stack = []
        paren_stack = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('%%'):
                continue
                
            # Skip validation for lines that are clearly node definitions with content

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.