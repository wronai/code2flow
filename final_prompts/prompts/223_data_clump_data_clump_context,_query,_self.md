## Cel refaktoryzacji
Move method `context, query, self` from module `intent_matching` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (context, query, self) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher.match, code2flow.nlp.intent_matching.IntentMatcher.step_2d_context_score, code2flow.nlp.intent_matching.match, code2flow.nlp.intent_matching.step_2d_context_score.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `intent_matching`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.