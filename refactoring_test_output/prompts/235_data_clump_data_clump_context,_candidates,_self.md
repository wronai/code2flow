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
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 179-199)

## Kod źródłowy do refaktoryzacji
```python
    def _disambiguate(
        self,
        candidates: List[Entity],
        context: str
    ) -> List[Entity]:
        """3c. Disambiguate entities using context."""
        if not candidates:
            return candidates
        
        context_lower = context.lower()
        
        # Boost confidence for entities mentioned in context
        for candidate in candidates:
            # Check if entity name or related terms appear in context
            if candidate.name.lower() in context_lower:
                candidate.confidence = min(1.0, candidate.confidence + 0.15)
            
            # Check if source file is mentioned in context
            if candidate.source_file:
                file_name = candidate.source_file.split('/')[-1].lower()
                if file_name in context_lower:
                    candidate.confidence = min(1.0, candidate.confidence + 0.1)
        
        # Re-sort by updated confidence
        return sorted(candidates, key=lambda e: e.confidence, reverse=True)
    
    def _resolve_hierarchical(self, candidates: List[Entity]) -> List[Entity]:
        """3d. Resolve hierarchical names (Class.method -> method)."""
        resolved = []
        
        for candidate in candidates:
            # Check if name contains hierarchy separator
            if '.' in candidate.name:
                parts = candidate.name.split('.')
                
                # Create resolved entity with short name
                short_name = parts[-1]
                resolved_entity = Entity(
                    name=short_name,
                    qualified_name=candidate.qualified_name,
                    entity_type=candidate.entity_type,
                    confidence=candidate.confidence,
                    source_file=candidate.source_file,
                    line_number=candidate.line_number,
                    context=candidate.context,
                    aliases=candidate.aliases + [candidate.name]
                )
                resolved.append(resolved_entity)
                
                # Also keep original

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.