## Cel refaktoryzacji
Extract logic from `context, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (context, self, query) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher.match, code2flow.nlp.intent_matching.IntentMatcher.step_2d_context_score, code2flow.nlp.intent_matching.match, code2flow.nlp.intent_matching.step_2d_context_score.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py (linie 283-303)

## Kod źródłowy do refaktoryzacji
```python
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