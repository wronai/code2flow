## Cel refaktoryzacji
Extract logic from `analyze_project` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'analyze_project' is highly complex: CC=1, fan-out=18, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 450+)

## Kod źródłowy do refaktoryzacji
```python
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
        self._perform_refactoring_analysis(merged)
        
        # Calculate stats
        elapsed = time.time() - start_time
        merged.stats = {
            'files_processed': len(files),
            'functions_found': len(merged.functions),
            'classes_found': len(merged.classes),
            'nodes_created': len(merged.nodes),
            'edges_created': len(merged.edges),
            'patterns_detected': len(merged.patterns),
            'analysis_time_seconds': round(elapsed, 2),
            'cache_hits': sum(r.get('cache_hits', 0) for r in results),
        }
        
        if self.config.verbose:
            print(f"Analysis complete in {elapsed:.2f}s")
            print(f"  Functions: {len(merged.functions)}")
            print(f"  Classes: {len(merged.classes)}")
            print(f"  CFG Nodes: {len(merged.nodes)}")
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji analyze_project. Skup się na wydzieleniu operacji o największej liczbie mutacji.