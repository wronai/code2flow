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
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 120-140)

## Kod źródłowy do refaktoryzacji
```python
    def _get_cache_key(self, file_path: str, content: str) -> str:
        """Generate cache key."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
        return f"{Path(file_path).stem}_{content_hash}"
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache is full."""
        while len(self._memory_cache) >= self.max_size:
            if self._access_order:
                oldest = self._access_order.pop(0)
                if oldest in self._memory_cache:
                    del self._memory_cache[oldest]
    
    def get(self, file_path: str, content: str) -> Optional[Tuple[ast.AST, str]]:
        """Get from cache with LRU tracking."""
        key = self._get_cache_key(file_path, content)
        
        if key in self._memory_cache:
            # Move to end (most recently used)
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            return self._memory_cache[key]
        
        return None
    
    def put(self, file_path: str, content: str, data: Tuple[ast.AST, str]) -> None:
        """Store in cache with LRU management."""
        self._evict_if_needed()
        
        key = self._get_cache_key(file_path, content)
        self._memory_cache[key] = data
        self._access_order.append(key)


class SmartPrioritizer:
    """Smart file prioritization for optimal analysis order."""
    
    def __init__(self, strategy: ScanStrategy):
        self.strategy = strategy
    
    def prioritize_files(
        self,
        files: List[Tuple[str, str]],
        project_path: Path
    ) -> List[FilePriority]:
        """Score and sort files by importance."""
        scored = []
        
        # First pass: gather import relationships

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.