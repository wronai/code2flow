## Cel refaktoryzacji
Extract logic from `normalize` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'normalize' is highly complex: CC=1, fan-out=8, mutations=14.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/nlp/normalization.py (linie 34+)

## Kod źródłowy do refaktoryzacji
```python
    def normalize(self, query: str, language: str = "en") -> NormalizationResult:
        """Apply full normalization pipeline (1a-1e)."""
        result = NormalizationResult(
            original=query,
            normalized=query,
            language=language,
        )
        
        # 1d. Unicode normalization (NFKC) - do first
        if self.config.unicode_normalize:
            result.normalized = self._unicode_normalize(result.normalized)
            result.steps_applied.append("unicode_nfkc")
        
        # 1a. Lowercase conversion
        if self.config.lowercase:
            result.normalized = self._lowercase(result.normalized)
            result.steps_applied.append("lowercase")
        
        # 1b. Punctuation removal
        if self.config.remove_punctuation:
            result.normalized = self._remove_punctuation(result.normalized)
            result.steps_applied.append("remove_punctuation")
        
        # 1c. Whitespace normalization
        if self.config.normalize_whitespace:
            result.normalized = self._normalize_whitespace(result.normalized)
            result.steps_applied.append("normalize_whitespace")
        
        # 1e. Stopword removal
        if self.config.remove_stopwords:
            result.normalized = self._remove_stopwords(result.normalized, language)
            result.steps_applied.append("remove_stopwords")
        
        # Tokenize
        result.tokens = self._tokenize(result.normalized)
        
        return result
    
    def _unicode_normalize(self, text: str) -> str:
        """1d. Normalize Unicode to NFKC form."""
        return unicodedata.normalize('NFKC', text)
    
    def _lowercase(self, text: str) -> str:
        """1a. Convert to lowercase."""
        return text.lower()
    
    def _remove_punctuation(self, text: str) -> str:
        """1b. Remove punctuation marks."""
        # Keep alphanumeric, whitespace, and dots (for qualified names)
        return re.sub(r'[^\w\s\.]', ' ', text)
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji normalize. Skup się na wydzieleniu operacji o największej liczbie mutacji.