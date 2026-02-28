## Cel refaktoryzacji
Extract logic from `detect` to a new method/function.

## Powód (z analizy DFG)
- Function 'detect' has high complexity: fan-out=5, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 11-31)

## Kod źródłowy do refaktoryzacji
```python
    def detect(self) -> List[CodeSmell]:
        """Record and return detected code smells."""
        smells = []
        smells.extend(self._detect_god_functions())
        smells.extend(self._detect_feature_envy())
        smells.extend(self._detect_data_clumps())
        smells.extend(self._detect_shotgun_surgery())
        
        self.result.smells = smells
        return smells
        
    def _detect_god_functions(self) -> List[CodeSmell]:
        """Detect high fan-out / large functions."""
        smells = []
        for func_name, metrics in self.result.metrics.items():
            fan_out = metrics.get('fan_out', 0)
            mutation_count = len([m for m in self.result.mutations if m.scope == func_name])
            
            if fan_out > 8 or mutation_count > 5:
                func_info = self.result.functions.get(func_name)
                if not func_info: continue
                
                smells.append(CodeSmell(
                    name=f"God Function: {func_info.name}",
                    type="god_function",
                    file=func_info.file,
                    line=func_info.line,
                    severity=min(1.0, (fan_out / 15) + (mutation_count / 20)),
                    description=f"Function '{func_info.name}' has high complexity: fan-out={fan_out}, mutations={mutation_count}.",
                    context={"fan_out": fan_out, "mutations": mutation_count}
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
                    if '.' in mutation.variable:
                        origin_mod = mutation.variable.split('.')[0]
                        if origin_mod != mut_mod:
                            foreign_mutations.append(mutation.variable)
                            
            if len(set(foreign_mutations)) >= 3:
                smells.append(CodeSmell(

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji detect. Skup się na wydzieleniu operacji o największej liczbie mutacji.