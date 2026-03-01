# Plan Refaktoryzacji code2llm (v0.4.0)

## Podsumowanie Zmian

Refaktoryzacja monolitycznego `flow.py` (1145 linii) w modularną paczkę Python,
wprowadzenie **taksonomii 4 formatów** (v0.3.0), a następnie:
- **Rename**: `code2flow` → `code2llm` (v0.4.0)
- **Cleanup**: usunięcie martwego kodu (optimization/, visualizers/)
- **Reorganizacja**: generatory przeniesione do `generators/` subpakietu
- **Testy**: nazwy sprint-based → feature-based

## Aktualna Struktura (v0.4.0)

```
code2llm/
├── code2llm/                  # Główna paczka
│   ├── __init__.py            # Eksportuje publiczne API (v0.4.0)
│   ├── __main__.py            # Entry point: python -m code2llm
│   ├── cli.py                 # CLI: code2llm (map,toon,flow,context,all)
│   ├── core/                  # Klasy bazowe i konfiguracja
│   │   ├── __init__.py
│   │   ├── config.py          # Config, ANALYSIS_MODES, NODE_COLORS
│   │   ├── models.py          # FlowNode, FlowEdge, DataFlow, AnalysisResult
│   │   ├── analyzer.py        # ProjectAnalyzer - główny orchestrator
│   │   └── streaming_analyzer.py  # StreamingAnalyzer z priorytetyzacją
│   ├── analysis/              # Moduły analizy
│   │   ├── call_graph.py      # CallGraphExtractor
│   │   ├── cfg.py             # CFGExtractor - Control Flow Graph
│   │   ├── coupling.py        # CouplingAnalyzer
│   │   ├── data_analysis.py   # DataAnalyzer
│   │   ├── dfg.py             # DFGExtractor - Data Flow Graph
│   │   ├── pipeline_detector.py # PipelineDetector (networkx)
│   │   ├── side_effects.py    # SideEffectDetector
│   │   ├── type_inference.py  # TypeInference (AST-based)
│   │   └── smells.py          # SmellDetector
│   ├── exporters/             # Eksport do formatów (7 eksporterów)
│   │   ├── __init__.py
│   │   ├── base.py            # Exporter ABC
│   │   ├── toon.py            # ToonExporter → analysis.toon (diagnostyka)
│   │   ├── map_exporter.py    # MapExporter → map.toon (struktura)
│   │   ├── flow_exporter.py   # FlowExporter → flow.toon (data-flow)
│   │   ├── context_exporter.py # ContextExporter → context.md (LLM)
│   │   ├── llm_exporter.py    # backward-compat shim → ContextExporter
│   │   ├── yaml_exporter.py   # YAMLExporter → analysis.yaml
│   │   ├── json_exporter.py   # JSONExporter → analysis.json
│   │   └── mermaid_exporter.py # MermaidExporter → *.mmd
│   ├── generators/            # Generatory (przeniesione z root-level)
│   │   ├── __init__.py
│   │   ├── llm_flow.py        # LLM flow summary generator
│   │   ├── llm_task.py        # LLM task breakdown generator
│   │   └── mermaid.py         # Mermaid PNG generator
│   ├── nlp/                   # NLP pipeline
│   ├── patterns/              # Detekcja wzorców (do podłączenia w v0.5)
│   └── refactor/              # Silnik refaktoryzacji
├── tests/
│   ├── test_analyzer.py
│   ├── test_edge_cases.py
│   ├── test_nlp_pipeline.py
│   ├── test_flow_exporter.py      # (was test_sprint2_flow.py)
│   ├── test_pipeline_detector.py  # (was test_sprint3_pipelines.py)
│   ├── test_deep_analysis.py      # (was test_sprint4.py)
│   ├── test_prompt_engine.py      # (was test_sprint5.py)
│   ├── test_toon_v2.py
│   ├── test_refactoring_engine.py
│   ├── test_format_quality.py
│   └── test_advanced_analysis.py
├── benchmarks/
│   ├── benchmark_performance.py
│   ├── benchmark_format_quality.py
│   └── test_performance.py
├── setup.py
├── pyproject.toml
├── Makefile
├── requirements.txt
└── README.md
```

### Usunięte w v0.4.0
- `optimization/` — 1590L martwego kodu (zero importów z zewnątrz)
- `visualizers/` — 150L martwego kodu (PNG via mermaid)

## Kluczowe Decyzje Architektoniczne

