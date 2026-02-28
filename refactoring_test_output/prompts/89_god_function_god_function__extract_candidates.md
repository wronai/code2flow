## Cel refaktoryzacji
Extract logic from `_extract_candidates` to a new method/function.

## Powód (z analizy DFG)
- Function '_extract_candidates' has high complexity: fan-out=6, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 111-131)

## Kod źródłowy do refaktoryzacji
```python
    def _extract_candidates(self, query: str, entity_type: str) -> List[Entity]:
        """3a. Extract candidate entities of given type from query."""
        candidates = []
        
        # Get entities from codebase
        type_entities = self.codebase_entities.get(entity_type, [])
        
        for entity in type_entities:
            # Calculate name similarity
            similarity = self._name_similarity(query, entity.name)
            
            if similarity > 0.5:  # Minimum threshold for candidacy
                candidate = Entity(
                    name=entity.name,
                    qualified_name=entity.qualified_name,
                    entity_type=entity_type,
                    confidence=similarity,
                    source_file=entity.source_file,
                    line_number=entity.line_number,
                )
                candidates.append(candidate)
        
        # Also extract potential entities from query patterns
        pattern_matches = self._extract_from_patterns(query, entity_type)
        candidates.extend(pattern_matches)
        
        return candidates
    
    def _extract_from_patterns(self, query: str, entity_type: str) -> List[Entity]:
        """Extract entities using regex patterns."""
        candidates = []
        
        if entity_type == "function":
            # Match patterns like: function_name(), call function_name, etc.
            patterns = [
                r'\b(\w+)\s*\(',  # function_name(
                r'function\s+(\w+)',
                r'call\s+(\w+)',
                r'wywołaj\s+(\w+)',  # Polish
            ]
        elif entity_type == "class":
            patterns = [
                r'class\s+(\w+)',
                r'klasa\s+(\w+)',
                r'(\w+)\s*\.\s*\w+\s*\(',  # ClassName.method()
            ]
        elif entity_type == "file":
            patterns = [
                r'(\w+\.py)\b',
                r'file\s+(\w+)',

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _extract_candidates. Skup się na wydzieleniu operacji o największej liczbie mutacji.