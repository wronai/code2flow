## Cel refaktoryzacji
Extract logic from `match` to a new method/function.

## Powód (z analizy DFG)
- Function 'match' has high complexity: fan-out=6, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py (linie 88-108)

## Kod źródłowy do refaktoryzacji
```python
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
                    ))
        
        return matches
    
    def _keyword_match(self, query: str) -> List[IntentMatch]:
        """2c. Keyword matching with configurable weight."""
        matches = []
        query_words = set(query.lower().split())

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji match. Skup się na wydzieleniu operacji o największej liczbie mutacji.