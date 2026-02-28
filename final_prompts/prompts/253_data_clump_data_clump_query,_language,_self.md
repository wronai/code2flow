## Cel refaktoryzacji
Move method `query, language, self` from module `pipeline` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (query, language, self) are used together in multiple functions: code2flow.nlp.normalization.QueryNormalizer.normalize, code2flow.nlp.normalization.normalize, code2flow.nlp.pipeline.NLPPipeline.process, code2flow.nlp.pipeline.NLPPipeline._step_normalize, code2flow.nlp.pipeline.process, code2flow.nlp.pipeline._step_normalize.
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
    def process(self, query: str, language: str = "en") -> NLPPipelineResult:
        """Process query through full pipeline (4a-4e)."""
        import time
        
        start_time = time.time()
        stages = []
        
        # 4a. Pipeline orchestration - Step 1: Normalization
        norm_start = time.time()
        normalized = self._step_normalize(query, language)
        norm_time = (time.time() - norm_start) * 1000
        
        stages.append(PipelineStage(
            stage_name="normalization",
            success=True,
            result=normalized,
            execution_time_ms=norm_time
        ))
        
        # Step 2: Intent Matching
        intent_start = time.time()
        intent_result = self._step_match_intent(normalized.normalized)
        intent_time = (time.time() - intent_start) * 1000
        
        intent_success = intent_result.primary_intent is not None
        stages.append(PipelineStage(
            stage_name="intent_matching",
            success=intent_success,
            result=intent_result,
            execution_time_ms=intent_time
        ))
        
        # Step 3: Entity Resolution
        entity_start = time.time()
        
        # Determine expected entity types from intent
        expected_types = self._infer_entity_types(intent_result)
        
        entity_result = self._step_resolve_entities(
            normalized.normalized,
            expected_types=expected_types,
            context=normalized.normalized
        )
        entity_time = (time.time() - entity_start) * 1000
        
        entity_success = len(entity_result.entities) > 0
        stages.append(PipelineStage(
            stage_name="entity_resolution",
            success=entity_success,
            result=entity_result,
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.