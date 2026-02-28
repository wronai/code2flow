## Cel refaktoryzacji
Extract logic from `benchmark_streaming_analyzer` to a new method/function.

## Powód (z analizy DFG)
- Function 'benchmark_streaming_analyzer' has high complexity: fan-out=10, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/benchmarks/benchmark_performance.py (linie 101-121)

## Kod źródłowy do refaktoryzacji
```python
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
        'avg_time': statistics.mean(times),
        'min_time': min(times),
        'max_time': max(times),
        'functions': function_count,
    }


def benchmark_with_strategies(project_path: str) -> dict:
    """Benchmark all strategies."""
    strategies = {
        'Quick': STRATEGY_QUICK,
        'Standard': STRATEGY_STANDARD,
        'Deep': STRATEGY_DEEP,
    }
    
    results = {}
    
    for name, strategy in strategies.items():
        print(f"\n[Strategy: {name}]")
        
        start = time.time()
        
        analyzer = StreamingAnalyzer(strategy=strategy)
        stats = {'files': 0, 'functions': 0, 'nodes': 0}
        
        for update in analyzer.analyze_streaming(project_path):

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji benchmark_streaming_analyzer. Skup się na wydzieleniu operacji o największej liczbie mutacji.