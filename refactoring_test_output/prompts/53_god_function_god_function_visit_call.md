## Cel refaktoryzacji
Extract logic from `visit_Call` to a new method/function.

## Powód (z analizy DFG)
- Function 'visit_Call' has high complexity: fan-out=11, mutations=9.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py (linie 145-165)

## Kod źródłowy do refaktoryzacji
```python
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

        # Track potential mutations via calls (heuristics)
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if any(s in method_name.lower() for s in ['update', 'set', 'add', 'remove', 'append', 'extend', 'pop', 'clear']):
                obj_name = self._expr_to_str(node.func.value)
                self.result.mutations.append(Mutation(
                    variable=obj_name,
                    file=self.file_path,
                    line=node.lineno,
                    type="method_call",
                    scope=self.current_scope,
                    context=f"call to {method_name}"
                ))

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
            if isinstance(child, ast.Name):
                names.append(child.id)
            elif isinstance(child, ast.Tuple) or isinstance(child, ast.List):
                for elt in child.elts:
                    names.extend(self._get_names(elt))

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_Call. Skup się na wydzieleniu operacji o największej liczbie mutacji.