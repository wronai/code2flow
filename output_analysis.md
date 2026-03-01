# Analiza plików wyjściowych code2llm — przydatność do ewolucyjnej refaktoryzacji

## Ranking plików od najważniejszego do najmniej przydatnego

| # | Plik | Rozmiar | Cel | Ocena jakości | Użyteczność dla refaktoryzacji |
|---|------|---------|-----|---------------|-------------------------------|
| 🥇 | [analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon) | 34KB, 620L | Diagnostyka zdrowia kodu | ⭐⭐⭐⭐ | **Najlepsza baza** — CC, hotspoty, god modules |
| 🥈 | [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon) | 12KB, 245L | Przepływ danych | ⭐⭐⭐ | Pipelines + contracts, ale wymaga poprawek |
| 🥉 | [map.toon](file:///home/tom/github/wronai/code2llm/output_all/map.toon) | 22KB, 311L | Mapa strukturalna | ⭐⭐⭐⭐ | Doskonały przegląd API i sygnatur |
| 4 | [context.md](file:///home/tom/github/wronai/code2llm/output_all/context.md) | 35KB, 611L | Narracja dla LLM | ⭐⭐ | Zbyt rozwlekły, mało unikalnych insightów |
| 5 | [flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/flow.mmd) | 11KB, 206L | Diagram przepływu | ⭐ | **BUG**: identyczny z calls.mmd i compact_flow.mmd |
| 5 | [compact_flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/compact_flow.mmd) | 11KB, 206L | Kompaktowy diagram | ⭐ | **BUG**: identyczna kopia flow.mmd |
| 5 | [calls.mmd](file:///home/tom/github/wronai/code2llm/output_all/calls.mmd) | 11KB, 206L | Graf wywołań | ⭐ | **BUG**: identyczna kopia flow.mmd |

---

## Szczegółowa analiza każdego pliku

### 🥇 [analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon) — Najlepszy do refaktoryzacji

**Mocne strony:**
- **HEALTH[20]** — precyzyjna identyfikacja god modules (3 pliki 🔴) i 17 funkcji z CC>15
- **REFACTOR[4]** — konkretne akcje: *"split analyzer.py, split streaming_analyzer.py, split 17 high-CC methods"*
- **FUNCTIONS** — 50 funkcji CC≥10, z flagami `loops+cond+ret`, liczbą wyjść i węzłów — doskonałe do priorytetyzacji
- **HOTSPOTS** — top-10 funkcji po fan-out, czytelne opisy
- **CLASSES** — wizualne bar-charty z CC̄ i max, czytelne `!!` markery
- **D: (Details)** — call-chain per klasa z CC na każdym poziomie — widać dokładnie gdzie jest "gorąco"

**Słabe strony:**
- COUPLING mówi "*no cross-package imports detected*" — **fałszywie negatywne** — `flow_exporter` importuje z `core.models`, `analysis.pipeline_detector`, `analysis.type_inference` itd.
- LAYERS nie pokazuje `←in` (import count) — wszystko ma `←0`, co sugeruje bug w ekstrakcji importów cross-package
- Brak sekcji **EVOLUTION** — nie porównuje z poprzednimi uruchomieniami

**Rekomendacja:** To plik #1 do podpisania backlogu refaktoryzacji. Każdy `!!` w FUNCTIONS to potencjalny ticket.

---

### 🥈 [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon) — Przepływ danych i kontrakty

**Mocne strony:**
- **PIPELINES[6]** — wykrywa łańcuchy wywołań z CC per stage, purity scoring, bottleneck identification
- **CONTRACTS** — IN/OUT types, SIDE-EFFECT, SMELL per stage — kluczowe do Interface Segregation
- **DATA_TYPES** — hub-type detection ze split recommendations (np. `AnalysisResult → StructureResult, MetricsResult, FlowResult`)
- **TRANSFORMS** — fan-out ≥10, identyfikuje "script-in-disguise" patterny

**Poważne problemy:**
1. **Pipeline detection nie widzi głównych pipeline'ów code2llm:**
   - Brak: `CLI → ProjectAnalyzer → FileAnalyzer → Exporters` (to jest GŁÓWNY pipeline)
   - Brak: `NLPPipeline: normalize → match_intent → resolve_entities → format`
   - Znalazł: `validate_toon`, `generators`, `scripts` — to są **peripheral**, nie core
2. **Klasyfikacja domen:** 4 z 6 to "IO" — zbyt generyczne, nie mówi nic o architekturze
3. **HUB-TYPES:** `str` z 205 consumerami nie jest użytecznym hub-type — to szum
4. **SIDE_EFFECTS:** klasyfikuje `dict.get()` jako IO — fałszywie pozytywne

**Rekomendacja:** flow.toon ma NAJWYŻSZY potencjał po poprawkach, ale obecna wersja nie widzi prawdziwych pipeline'ów aplikacji.

---

### 🥉 [map.toon](file:///home/tom/github/wronai/code2llm/output_all/map.toon) — Strukturalna mapa

**Mocne strony:**
- **M[49]** — kompletna lista modułów z LOC — instant overview
- **D: Details** — pełne sygnatury funkcji z liczbą argumentów i docstring
- **Klasy z method-count i krótkim opisem** — idealne do szybkiego API review

**Słabe strony:**
- Brak informacji o **import graph** (kto importuje kogo)
- Brak **dependency layers** — nie wiadomo które moduły zależą od których
- Brak **public/private** rozróżnienia — `_render_details` i `export` traktowane jednakowo

**Rekomendacja:** Doskonały "spis treści" projektu. Używaj go do szybkiego nav po strukturze.

---

### 4. [context.md](file:///home/tom/github/wronai/code2llm/output_all/context.md) — Narracja dla LLM

**Mocne strony:**
- Jedyny plik w Markdown — bezpośrednio gotowy do wklejenia w prompt LLM
- **Public API Surface** z liczbą wywołań — widać najważniejsze interfejsy
- **System Interactions** mermaid diagram — szybki overview

**Poważne problemy:**
1. **Za długi (611L, 35KB)** — większość to redundancja z [map.toon](file:///home/tom/github/wronai/code2llm/output_all/map.toon)
2. **Process Flows** są puste/jednopoziomowe — np. "Flow 1: main → create_parser" i koniec
3. **Architecture by Module** to prosta lista (functions/classes count) — bez żadnych insightów
4. **Data Transformation Functions** — lista bez wyjaśnienia jakie transformacje wykonują
5. **Entry Points: 406** — to fałszywe, traktuje KAŻDĄ publiczną funkcję jako entry point

**Rekomendacja:** Wymaga gruntownej przebudowy. W obecnej formie jest zbyt rozwlekły i mało informacyjny.

---

### 5. [flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/flow.mmd), [compact_flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/compact_flow.mmd), [calls.mmd](file:///home/tom/github/wronai/code2llm/output_all/calls.mmd) — Diagramy Mermaid

> [!CAUTION]
> **BUG: Wszystkie 3 pliki są IDENTYCZNE (11264 bajtów każdy)**. To wyraźny bug w `MermaidExporter` — [compact_flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/compact_flow.mmd) powinien mieć deduplikowane węzły, [calls.mmd](file:///home/tom/github/wronai/code2llm/output_all/calls.mmd) powinien mieć tylko krawędzie wywołań.

**Dodatkowe problemy:**
- Node IDs są hashowane (`code2llm_analysis_da_851`) — nieczytalne dla człowieka
- Brak cross-subgraph edges — większość modułów wygląda jak izolowane wyspy
- PNG wagi 38KB mimo 206L — podejrzanie mały, prawdopodobnie renderuje się jako flat grid
- Brak colour-coding wg CC czy fan-out

---

## Który plik najlepszy do ewolucyjnej refaktoryzacji?

### Odpowiedź: **[analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon) + [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon) razem**

| Wymiar refaktoryzacji | Plik źródłowy | Co daje |
|----------------------|---------------|---------|
| "Co rozbić na mniejsze?" | [analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon) HEALTH + FUNCTIONS | CC, god modules |
| "Jak rozbić?" | [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon) CONTRACTS + DATA_TYPES | Interface Segregation hints |
| "W jakiej kolejności?" | [analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon) HOTSPOTS | Fan-out ranking = impact |
| "Co jest czystym kodem?" | [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon) SIDE_EFFECTS + PURITY | Pure vs IO vs Mutation |
| "Gdzie szukać konkretnej funkcji?" | [map.toon](file:///home/tom/github/wronai/code2llm/output_all/map.toon) D: Details | Sygnatury + lokalizacja |

---

## Co poprawić w istniejących plikach?

### Priorytet 1: Naprawić pipeline detection w [flow.toon](file:///home/tom/github/wronai/code2llm/output_all/flow.toon)

Obecny `PipelineDetector` nie widzi głównych pipeline'ów, bo bazuje na call graph paths, ale **nie uwzględnia importów cross-package**. Powinien:
1. Budować graf z uwzględnieniem `from X import Y` relationships
2. Priorytetyzować pipeline'y wg domain classification (core > peripheral)
3. Filtrować [validate_toon.py](file:///home/tom/github/wronai/code2llm/validate_toon.py), `scripts/`, `benchmarks/` z wyników (to nie jest core)

### Priorytet 2: Naprawić identyczne Mermaid files (BUG)

`MermaidExporter.export()` prawdopodobnie generuje ten sam output dla [flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/flow.mmd), [compact_flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/compact_flow.mmd) i [calls.mmd](file:///home/tom/github/wronai/code2llm/output_all/calls.mmd). Trzeba:
1. [calls.mmd](file:///home/tom/github/wronai/code2llm/output_all/calls.mmd) — tylko krawędzie, bez izolowanych węzłów
2. [compact_flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/compact_flow.mmd) — agregacja per-moduł zamiast per-funkcja
3. [flow.mmd](file:///home/tom/github/wronai/code2llm/output_all/flow.mmd) — pełny graf z colour-coding wg CC

### Priorytet 3: Naprawić COUPLING w [analysis.toon](file:///home/tom/github/wronai/code2llm/output_all/analysis.toon)

Sekcja mówi "no cross-package imports" co jest fałszywie negatywne. `ToonExporter._compute_coupling_matrix()` prawdopodobnie patrzy na `result.functions` call targets, ale nie rozwiązuje ich do pakietów źródłowych.

### Priorytet 4: Skrócić [context.md](file:///home/tom/github/wronai/code2llm/output_all/context.md)

Zredukować z 611L do ~200L przez:
- Usunięcie redundantnego Architecture by Module (jest w [map.toon](file:///home/tom/github/wronai/code2llm/output_all/map.toon))
- Skrócenie Key Classes do top-10 (teraz jest 20+)
- Usunięcie pustych Process Flows

---

## Propozycja nowego pliku: `evolution.toon`

> [!IMPORTANT]
> **Brak pliku, który łączy informacje z wszystkich formatów w actionable refactoring queue.**

### Cel: Priorytetyzowana kolejka refaktoryzacji dla iteracyjnej ewolucji

```
# code2llm/evolution | 49f 12186L | v0.4.0 → v0.5.0 | 2026-03-01

NEXT[5] (ranked by impact × effort):
  [1] !! SPLIT  cli.py:main  CC=61  fan=44  →  cli.py + commands/analyze.py + commands/export.py
      WHY: Największy bottleneck — 61 ścieżek, 44 wywołania, blokuje testowanie CLI
      HOW: Extract export_dispatch(), analyze_command(), dotyczące 3 bloków if/elif
      EFFORT: ~2h  IMPACT: unblocks testing, reduces CC to ~15 per file

  [2] !! SPLIT  ToonExporter._render_details  CC=31  982L
      WHY: Największa klasa, 29 metod, CC̄=9.5 — god class
      HOW: Extract _render_health+_render_refactor do HealthRenderer
      EFFORT: ~4h  IMPACT: testability ++, reuse in other exporters

  [3] !! INTERFACE-SPLIT  AnalysisResult  consumed:65
      WHY: Hub-type — 65 konsumentów, każdy używa innego podzbioru pól
      HOW: StructureResult(modules, classes) + MetricsResult(cc, coupling) + FlowResult(call_graph)
      EFFORT: ~6h  IMPACT: decoupling, enables lazy computation

  [4] !  FIX-PIPELINE-DETECTION  PipelineDetector misses core pipelines
      WHY: flow.toon shows IO:4, Export:2 — missing Analysis, NLP, Core domains
      HOW: Add cross-module edge resolution in _build_graph()
      EFFORT: ~3h  IMPACT: flow.toon quality ↑ 40%

  [5]    IMPROVE-PURITY  SideEffectDetector false positives
      WHY: dict.get() classified as IO — inflates impurity
      HOW: Whitelist standard built-in methods
      EFFORT: ~1h  IMPACT: CONTRACTS accuracy ++

RISKS[3]:
  ⚠ cli.py main() has 2 import paths — ensure backward compat
  ⚠ AnalysisResult split changes public API — need migration guide
  ⚠ ToonExporter split may break subclass overrides

METRICS-TARGET (v0.5.0):
  CC̄:          4.9 → ≤3.5
  max-CC:      61 → ≤20
  god-modules: 3 → 0
  pipeline-detection-recall: ~30% → ≥80%
  hub-types:   10 → ≤5

HISTORY:
  v0.3.3→v0.4.0: removed 1740L dead code, renamed code2flow→code2llm
  v0.4.0→v0.5.0: [planned] split god modules, fix pipeline detection
```

### Dlaczego `evolution.toon`?

1. **Łączy dane z analysis.toon + flow.toon + map.toon** w jednym pliku
2. **Priorytetyzacja IMPACT × EFFORT** — nie tylko "co jest źle" ale "co naprawić najpierw"
3. **Actionable HOW** — konkretne kroki refaktoryzacji, nie tylko diagnozy
4. **METRICS-TARGET** — mierzalne cele wersji, porównanie z baseline
5. **HISTORY** — śledzenie ewolucji między wersjami (delta CC, delta LOC)
6. **RISKS** — identyfikacja breaking changes przed ich wprowadzeniem

### Implementacja

Nowy `EvolutionExporter` który:
1. Bierze wyniki z `ToonExporter`, `FlowExporter`, `MapExporter`
2. Cross-referencuje HEALTH issues z CONTRACTS i DATA_TYPES
3. Sortuje po `impact_score = CC × fan_out × consumer_count`
4. Generuje `evolution.toon` z sekcjami NEXT, RISKS, METRICS-TARGET, HISTORY
5. Opcjonalnie porównuje z poprzednim `evolution.toon` (diff mode)
