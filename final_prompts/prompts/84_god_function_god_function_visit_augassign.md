## Cel refaktoryzacji
Extract logic from `visit_AugAssign` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_AugAssign' is highly complex: CC=1, fan-out=9, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py (linie 97+)

## Kod źródłowy do refaktoryzacji
```python
    def visit_AugAssign(self, node: ast.AugAssign):
        """Track augmented assignments (+=, *=, etc.)."""
        target = self._expr_to_str(node.target)
        dependencies = self._extract_names(node.value)
        
        scoped_name = f"{self.current_scope}.{target}"
        
        if scoped_name not in self.result.data_flows:
            self.result.data_flows[scoped_name] = DataFlow(
                variable=target,
                dependencies=set()
            )
            
        # Augmented assignment both uses and defines
        self.result.data_flows[scoped_name].dependencies.add(target)
        self.result.data_flows[scoped_name].dependencies.update(dependencies)
        
        # Record as mutation
        self.result.mutations.append(Mutation(
            variable=target,
            file=self.file_path,
            line=node.lineno,
            type="aug_assign",
            scope=self.current_scope,
            context=self._expr_to_str(node)
        ))
        
        self.generic_visit(node)
        
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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_AugAssign. Skup się na wydzieleniu operacji o największej liczbie mutacji.