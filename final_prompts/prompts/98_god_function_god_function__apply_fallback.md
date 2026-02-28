## Cel refaktoryzacji
Extract logic from `_apply_fallback` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_apply_fallback' is highly complex: CC=1, fan-out=4, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/nlp/pipeline.py (linie 287+)

## Kod źródłowy do refaktoryzacji
```python
    def _apply_fallback(self, result: NLPPipelineResult) -> NLPPipelineResult:
        """4d. Apply fallback strategies when confidence is low."""
        result.fallback_used = True
        
        # Try keyword-only matching as fallback
        if result.intent_result.get_confidence() < 0.3:
            # Re-run with lower thresholds
            self.intent_matcher.config.fuzzy_threshold = 0.5
            fallback_intent = self.intent_matcher.match(
                result.normalized_query.normalized
            )
            
            if fallback_intent.get_confidence() > result.intent_result.get_confidence():
                result.intent_result = fallback_intent
                result.fallback_reason = "lowered_threshold"
            
            # Restore original threshold
            self.intent_matcher.config.fuzzy_threshold = self.config.intent_matching.fuzzy_threshold
        
        # If still no intent, default to generic search
        if result.intent_result.get_confidence() < 0.2:
            from .intent_matching import IntentMatch
            result.intent_result.primary_intent = IntentMatch(
                intent="generic_search",
                confidence=0.3,
                matched_phrase=result.normalized_query.normalized,
                match_type="fallback"
            )
            result.fallback_reason = "generic_search"
        
        return result
    
    def _format_action(self, result: NLPPipelineResult) -> Optional[str]:
        """4e. Format action recommendation."""
        intent = result.get_intent()
        entities = result.get_entities()
        
        if not intent:
            return "Unable to determine action. Please clarify your query."
        
        # Format based on intent type
        if intent == "find_function":
            if entities:
                return f"Search for function: {entities[0].name}"
            return "Search for functions"
        
        elif intent == "find_class":
            if entities:
                return f"Search for class: {entities[0].name}"
            return "Search for classes"
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _apply_fallback. Skup się na wydzieleniu operacji o największej liczbie mutacji.