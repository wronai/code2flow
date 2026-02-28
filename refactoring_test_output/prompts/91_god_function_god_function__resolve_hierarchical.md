## Cel refaktoryzacji
Extract logic from `_resolve_hierarchical` to a new method/function.

## Powód (z analizy DFG)
- Function '_resolve_hierarchical' has high complexity: fan-out=3, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 205-225)

## Kod źródłowy do refaktoryzacji
```python
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
                resolved.append(candidate)
            else:
                resolved.append(candidate)
        
        return resolved
    
    def _resolve_aliases(self, candidates: List[Entity]) -> List[Entity]:
        """3e. Resolve aliases to canonical names."""
        resolved = []
        
        for candidate in candidates:
            # Check for known aliases
            if candidate.aliases:
                # Prefer qualified name as canonical
                if len(candidate.qualified_name) > len(candidate.name):
                    candidate.aliases.append(candidate.name)
                    candidate.name = candidate.qualified_name
            
            resolved.append(candidate)
        
        return resolved
    
    def _name_similarity(self, query: str, name: str) -> float:
        """Calculate similarity between query and entity name."""
        # Direct match
        if name.lower() in query.lower():

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _resolve_hierarchical. Skup się na wydzieleniu operacji o największej liczbie mutacji.