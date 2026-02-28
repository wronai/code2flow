## Cel refaktoryzacji
Move method `context, query, matches, self` from module `intent_matching` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (context, query, matches, self) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher._apply_context, code2flow.nlp.intent_matching._apply_context.
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
            
            for phrase in intent_phrases:
                phrase_words = phrase.lower().split()
                for word in phrase_words:
                    if word in context_text:
                        context_score += 0.1
            
            match.context_score = min(context_score, 0.5)  # Cap at 0.5
            match.confidence = min(1.0, match.confidence + match.context_score)
    
    def _combine_matches(self, matches: List[IntentMatch]) -> List[IntentMatch]:
        """Combine and deduplicate matches, keeping highest confidence per intent."""
        best_by_intent: Dict[str, IntentMatch] = {}
        
        for match in matches:
            if match.intent not in best_by_intent:
                best_by_intent[match.intent] = match
            elif match.confidence > best_by_intent[match.intent].confidence:
                best_by_intent[match.intent] = match
        
        # Sort by confidence descending
        return sorted(best_by_intent.values(), key=lambda m: m.confidence, reverse=True)
    
    def _resolve_multi_intent(self, matches: List[IntentMatch]) -> Optional[IntentMatch]:
        """2e. Multi-intent resolution strategy."""
        if not matches:
            return None
        
        strategy = self.config.multi_intent_strategy
        
        if strategy == "best_match":
            return matches[0]
        
        elif strategy == "combine":
            # Combine top matches if close in confidence
            if len(matches) >= 2:
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.