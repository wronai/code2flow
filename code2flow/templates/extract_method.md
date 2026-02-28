## Cel refaktoryzacji
Extract logic from `{{ target_function }}` to a new method/function.

## Powód (Głęboka Analiza)
- {{ reason }}
- Złożoność Cyklomatyczna: {{ metrics.complexity.cyclomatic if metrics.complexity else 'N/A' }} (Rank: {{ metrics.complexity.rank if metrics.complexity else 'N/A' }})
- Fan-out: {{ metrics.fan_out }}
- Mutacje: {{ mutations_context }}
- Reachability: {{ reachability }}

## Kontekst przepływu danych
- Wejście: {{ input_data }}
- Mutacje: {{ mutations_context }}

## Plik i Zakres
- {{ source_file }} (linie {{ start_line }}+)

## Kod źródłowy do refaktoryzacji
```python
{{ source_code }}
```

## Instrukcja
{{ instruction }}
