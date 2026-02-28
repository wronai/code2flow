## Cel refaktoryzacji
Extract logic from `_analyze_module_interactions` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_module_interactions' has high complexity: fan-out=7, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/coupling.py (linie 21-41)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_module_interactions(self) -> Dict[str, Set[str]]:
        """Track which modules call which other modules."""
        interactions = {}
        for func_name, func_info in self.result.functions.items():
            caller_mod = func_info.module or func_name.split('.')[0]
            if caller_mod not in interactions:
                interactions[caller_mod] = set()
                
            for callee in func_info.calls:
                callee_mod = callee.split('.')[0]
                if callee_mod != caller_mod:
                    interactions[caller_mod].add(callee_mod)
                    
        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in interactions.items()}
        
    def _detect_data_leakage(self) -> List[Dict[str, Any]]:
        """Detect when a module mutates data defined in another module."""
        leakages = []
        # Heuristic: if a function in module A mutates an object passed from module B
        # This is simplified: we look for mutations where the scope module 
        # is different from the variable's likely origin.
        for mutation in self.result.mutations:
            scope_parts = mutation.scope.split('.')
            mut_mod = scope_parts[0]
            
            # If the variable name looks like it belongs to another module (e.g. 'other_mod.data')
            if '.' in mutation.variable:
                origin_mod = mutation.variable.split('.')[0]
                if origin_mod != mut_mod and origin_mod in self.result.modules:
                    leakages.append({
                        "variable": mutation.variable,
                        "mutator_module": mut_mod,
                        "origin_module": origin_mod,
                        "line": mutation.line,
                        "file": mutation.file
                    })
        return leakages

    def _detect_shared_state(self) -> List[Dict[str, Any]]:
        """Detect modules that access/mutate the same global/shared variables."""
        shared = []
        variable_accessors = {} # var -> set(modules)
        
        for mutation in self.result.mutations:
            mut_mod = mutation.scope.split('.')[0]
            if mutation.variable not in variable_accessors:
                variable_accessors[mutation.variable] = set()
            variable_accessors[mutation.variable].add(mut_mod)
            

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_module_interactions. Skup się na wydzieleniu operacji o największej liczbie mutacji.