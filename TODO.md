# TODO - code2llm Project

## ✅ Completed — Rebranding (v0.3.8)

- [x] **Project Rebranding to code2llm**
  - [x] Package name: `code2flow-toon` → `code2llm`
  - [x] Documentation updates (README.md, API.md)
  - [x] CLI commands: `code2flow` → `code2llm`
  - [x] Makefile targets updated
  - [x] setup.py and pyproject.toml updated
  - [x] CHANGELOG.md and ROADMAP.md updated

## ✅ Completed — Sprint 1 (v0.3.0)

- [x] **Format Taxonomy Refactoring**
  - [x] Rename `project.toon` → `project.map` (new `MapExporter`)
  - [x] Rename `llm_prompt.md` → `context.md` (updated CLI output)
  - [x] New `FlowExporter` → `flow.toon` (data-flow: PIPELINES, TRANSFORMS, CONTRACTS, DATA_TYPES)
  - [x] Update CLI: `--format map,toon,flow,context,all`
  - [x] 4 files, 4 purposes: map (structure), toon (health), flow (data-flow), context (LLM)

## ✅ Completed — Sprint 2 (v0.3.1)

- [x] **Type inference from AST** (`analysis/type_inference.py`)
  - [x] Parse `->` return annotations
  - [x] Parse arguments with type hints
  - [x] Fallback: infer from names (`parse_*` → str input, `to_dict` → dict output)
  - [x] Batch mode: `extract_all_types()` for all project functions

- [x] **CONTRACTS section enhancement**
  - [x] Per-pipeline: IN types, OUT type for each stage
  - [x] Side-effect detection via AST: `self.`, `.write`, `open()`, `global`, `cache`
  - [x] Purity scoring: pure / IO / cache / mutation
  - [x] INVARIANT inference (normalize → `len(output) <= len(input)`)
  - [x] SMELL markers for CC ≥ 15

- [x] **DATA_TYPES section enhancement**
  - [x] Count consumed/produced per type (AST-based)
  - [x] Auto-detect hub-types (consumed ≥ 10)
  - [x] Hub-type split recommendations with named sub-interfaces
  - [x] Source counts: `[N annotated, M inferred / T functions]`

- [x] **SideEffectDetector** (`analysis/side_effects.py`)
  - [x] AST scan: `open()`, `write()`, `self.x = ...`, `global`, `del`
  - [x] Classification: IO / Cache / Mutation / Pure
  - [x] Heuristic fallback when source unavailable

- [x] **26 new tests** (`tests/test_sprint2_flow.py`)

## ✅ Completed — Sprint 3 (v0.3.2)

- [x] **Pipeline detection with networkx** (`analysis/pipeline_detector.py`)
  - [x] `networkx.DiGraph` call graph, `dag_longest_path` + DFS fallback
  - [x] Domain classification: NLP, Analysis, Export, Refactor, Core, IO
  - [x] Entry/exit point labeling (▶/■ markers)
  - [x] `Pipeline` and `PipelineStage` dataclasses

- [x] **SIDE_EFFECTS analysis** (done in Sprint 2, integrated in Sprint 3)
  - [x] AST scan: `open()`, `write()`, `self.cache`, `global`
  - [x] Classification: IO / Cache / Mutation / Pure
  - [x] Pipeline purity aggregation per pipeline

- [x] **Integration: flow.toon ← analysis.toon**
  - [x] CC metrics inline in pipeline stages
  - [x] Bottleneck identification per pipeline
  - [x] `!!` markers for CC ≥ 15
  - [x] Domain summary in PIPELINES header
  - [x] Entry→exit type flow per pipeline

- [x] **22 new tests** (`tests/test_sprint3_pipelines.py`)
  - [x] ≥3 pipelines with ≥3 stages each (success metric ✅)

## ✅ Completed — Sprint 4 (v0.3.3)

- [x] **Format Quality Benchmark** (`benchmarks/benchmark_format_quality.py`)
  - [x] Ground-truth project with 8 known problems, 2 pipelines, 2 hub types
  - [x] Scoring: problem_score, pipeline_score, hub_type_score, structural_score
  - [x] Gap analysis per format — identifies what each format misses
  - [x] Results: flow.toon 79%, analysis.toon 66%, context.md 59%, project.map 21%

- [x] **24 format quality tests** (`tests/test_format_quality.py`)
  - [x] TestAnalysisToon, TestFlowToon, TestProjectMap, TestContextMd, TestCrossFormat

- [x] **Rename llm_exporter → context_exporter**
  - [x] `ContextExporter` in `context_exporter.py` (canonical)
  - [x] Backward-compat shim in `llm_exporter.py`
  - [x] CLI updated to use `ContextExporter`

## ✅ Completed — Bug Fixes + Evolution (v0.5.0)

- [x] **Fix MermaidExporter BUG**: 3 identical files → 3 distinct outputs
  - [x] `flow.mmd` — full graph with CC-based styling
  - [x] `calls.mmd` — edges only, no isolated nodes
  - [x] `compact_flow.mmd` — module-level aggregation with weighted edges

- [x] **Fix SideEffectDetector**: `dict.get()` false positive as IO
  - [x] HTTP verbs extracted to `HTTP_METHODS` + `HTTP_CALLERS` context
  - [x] Only `requests.get()`, `session.post()` etc. trigger IO classification

