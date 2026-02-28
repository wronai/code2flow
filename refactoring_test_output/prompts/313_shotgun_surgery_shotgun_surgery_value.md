## Cel refaktoryzacji
Extract logic from `value` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'value' spans 5 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 225-245)

## Kod źródłowy do refaktoryzacji
```python
    def visit_Assign(self, node: ast.Assign):
        """Visit assignment."""
        targets = [self._expr_to_str(t) for t in node.targets]
        value = self._expr_to_str(node.value)
        label = f"{' = '.join(targets)} = {value[:50]}"
        
        assign_node = self.new_node("ASSIGN", label, line=node.lineno)
        self.connect(self.current_node, assign_node)
        self.current_node = assign_node
        
    def visit_Return(self, node: ast.Return):
        """Visit return statement."""
        value = self._expr_to_str(node.value) if node.value else "None"
        return_node = self.new_node("RETURN", f"return {value[:50]}", line=node.lineno)
        self.connect(self.current_node, return_node)
        self.current_node = return_node
        
    def visit_Expr(self, node: ast.Expr):
        """Visit expression statement."""
        if isinstance(node.value, ast.Call):
            # Function call
            call_name = self._expr_to_str(node.value.func)
            args = [self._expr_to_str(a) for a in node.value.args]
            label = f"CALL {call_name}({', '.join(args)})"[:80]
            
            call_node = self.new_node("CALL", label, line=node.lineno)
            self.connect(self.current_node, call_node)
            self.current_node = call_node
            
            # Track call in function info
            if self.function_stack:
                func_name = self.function_stack[-1]
                if func_name in self.result.functions:
                    self.result.functions[func_name].calls.add(call_name)
        else:
            self.generic_visit(node)
            
    def _qualified_name(self, name: str) -> str:
        """Get fully qualified name."""
        parts = [self.module_name]
        if self.class_stack:
            parts.append(self.class_stack[-1])
        parts.append(name)
        return '.'.join(parts)
        
    def _extract_condition(self, node: ast.AST) -> str:
        """Extract condition as string."""
        try:
            return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)[:50]
        except:

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.