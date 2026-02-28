## Cel refaktoryzacji
Extract logic from `extract` to a new method/function.

## Powód (z analizy DFG)
- Function 'extract' has high complexity: fan-out=3, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 24-44)

## Kod źródłowy do refaktoryzacji
```python
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract call graph from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.function_stack = []
        self.class_stack = []
        self.imports = {}
        
        self.visit(tree)
        self._calculate_metrics()
        return self.result

    def _calculate_metrics(self):
        """Calculate fan-in and fan-out metrics."""
        # First, populate called_by for all functions
        for caller_name, caller_info in self.result.functions.items():
            for callee_name in caller_info.calls:
                if callee_name in self.result.functions:
                    self.result.functions[callee_name].called_by.append(caller_name)

        # Then calculate metrics
        for func_name, func_info in self.result.functions.items():
            fan_out = len(set(func_info.calls))
            fan_in = len(set(func_info.called_by))
            
            self.result.metrics[func_name] = {
                "fan_in": fan_in,
                "fan_out": fan_out,
                "complexity": getattr(func_info, 'complexity', 1) # Placeholder for now
            }
        
    def visit_Import(self, node: ast.Import):
        """Track imports."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = alias.name
            self.result.imports[name] = alias.name
            
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports."""
        module = node.module or ""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[name] = full_name
            self.result.imports[name] = full_name
            
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definition."""

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji extract. Skup się na wydzieleniu operacji o największej liczbie mutacji.