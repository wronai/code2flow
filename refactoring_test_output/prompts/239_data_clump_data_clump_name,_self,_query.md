## Cel refaktoryzacji
Extract logic from `name, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (name, self, query) are used together in multiple functions: code2flow.nlp.entity_resolution.EntityResolver._name_similarity, code2flow.nlp.entity_resolution._name_similarity.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py (linie 251-271)

## Kod źródłowy do refaktoryzacji
```python
    def _name_similarity(self, query: str, name: str) -> float:
        """Calculate similarity between query and entity name."""
        # Direct match
        if name.lower() in query.lower():
            return 0.95
        
        if query.lower() in name.lower():
            return 0.9
        
        # Fuzzy match
        return SequenceMatcher(None, query.lower(), name.lower()).ratio()
    
    def load_from_analysis(self, analysis_result) -> None:
        """Load entities from code analysis result."""
        self.codebase_entities = {
            "function": [],
            "class": [],
            "module": [],
        }
        
        # Load functions
        for func_name, func_info in analysis_result.functions.items():
            entity = Entity(
                name=func_info.name,
                qualified_name=func_info.qualified_name,
                entity_type="function",
                confidence=1.0,
                source_file=func_info.file,
                line_number=func_info.line,
            )
            self.codebase_entities["function"].append(entity)
        
        # Load classes
        for class_name, class_info in analysis_result.classes.items():
            entity = Entity(
                name=class_info.name,
                qualified_name=class_info.qualified_name,
                entity_type="class",
                confidence=1.0,
                source_file=class_info.file,
                line_number=class_info.line,
            )
            self.codebase_entities["class"].append(entity)
        
        # Load modules
        for mod_name, mod_info in analysis_result.modules.items():
            entity = Entity(
                name=mod_info.name,
                qualified_name=mod_info.name,
                entity_type="module",

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.