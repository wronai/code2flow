## Cel refaktoryzacji
Move method `visit_Assign` from module `dfg` to `self`.

## Powód (z analizy DFG)
- Function 'visit_Assign' mutates multiple variables in other modules: self.result.data_flows[scoped_name].dependencies, self.variable_uses[scoped_dep], self.result.mutations.
- Feature Envy: Accesses more data from `self` than `dfg`.
- Foreign Mutatons: self.result.data_flows[scoped_name].dependencies, self.variable_uses[scoped_dep], self.result.mutations

## Kontekst przepływu danych
- Zależności: 
- Mutacje w module docelowym: This code mutates state in self

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/dfg.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
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
            
        # Also record uses in the value
        for dep in dependencies:
            scoped_dep = f"{self.current_scope}.{dep}" if dep not in self.variable_defs else dep
            if scoped_dep not in self.variable_uses:
                self.variable_uses[scoped_dep] = []
            self.variable_uses[scoped_dep].append(node.lineno)
            
        # Track this as a mutation
        for target in targets:
            self.result.mutations.append(Mutation(
                variable=target,
                file=self.file_path,
                line=node.lineno,
                type="assign",
                scope=self.current_scope,
                context=self._expr_to_str(node.value)
            ))
            
        self.generic_visit(node)
        
    def visit_AugAssign(self, node: ast.AugAssign):
        """Track augmented assignments (+=, *=, etc.)."""
        target = self._expr_to_str(node.target)
        dependencies = self._extract_names(node.value)
        
        scoped_name = f"{self.current_scope}.{target}"
        

```

## Instrukcja
Przenieś metodę visit_Assign do modułu, który posiada większość używanych w niej danych.