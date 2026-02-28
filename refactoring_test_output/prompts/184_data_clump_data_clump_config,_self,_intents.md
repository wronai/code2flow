## Cel refaktoryzacji
Extract logic from `config, self, intents` to a new method/function.

## Powód (z analizy DFG)
- Arguments (config, self, intents) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher.__init__, code2flow.nlp.intent_matching.__init__.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py (linie 80-100)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(
        self,
        config: Optional[IntentMatchingConfig] = None,
        intents: Optional[Dict[str, List[str]]] = None
    ):
        self.config = config or IntentMatchingConfig()
        self.intents = intents or self.DEFAULT_INTENTS
    
    def match(
        self,
        query: str,
        context: Optional[List[str]] = None
    ) -> IntentMatchingResult:
        """Match query to intents (steps 2a-2e)."""
        result = IntentMatchingResult(query=query)
        
        # 2a. Fuzzy matching
        fuzzy_matches = self._fuzzy_match(query)
        
        # 2c. Keyword matching
        keyword_matches = self._keyword_match(query)
        
        # 2d. Context scoring
        if context:
            self._apply_context(query, fuzzy_matches + keyword_matches, context)
        
        # Combine and deduplicate
        all_matches = self._combine_matches(fuzzy_matches + keyword_matches)
        result.all_matches = all_matches
        
        # 2e. Multi-intent resolution
        result.primary_intent = self._resolve_multi_intent(all_matches)
        result.strategy_used = self.config.multi_intent_strategy
        
        return result
    
    def _fuzzy_match(self, query: str) -> List[IntentMatch]:
        """2a. Fuzzy matching with configurable threshold."""
        matches = []
        threshold = self.config.fuzzy_threshold
        
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                similarity = self._calculate_similarity(query, phrase)
                if similarity >= threshold:
                    matches.append(IntentMatch(
                        intent=intent,
                        confidence=similarity,
                        matched_phrase=phrase,
                        match_type="fuzzy"

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.