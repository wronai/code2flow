## Cel refaktoryzacji
Move method `context, candidates, self` from module `entity_resolution` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (context, candidates, self) are used together in multiple functions: code2flow.nlp.entity_resolution.EntityResolver._disambiguate, code2flow.nlp.entity_resolution.EntityResolver.step_3c_disambiguate, code2flow.nlp.entity_resolution._disambiguate, code2flow.nlp.entity_resolution.step_3c_disambiguate.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `entity_resolution`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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