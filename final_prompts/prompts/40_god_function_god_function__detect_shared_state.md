## Cel refaktoryzacji
Extract logic from `_detect_shared_state` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_shared_state' is highly complex: CC=1, fan-out=7, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/coupling.py (linie 60+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_shared_state(self) -> List[Dict[str, Any]]:
        """Detect modules that access/mutate the same global/shared variables."""
        shared = []
        variable_accessors = {} # var -> set(modules)
        
        for mutation in self.result.mutations:
            mut_mod = mutation.scope.split('.')[0]
            if mutation.variable not in variable_accessors:
                variable_accessors[mutation.variable] = set()
            variable_accessors[mutation.variable].add(mut_mod)
            
        for var, mods in variable_accessors.items():
            if len(mods) > 1:
                shared.append({
                    "variable": var,
                    "modules": list(mods)
                })
        return shared
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_shared_state. Skup się na wydzieleniu operacji o największej liczbie mutacji.