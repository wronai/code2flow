## Cel refaktoryzacji
Extract logic from `self` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'self' spans 69 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/extractors/dfg_extractor.py (linie 86-106)

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
        # Track arguments as data flow to the call
        for i, arg in enumerate(node.args):
            deps = self._extract_names(arg)
            if deps:
                # Create implicit data flow for this argument
                call_str = self._expr_to_str(node.func)
                flow_key = f"{call_str}.arg{i}"
                
                if flow_key not in self.result.data_flows:
                    self.result.data_flows[flow_key] = DataFlow(

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.