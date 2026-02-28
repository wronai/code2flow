## Cel refaktoryzacji
Extract logic from `visit_Call` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_Call' is highly complex: CC=1, fan-out=6, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 112+)

## Kod źródłowy do refaktoryzacji
```python
    def visit_Call(self, node: ast.Call):
        """Track function calls."""
        if not self.function_stack:
            self.generic_visit(node)
            return
            
        caller = self.function_stack[-1]
        callee = self._resolve_call(node.func)
        
        # If ast-based resolution failed or returned None.sth, try astroid
        if (not callee or 'None.' in callee) and self.astroid_tree:
            astroid_callee = self._resolve_with_astroid(node)
            if astroid_callee:
                callee = astroid_callee
        
        if callee and caller in self.result.functions:
            self.result.functions[caller].calls.append(callee)
            
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
            
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_Call. Skup się na wydzieleniu operacji o największej liczbie mutacji.