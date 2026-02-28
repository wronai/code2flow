## Cel refaktoryzacji
Extract logic from `file_path, self, content, data` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, content, data) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingFileCache.put, code2flow.core.streaming_analyzer.put, code2flow.core.analyzer.FileCache.put, code2flow.core.analyzer.put.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 63-83)

## Kod źródłowy do refaktoryzacji
```python
    def put(self, file_path: str, content: str, data: Tuple[ast.AST, str]) -> None:
        """Store AST in cache."""
        cache_key = self._get_cache_key(file_path, content)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
    
    def clear(self) -> None:
        """Clear all cached files."""
        for f in self.cache_dir.glob("*.pkl"):
            f.unlink()


class FastFileFilter:
    """Fast file filtering with pattern matching."""
    
    def __init__(self, config: FilterConfig):
        self.config = config
        self._exclude_patterns = [p.lower() for p in config.exclude_patterns]
        self._include_patterns = [p.lower() for p in config.include_patterns]
    
    def should_process(self, file_path: str) -> bool:
        """Check if file should be processed."""
        path_lower = file_path.lower()
        
        # Check exclude patterns
        for pattern in self._exclude_patterns:
            if fnmatch.fnmatch(path_lower, pattern) or pattern in path_lower:
                return False
        
        # Check include patterns (if any)
        if self._include_patterns:
            return any(
                fnmatch.fnmatch(path_lower, p) or p in path_lower
                for p in self._include_patterns
            )
        
        return True
    
    def should_skip_function(self, name: str, line_count: int, is_private: bool = False, 
                            is_property: bool = False, is_accessor: bool = False) -> bool:
        """Check if function should be skipped."""
        if line_count < self.config.min_function_lines:
            return True
        if self.config.skip_private and is_private:
            return True

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.