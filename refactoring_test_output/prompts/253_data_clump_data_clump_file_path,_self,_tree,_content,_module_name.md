## Cel refaktoryzacji
Extract logic from `file_path, self, tree, content, module_name` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, tree, content, module_name) are used together in multiple functions: code2flow.core.analyzer.FileAnalyzer._analyze_ast, code2flow.core.analyzer._analyze_ast.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 167-187)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_ast(self, tree: ast.AST, file_path: str, module_name: str, content: str) -> Dict:
        """Analyze AST and extract structure."""
        result = {
            'module': ModuleInfo(
                name=module_name,
                file=file_path,
                is_package=Path(file_path).name == '__init__.py'
            ),
            'functions': {},
            'classes': {},
            'nodes': {},
            'edges': [],
        }
        
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._process_class(node, file_path, module_name, result, lines)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                self._process_function(node, file_path, module_name, result, lines, None)
        
        # New: Deep Analysis for refactoring
        try:
            dfg_ext = DFGExtractor(self.config)
            dfg_res = dfg_ext.extract(tree, module_name, file_path)
            result['mutations'] = dfg_res.mutations
            result['data_flows'] = dfg_res.data_flows
            
            # Update function calls from CG extractor which is more robust
            cg_ext = CallGraphExtractor(self.config)
            cg_res = cg_ext.extract(tree, module_name, file_path)
            for func_name, cg_func in cg_res.functions.items():
                if func_name in result['functions']:
                    result['functions'][func_name].calls.extend(list(cg_func.calls))
        except Exception as e:
            if self.config.verbose:
                print(f"Error in deep analysis for {file_path}: {e}")

        self.stats['files_processed'] += 1
        return result
    
    def _process_class(self, node: ast.ClassDef, file_path: str, module_name: str, 
                       result: Dict, lines: List[str]) -> None:
        """Process class definition."""
        class_name = node.name
        qualified_name = f"{module_name}.{class_name}"
        
        methods = []
        for item in node.body:

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.