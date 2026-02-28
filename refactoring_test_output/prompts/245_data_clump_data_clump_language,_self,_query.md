## Cel refaktoryzacji
Extract logic from `language, self, query` to a new method/function.

## Powód (z analizy DFG)
- Arguments (language, self, query) are used together in multiple functions: code2flow.nlp.pipeline.NLPPipeline.process, code2flow.nlp.pipeline.NLPPipeline._step_normalize, code2flow.nlp.pipeline.process, code2flow.nlp.pipeline._step_normalize, code2flow.nlp.normalization.QueryNormalizer.normalize, code2flow.nlp.normalization.normalize.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/normalization.py (linie 34-54)

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
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.