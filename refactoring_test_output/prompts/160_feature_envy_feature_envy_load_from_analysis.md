## Cel refaktoryzacji
Move method `load_from_analysis` from module `entity_resolution` to `self`.

## Powód (z analizy DFG)
- Function 'load_from_analysis' mutates multiple variables in other modules: self.codebase_entities['function'], self.codebase_entities['class'], self.codebase_entities['module'].
- Feature Envy: Accesses more data from `self` than `entity_resolution`.
- Foreign Mutatons: self.codebase_entities['function'], self.codebase_entities['class'], self.codebase_entities['module']

## Kontekst przepływu danych
- Zależności: 
- Mutacje w module docelowym: This code mutates state in self

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/entity_resolution.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
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
                confidence=1.0,
                source_file=mod_info.file,
            )
            self.codebase_entities["module"].append(entity)
    
    # Individual step methods
    def step_3a_extract_entities(self, query: str, entity_type: str) -> List[Entity]:
        """Step 3a: Extract entities by type."""
        return self._extract_candidates(query, entity_type)
    
    def step_3b_match_threshold(self, candidates: List[Entity]) -> List[Entity]:
        """Step 3b: Apply name matching threshold."""

```

## Instrukcja
Przenieś metodę load_from_analysis do modułu, który posiada większość używanych w niej danych.