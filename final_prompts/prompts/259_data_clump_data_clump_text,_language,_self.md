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
    def _remove_stopwords(self, text: str, language: str) -> str:
        """1e. Remove stopwords."""
        stopwords = self.config.stopwords.get(language, [])
        words = text.split()
        filtered = [w for w in words if w not in stopwords]
        return ' '.join(filtered)
    
    def _tokenize(self, text: str) -> List[str]:
        """Split text into tokens."""
        return text.split()
    
    # Individual step methods for granular control
    def step_1a_lowercase(self, text: str) -> str:
        """Step 1a: Convert to lowercase."""
        return text.lower()
    
    def step_1b_remove_punctuation(self, text: str) -> str:
        """Step 1b: Remove punctuation."""
        return re.sub(r'[^\w\s\.]', ' ', text)
    
    def step_1c_normalize_whitespace(self, text: str) -> str:
        """Step 1c: Normalize whitespace."""
        return ' '.join(text.split())
    
    def step_1d_unicode_normalize(self, text: str) -> str:
        """Step 1d: Unicode NFKC normalization."""
        return unicodedata.normalize('NFKC', text)
    
    def step_1e_remove_stopwords(self, text: str, language: str = "en") -> str:
        """Step 1e: Remove stopwords."""
        stopwords = self.config.stopwords.get(language, [])
        words = text.split()
        filtered = [w for w in words if w not in stopwords]
        return ' '.join(filtered)
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.