## Cel refaktoryzacji
Extract logic from `visit_Try` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_Try' is highly complex: CC=1, fan-out=4, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 199+)

## Kod źródłowy do refaktoryzacji
```python
    def visit_Try(self, node: ast.Try):
        """Visit try statement."""
        try_entry = self.new_node("TRY", "try", line=node.lineno)
        self.connect(self.current_node, try_entry)
        
        # Try body
        self.current_node = try_entry
        for stmt in node.body:
            self.visit(stmt)
        try_last = self.current_node
        
        # Except handlers
        for handler in node.handlers:
            handler_node = self.new_node("EXCEPT", self._format_except(handler), 
                                         line=handler.lineno)
            self.connect(try_entry, handler_node, edge_type="exception")
            
            self.current_node = handler_node
            for stmt in handler.body:
                self.visit(stmt)
                
        # Merge
        merge = self.new_node("MERGE", "merge", line=node.end_lineno)
        self.connect(try_last, merge)
        self.current_node = merge
        
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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_Try. Skup się na wydzieleniu operacji o największej liczbie mutacji.