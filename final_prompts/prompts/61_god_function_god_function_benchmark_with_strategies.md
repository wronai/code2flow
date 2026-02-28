## Cel refaktoryzacji
Extract logic from `benchmark_with_strategies` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'benchmark_with_strategies' is highly complex: CC=6, fan-out=6, mutations=11.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/benchmarks/benchmark_performance.py (linie 132+)

## Kod źródłowy do refaktoryzacji
```python
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
            if update['type'] == 'file_complete':
                stats['files'] += 1
                stats['functions'] += update.get('functions', 0)
            elif update['type'] == 'deep_complete':
                stats['nodes'] += update.get('nodes', 0)
            elif update['type'] == 'complete':
                pass
        
        elapsed = time.time() - start
        
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Files: {stats['files']}, Functions: {stats['functions']}")
        
        results[name] = {
            'time': elapsed,
            **stats
        }
    
    return results


def print_comparison(original: dict, streaming: dict):
    """Print comparison table."""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    print(f"\n{'Metric':<20} {'Original':<15} {'Streaming':<15} {'Speedup':<10}")
    print("-"*60)
    
    orig_avg = original['avg_time']
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji benchmark_with_strategies. Skup się na wydzieleniu operacji o największej liczbie mutacji.