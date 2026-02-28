## Cel refaktoryzacji
Extract logic from `label, node_type, self` to a new method/function.

## Powód (z analizy DFG)
- Arguments (label, node_type, self) are used together in multiple functions: code2flow.extractors.cfg_extractor.CFGExtractor.new_node, code2flow.extractors.cfg_extractor.new_node, code2flow.analysis.cfg.CFGExtractor.new_node, code2flow.analysis.cfg.new_node.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 37-57)

## Kod źródłowy do refaktoryzacji
```python
    def new_node(self, node_type: str, label: str, **kwargs) -> int:
        """Create new flow node."""
        node_id = self.node_counter
        self.node_counter += 1
        
        node = FlowNode(
            id=node_id,
            type=node_type,
            label=label,
            function=self.function_stack[-1] if self.function_stack else None,
            file=self.file_path,
            line=kwargs.get('line'),
            column=kwargs.get('column'),
            conditions=kwargs.get('conditions', []),
            data_flow=kwargs.get('data_flow', [])
        )
        
        self.result.nodes[node_id] = node
        return node_id
        
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.