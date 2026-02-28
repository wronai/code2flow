## Cel refaktoryzacji
Extract logic from `visit_For` to a new method/function.

## Powód (z analizy DFG)
- Function 'visit_For' has high complexity: fan-out=5, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 147-167)

## Kod źródłowy do refaktoryzacji
```python
    def visit_For(self, node: ast.For):
        """Visit for loop."""
        # Create loop header
        iter_str = self._expr_to_str(node.iter)
        target_str = self._expr_to_str(node.target)
        loop_header = self.new_node("FOR", f"for {target_str} in {iter_str}", 
                                    line=node.lineno)
        self.connect(self.current_node, loop_header)
        
        # Loop body
        body_entry = loop_header
        body_last = []
        for stmt in node.body:
            self.current_node = body_entry
            self.visit(stmt)
            body_last.append(self.current_node)
            body_entry = self.current_node
            
        # Back edge to header
        for last in body_last:
            self.connect(last, loop_header, edge_type="loop")
            
        # Exit (after loop)
        exit_node = self.new_node("EXIT_LOOP", "exit_loop", line=node.end_lineno)
        self.connect(loop_header, exit_node)  # False branch
        self.current_node = exit_node
        
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_For. Skup się na wydzieleniu operacji o największej liczbie mutacji.