## Cel refaktoryzacji
Move method `entity_type, query, self` from module `entity_resolution` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (entity_type, query, self) are used together in multiple functions: code2flow.nlp.entity_resolution.EntityResolver._extract_candidates, code2flow.nlp.entity_resolution.EntityResolver._extract_from_patterns, code2flow.nlp.entity_resolution.EntityResolver.step_3a_extract_entities, code2flow.nlp.entity_resolution._extract_candidates, code2flow.nlp.entity_resolution._extract_from_patterns, code2flow.nlp.entity_resolution.step_3a_extract_entities.
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
    def step_3a_extract_entities(self, query: str, entity_type: str) -> List[Entity]:
        """Step 3a: Extract entities by type."""
        return self._extract_candidates(query, entity_type)
    
    def step_3b_match_threshold(self, candidates: List[Entity]) -> List[Entity]:
        """Step 3b: Apply name matching threshold."""
        threshold = self.config.name_match_threshold
        return [c for c in candidates if c.confidence >= threshold]
    
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