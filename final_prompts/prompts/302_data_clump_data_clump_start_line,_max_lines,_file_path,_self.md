## Cel refaktoryzacji
Move method `start_line, max_lines, file_path, self` from module `prompt_engine` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (start_line, max_lines, file_path, self) are used together in multiple functions: code2flow.refactor.prompt_engine.PromptEngine._get_source_context, code2flow.refactor.prompt_engine._get_source_context.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `prompt_engine`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def _get_source_context(self, file_path: str, start_line: int, max_lines: int = 50) -> str:
        """Read source code lines from a file."""
        if not os.path.exists(file_path):
            return "# Source file not found."
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # If tree-sitter is available, use it to accurately find function boundaries
            if self.parser and "method" not in file_path: # simplified check
                tree = self.parser.parse(bytes(content, "utf8"))
                root_node = tree.root_node
                
                # Simple function extraction using tree-sitter
                # (Ideally we'd search for the function node at start_line)
                lines = content.splitlines()
                start = max(0, start_line - 1)
                end = min(len(lines), start + max_lines)
                return "\n".join(lines[start:end])
            else:
                lines = content.splitlines()
                start = max(0, start_line - 1)
                end = min(len(lines), start + max_lines)
                return "\n".join(lines[start:end])
        except Exception as e:
            return f"# Error reading source: {e}"

    def _get_instruction_for_smell(self, smell: CodeSmell) -> str:
        """Generate specific instruction based on smell type."""
        if smell.type == "god_function":
            return f"Wyekstrahuj mniejsze, spójne metody z funkcji {smell.name.split(': ')[-1]}. Skup się na wydzieleniu operacji o największej liczbie mutacji."
        elif smell.type == "feature_envy":
            return f"Przenieś metodę {smell.name.split(': ')[-1]} do modułu, który posiada większość używanych w niej danych. Zmniejsz coupling między modułami."
        elif smell.type == "bottleneck":
            return f"Funkcja {smell.name.split(': ')[-1]} jest wąskim gardłem strukturalnym. Wyekstrahuj z niej niezależne części pomocnicze, aby ułatwić zrozumienie przepływu."
        elif smell.type == "circular_dependency":
            return f"Wykryto cykl zależności. Przenieś część logiki do nowego modułu lub użyj interfejsu, aby przerwać cykl."
        return "Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność."
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.