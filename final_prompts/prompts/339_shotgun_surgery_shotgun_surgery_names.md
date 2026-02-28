## Cel refaktoryzacji
Extract logic from `names` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'names' spans 6 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/extractors/dfg_extractor.py (linie 151+)

## Kod źródłowy do refaktoryzacji
```python
    def _get_names(self, node: ast.AST) -> List[str]:
        """Get all variable names from an AST node."""
        names = []
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                names.append(child.id)
            elif isinstance(child, ast.Tuple) or isinstance(child, ast.List):
                for elt in child.elts:
                    names.extend(self._get_names(elt))
        return names
        
    def _extract_names(self, node: ast.AST) -> Set[str]:
        """Extract all variable names used in expression."""
        names = set()
        if node is None:
            return names
            
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                names.add(child.id)
                
        return names
        
    def _expr_to_str(self, node: ast.AST) -> str:
        """Convert AST expression to string."""
        if node is None:
            return "None"
        try:
            return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
        except:
            return str(node)
            
    def _build_data_flow_edges(self):
        """Build DFG edges from data flow records."""
        # For each variable, create edges from its dependencies
        for var_name, data_flow in self.result.data_flows.items():
            # This is a simplified representation
            # In a full implementation, we'd map to actual node IDs
            pass  # Edges built during CFG extraction
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.