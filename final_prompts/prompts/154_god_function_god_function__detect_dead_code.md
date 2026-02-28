## Cel refaktoryzacji
Extract logic from `_detect_dead_code` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_dead_code' is highly complex: CC=1, fan-out=14, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 705+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_dead_code(self, result: AnalysisResult) -> None:
        """Use vulture to find dead code and update reachability."""
        if self.config.verbose:
            print("Detecting dead code with vulture...")
            
        try:
            v = vulture.Vulture(verbose=False)
            
            # vulture.scan takes the code content as a string
            for py_file in Path(result.project_path).rglob("*.py"):
                if not self.file_filter.should_process(str(py_file)):
                    continue
                try:
                    content = py_file.read_text(encoding='utf-8', errors='ignore')
                    v.scan(content, filename=str(py_file))
                except Exception:
                    continue
                    
            dead_code = v.get_unused_code()
            
            if self.config.verbose:
                print(f"  Vulture found {len(dead_code)} unused items")
            
            # Map unused code to our functions/classes
            for item in dead_code:
                if self.config.verbose:
                    item_lineno = getattr(item, 'lineno', getattr(item, 'first_lineno', 0))
                    print(f"  Vulture item: {item.filename}:{item_lineno} ({item.typ})")
                    
                # Match by file and line
                item_path = Path(item.filename).resolve()
                item_lineno = getattr(item, 'lineno', getattr(item, 'first_lineno', 0))
                for func_name, func_info in result.functions.items():
                    func_path = Path(func_info.file).resolve()
                    if func_path == item_path and func_info.line == item_lineno:
                        func_info.reachability = "unreachable"
                        
                for class_name, class_info in result.classes.items():
                    if Path(class_info.file).resolve() == Path(item.filename).resolve() and class_info.line == item.lineno:
                        class_info.reachability = "unreachable" # (if we add reachability to ClassInfo too)
                        
            # Mark others as reachable if they are NOT orphans
            for func_name, func_info in result.functions.items():
                if func_info.reachability == "unknown":
                    if func_info.called_by or func_name in result.entry_points:
                        func_info.reachability = "reachable"
        except Exception as e:
            if self.config.verbose:
                print(f"Error in dead code detection: {e}")
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_dead_code. Skup się na wydzieleniu operacji o największej liczbie mutacji.