# code2flow — Zaktualizowany Plan Działania v3

## Stan faktyczny po benchmarku

### Problem z nazewnictwem

Benchmark ujawnił fundamentalny problem: **dwa zupełnie różne formaty noszą tę samą nazwę `.toon`**.

```
project.toon   = klucz:wartość (M:, D:, i:, e:)  → to jest MAPA STRUKTURY
analysis.toon  = sekcje diagnostyczne (HEALTH, COUPLING, LAYERS)  → to jest RAPORT ZDROWIA
```

Strukturalnie nie mają ze sobą nic wspólnego. To tak jakby CSV i JSON nazywać `.data`.

### Benchmark: żaden format nie wystarcza do refaktoryzacji data-flow

Wyniki (skala 0-10, ważona):

| Format | Data Flow | Refactoring | Density | LLM | **TOTAL** |
|--------|-----------|-------------|---------|-----|-----------|
| analysis.toon | 5.6 | **9.0** | **8.0** | **7.5** | **🥇 7.0** |
| llm_prompt.md | 5.5 | 3.0 | 3.5 | 7.0 | 🥈 5.0 |
| project.toon | 5.5 | 2.3 | 7.0 | 4.5 | 🥉 4.8 |

**Kluczowe odkrycie**: w kategorii "Data Flow" WSZYSTKIE formaty mają ~5.5/10. Żaden nie jest zaprojektowany do opisania JAK DANE PŁYNĄ przez system. Każdy format ma unikalne mocne strony, których brakuje pozostałym:

- **project.toon** ma typy (`func(arg:type)->return`) — jedyny format z kontraktami
- **analysis.toon** ma call chains (`→`) i metryki — jedyny z diagnostyką
- **llm_prompt.md** ma opisy i wzorce — jedyny z semantyką

---

## Nowa taksonomia formatów

### Nazewnictwo: 4 pliki, 4 cele

```
output/
├── project.map         # MAPA STRUKTURY — moduły, importy, sygnatury, typy
│                       # (dawniej: project.toon)
│                       # Cel: "co istnieje i jak jest połączone"
│                       # Format: klucz:wartość (M:, D:, i:, e:)
│
├── analysis.toon       # DIAGNOSTYKA ZDROWIA — CC, coupling, HEALTH, REFACTOR
│                       # (dawniej: analysis.toon — nazwa zostaje)
│                       # Cel: "co jest nie tak i jak to naprawić"
│                       # Format: sekcje diagnostyczne z markerami severity
│
├── flow.toon           # ⭐ NOWY — PRZEPŁYW DANYCH — pipelines, transforms, kontrakty
│                       # Cel: "jak dane płyną przez system"
│                       # Format: PIPELINES, TRANSFORMS, CONTRACTS, DATA_TYPES
│
└── context.md          # KONTEKST LLM — architektura narracyjna, wzorce, API
                        # (dawniej: llm_prompt.md)
                        # Cel: "zrozum system żeby go przebudować"
                        # Format: markdown z mermaid
```

### Opisy formatów

| Format | Rozszerzenie | Cel | Odbiorca | Analogia |
|--------|-------------|-----|----------|----------|
| **Map** | `.map` | Struktura statyczna | Nawigacja, grep | Mapa miasta |
| **Toon** | `.toon` | Diagnostyka + refactoring | Decydent, CI/CD | Raport lekarski |
| **Flow** | `.toon` (flow sekcja) | Przepływ danych | LLM refactoring | Schemat hydrauliczny |
| **Context** | `.md` | Zrozumienie systemu | LLM, nowy developer | Przewodnik turystyczny |

### Kiedy używać którego formatu

```
"Co jest w projekcie?"           → project.map
"Co jest zepsute?"               → analysis.toon (HEALTH)
"Jak naprawić?"                  → analysis.toon (REFACTOR)
"Jak dane płyną przez system?"   → flow.toon (PIPELINES)
"Gdzie podzielić typ?"           → flow.toon (DATA_TYPES consumed/produced)
"Czy pipeline jest pure?"        → flow.toon (CONTRACTS)
"Jak przebudować w innym języku?"→ context.md
"Ile zależy od tego modułu?"     → analysis.toon (COUPLING)
"Jaki typ zwraca funkcja?"       → project.map (sygnatury)
```

