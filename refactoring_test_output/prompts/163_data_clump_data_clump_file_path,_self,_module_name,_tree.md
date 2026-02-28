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
- /home/tom/github/wronai/code2flow/code2flow/extractors/call_graph.py (linie 24-44)

## Kod źródłowy do refaktoryzacji
```python
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract call graph from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.function_stack = []
        self.class_stack = []
        self.imports = {}
        
        self.visit(tree)
        return self.result
        
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
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[name] = full_name
            self.result.imports[name] = full_name
            
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definition."""
        self.class_stack.append(node.name)
        
        # Store class info
        self.result.classes[node.name] = {
            'file': self.file_path,
            'line': node.lineno,
            'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
            'bases': [self._expr_to_str(b) for b in node.bases]
        }
        
        for stmt in node.body:
            self.visit(stmt)
            
        self.class_stack.pop()
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definition and track calls within it."""
        func_name = self._qualified_name(node.name)
        self.function_stack.append(func_name)
        

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.