## Cel refaktoryzacji
Extract logic from `visit_If` to a new method/function.

## Powód (z analizy DFG)
- Function 'visit_If' has high complexity: fan-out=6, mutations=16.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 110-130)

## Kod źródłowy do refaktoryzacji
```python
    def visit_If(self, node: ast.If):
        """Visit if statement."""
        # Create condition node
        condition = self._extract_condition(node.test)
        cond_node = self.new_node("IF", condition, line=node.lineno)
        self.connect(self.current_node, cond_node, condition=condition)
        
        # Save current for branches
        branch_entry = cond_node
        
        # Visit then branch
        then_last = []
        for stmt in node.body:
            prev = self.current_node
            self.current_node = branch_entry
            self.visit(stmt)
            then_last.append(self.current_node)
            branch_entry = self.current_node
            
        # Visit else branch
        else_last = []
        if node.orelse:
            branch_entry = cond_node
            for stmt in node.orelse:
                prev = self.current_node
                self.current_node = branch_entry
                self.visit(stmt)
                else_last.append(self.current_node)
                branch_entry = self.current_node
                
        # Merge point
        merge_node = self.new_node("MERGE", "merge", line=node.end_lineno)
        for last in then_last + else_last:
            self.connect(last, merge_node)
            
        self.current_node = merge_node
        
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_If. Skup się na wydzieleniu operacji o największej liczbie mutacji.