---

## Specyfikacja flow.toon — nowy format data-flow

### Filozofia

Refaktoryzacja powinna wynikać z **przepływu danych** a nie z **struktury kodu**:

| Podejście code-first | Podejście data-flow-first |
|----------------------|--------------------------|
| "base.py ma 1240 linii → split" | "AnalysisResult consumed:18 → typ jest hub-em, split" |
| "CC=45 → za złożone" | "export() łączy 5 pipelines → extract pipeline runner" |
| "duplikat klasy → usuń" | "dwa moduły produkują ten sam typ → merge producers" |
| "god module → split by class" | "3 transformacje w jednym pipeline → extract stages" |

### Struktura flow.toon

```
# code2flow/flow | 335 func | 12 pipelines | 4 hub-types | 2026-03-01

PIPELINES[4]:
  NLP:        query:str
              → normalize(str→str)                    CC=6   pure
              → match_intent(str→IntentMatch)          CC=7   pure
              → resolve(IntentMatch→Entity[])          CC=13  cache
              → format_action(Entity[]→str)            CC=10  10-branch
              PURITY: 2/4 pure  BOTTLENECK: resolve(CC=13)

  Analysis:   path:Path
              → collect_files(Path→Path[])             CC=4   pure
              → analyze_file(Path→AnalysisResult)      CC=15  IO+cache
              → merge_results(AR[]→AR)                 CC=8   pure
              → build_call_graph(AR→AR)                CC=9   mutation
              PURITY: 2/4 pure  BOTTLENECK: analyze_file(CC=15)

  Export:     result:AnalysisResult
              → compute_metrics(AR→Context)            CC=21  !! 
              → render_sections(Context→str[])          CC=31  !! 
              → write(str[]→file)                       CC=1   IO
              PURITY: 0/3 pure  BOTTLENECK: render_sections(CC=31)

  Refactor:   result:AnalysisResult
              → detect_smells(AR→CodeSmell[])          CC=7   pure
              → build_context(AR+CS[]→dict)            CC=12  pure
              → render_prompt(dict→str)                CC=8   template
              PURITY: 2/3 pure  OK

TRANSFORMS (fan-out ≥10):
  main(args:list) → {Config,Path,AR}              fan=45  !! script-in-disguise
  _compute_file_metrics(AR) → Dict[str,Metrics]   fan=22  !! side-effects
  analyze_project(Path) → AR                       fan=18  PIPELINE:Analysis.entry
  process(str) → NLPPipelineResult                 fan=18  PIPELINE:NLP.entry
  fix_mermaid_file(Path) → None                    fan=29  !! mutation-heavy
  export(AR,Path) → None                           fan=18  PIPELINE:Export.entry

CONTRACTS:
  Pipeline: NLP
    normalize(query:str, lang:str='en') → str
      IN:  raw user query (unicode, mixed case, with stopwords)
      OUT: cleaned lowercase string without stopwords
      INVARIANT: len(output) <= len(input)

    match_intent(normalized:str, config:NLPConfig) → IntentMatch
      IN:  normalized query string
      OUT: matched intent with confidence score
      INVARIANT: confidence ∈ [0.0, 1.0]

    resolve(match:IntentMatch, analysis:AR) → Entity[]
      IN:  intent match + full analysis context
      OUT: resolved entities (functions, classes, modules)
      SIDE-EFFECT: cache lookup/store
      INVARIANT: all entities exist in analysis

    format_action(entities:Entity[], intent:str) → str
      IN:  resolved entities + intent type
      OUT: formatted response string
      DISPATCH: 10 branches by intent type

  Pipeline: Export
    compute_metrics(result:AR) → Context
      IN:  full analysis result
      OUT: computed metrics dict (CC, coupling, health, hotspots)
      SMELL: CC=21, does 6 different computations → split

    render_sections(ctx:Context) → str[]
      IN:  computed context
      OUT: list of formatted text sections
      SMELL: CC=31, renders 8 section types → extract per-section renderers

DATA_TYPES (by cross-function usage):
  AnalysisResult   consumed:18  produced:4   !! HUB-TYPE → split interface
  str              consumed:45  produced:30  ubiquitous (input/output carrier)
  Path             consumed:12  produced:3   input-heavy (read-only flow)
  FunctionInfo     consumed:8   produced:2   read-mostly (analysis output)
  dict             consumed:15  produced:12  generic → replace with typed
  CodeSmell        consumed:3   produced:2   narrow scope (refactor pipeline only)
  IntentMatch      consumed:2   produced:1   narrow scope (NLP pipeline only)
  Entity           consumed:2   produced:1   narrow scope (NLP pipeline only)
  Context          consumed:3   produced:1   internal to Export pipeline

  HUB TYPES (consumed ≥10):
    AnalysisResult → 18 consumers → split into:
      StructureResult (modules, classes, functions)
      MetricsResult (complexity, coupling)
      FlowResult (call_graph, cfg, dfg)
    dict → 15 consumers → replace with typed alternatives
    str → 45 consumers → OK (primitive, expected)

SIDE_EFFECTS:
  IO:      analyze_file (reads files), write (writes output), load_input
  Cache:   resolve (entity cache), FileCache.get/set
  Mutation: build_call_graph (mutates AR), fix_mermaid_file (modifies files)
  Pure:    normalize, match_intent, detect_smells, format_action
  
  PIPELINE PURITY:
    NLP:        ██░░ 50% pure (resolve has cache)
    Analysis:   ██░░ 50% pure (analyze_file has IO)
    Export:     ░░░░  0% pure (all stages compute+write)
    Refactor:   ███░ 67% pure (render uses template)
```

