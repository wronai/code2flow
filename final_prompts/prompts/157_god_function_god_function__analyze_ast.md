## Cel refaktoryzacji
Extract logic from `_analyze_ast` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_analyze_ast' is highly complex: CC=1, fan-out=17, mutations=15.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 170+)

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
        
        # Calculate complexity with radon
        try:
            complexity_results = cc_visit(content)
            for entry in complexity_results:
                # Radon returns a list of objects (Function, Class, Method)
                # We need to match them to our function/class records
                full_name = f"{module_name}.{entry.name}"
                if entry.classname:
                    full_name = f"{module_name}.{entry.classname}.{entry.name}"
                
                if full_name in result['functions']:
                    result['functions'][full_name].complexity = {
                        'cyclomatic': entry.complexity,
                        'rank': cc_rank(entry.complexity)
                    }
        except Exception as e:
            if self.config.verbose:
                print(f"Error calculating complexity for {file_path}: {e}")
        
        # New: Deep Analysis for refactoring
        try:
            dfg_ext = DFGExtractor(self.config)
            dfg_res = dfg_ext.extract(tree, module_name, file_path)
            result['mutations'] = dfg_res.mutations
            result['data_flows'] = dfg_res.data_flows
            
            # Update function calls from CG extractor which is more robust
            cg_ext = CallGraphExtractor(self.config)
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_ast. Skup się na wydzieleniu operacji o największej liczbie mutacji.