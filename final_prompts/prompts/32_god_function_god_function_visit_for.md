## Cel refaktoryzacji
Extract logic from `visit_For` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_For' is highly complex: CC=1, fan-out=6, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/extractors/dfg_extractor.py (linie 105+)

## Kod źródłowy do refaktoryzacji
```python
    def visit_For(self, node: ast.For):
        """Track loop variable."""
        if isinstance(node.target, ast.Name):
            loop_var = node.target.id
            scoped_name = f"{self.current_scope}.{loop_var}"
            
            # Loop variable depends on iterator
            iter_deps = self._extract_names(node.iter)
            
            if scoped_name not in self.result.data_flows:
                self.result.data_flows[scoped_name] = DataFlow(
                    variable=loop_var,
                    dependencies=set(iter_deps)
                )
            else:
                self.result.data_flows[scoped_name].dependencies.update(iter_deps)
                
        self.generic_visit(node)
        
    def visit_Call(self, node: ast.Call):
        """Track data flow through function calls."""
        # Track arguments as data flow to the call
        for i, arg in enumerate(node.args):
            deps = self._extract_names(arg)
            if deps:
                # Create implicit data flow for this argument
                call_str = self._expr_to_str(node.func)
                flow_key = f"{call_str}.arg{i}"
                
                if flow_key not in self.result.data_flows:
                    self.result.data_flows[flow_key] = DataFlow(
                        variable=flow_key,
                        dependencies=deps
                    )
                else:
                    self.result.data_flows[flow_key].dependencies.update(deps)
                    
        self.generic_visit(node)
        
    def _extract_targets(self, targets: List[ast.AST]) -> List[str]:
        """Extract variable names from assignment targets."""
        names = []
        for target in targets:
            names.extend(self._get_names(target))
        return names
        
    def _get_names(self, node: ast.AST) -> List[str]:
        """Get all variable names from an AST node."""
        names = []
        for child in ast.walk(node):
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_For. Skup się na wydzieleniu operacji o największej liczbie mutacji.