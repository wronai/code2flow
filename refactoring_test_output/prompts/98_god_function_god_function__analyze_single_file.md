## Cel refaktoryzacji
Extract logic from `_analyze_single_file` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_single_file' has high complexity: fan-out=3, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 408-428)

## Kod źródłowy do refaktoryzacji
```python
def _analyze_single_file(args):
    """Analyze single file - module level function for pickle compatibility."""
    file_path, module_name, config_dict = args
    from .config import Config
    config = Config(**config_dict)
    analyzer = FileAnalyzer(config, None)
    return analyzer.analyze_file(file_path, module_name)


class ProjectAnalyzer:
    """Main analyzer with parallel processing."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or FAST_CONFIG
        self.cache = FileCache(
            self.config.performance.cache_dir,
            self.config.performance.cache_ttl_hours
        ) if self.config.performance.enable_cache else None
        self.file_filter = FastFileFilter(self.config.filters)
    
    def analyze_project(self, project_path: str) -> AnalysisResult:
        """Analyze entire project."""
        start_time = time.time()
        
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")
        
        # Collect Python files
        files = self._collect_files(project_path)
        
        if self.config.verbose:
            print(f"Found {len(files)} files to analyze")
        
        # Analyze files
        if self.config.performance.parallel_enabled and len(files) > 1:
            results = self._analyze_parallel(files)
        else:
            results = self._analyze_sequential(files)
        
        # Merge results
        merged = self._merge_results(results, str(project_path))
        
        # Build call graph
        self._build_call_graph(merged)
        
        if not self.config.performance.skip_pattern_detection:
            self._detect_patterns(merged)
            
        # New: Refactoring analysis

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_single_file. Skup się na wydzieleniu operacji o największej liczbie mutacji.