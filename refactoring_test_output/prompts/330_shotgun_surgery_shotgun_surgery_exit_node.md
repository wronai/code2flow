## Cel refaktoryzacji
Extract logic from `exit_node` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'exit_node' spans 6 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/extractors/cfg_extractor.py (linie 69-89)

## Kod źródłowy do refaktoryzacji
```python
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definition."""
        func_name = self._qualified_name(node.name)
        self.function_stack.append(func_name)
        
        # Create entry node
        entry = self.new_node("FUNC", f"FUNC:{func_name}", line=node.lineno)
        self.entry_nodes[func_name] = entry
        
        # Track previous node
        prev_node = self.current_node
        self.current_node = entry
        
        # Store function info
        func_info = FunctionInfo(
            name=node.name,
            qualified_name=func_name,
            file=self.file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            args=[arg.arg for arg in node.args.args]
        )
        self.result.functions[func_name] = func_info
        
        # Visit body
        for stmt in node.body:
            self.visit(stmt)
            
        # Create exit node
        exit_node = self.new_node("RETURN", f"RETURN:{func_name}", 
                                  line=node.end_lineno or node.lineno)
        self.connect(self.current_node, exit_node)
        
        # Restore context
        self.function_stack.pop()
        self.current_node = prev_node
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visit async function definition."""
        self.visit_FunctionDef(node)  # Treat same as sync for CFG
        
    def visit_If(self, node: ast.If):
        """Visit if statement."""
        # Create condition node
        condition = self._extract_condition(node.test)
        cond_node = self.new_node("IF", condition, line=node.lineno)
        self.connect(self.current_node, cond_node, condition=condition)
        
        # Save current for branches
        branch_entry = cond_node

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.