### 1. Separacja Odpowiedzialności
- **core/**: Modele danych i główny analyzer
- **analysis/**: Logika parsowania AST (CFG, DFG, Call Graph, pipelines, side effects)
- **exporters/**: Formaty wyjściowe (TOON, YAML, JSON, Mermaid, Context)
- **generators/**: Generatory LLM flow, task, Mermaid PNG
- **patterns/**: Detekcja wzorców behawioralnych

### 2. API Publiczne
```python
from code2llm import ProjectAnalyzer, Config
from code2llm.core.models import AnalysisResult
```

### 3. CLI
```bash
code2llm /path/to/project -m hybrid -o ./output -f toon,map,flow,context,all
```

### 4. Konfiguracja
- `Config` dataclass z opcjami analizy
- `ANALYSIS_MODES` - dostępne tryby
- `NODE_COLORS` - kolory dla wizualizacji

## Porównanie z Narzędziami Referencyjnymi

| Cecha | code2llm | PyCG | Pyan | Angr | Code2Logic |
|-------|----------|------|------|------|------------|
| CFG | ✓ | ✓ | ✗ | ✓ | ✓ |
| DFG | ✓ | ✗ | ✗ | ✓ | ✓ |
| Call Graph | ✓ | ✓ | ✓ | ✓ | ✓ |
| Wzorce | ✓ | ✗ | ✗ | ✗ | ✓ |
| LLM Output | ✓ | ✗ | ✗ | ✗ | ✓ |
| Modularność | ✓ | ✓ | ✓ | ✗ | ? |

## Przyszłe Rozszerzenia

### Priorytet Wysoki
1. [ ] CI/CD pipeline (GitHub Actions)
2. [ ] Type hints (mypy compliant)
3. [ ] Obsługa dynamicznej analizy (sys.settrace)

### Priorytet Średni
4. [ ] Więcej formatów wyjściowych (Graphviz DOT, PlantUML)
5. [ ] Interaktywna wizualizacja (D3.js/Plotly)
6. [ ] Plugin system dla custom extractors
7. [ ] Cache analizy (pickle/JSON)

### Priorytet Niski
8. [ ] Wsparcie dla Cython
9. [ ] Analiza bytecode (dis)
10. [ ] Integracja z IDE (VS Code extension)
11. [ ] Web UI (Flask/FastAPI)

## Komendy Makefile

```bash
make install       # pip install -e .
make dev-install   # pip install -e ".[dev]"
make test          # pytest tests/
make lint          # flake8 + black --check
make format        # black code2llm/
make typecheck     # mypy code2llm/
make run           # code2llm ../python/stts_core
make build         # python setup.py sdist bdist_wheel
make clean         # rm -rf build/ dist/
make check         # lint + typecheck + test
```

## Instalacja

```bash
pip install -e .
code2llm /path/to/project -v
```

## Użycie Programowe

```python
from code2llm import ProjectAnalyzer, Config
from code2llm.exporters import YAMLExporter

config = Config(mode='hybrid', max_depth_enumeration=10)
analyzer = ProjectAnalyzer(config)
result = analyzer.analyze_project('/path/to/project')

exporter = YAMLExporter()
exporter.export(result, 'output.yaml')  # Default: skip empty values
exporter.export(result, 'output_full.yaml', include_defaults=True)  # Full output
```

## Eksport Danych (Compact by Default)

Wszystkie eksporty YAML/JSON domyślnie **ukrywają puste wartości**:
- `column: null` - pomijane
- `conditions: []` - pomijane  
- `data_flow: []` - pomijane
- `metadata: {}` - pomijane
- `returns: null` - pomijane

Aby pokazać wszystkie pola (np. dla debugowania):
```bash
code2llm /path/to/project --full
```

Programowo:
```python
result.to_dict()  # Default: False - skip empty values
result.to_dict(include_defaults=True)  # Include all fields
```

## Znane Problemy

1. **Dynamic analysis**: Wymaga implementacji `DynamicTracer` w pełni
2. **Cross-file resolution**: Może nie rozwiązać wszystkich importów
3. **Complex control flow**: Np. async/await, generators - uproszczona obsługa
4. **Performance**: Duże projekty (>10k LOC) mogą być wolne

## Konwencje Kodu

- **PEP 8** z line-length=100
- **Type hints** dla wszystkich funkcji publicznych
- **Docstrings** Google style
- **Black** do formatowania
- **isort** do importów (opcjonalnie)

## Status: ✅ Ukończone (v0.4.0)

- [x] Rename code2flow → code2llm
- [x] Struktura katalogów (reorganizacja generators/)
- [x] Moduły core/
- [x] Moduły analysis/ (+ pipeline_detector, side_effects, type_inference)
- [x] Moduły exporters/ (7 eksporterów, wszystkie podłączone do CLI)
- [x] Moduły generators/ (przeniesione z root-level)
- [x] Usunięcie martwego kodu (optimization/, visualizers/)
- [x] CLI
- [x] setup.py / pyproject.toml
- [x] Makefile
- [x] Testy (feature-named)
- [ ] Dokumentacja API (do zrobienia)
