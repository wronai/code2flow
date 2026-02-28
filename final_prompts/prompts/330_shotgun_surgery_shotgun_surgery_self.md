## Cel refaktoryzacji
Extract logic from `self` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'self' spans 69 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/nlp/pipeline.py (linie 97+)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, config: Optional[NLPConfig] = None):
        self.config = config or FAST_NLP_CONFIG
        
        # Initialize components
        self.normalizer = QueryNormalizer(self.config.normalization)
        self.intent_matcher = IntentMatcher(self.config.intent_matching)
        self.entity_resolver = EntityResolver(self.config.entity_resolution)
        
        # Execution history for context
        self.query_history: List[str] = []
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.