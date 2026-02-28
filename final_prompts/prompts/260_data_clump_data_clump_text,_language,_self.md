## Cel refaktoryzacji
Move method `text, language, self` from module `normalization` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (text, language, self) are used together in multiple functions: code2flow.nlp.normalization.QueryNormalizer._remove_stopwords, code2flow.nlp.normalization.QueryNormalizer.step_1e_remove_stopwords, code2flow.nlp.normalization._remove_stopwords, code2flow.nlp.normalization.step_1e_remove_stopwords.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `normalization`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/nlp/normalization.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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