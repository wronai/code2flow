## Cel refaktoryzacji
Extract logic from `_resolve_call` to a new method/function.

## Powód (z analizy DFG)
- Function '_resolve_call' has high complexity: fan-out=4, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/extractors/call_graph.py (linie 115-135)

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
        
    def _expr_to_str(self, node: ast.AST) -> str:
        """Convert AST expression to string."""
        if node is None:
            return ""
        try:
            return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
        except:
            return str(node)

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _resolve_call. Skup się na wydzieleniu operacji o największej liczbie mutacji.