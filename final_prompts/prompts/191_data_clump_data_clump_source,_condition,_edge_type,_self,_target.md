## Cel refaktoryzacji
Move method `source, condition, edge_type, self, target` from module `cfg` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (source, condition, edge_type, self, target) are used together in multiple functions: code2flow.extractors.cfg_extractor.CFGExtractor.connect, code2flow.extractors.cfg_extractor.connect, code2flow.analysis.cfg.CFGExtractor.connect, code2flow.analysis.cfg.connect.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `cfg`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def connect(self, source: Optional[int], target: Optional[int], 
                edge_type: str = "control", condition: Optional[str] = None):
        """Create edge between nodes."""
        if source is not None and target is not None:
            edge = FlowEdge(
                source=source,
                target=target,
                edge_type=edge_type,
                condition=condition
            )
            self.result.cfg_edges.append(edge)
            
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.