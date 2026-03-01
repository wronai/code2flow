# TODO

## ✅ Completed — Sprint 1 (v0.3.0)

- [x] **Format Taxonomy Refactoring**
  - [x] Rename `project.toon` → `project.map` (new `MapExporter`)
  - [x] Rename `llm_prompt.md` → `context.md` (updated CLI output)
  - [x] New `FlowExporter` → `flow.toon` (data-flow: PIPELINES, TRANSFORMS, CONTRACTS, DATA_TYPES)
  - [x] Update CLI: `--format map,toon,flow,context,all`
  - [x] 4 files, 4 purposes: map (structure), toon (health), flow (data-flow), context (LLM)

## 🎯 Sprint 2 — CONTRACTS + DATA_TYPES (v0.3.1)

### High Priority

- [ ] **Type inference from AST**
  - Parse `->` return annotations
  - Parse arguments with type hints
  - Fallback: infer from names (`parse_*` → str input, `to_dict` → dict output)

- [ ] **CONTRACTS section enhancement**
  - Per-pipeline: input→output for each stage
  - Side-effect detection: `self.`, `.write`, `.save`, `cache`
  - Purity scoring: pure / IO / cache / mutation

- [ ] **DATA_TYPES section enhancement**
  - Count consumed/produced per type
  - Auto-detect hub-types (consumed ≥ 10)
  - Recommend split for hub-types

## 🎯 Sprint 3 — PIPELINES auto-detection + SIDE_EFFECTS (v0.3.2)

### High Priority

- [ ] **Pipeline detection with networkx**
  - Find longest paths in call graph
  - Group by module (NLP, Analysis, Export, Refactor)
  - Label entry/exit points

- [ ] **SIDE_EFFECTS analysis**
  - AST scan: `open()`, `write()`, `self.cache`, `global`
  - Classification: IO / Cache / Mutation / Pure
  - Pipeline purity aggregation

- [ ] **Integration: flow.toon ← analysis.toon**
  - CC metrics inline in pipeline stages
  - Bottleneck identification per pipeline
  - `!!` markers for CC ≥ 15

## 🎯 Sprint 4 — Self-test + benchmark v2 (v0.3.3)

### High Priority

- [ ] **Self-analysis**
  - Run code2flow on itself with new flow.toon
  - Verify: detect NLP, Analysis, Export, Refactor pipelines
  - Verify: AnalysisResult marked as hub-type

- [ ] **Benchmark v2**
  - Run benchmark with 4 formats (map, toon, flow, context)
  - Target: flow.toon ≥ 8.0/10 in Data Flow (currently: 5.5)
  - Target: combined score ≥ 8.5/10

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

- Format taxonomy based on TODO/action_plan_v3.md benchmark results
- Each format has one purpose: map=structure, toon=health, flow=data-flow, context=LLM
- This TODO list is managed by Goal — use `goal -t` for auto-detection

Last updated: 2026-03-01