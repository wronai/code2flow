## Cel refaktoryzacji
Extract logic from `_analyze_parallel` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_parallel' has high complexity: fan-out=8, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 503-523)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_parallel(self, files: List[Tuple[str, str]]) -> List[Dict]:
        """Analyze files in parallel."""
        results = []
        workers = min(self.config.performance.parallel_workers, len(files))
        
        # Convert config to dict for pickle compatibility
        config_dict = {
            'mode': self.config.mode,
            'max_depth_enumeration': self.config.max_depth_enumeration,
            'detect_state_machines': self.config.detect_state_machines,
            'detect_recursion': self.config.detect_recursion,
            'output_dir': self.config.output_dir,
        }
        
        # Prepare args with config dict
        args_list = [(f[0], f[1], config_dict) for f in files]
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(_analyze_single_file, a): a for a in args_list}
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    if self.config.verbose:
                        print(f"Error analyzing {futures[future]}: {e}")
        
        return results
    
    def _analyze_sequential(self, files: List[Tuple[str, str]]) -> List[Dict]:
        """Analyze files sequentially."""
        results = []
        analyzer = FileAnalyzer(self.config, self.cache)
        
        for file_path, module_name in files:
            result = analyzer.analyze_file(file_path, module_name)
            if result:
                results.append(result)
        
        return results
    
    def _merge_results(self, results: List[Dict], project_path: str) -> AnalysisResult:
        """Merge all file analysis results."""
        merged = AnalysisResult(
            project_path=project_path,
            analysis_mode=self.config.mode,
        )
        

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_parallel. Skup się na wydzieleniu operacji o największej liczbie mutacji.