## Cel refaktoryzacji
Move method `normalized_query, expected_types, context, self` from module `pipeline` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (normalized_query, expected_types, context, self) are used together in multiple functions: code2flow.nlp.pipeline.NLPPipeline._step_resolve_entities, code2flow.nlp.pipeline._step_resolve_entities.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `pipeline`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/pipeline.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def _step_resolve_entities(
        self,
        normalized_query: str,
        expected_types: Optional[List[str]] = None,
        context: Optional[str] = None
    ) -> EntityResolutionResult:
        """Step 3: Entity resolution."""
        if not self.config.enable_entity_resolution:
            return EntityResolutionResult(query=normalized_query)
        
        return self.entity_resolver.resolve(
            normalized_query,
            context=context,
            expected_types=expected_types
        )
    
    def _infer_entity_types(
        self,
        intent_result: IntentMatchingResult
    ) -> Optional[List[str]]:
        """Infer expected entity types from matched intent."""
        if not intent_result.primary_intent:
            return None
        
        intent = intent_result.primary_intent.intent
        
        # Map intents to expected entity types
        intent_to_entities = {
            "find_function": ["function"],
            "find_class": ["class"],
            "analyze_flow": ["function", "class"],
            "show_call_graph": ["function", "class", "module"],
            "find_dependencies": ["module", "file"],
            "explain_code": ["function", "class"],
        }
        
        return intent_to_entities.get(intent)
    
    def _calculate_overall_confidence(self, result: NLPPipelineResult) -> float:
        """4c. Calculate overall pipeline confidence."""
        weights = {
            "intent": 0.5,
            "entity": 0.3,
            "normalization": 0.2,
        }
        
        intent_conf = result.intent_result.get_confidence()
        entity_conf = self._calculate_entity_confidence(result.entity_result)
        norm_conf = 1.0  # Normalization is reliable
        
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.