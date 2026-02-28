## Cel refaktoryzacji
Extract logic from `benchmark_original_analyzer` to a new method/function.

## Powód (z analizy DFG)
- Function 'benchmark_original_analyzer' has high complexity: fan-out=11, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/benchmarks/benchmark_performance.py (linie 75-95)

## Kod źródłowy do refaktoryzacji
```python
def benchmark_original_analyzer(project_path: str, runs: int = 3) -> dict:
    """Benchmark original ProjectAnalyzer."""
    print(f"\n[Original Analyzer - {runs} runs]")
    
    times = []
    
    for run in range(runs):
        start = time.time()
        
        FAST_CONFIG.performance.parallel_enabled = False
        analyzer = ProjectAnalyzer(FAST_CONFIG)
        result = analyzer.analyze_project(project_path)
        
        elapsed = time.time() - start
        times.append(elapsed)
        
        print(f"  Run {run+1}: {elapsed:.2f}s - {result.get_function_count()} functions")
    
    return {
        'avg_time': statistics.mean(times),
        'min_time': min(times),
        'max_time': max(times),
        'functions': result.get_function_count() if 'result' in dir() else 0,
    }


def benchmark_streaming_analyzer(project_path: str, runs: int = 3) -> dict:
    """Benchmark new StreamingAnalyzer."""
    print(f"\n[Streaming Analyzer (Quick) - {runs} runs]")
    
    times = []
    
    for run in range(runs):
        start = time.time()
        
        analyzer = StreamingAnalyzer(strategy=STRATEGY_QUICK)
        
        function_count = 0
        for update in analyzer.analyze_streaming(project_path):
            if update['type'] == 'file_complete':
                function_count += update.get('functions', 0)
            elif update['type'] == 'complete':
                pass
        
        elapsed = time.time() - start
        times.append(elapsed)
        
        print(f"  Run {run+1}: {elapsed:.2f}s")
    
    return {

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji benchmark_original_analyzer. Skup się na wydzieleniu operacji o największej liczbie mutacji.