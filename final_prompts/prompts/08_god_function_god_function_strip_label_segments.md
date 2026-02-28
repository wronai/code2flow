## Cel refaktoryzacji
Extract logic from `strip_label_segments` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'strip_label_segments' is highly complex: CC=1, fan-out=1, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/mermaid_generator.py (linie 32+)

## Kod źródłowy do refaktoryzacji
```python
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
            # Node definitions have the pattern: ID[content] or ID(content) or ID{content}
            if (('[' in line and ']' in line) or 
                ('(' in line and ')' in line) or 
                ('{' in line and '}' in line)):
                # This looks like a node definition, check if it's properly formed
                # but don't count parentheses inside the node content
                continue
                
            # Count brackets and parentheses (ignoring those inside label segments)
            check_line = strip_label_segments(line)
            for char in check_line:
                if char == '[':
                    bracket_stack.append((']', line_num))
                elif char == ']':
                    if not bracket_stack or bracket_stack[-1][0] != ']':
                        errors.append(f"Line {line_num}: Unmatched ']'")
                    else:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji strip_label_segments. Skup się na wydzieleniu operacji o największej liczbie mutacji.