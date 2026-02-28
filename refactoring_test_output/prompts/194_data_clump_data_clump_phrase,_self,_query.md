## Cel refaktoryzacji
Extract logic from `phrase, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (phrase, self, query) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher.step_2a_fuzzy_match, code2flow.nlp.intent_matching.IntentMatcher.step_2b_semantic_match, code2flow.nlp.intent_matching.IntentMatcher.step_2c_keyword_match, code2flow.nlp.intent_matching.step_2a_fuzzy_match, code2flow.nlp.intent_matching.step_2b_semantic_match, code2flow.nlp.intent_matching.step_2c_keyword_match.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py (linie 267-287)

## Kod źródłowy do refaktoryzacji
```python
    def step_2b_semantic_match(self, query: str, phrase: str) -> float:
        """Step 2b: Semantic similarity (placeholder for embeddings)."""
        # Placeholder - would use sentence embeddings in production
        return self._calculate_similarity(query, phrase)
    
    def step_2c_keyword_match(self, query: str, phrase: str) -> float:
        """Step 2c: Keyword matching score."""
        query_words = set(query.lower().split())
        phrase_words = set(phrase.lower().split())
        
        if not phrase_words:
            return 0.0
        
        intersection = len(query_words & phrase_words)
        return intersection / len(phrase_words)
    
    def step_2d_context_score(self, query: str, context: List[str]) -> float:
        """Step 2d: Calculate context relevance score."""
        window = ' '.join(context[-self.config.context_window:]).lower()
        query_words = query.lower().split()
        
        score = 0.0
        for word in query_words:
            if word in window:
                score += 0.1
        
        return min(score, 0.5)
    
    def step_2e_resolve_intents(self, matches: List[IntentMatch]) -> Optional[IntentMatch]:
        """Step 2e: Resolve multiple intent matches."""
        return self._resolve_multi_intent(matches)

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.