### Co umożliwia flow.toon (czego nie dają pozostałe formaty)

| Insight | Jak flow.toon to pokazuje | Akcja refaktoryzacyjna |
|---------|--------------------------|----------------------|
| AnalysisResult to hub-type | `consumed:18 produced:4 !! HUB-TYPE` | Split na 3 interfejsy |
| Pipeline Export jest 0% pure | `PURITY: 0/3 pure` | Extract pure compute stage |
| resolve() ma side-effect | `SIDE-EFFECT: cache lookup/store` | Inject cache as parameter |
| render_sections robi 8 rzeczy | `SMELL: CC=31, renders 8 section types` | Extract per-section renderers |
| main() to skrypt w przebraniu | `fan=45 !! script-in-disguise` | Extract pipeline runner |
| dict used 15× generycznie | `consumed:15 → replace with typed` | Introduce typed dataclasses |

---

## Zaktualizowany roadmap implementacji

### Sprint 1 (tydzień 1): Rename + flow.toon prototype

**Cel**: uporządkować nazwy + dostarczyć minimalny flow.toon

Zadania:
1. **Rename project.toon → project.map**
   - Zmiana w `ToonExporter` (dotychczasowy format project.toon → osobny MapExporter)
   - Update CLI: `--format map,toon,flow,context,all`
   - Update docs
   
2. **Rename llm_prompt.md → context.md**
   - Zmiana w `LLMPromptExporter`
   - Update CLI
   
3. **Nowy FlowExporter (flow.toon)**
   - PIPELINES: wykrywanie łańcuchów call graph jako pipeline'ów
   - TRANSFORMS: top-N funkcji po fan-out z sygnaturami typów
   - Minimalny: ~150 linii kodu, bazujący na istniejących danych z AnalysisResult

Metryki sukcesu:
- `code2flow ./project -f all` generuje 4 pliki z poprawnymi rozszerzeniami
- flow.toon zawiera ≥2 wykrytych pipeline'ów
- Testy: 5 testów walidacji flow.toon

### Sprint 2 (tydzień 2): CONTRACTS + DATA_TYPES

**Cel**: flow.toon pokazuje kontrakty danych i hub-typy

Zadania:
1. **Type inference z AST**
   - Parsowanie `->` return annotations
   - Parsowanie argumentów z typami
   - Fallback: inferowanie z nazw (`parse_*` → str input, `to_dict` → dict output)
   
2. **Sekcja CONTRACTS**
   - Per-pipeline: input→output dla każdego stage'a
   - Side-effect detection: szukanie `self.`, `.write`, `.save`, `cache`
   - Purity scoring: pure / IO / cache / mutation
   
