## Cel refaktoryzacji
Extract logic from `language, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (language, self, query) are used together in multiple functions: code2flow.nlp.pipeline.NLPPipeline.process, code2flow.nlp.pipeline.NLPPipeline._step_normalize, code2flow.nlp.pipeline.process, code2flow.nlp.pipeline._step_normalize, code2flow.nlp.normalization.QueryNormalizer.normalize, code2flow.nlp.normalization.normalize.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/pipeline.py (linie 196-216)

## Kod źródłowy do refaktoryzacji
```python
    def _step_normalize(self, query: str, language: str) -> NormalizationResult:
        """Step 1: Query normalization."""
        if not self.config.enable_normalization:
            # Skip normalization, return identity
            return NormalizationResult(
                original=query,
                normalized=query,
                tokens=query.split(),
                language=language,
                steps_applied=["skipped"]
            )
        
        return self.normalizer.normalize(query, language)
    
    def _step_match_intent(self, normalized_query: str) -> IntentMatchingResult:
        """Step 2: Intent matching."""
        if not self.config.enable_intent_matching:
            return IntentMatchingResult(query=normalized_query)
        
        return self.intent_matcher.match(
            normalized_query,
            context=self.query_history[-3:] if self.query_history else None
        )
    
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
        

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.