## Cel refaktoryzacji
Extract logic from `process` to a new method/function.

## Powód (z analizy DFG)
- Function 'process' has high complexity: fan-out=17, mutations=26.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/pipeline.py (linie 108-128)

## Kod źródłowy do refaktoryzacji
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
Wyekstrahuj mniejsze, spójne metody z funkcji process. Skup się na wydzieleniu operacji o największej liczbie mutacji.