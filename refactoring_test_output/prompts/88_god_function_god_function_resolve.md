## Cel refaktoryzacji
Extract logic from `resolve` to a new method/function.

## Powód (z analizy DFG)
- Function 'resolve' has high complexity: fan-out=8, mutations=14.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 62-82)

## Kod źródłowy do refaktoryzacji
```python
    def resolve(
        self,
        query: str,
        context: Optional[str] = None,
        expected_types: Optional[List[str]] = None
    ) -> EntityResolutionResult:
        """Resolve entities from query (steps 3a-3e)."""
        result = EntityResolutionResult(query=query)
        
        # Determine expected entity types
        if expected_types is None:
            expected_types = self.config.entity_types
        
        # 3a. Extract candidate entities by type
        candidates = []
        for entity_type in expected_types:
            type_candidates = self._extract_candidates(query, entity_type)
            candidates.extend(type_candidates)
        
        # 3b. Match with threshold
        threshold = self.config.name_match_threshold
        matches = [c for c in candidates if c.confidence >= threshold]
        
        # 3c. Context-aware disambiguation
        if context and self.config.context_disambiguation:
            matches = self._disambiguate(matches, context)
        
        # 3d. Hierarchical resolution
        if self.config.hierarchical_resolution:
            matches = self._resolve_hierarchical(matches)
        
        # 3e. Alias resolution
        if self.config.alias_resolution:
            matches = self._resolve_aliases(matches)
        
        result.entities = matches
        
        # Determine if disambiguation needed
        if len(matches) > 1:
            top_confidences = [m.confidence for m in matches[:2]]
            if abs(top_confidences[0] - top_confidences[1]) < 0.1:
                result.disambiguation_needed = True
        
        # Set primary entity
        if matches:
            result.primary_entity = matches[0]
        
        return result
    
    def _extract_candidates(self, query: str, entity_type: str) -> List[Entity]:

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji resolve. Skup się na wydzieleniu operacji o największej liczbie mutacji.