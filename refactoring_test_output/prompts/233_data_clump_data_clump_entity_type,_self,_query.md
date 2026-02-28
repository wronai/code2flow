## Cel refaktoryzacji
Extract logic from `entity_type, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (entity_type, self, query) are used together in multiple functions: code2flow.nlp.entity_resolution.EntityResolver._extract_candidates, code2flow.nlp.entity_resolution.EntityResolver._extract_from_patterns, code2flow.nlp.entity_resolution.EntityResolver.step_3a_extract_entities, code2flow.nlp.entity_resolution._extract_candidates, code2flow.nlp.entity_resolution._extract_from_patterns, code2flow.nlp.entity_resolution.step_3a_extract_entities.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 139-159)

## Kod źródłowy do refaktoryzacji
```python
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
                r'plik\s+(\w+)',
            ]
        else:
            patterns = [r'\b(\w+)\b']
        
        for pattern in patterns:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                candidates.append(Entity(
                    name=name,
                    qualified_name=name,
                    entity_type=entity_type,
                    confidence=0.7,  # Pattern-based confidence
                ))
        
        return candidates
    
    def _disambiguate(
        self,
        candidates: List[Entity],
        context: str
    ) -> List[Entity]:
        """3c. Disambiguate entities using context."""
        if not candidates:
            return candidates
        
        context_lower = context.lower()

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.