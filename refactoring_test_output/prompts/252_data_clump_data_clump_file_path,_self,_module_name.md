## Cel refaktoryzacji
Extract logic from `file_path, self, module_name` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, module_name) are used together in multiple functions: code2flow.core.analyzer.FileAnalyzer.analyze_file, code2flow.core.analyzer.analyze_file.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 134-154)

## Kod źródłowy do refaktoryzacji
```python
    def analyze_file(self, file_path: str, module_name: str) -> Dict:
        """Analyze a single Python file."""
        path = Path(file_path)
        if not path.exists():
            return {}
        
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return {}
        
        # Try cache
        if self.cache and self.config.performance.enable_cache:
            cached = self.cache.get(file_path, content)
            if cached:
                self.stats['cache_hits'] += 1
                ast_tree, _ = cached
            else:
                try:
                    ast_tree = ast.parse(content)
                    self.cache.put(file_path, content, (ast_tree, content))
                except SyntaxError:
                    return {}
        else:
            try:
                ast_tree = ast.parse(content)
            except SyntaxError:
                return {}
        
        result = self._analyze_ast(ast_tree, file_path, module_name, content)
        self.stats['files_processed'] += 1
        return result
    
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.