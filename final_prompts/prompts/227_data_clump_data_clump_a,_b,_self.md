## Cel refaktoryzacji
Move method `a, b, self` from module `intent_matching` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (a, b, self) are used together in multiple functions: code2flow.nlp.intent_matching.IntentMatcher._calculate_similarity, code2flow.nlp.intent_matching._calculate_similarity.
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
    def _calculate_similarity(self, a: str, b: str) -> float:
        """Calculate string similarity using configured algorithm."""
        algorithm = self.config.fuzzy_algorithm
        
        if algorithm == "ratio":
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()
        
        elif algorithm == "partial_ratio":
            # Check if one is substring of other
            a_lower = a.lower()
            b_lower = b.lower()
            
            if a_lower in b_lower or b_lower in a_lower:
                return 0.9  # High score for partial match
            
            return SequenceMatcher(None, a_lower, b_lower).ratio()
        
        elif algorithm == "token_sort_ratio":
            # Sort tokens and compare
            a_sorted = ' '.join(sorted(a.lower().split()))
            b_sorted = ' '.join(sorted(b.lower().split()))
            return SequenceMatcher(None, a_sorted, b_sorted).ratio()
        
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    # Individual step methods
    def step_2a_fuzzy_match(self, query: str, phrase: str) -> float:
        """Step 2a: Calculate fuzzy match score."""
        return self._calculate_similarity(query, phrase)
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.