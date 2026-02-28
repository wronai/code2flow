## Cel refaktoryzacji
Extract logic from `visit_While` to a new method/function.

## Powód (z analizy DFG)
- Function 'visit_While' has high complexity: fan-out=5, mutations=9.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 174-194)

## Kod źródłowy do refaktoryzacji
```python
    def visit_While(self, node: ast.While):
        """Visit while loop."""
        # Loop header with condition
        condition = self._extract_condition(node.test)
        loop_header = self.new_node("WHILE", f"while {condition}", line=node.lineno)
        self.connect(self.current_node, loop_header)
        
        # Loop body
        body_entry = loop_header
        body_last = []
        for stmt in node.body:
            self.current_node = body_entry
            self.visit(stmt)
            body_last.append(self.current_node)
            body_entry = self.current_node
            
        # Back edge
        for last in body_last:
            self.connect(last, loop_header, edge_type="loop")
            
        # Exit
        exit_node = self.new_node("EXIT_LOOP", "exit_loop", line=node.end_lineno)
        self.connect(loop_header, exit_node, condition="False")
        self.current_node = exit_node
        
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_While. Skup się na wydzieleniu operacji o największej liczbie mutacji.