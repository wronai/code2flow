## Cel refaktoryzacji
Extract logic from `analyze_streaming` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'analyze_streaming' is highly complex: CC=1, fan-out=16, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 294+)

## Kod źródłowy do refaktoryzacji
```python
    def analyze_streaming(
        self,
        project_path: str,
        output_callback: Optional[callable] = None
    ) -> Iterator[Dict]:
        """Analyze project with streaming output (yields partial results)."""
        start_time = time.time()
        project_path = Path(project_path).resolve()
        
        # Phase 1: Collect and prioritize files
        raw_files = self._collect_files(project_path)
        prioritized = self.prioritizer.prioritize_files(raw_files, project_path)
        
        total_files = len(prioritized)
        processed = 0
        
        self._report_progress(
            phase="collect",
            current=0,
            total=total_files,
            message=f"Found {total_files} files to analyze"
        )
        
        # Phase 2: Quick scan (functions/classes only)
        quick_results = []
        for priority in prioritized:
            if self._cancelled:
                break
            
            result = self._quick_scan_file(priority)
            if result:
                quick_results.append(result)
                processed += 1
                
                # Yield incremental result
                yield {
                    'type': 'file_complete',
                    'file': priority.file_path,
                    'priority': priority.priority_score,
                    'functions': len(result.get('functions', {})),
                    'classes': len(result.get('classes', {})),
                    'progress': processed / total_files,
                    'eta_seconds': self._estimate_eta(start_time, processed, total_files)
                }
                
                self._report_progress(
                    phase="quick_scan",
                    current=processed,
                    total=total_files,
                    message=f"Scanned {priority.module_name} (priority: {priority.priority_score:.1f})"
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji analyze_streaming. Skup się na wydzieleniu operacji o największej liczbie mutacji.