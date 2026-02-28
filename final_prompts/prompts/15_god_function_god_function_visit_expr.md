## Cel refaktoryzacji
Extract logic from `visit_Expr` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_Expr' is highly complex: CC=1, fan-out=7, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/extractors/cfg_extractor.py (linie 242+)

## Kod źródłowy do refaktoryzacji
```python
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
            return str(node)[:50]
            
    def _expr_to_str(self, node: ast.AST) -> str:
        """Convert AST expression to string."""
        if node is None:
            return "None"
        try:
            return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)
        except:
            return str(node)
            
    def _format_except(self, handler: ast.ExceptHandler) -> str:
        """Format except handler."""
        if handler.type:
            type_str = self._expr_to_str(handler.type)
            if handler.name:
                return f"except {type_str} as {handler.name}"
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_Expr. Skup się na wydzieleniu operacji o największej liczbie mutacji.