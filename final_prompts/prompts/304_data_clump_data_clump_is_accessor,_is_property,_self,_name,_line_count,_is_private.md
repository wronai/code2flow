## Cel refaktoryzacji
Move method `is_accessor, is_property, self, name, line_count, is_private` from module `analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (is_accessor, is_property, self, name, line_count, is_private) are used together in multiple functions: code2flow.core.analyzer.FastFileFilter.should_skip_function, code2flow.core.analyzer.should_skip_function.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `analyzer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def should_skip_function(self, name: str, line_count: int, is_private: bool = False, 
                            is_property: bool = False, is_accessor: bool = False) -> bool:
        """Check if function should be skipped."""
        if line_count < self.config.min_function_lines:
            return True
        if self.config.skip_private and is_private:
            return True
        if self.config.skip_properties and is_property:
            return True
        if self.config.skip_accessors and is_accessor:
            return True
        return False


class FileAnalyzer:
    """Analyzes a single file."""
    
    def __init__(self, config: Config, cache: Optional[FileCache] = None):
        self.config = config
        self.cache = cache
        self.stats = {
            'files_processed': 0,
            'functions_found': 0,
            'classes_found': 0,
            'nodes_created': 0,
            'cache_hits': 0,
        }
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.