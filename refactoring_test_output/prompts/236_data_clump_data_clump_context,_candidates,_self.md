## Cel refaktoryzacji
Extract logic from `context, candidates, self` to a new method/function.

## Powód (z analizy DFG)
- Arguments (context, candidates, self) are used together in multiple functions: code2flow.nlp.entity_resolution.EntityResolver._disambiguate, code2flow.nlp.entity_resolution.EntityResolver.step_3c_disambiguate, code2flow.nlp.entity_resolution._disambiguate, code2flow.nlp.entity_resolution.step_3c_disambiguate.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 316-336)

## Kod źródłowy do refaktoryzacji
```python
    def step_3c_disambiguate(self, candidates: List[Entity], context: str) -> List[Entity]:
        """Step 3c: Context-aware disambiguation."""
        return self._disambiguate(candidates, context)
    
    def step_3d_hierarchical_resolve(self, candidates: List[Entity]) -> List[Entity]:
        """Step 3d: Resolve hierarchical names."""
        return self._resolve_hierarchical(candidates)
    
    def step_3e_alias_resolve(self, candidates: List[Entity]) -> List[Entity]:
        """Step 3e: Resolve aliases."""
        return self._resolve_aliases(candidates)

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.