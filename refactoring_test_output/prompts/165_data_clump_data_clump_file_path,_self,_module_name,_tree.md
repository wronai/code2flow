## Cel refaktoryzacji
Extract logic from `file_path, self, module_name, tree` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, module_name, tree) are used together in multiple functions: code2flow.extractors.call_graph.CallGraphExtractor.extract, code2flow.extractors.call_graph.extract, code2flow.extractors.cfg_extractor.CFGExtractor.extract, code2flow.extractors.cfg_extractor.extract, code2flow.extractors.dfg_extractor.DFGExtractor.extract, code2flow.extractors.dfg_extractor.extract, code2flow.analysis.call_graph.CallGraphExtractor.extract, code2flow.analysis.call_graph.extract, code2flow.analysis.dfg.DFGExtractor.extract, code2flow.analysis.dfg.extract, code2flow.analysis.cfg.CFGExtractor.extract, code2flow.analysis.cfg.extract.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/extractors/cfg_extractor.py (linie 27-47)

## Kod źródłowy do refaktoryzacji
```python
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract CFG from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.node_counter = 0
        
        self.visit(tree)
        return self.result
        
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.