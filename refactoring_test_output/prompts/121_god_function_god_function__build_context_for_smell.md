## Cel refaktoryzacji
Extract logic from `_build_context_for_smell` to a new method/function.

## Powód (z analizy DFG)
- Function '_build_context_for_smell' has high complexity: fan-out=12, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py (linie 54-74)

## Kod źródłowy do refaktoryzacji
```python
    def _build_context_for_smell(self, smell: CodeSmell) -> Dict[str, Any]:
        """Prepare context data for the Jinja2 template."""
        # Extract source code for context
        source_code = self._get_source_context(smell.file, smell.line)
        
        # Prepare metrics
        metrics = self.result.metrics.get(smell.name.split(': ')[-1], {}) # Heuristic to find function name
        if not metrics and 'function' in smell.context:
            metrics = self.result.metrics.get(smell.context['function'], {})

        # Prepare mutations
        mutations = [m for m in self.result.mutations if m.scope in (smell.name.split(': ')[-1], smell.context.get('function'))]
        mutations_summary = f"{len(mutations)} modifications recorded: {', '.join(set([m.variable for m in mutations[:5]]))}..."

        context = {
            "target_function": smell.name.split(': ')[-1],
            "reason": smell.description,
            "metrics": metrics,
            "mutations_context": mutations_summary,
            "source_file": smell.file,
            "start_line": smell.line,
            "end_line": smell.line + 20, # Heuristic: end of function or next 20 lines
            "source_code": source_code,
            "instruction": self._get_instruction_for_smell(smell),
            # move_method specific
            "source_module": smell.file.split('/')[-1].replace('.py', ''),
            "target_module": smell.context.get('foreign_mutations', ["other_module"])[0].split('.')[0] if smell.type == "feature_envy" else "other_module",
            "foreign_mutations": ", ".join(smell.context.get('foreign_mutations', [])),
            "foreign_mutations_context": f"This code mutates state in {', '.join(set([v.split('.')[0] for v in smell.context.get('foreign_mutations', []) if '.' in v]))}",
            "dependencies": ", ".join(set([m.variable for m in mutations if '.' in m.variable]))
        }
        return context

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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _build_context_for_smell. Skup się na wydzieleniu operacji o największej liczbie mutacji.