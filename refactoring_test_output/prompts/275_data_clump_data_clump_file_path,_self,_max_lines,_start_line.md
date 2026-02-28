## Cel refaktoryzacji
Extract logic from `file_path, self, max_lines, start_line` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, max_lines, start_line) are used together in multiple functions: code2flow.refactor.prompt_engine.PromptEngine._get_source_context, code2flow.refactor.prompt_engine._get_source_context.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py (linie 87-107)

## Kod źródłowy do refaktoryzacji
```python
    def _get_source_context(self, file_path: str, start_line: int, max_lines: int = 50) -> str:
        """Read source code lines from a file."""
        if not os.path.exists(file_path):
            return "# Source file not found."
            
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                # line numbers in smell are 1-indexed
                start = max(0, start_line - 1)
                end = min(len(lines), start + max_lines)
                return "".join(lines[start:end])
        except Exception as e:
            return f"# Error reading source: {e}"

    def _get_instruction_for_smell(self, smell: CodeSmell) -> str:
        """Generate specific instruction based on smell type."""
        if smell.type == "god_function":
            return f"Wyekstrahuj mniejsze, spójne metody z funkcji {smell.name.split(': ')[-1]}. Skup się na wydzieleniu operacji o największej liczbie mutacji."
        elif smell.type == "feature_envy":
            return f"Przenieś metodę {smell.name.split(': ')[-1]} do modułu, który posiada większość używanych w niej danych."
        return "Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność."

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.