## Cel refaktoryzacji
Extract logic from `__init__` to a new method/function.

## Powód (Głęboka Analiza)
- Function '__init__' is highly complex: CC=1, fan-out=2, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py (linie 14+)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, config: Config):
        self.config = config
        self.result = AnalysisResult()
        self.module_name = ""
        self.file_path = ""
        
        # Data flow tracking
        self.variable_defs: Dict[str, int] = {}  # variable -> node_id where defined
        self.variable_uses: Dict[str, List[int]] = defaultdict(list)  # variable -> nodes where used
        self.current_scope = ""
        self.scope_stack = []
        
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract DFG from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.variable_defs = {}
        self.variable_uses = defaultdict(list)
        self.current_scope = module_name
        self.scope_stack = [module_name]
        
        self.visit(tree)
        self._build_data_flow_edges()
        
        return self.result
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definition."""
        func_name = f"{self.module_name}.{node.name}"
        self.scope_stack.append(func_name)
        self.current_scope = func_name
        
        # Visit body
        for stmt in node.body:
            self.visit(stmt)
            
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1] if self.scope_stack else self.module_name
        
    def visit_Assign(self, node: ast.Assign):
        """Track variable assignments."""
        # Get variables being assigned
        targets = self._extract_targets(node.targets)
        
        # Get dependencies from value
        dependencies = self._extract_names(node.value)
        
        for target in targets:
            scoped_name = f"{self.current_scope}.{target}"
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji __init__. Skup się na wydzieleniu operacji o największej liczbie mutacji.