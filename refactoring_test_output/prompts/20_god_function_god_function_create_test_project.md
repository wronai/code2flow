## Cel refaktoryzacji
Extract logic from `create_test_project` to a new method/function.

## Powód (z analizy DFG)
- Function 'create_test_project' has high complexity: fan-out=8, mutations=24.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/benchmarks/benchmark_performance.py (linie 24-44)

## Kod źródłowy do refaktoryzacji
```python
def create_test_project(size: str = "medium") -> str:
    """Create test project of specified size."""
    tmp_dir = Path(tempfile.mkdtemp())
    
    configs = {
        "small": {"modules": 10, "funcs_per_module": 5},
        "medium": {"modules": 50, "funcs_per_module": 10},
        "large": {"modules": 100, "funcs_per_module": 20},
    }
    
    config = configs.get(size, configs["medium"])
    
    for i in range(config["modules"]):
        lines = []
        
        # Add class
        lines.append(f"class Module{i}:")
        lines.append(f'    """Module {i} documentation."""')
        lines.append("")
        lines.append(f"    def __init__(self):")
        lines.append(f"        self.value = {i}")
        lines.append("")
        
        # Add methods
        for j in range(config["funcs_per_module"] // 2):
            lines.append(f"    def method_{j}(self, x):")
            lines.append(f"        if x > 0:")
            lines.append(f"            return self.value + x")
            lines.append(f"        return None")
            lines.append("")
        
        # Add standalone functions
        for j in range(config["funcs_per_module"] // 2):
            lines.append(f"def standalone_{i}_{j}(data):")
            lines.append(f"    result = []")
            lines.append(f"    for item in data:")
            lines.append(f"        if item > 0:")
            lines.append(f"            result.append(item * 2)")
            lines.append(f"    return result")
            lines.append("")
        
        # Add main for first module
        if i == 0:
            lines.append('if __name__ == "__main__":')
            lines.append('    print("Main entry point")')
        
        (tmp_dir / f"module_{i}.py").write_text('\n'.join(lines))
    
    return str(tmp_dir)


```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji create_test_project. Skup się na wydzieleniu operacji o największej liczbie mutacji.