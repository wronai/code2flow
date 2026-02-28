## Cel refaktoryzacji
Extract logic from `extract` to a new method/function.

## Powód (z analizy DFG)
- Function 'extract' has high complexity: fan-out=4, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py (linie 26-46)

## Kod źródłowy do refaktoryzacji
```python
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
            
            # Create data flow record
            if scoped_name not in self.result.data_flows:
                self.result.data_flows[scoped_name] = DataFlow(
                    variable=target,
                    dependencies=set()
                )
                
            self.result.data_flows[scoped_name].dependencies.update(dependencies)
            
            # Track this as a definition
            self.variable_defs[scoped_name] = node.lineno

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji extract. Skup się na wydzieleniu operacji o największej liczbie mutacji.