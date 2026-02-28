## Cel refaktoryzacji
Extract logic from `benchmark_streaming_analyzer` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'benchmark_streaming_analyzer' is highly complex: CC=5, fan-out=10, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/benchmarks/benchmark_performance.py (linie 101+)

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