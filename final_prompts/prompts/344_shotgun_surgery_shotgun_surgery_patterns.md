## Cel refaktoryzacji
Extract logic from `patterns` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'patterns' spans 11 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 139+)

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