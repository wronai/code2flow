## Cel refaktoryzacji
Extract logic from `detect` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'detect' is highly complex: CC=1, fan-out=7, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 11+)

## Kod źródłowy do refaktoryzacji
```python
    def detect(self) -> List[CodeSmell]:
        """Record and return detected code smells."""
        smells = []
        smells.extend(self._detect_god_functions())
        smells.extend(self._detect_feature_envy())
        smells.extend(self._detect_data_clumps())
        smells.extend(self._detect_shotgun_surgery())
        smells.extend(self._detect_bottlenecks())
        smells.extend(self._detect_circular_dependencies())
        
        self.result.smells = smells
        return smells
        
    def _detect_god_functions(self) -> List[CodeSmell]:
        """Detect high fan-out / large functions."""
        smells = []
        for func_name, func_info in self.result.functions.items():
            metrics = self.result.metrics.get(func_name, {})
            fan_out = metrics.get('fan_out', 0)
            mutation_count = len([m for m in self.result.mutations if m.scope == func_name])
            
            # Use radon complexity if available
            complexity = func_info.complexity.get('cyclomatic', 1)
            
            if fan_out > 8 or mutation_count > 5 or complexity > 15:
                # Severity based on multiple factors
                severity = (fan_out / 15) * 0.4 + (mutation_count / 20) * 0.3 + (complexity / 25) * 0.3
                severity = min(1.0, severity)
                
                smells.append(CodeSmell(
                    name=f"God Function: {func_info.name}",
                    type="god_function",
                    file=func_info.file,
                    line=func_info.line,
                    severity=severity,
                    description=f"Function '{func_info.name}' is highly complex: CC={complexity}, fan-out={fan_out}, mutations={mutation_count}.",
                    context={"fan_out": fan_out, "mutations": mutation_count, "complexity": complexity}
                ))
        return smells
        
    def _detect_feature_envy(self) -> List[CodeSmell]:
        """Detect functions that use other objects more than their own."""
        smells = []
        # Simplified: look for functions mutating many variables in OTHER modules
        for func_name, func_info in self.result.functions.items():
            mut_mod = func_name.split('.')[0]
            foreign_mutations = []
            
            for mutation in self.result.mutations:
                if mutation.scope == func_name:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji detect. Skup się na wydzieleniu operacji o największej liczbie mutacji.