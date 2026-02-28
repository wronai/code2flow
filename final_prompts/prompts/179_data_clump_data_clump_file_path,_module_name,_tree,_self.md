## Cel refaktoryzacji
Move method `file_path, module_name, tree, self` from module `call_graph` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (file_path, module_name, tree, self) are used together in multiple functions: code2flow.extractors.cfg_extractor.CFGExtractor.extract, code2flow.extractors.cfg_extractor.extract, code2flow.extractors.call_graph.CallGraphExtractor.extract, code2flow.extractors.call_graph.extract, code2flow.extractors.dfg_extractor.DFGExtractor.extract, code2flow.extractors.dfg_extractor.extract, code2flow.analysis.call_graph.CallGraphExtractor.extract, code2flow.analysis.call_graph.extract, code2flow.analysis.cfg.CFGExtractor.extract, code2flow.analysis.cfg.extract, code2flow.analysis.dfg.DFGExtractor.extract, code2flow.analysis.dfg.extract.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `call_graph`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract call graph from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.function_stack = []
        self.class_stack = []
        self.imports = {}
        
        # Try to get astroid tree for better resolution
        try:
            self.astroid_tree = astroid.MANAGER.ast_from_file(file_path)
        except Exception:
            self.astroid_tree = None
            
        self.visit(tree)
        self._calculate_metrics()
        return self.result

    def _calculate_metrics(self):
        """Calculate fan-in and fan-out metrics."""
        # First, populate called_by for all functions
        for caller_name, caller_info in self.result.functions.items():
            for callee_name in caller_info.calls:
                if callee_name in self.result.functions:
                    self.result.functions[callee_name].called_by.append(caller_name)

        # Then calculate metrics
        for func_name, func_info in self.result.functions.items():
            fan_out = len(set(func_info.calls))
            fan_in = len(set(func_info.called_by))
            
            self.result.metrics[func_name] = {
                "fan_in": fan_in,
                "fan_out": fan_out,
                "complexity": getattr(func_info, 'complexity', 1) # Placeholder for now
            }
        
    def visit_Import(self, node: ast.Import):
        """Track imports."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = alias.name
            self.result.imports[name] = alias.name
            
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports."""
        module = node.module or ""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.