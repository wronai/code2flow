## Cel refaktoryzacji
Extract logic from `_collect_files` to a new method/function.

## Powód (z analizy DFG)
- Function '_collect_files' has high complexity: fan-out=7, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 482-502)

## Kod źródłowy do refaktoryzacji
```python
    def _collect_files(self, project_path: Path) -> List[Tuple[str, str]]:
        """Collect all Python files with their module names."""
        files = []
        
        for py_file in project_path.rglob("*.py"):
            file_str = str(py_file)
            if not self.file_filter.should_process(file_str):
                continue
            
            # Calculate module name
            rel_path = py_file.relative_to(project_path)
            parts = list(rel_path.parts)[:-1]  # Remove .py
            if py_file.name == '__init__.py':
                module_name = '.'.join(parts) if parts else project_path.name
            else:
                module_name = '.'.join(parts + [py_file.stem])
            
            files.append((file_str, module_name))
        
        return files
    
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
        

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _collect_files. Skup się na wydzieleniu operacji o największej liczbie mutacji.