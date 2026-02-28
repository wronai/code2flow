## Cel refaktoryzacji
Extract logic from `_keyword_match` to a new method/function.

## Powód (z analizy DFG)
- Function '_keyword_match' has high complexity: fan-out=8, mutations=12.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/intent_matching.py (linie 134-154)

## Kod źródłowy do refaktoryzacji
```python
    def _keyword_match(self, query: str) -> List[IntentMatch]:
        """2c. Keyword matching with configurable weight."""
        matches = []
        query_words = set(query.lower().split())
        
        for intent, phrases in self.intents.items():
            best_score = 0.0
            best_phrase = ""
            
            for phrase in phrases:
                phrase_words = set(phrase.lower().split())
                
                # Calculate Jaccard similarity
                intersection = len(query_words & phrase_words)
                union = len(query_words | phrase_words)
                
                if union > 0:
                    score = intersection / union
                    if score > best_score:
                        best_score = score
                        best_phrase = phrase
            
            # Apply keyword weight
            weighted_score = best_score * self.config.keyword_weight
            
            if weighted_score > 0:
                matches.append(IntentMatch(
                    intent=intent,
                    confidence=weighted_score,
                    matched_phrase=best_phrase,
                    match_type="keyword"
                ))
        
        return matches
    
    def _apply_context(
        self,
        query: str,
        matches: List[IntentMatch],
        context: List[str]
    ) -> None:
        """2d. Apply context window scoring."""
        window_size = self.config.context_window
        context_text = ' '.join(context[-window_size:]).lower()
        
        for match in matches:
            # Boost confidence if intent keywords appear in context
            intent_phrases = self.intents.get(match.intent, [])
            context_score = 0.0
            

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _keyword_match. Skup się na wydzieleniu operacji o największej liczbie mutacji.