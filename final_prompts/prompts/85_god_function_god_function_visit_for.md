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
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py (linie 126+)

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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_For. Skup się na wydzieleniu operacji o największej liczbie mutacji.