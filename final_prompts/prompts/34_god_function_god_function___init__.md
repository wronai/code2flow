## Cel refaktoryzacji
Extract logic from `__init__` to a new method/function.

## Powód (Głęboka Analiza)
- Function '__init__' is highly complex: CC=1, fan-out=1, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 14+)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, config: Config):
        self.config = config
        self.result = AnalysisResult()
        self.module_name = ""
        self.file_path = ""
        
        # Context
        self.function_stack = []
        self.class_stack = []
        self.imports = {}
        self.astroid_tree = None
        
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract call graph from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.function_stack = []
        self.class_stack = []
        self.imports = {}
        
        # Try to get astroid tree for better resolution
        try:
            self.astroid_tree = astroid.MANAGER.ast_from_file(file_path)
        except Exception:
            self.astroid_tree = None
            
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
        
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji __init__. Skup się na wydzieleniu operacji o największej liczbie mutacji.