- [x] **Fix Coupling Matrix**: improved callee disambiguation
  - [x] Candidates-based approach preferring same-package callees

- [x] **Fix Pipeline Detection**: safe ambiguous handling
  - [x] `_resolve_callee()` returns None for ambiguous matches

- [x] **New EvolutionExporter** → `evolution.toon`
  - [x] Ranked refactoring queue (CC × fan_out impact scoring)
  - [x] NEXT[N], RISKS[N], METRICS-TARGET, HISTORY sections
  - [x] CLI: `--format evolution` or included in `--format all`
  - [x] Venv/site-packages exclusion

## ✅ Completed — Structural Refactoring (v0.5.1)

- [x] **Split 9 god-functions** guided by `evolution.toon` NEXT list:
  - [x] `cli.main()` CC=63 → 7 functions
  - [x] `ToonExporter._render_details` CC=31 → 5 methods
  - [x] `ToonExporter._compute_file_metrics` CC=21 → 4 methods
  - [x] `ToonExporter._compute_health` CC=28 → 4 methods
  - [x] `EvolutionExporter._build_context` CC=31 → 3 methods
  - [x] `MermaidExporter.export` CC=22 → 4 methods
  - [x] `MapExporter._render_details` CC=24 → 3 methods
  - [x] `validate_mermaid_file` CC=42 → 3 functions
  - [x] `fix_mermaid_file` CC=25 → 3 functions
- [x] **Metrics**: CC̄ 5.1→4.8, max-CC 63→35 (↓44%), high-CC 27→21 (↓22%)
- [x] **Auto-benchmark** script (`benchmarks/benchmark_evolution.py`)
- [x] **Example projects** (Claude Code, shell LLM, LiteLLM)

## ✅ Completed — Sprint 5 (v0.6.0)

- [x] **Structural splits** (Phase 1-3)
  - [x] `exporters/toon.py` → `exporters/toon/` package (renderer, metrics, helpers, module_detail)
  - [x] `core/analyzer.py` → `core/core/` subpackage (file_analyzer, file_filter, refactoring, cache)
  - [x] `core/streaming_analyzer.py` → `core/streaming/` subpackage (scanner, prioritizer, incremental)

- [x] **Split high-CC functions** (Phase 4)
  - [x] `render_coupling` CC=28 → 6 sub-methods
  - [x] `render_layers` CC=21 → 4 sub-methods
  - [x] `render_functions` CC=18 → 2 sub-methods
  - [x] `parse_toon_content` CC=35 → dispatch dict + 4 parsers
  - [x] `_annotation_to_str` CC=18 → dispatch dict + 6 handlers

- [x] **Bug fixes** (Phase 5)
  - [x] `PipelineDetector._resolve_callee` — method→method edges (self.X resolution)
  - [x] `MermaidExporter._module_of` — subpackage-level grouping in compact_flow.mmd
  - [x] Cleanup: removed `analyzer_old.py`, `streaming_analyzer_old.py`, `TODO/`

- [x] **Test fixes** — 8 broken tests fixed, 159/159 passing
  - [x] `test_advanced_analysis.py` — updated imports for RefactoringAnalyzer, fixed complexity key
  - [x] `test_edge_cases.py` — fixed should_skip_function signature, nested classes assertion
  - [x] `test_prompt_engine.py` — updated assertions to match Jinja2 template output
  - [x] `test_refactoring_engine.py` — fixed god_function detection threshold

- [x] **Self-analysis benchmark**
  - [x] CC̄=4.7 (was 5.1), max-CC=19 (was 35), 0 god modules
  - [x] 12 pipelines detected (Analysis:8, Export:4)
  - [x] compact_flow.mmd: 5 subpackage nodes with weighted edges

## 🎯 Sprint 6 — Remaining improvements (v0.7.0)

### High Priority

- [ ] **Fix 9 remaining CC>15 functions** (CC̄ 4.7 → target ≤3.5)
  - [ ] `parse_llm_task_text` CC=19
  - [ ] `_resolve_callee` CC=18
  - [ ] `_infer_from_name` CC=17
  - [ ] `_find_data_pipelines` CC=17
  - [ ] `_compute_god_modules` CC=16
  - [ ] `_run_exports` CC=15
  - [ ] `_analyze_data_types` CC=15
  - [ ] `_trace_flow` CC=15
  - [ ] `_collect_entrypoints` CC=15

- [ ] **Streaming analysis** — accumulate results properly (remove double-analysis TODO in cli.py:305)

### Medium Priority

- [ ] **Semantic Code Search** (Phase 1.1)
  - Integrate sentence transformers for semantic embeddings
  - Build vector index for similarity search

- [ ] **Advanced Pattern Detection** (Phase 1.2)
  - Factory, Singleton, Observer, Strategy patterns

- [ ] **Interactive Web UI** (Phase 1.3)
  - Streamlit-based web interface
  - Interactive graph visualization (D3.js/Plotly)

### Low Priority

- [ ] **VS Code Extension** (Phase 2.1)
- [ ] **Real-time Analysis** (Phase 2.2)
- [ ] **Git Integration** (Phase 2.3)
- [ ] **JavaScript/TypeScript Support** (Phase 3.1)
- [ ] **Security Analysis** (Phase 4.1)

## 📝 Notes

- Each format has one purpose: map=structure, toon=health, flow=data-flow, context=LLM, evolution=refactoring

Last updated: 2026-03-01