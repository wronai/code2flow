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
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 146-166)

## Kod źródłowy do refaktoryzacji
```python
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
        import_graph = self._build_import_graph(files, project_path)
        
        for file_path, module_name in files:
            score = 0.0
            reasons = []
            
            # Check if has main
            has_main = self._check_has_main(file_path)
            if has_main:
                score += 100.0
                reasons.append("has_main")
            
            # Check if entry point (not imported by others)
            is_entry = module_name not in import_graph or len(import_graph[module_name]) == 0
            if is_entry:
                score += 50.0
                reasons.append("entry_point")
            
            # Check if public API (no underscore prefix)
            is_public = not any(part.startswith('_') for part in module_name.split('.'))
            if is_public:
                score += 20.0
                reasons.append("public_api")
            
            # Import count (more imports = more central)
            import_count = len(import_graph.get(module_name, []))

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.