3. **Sekcja DATA_TYPES**
   - Zliczanie consumed/produced per typ
   - Automatyczne wykrywanie hub-typów (consumed ≥ 10)
   - Rekomendacja split dla hub-typów

Metryki sukcesu:
- flow.toon zawiera CONTRACTS z ≥4 typami per pipeline
- DATA_TYPES identyfikuje ≥1 hub-typ
- Purity scoring działa dla ≥80% funkcji

### Sprint 3 (tydzień 3): PIPELINES auto-detection + SIDE_EFFECTS

**Cel**: automatyczne wykrywanie pipeline'ów z call graph

Zadania:
1. **Pipeline detection z networkx**
   - Znajdowanie najdłuższych ścieżek w call graph (longest path)
   - Grupowanie po module (NLP, Analysis, Export, Refactor)
   - Labeling entry/exit points pipeline'u
   
2. **SIDE_EFFECTS analysis**
   - AST scan: szukanie `open()`, `write()`, `self.cache`, `global`
   - Klasyfikacja: IO / Cache / Mutation / Pure
   - Pipeline purity aggregation
   
3. **Integration: flow.toon ← analysis.toon**
   - CC metrics inline w pipeline stages
   - Bottleneck identification per pipeline
   - !! markers dla CC ≥ 15 w pipeline context

Metryki sukcesu:
- Auto-detected ≥3 pipelines z ≥3 stages każdy
- Side-effect detection accuracy ≥70% (manual verification)
- Pipeline purity scoring matches manual analysis

### Sprint 4 (tydzień 4): Self-test + benchmark v2

**Cel**: code2flow generuje flow.toon dla siebie i benchmark potwierdza poprawę

Zadania:
1. **Self-analysis**
   - Uruchomienie code2flow na sobie z nowym flow.toon
   - Weryfikacja: czy flow.toon wykrywa pipeline NLP, Analysis, Export, Refactor?
   - Weryfikacja: czy AnalysisResult jest oznaczony jako hub-type?
   
2. **Benchmark v2**
   - Ponowne uruchomienie benchmarku z 4 formatami (map, toon, flow, context)
   - Target: flow.toon ≥ 8.0/10 w kategorii Data Flow (teraz: 5.5)
   - Target: łączny score systemu (4 pliki) ≥ 8.5/10
   
3. **Dokumentacja**
   - Format specification dla flow.toon
   - Przykłady data-flow refactoring decisions
   - Comparisons: code-first vs data-flow-first refactoring

Metryki sukcesu:
- flow.toon Data Flow score ≥ 8.0/10
- Self-analysis wykrywa ≥4 pipeline'ów
- AnalysisResult identified as hub-type consumed ≥15
- 4-format system total score ≥ 8.5/10

---

## Podsumowanie zmian vs. poprzedni plan

| Aspekt | Plan v2 (poprzedni) | Plan v3 (aktualny) |
|--------|---------------------|---------------------|
| **Filozofia** | Ulepszenie .toon v2 | 4 oddzielne formaty, każdy z jednym celem |
| **Nazewnictwo** | project.toon + analysis.toon | project.map + analysis.toon + flow.toon + context.md |
| **Fokus** | Code structure (CC, GOD, DUP) | **Data flow** (pipelines, contracts, hub-types) |
| **Refactoring driver** | "CC=45 → split" | "AnalysisResult consumed:18 → split interface" |
| **Nowy format** | Brak (ulepszenie existing) | flow.toon — dedykowany data-flow format |
| **Pipeline detection** | Brak | Auto-detect z networkx longest path |
| **Type awareness** | Brak (typy tylko w project.toon) | CONTRACTS per pipeline + DATA_TYPES ranking |
| **Purity analysis** | Brak | SIDE_EFFECTS + pipeline purity scoring |
| **Sprinty** | 4 sprinty code-cleanup | 4 sprinty data-flow tooling |

Główna zmiana: **z "napraw kod" na "zrozum przepływ danych"**. Kod jest konsekwencją przepływu — jeśli poprawisz przepływ (split hub-typów, wydziel pipeline stages, oznacz side-effects), kod sam się uprości.
