## Cel refaktoryzacji
Move method `{{ target_function }}` from module `{{ source_module }}` to `{{ target_module }}`.

## Powód (Głęboka Analiza)
- {{ reason }}
- Status reachability: {{ reachability }}
- Feature Envy: Metoda używa więcej danych z `{{ target_module }}` niż z `{{ source_module }}`.
- Obce Mutacje: {{ foreign_mutations }}

## Kontekst strukturalny
- Zależności: {{ dependencies }}
- Mutacje w module docelowym: {{ foreign_mutations_context }}

## Dotknięte pliki
- {{ source_file }} — źródło
- {{ target_file }} — cel

## Kod źródłowy do przeniesienia
```python
{{ source_code }}
```

## Instrukcja
{{ instruction }}
