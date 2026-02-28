## Cel refaktoryzacji
Extract logic from `self, project_path, files` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, project_path, files) are used together in multiple functions: code2flow.core.streaming_analyzer.SmartPrioritizer.prioritize_files, code2flow.core.streaming_analyzer.SmartPrioritizer._build_import_graph, code2flow.core.streaming_analyzer.prioritize_files, code2flow.core.streaming_analyzer._build_import_graph.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 224-244)

## Kod źródłowy do refaktoryzacji
```python
    def _build_import_graph(
        self,
        files: List[Tuple[str, str]],
        project_path: Path
    ) -> Dict[str, Set[str]]:
        """Build import dependency graph."""
        # Map module names to who imports them
        imported_by: Dict[str, Set[str]] = defaultdict(set)
        
        for file_path, module_name in files:
            try:
                content = Path(file_path).read_text()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            # Simplified - just record the top-level module
                            top_module = alias.name.split('.')[0]
                            imported_by[top_module].add(module_name)
                    
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            top_module = node.module.split('.')[0]
                            imported_by[top_module].add(module_name)
            except:
                pass
        
        return imported_by
    
    def _check_has_main(self, file_path: str) -> bool:
        """Check if file has if __name__ == "__main__" block."""
        try:
            content = Path(file_path).read_text()
            return 'if __name__' in content and '__main__' in content
        except:
            return False


class StreamingAnalyzer:
    """Memory-efficient streaming analyzer with progress tracking."""
    
    def __init__(
        self,
        config: Optional[Config] = None,
        strategy: Optional[ScanStrategy] = None
    ):
        self.config = config or FAST_CONFIG
        self.strategy = strategy or STRATEGY_STANDARD
        

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.