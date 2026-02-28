## Cel refaktoryzacji
Extract logic from `visit_Assign` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_Assign' is highly complex: CC=1, fan-out=7, mutations=12.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/extractors/dfg_extractor.py (linie 54+)

## Kod źródłowy do refaktoryzacji
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
            if dep not in self.variable_uses:
                self.variable_uses[scoped_dep] = []
            self.variable_uses[scoped_dep].append(node.lineno)
            
        self.generic_visit(node)
        
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
        
        self.generic_visit(node)
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_Assign. Skup się na wydzieleniu operacji o największej liczbie mutacji.