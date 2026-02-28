## Cel refaktoryzacji
Extract logic from `edge` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'edge' spans 5 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/extractors/call_graph.py (linie 84-104)

## Kod źródłowy do refaktoryzacji
```python
    def visit_Call(self, node: ast.Call):
        """Track function calls."""
        if not self.function_stack:
            self.generic_visit(node)
            return
            
        caller = self.function_stack[-1]
        callee = self._resolve_call(node.func)
        
        if callee and caller in self.result.functions:
            self.result.functions[caller].calls.add(callee)
            
            # Create call edge
            edge = FlowEdge(
                source=-1,  # Will be resolved
                target=-1,
                edge_type="call",
                metadata={'caller': caller, 'callee': callee}
            )
            self.result.call_edges.append(edge)
            
        self.generic_visit(node)
        
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.