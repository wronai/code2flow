## Cel refaktoryzacji
Extract logic from `_resolve_call` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_resolve_call' is highly complex: CC=1, fan-out=4, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 149+)

## Kod źródłowy do refaktoryzacji
```python
    def _resolve_call(self, node: ast.AST) -> Optional[str]:
        """Resolve a call to its full name."""
        if isinstance(node, ast.Name):
            # Simple function call
            if node.id in self.imports:
                return self.imports[node.id]
            return f"{self.module_name}.{node.id}"
            
        elif isinstance(node, ast.Attribute):
            # Method or module.function call
            parts = []
            current = node
            
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
                
            if isinstance(current, ast.Name):
                parts.append(current.id)
                parts.reverse()
                
                # Check if root is an import
                root = parts[0]
                if root in self.imports:
                    return f"{self.imports[root]}.{'.'.join(parts[1:])}"
                    
                # Check for self/cls
                if root in ('self', 'cls') and self.class_stack:
                    return f"{self.module_name}.{self.class_stack[-1]}.{'.'.join(parts[1:])}"
                    
                return f"{self.module_name}.{'.'.join(parts)}"
                
        return None

    def _resolve_with_astroid(self, node: ast.Call) -> Optional[str]:
        """Use astroid to infer the call target."""
        if not self.astroid_tree:
            return None
            
        try:
            # Find the corresponding astroid node by line/col
            # This is a bit slow but robust
            for astroid_node in self.astroid_tree.nodes_of_class(astroid.Call):
                if astroid_node.lineno == node.lineno and astroid_node.col_offset == node.col_offset:
                    # Infer the targets
                    inferred = astroid_node.func.infer()
                    for target in inferred:
                        if hasattr(target, 'qname'):
                            return target.qname()
                    break
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _resolve_call. Skup się na wydzieleniu operacji o największej liczbie mutacji.