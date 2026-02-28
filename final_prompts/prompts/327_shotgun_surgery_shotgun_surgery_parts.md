## Cel refaktoryzacji
Extract logic from `parts` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'parts' spans 12 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 141+)

## Kod źródłowy do refaktoryzacji
```python
    def _qualified_name(self, name: str) -> str:
        """Get fully qualified name."""
        parts = [self.module_name]
        if self.class_stack:
            parts.append(self.class_stack[-1])
        parts.append(name)
        return '.'.join(parts)
        
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.