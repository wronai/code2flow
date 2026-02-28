## Cel refaktoryzacji
Move method `file_path, content, self` from module `analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (file_path, content, self) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingFileCache._get_cache_key, code2flow.core.streaming_analyzer.StreamingFileCache.get, code2flow.core.streaming_analyzer._get_cache_key, code2flow.core.streaming_analyzer.get, code2flow.core.analyzer.FileCache._get_cache_key, code2flow.core.analyzer.FileCache.get, code2flow.core.analyzer._get_cache_key, code2flow.core.analyzer.get.
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
    def get(self, file_path: str, content: str) -> Optional[Tuple[ast.AST, str]]:
        """Get cached AST if available and not expired."""
        cache_key = self._get_cache_key(file_path, content)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        # Check TTL
        age = time.time() - cache_path.stat().st_mtime
        if age > self.ttl_seconds:
            cache_path.unlink()
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.