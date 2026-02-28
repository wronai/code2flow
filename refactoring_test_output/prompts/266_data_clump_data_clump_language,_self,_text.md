## Cel refaktoryzacji
Extract logic from `language, self, text` to a new method/function.

## Powód (z analizy DFG)
- Arguments (language, self, text) are used together in multiple functions: code2flow.nlp.normalization.QueryNormalizer._remove_stopwords, code2flow.nlp.normalization.QueryNormalizer.step_1e_remove_stopwords, code2flow.nlp.normalization._remove_stopwords, code2flow.nlp.normalization.step_1e_remove_stopwords.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/normalization.py (linie 117-137)

## Kod źródłowy do refaktoryzacji
```python
    def step_1e_remove_stopwords(self, text: str, language: str = "en") -> str:
        """Step 1e: Remove stopwords."""
        stopwords = self.config.stopwords.get(language, [])
        words = text.split()
        filtered = [w for w in words if w not in stopwords]
        return ' '.join(filtered)

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.