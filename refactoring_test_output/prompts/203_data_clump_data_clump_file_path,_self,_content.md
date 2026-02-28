## Cel refaktoryzacji
Extract logic from `file_path, self, content` to a new method/function.

## Powód (z analizy DFG)
- Arguments (file_path, self, content) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingFileCache._get_cache_key, code2flow.core.streaming_analyzer.StreamingFileCache.get, code2flow.core.streaming_analyzer._get_cache_key, code2flow.core.streaming_analyzer.get, code2flow.core.analyzer.FileCache._get_cache_key, code2flow.core.analyzer.FileCache.get, code2flow.core.analyzer._get_cache_key, code2flow.core.analyzer.get.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 34-54)

## Kod źródłowy do refaktoryzacji
```python
    def _get_cache_key(self, file_path: str, content: str) -> str:
        """Generate cache key from file path and content hash."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
        return f"{Path(file_path).stem}_{content_hash}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{cache_key}.pkl"
    
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.