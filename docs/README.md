<!-- code2docs:start --># code2llm

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.8-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-1176-green)
> **1176** functions | **137** classes | **168** files | CC̄ = 3.9

> Auto-generated project documentation from source code analysis.

**Author:** Tom Sapletta  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/wronai/code2flow](https://github.com/wronai/code2flow)

## Installation

### From PyPI

```bash
pip install code2llm
```

### From Source

```bash
git clone https://github.com/wronai/code2flow
cd code2llm
pip install -e .
```

### Optional Extras

```bash
pip install code2llm[dev]    # development tools
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
code2llm ./my-project

# Only regenerate README
code2llm ./my-project --readme-only

# Preview what would be generated (no file writes)
code2llm ./my-project --dry-run

# Check documentation health
code2llm check ./my-project

# Sync — regenerate only changed modules
code2llm sync ./my-project
```

### Python API

```python
from code2llm import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```

## Generated Output

When you run `code2llm`, the following files are produced:

```
<project>/
├── README.md                 # Main project README (auto-generated sections)
├── docs/
│   ├── api.md               # Consolidated API reference
│   ├── modules.md           # Module documentation with metrics
│   ├── architecture.md      # Architecture overview with diagrams
│   ├── dependency-graph.md  # Module dependency graphs
│   ├── coverage.md          # Docstring coverage report
│   ├── getting-started.md   # Getting started guide
│   ├── configuration.md    # Configuration reference
│   └── api-changelog.md    # API change tracking
├── examples/
│   ├── quickstart.py       # Basic usage examples
│   └── advanced_usage.py   # Advanced usage examples
├── CONTRIBUTING.md         # Contribution guidelines
└── mkdocs.yml             # MkDocs site configuration
```

## Configuration

Create `code2llm.yaml` in your project root (or run `code2llm init`):

```yaml
project:
  name: my-project
  source: ./
  output: ./docs/

readme:
  sections:
    - overview
    - install
    - quickstart
    - api
    - structure
  badges:
    - version
    - python
    - coverage
  sync_markers: true

docs:
  api_reference: true
  module_docs: true
  architecture: true
  changelog: true

examples:
  auto_generate: true
  from_entry_points: true

sync:
  strategy: markers    # markers | full | git-diff
  watch: false
  ignore:
    - "tests/"
    - "__pycache__"
```

## Sync Markers

code2llm can update only specific sections of an existing README using HTML comment markers:

```markdown
<!-- code2llm:start -->
# Project Title
... auto-generated content ...
<!-- code2llm:end -->
```

Content outside the markers is preserved when regenerating. Enable this with `sync_markers: true` in your configuration.

## Architecture

```
code2llm/
├── orchestrator├── project2├── project        ├── sample        ├── sample_bad├── setup        ├── run            ├── utils    ├── project_generator    ├── benchmark_constants    ├── benchmark_optimizations    ├── reporting    ├── benchmark_evolution    ├── bump_version    ├── valid/    ├── invalid/├── validate_toon    ├── benchmark_badges    ├── cli    ├── server├── code2llm/    ├── api    ├── __main__    ├── cli_parser            ├── database    ├── analysis/        ├── pipeline_resolver            ├── main    ├── cli_analysis        ├── type_inference        ├── pipeline_classifier        ├── sample_project/        ├── sample        ├── coupling        ├── data_analysis            ├── ast_helpers        ├── utils/        ├── smells            ├── auth    ├── cli_commands        ├── ast_registry        ├── file_cache        ├── incremental        ├── side_effects    ├── core/        ├── demo        ├── gitignore            ├── api        ├── repo_files        ├── toon_size_manager        ├── streaming_analyzer        ├── analyzer        ├── export_pipeline        ├── persistent_cache        ├── file_filter        ├── streaming/        ├── refactoring            ├── incremental            ├── cache            ├── rust            ├── scanner        ├── file_analyzer            ├── strategies            ├── cpp            ├── ruby            ├── ts_extractors            ├── ts_parser        ├── lang/            ├── csharp            ├── php            ├── go_lang            ├── java            ├── typescript    ├── nlp/            ├── base            ├── generic        ├── call_graph    ├── format_evaluator        ├── dfg        ├── cfg        ├── base        ├── project_yaml_exporter    ├── benchmark_performance        ├── map_exporter        ├── pipeline_detector        ├── toon/    ├── exporters/        ├── json_exporter        ├── dashboard_renderer        ├── report_generators        ├── mermaid_exporter        ├── readme_exporter        ├── article_view        ├── context_view        ├── large_repo        ├── llm_exporter        ├── dashboard_data        ├── flow_constants        ├── html_dashboard        ├── validate_project            ├── prioritizer        ├── yaml_exporter        ├── index_generator/        ├── flow_renderer        ├── models        ├── toon_view        ├── flow_exporter            ├── metrics_duplicates            ├── helpers    ├── benchmark_format_quality            ├── metrics        ├── context_exporter        ├── project_yaml/            ├── metrics_health            ├── evolution            ├── module_detail            ├── constants            ├── hotspots            ├── renderer            ├── modules            ├── core        ├── _utils            ├── health    ├── generators/            ├── scanner        ├── evolution_exporter    ├── cli_exports/        ├── code2logic        ├── formats            ├── metrics_core    ├── refactor/            ├── renderer        ├── mermaid_flow_helpers    ├── patterns/        ├── llm_task        ├── toon_parser        ├── sample        ├── orchestrator        ├── detector        ├── mermaid        ├── prompt_engine        ├── llm_flow        ├── prompt    ├── functional_refactoring_example        ├── normalization        ├── intent_matching        ├── config        ├── pipeline        ├── entity_resolution        ├── config```

## API Overview

### Classes

- **`User`** — —
- **`UserService`** — —
- **`User`** — —
- **`UserService`** — —
- **`Product`** — —
- **`ProductRepository`** — —
- **`DatabaseConnection`** — Simple database connection simulator.
- **`PipelineResolver`** — Resolves callee names to qualified function names.
- **`UserRequest`** — User request data structure.
- **`Application`** — Main application class with multiple responsibilities.
- **`TypeInferenceEngine`** — Extract and infer type information from Python source files.
- **`PipelineClassifier`** — Classify pipelines by domain and derive human-readable names.
- **`User`** — —
- **`UserService`** — —
- **`CouplingAnalyzer`** — Analyze coupling between modules.
- **`DataAnalyzer`** — Analyze data flows, structures, and optimization opportunities.
- **`DataFlowAnalyzer`** — Analyze data flows: pipelines, state patterns, dependencies, and event flows.
- **`OptimizationAdvisor`** — Analyze optimization opportunities: data types and process patterns.
- **`SmellDetector`** — Detect code smells from analysis results.
- **`AuthManager`** — Manages user authentication and authorization.
- **`ASTRegistry`** — Parse each file exactly once; share the AST across all analysis consumers.
- **`FileCache`** — Cache for parsed AST files.
- **`IncrementalAnalyzer`** — Track file signatures to skip unchanged files on subsequent runs.
- **`SideEffectInfo`** — Side-effect analysis result for a single function.
- **`SideEffectDetector`** — Detect side effects in Python functions via AST analysis.
- **`GitIgnoreParser`** — Parse and apply .gitignore patterns to file paths.
- **`APIHandler`** — Handles API requests and responses.
- **`StreamingAnalyzer`** — Memory-efficient streaming analyzer with progress tracking.
- **`ProjectAnalyzer`** — Main analyzer with parallel processing.
- **`SharedExportContext`** — Pre-computed context shared across all exporters.
- **`ExportPipeline`** — Run multiple exporters with a single shared context.
- **`PersistentCache`** — Content-addressed persistent cache stored in ~/.code2llm/.
- **`FastFileFilter`** — Fast file filtering with pattern matching.
- **`RefactoringAnalyzer`** — Performs refactoring analysis on code.
- **`IncrementalAnalyzer`** — Incremental analysis with change detection.
- **`StreamingFileCache`** — Memory-efficient cache with LRU eviction.
- **`StreamingScanner`** — Handles file scanning operations.
- **`FileAnalyzer`** — Analyzes a single file.
- **`ScanStrategy`** — Scanning methodology configuration.
- **`RubyParser`** — Ruby language parser - registered via @register_language in __init__.py.
- **`TreeSitterParser`** — Unified tree-sitter parser for all supported languages.
- **`LanguageParser`** — Abstract base class for language-specific parsers.
- **`CallGraphExtractor`** — Extract call graph from AST.
- **`FormatScore`** — Wynik oceny pojedynczego formatu.
- **`DFGExtractor`** — Extract Data Flow Graph from AST.
- **`CFGExtractor`** — Extract Control Flow Graph from AST.
- **`BaseExporter`** — Abstract base class for all code2llm exporters.
- **`ViewGeneratorMixin`** — Mixin providing the shared ``generate`` implementation for view generators.
- **`MapExporter`** — Export to map.toon.yaml — structural map with a compact project header.
- **`PipelineStage`** — A single stage in a detected pipeline.
- **`Pipeline`** — A detected pipeline with stages, purity info, and domain.
- **`PipelineDetector`** — Detect pipelines in a codebase using networkx graph analysis.
- **`JSONExporter`** — Export to JSON format.
- **`DashboardRenderer`** — Render HTML dashboard from prepared data structures.
- **`MermaidExporter`** — Export call graph to Mermaid format.
- **`READMEExporter`** — Export README.md with documentation of all generated files.
- **`ArticleViewGenerator`** — Generate status.md — publishable project health article.
- **`ContextViewGenerator`** — Generate context.md from project.yaml data.
- **`SubProject`** — Represents a sub-project within a larger repository.
- **`HierarchicalRepoSplitter`** — Splits large repositories using hierarchical approach.
- **`DashboardDataBuilder`** — Build dashboard data structures from project analysis results.
- **`HTMLDashboardGenerator`** — Generate dashboard.html from project.yaml data.
- **`FilePriority`** — Priority scoring for file analysis order.
- **`SmartPrioritizer`** — Smart file prioritization for optimal analysis order.
- **`YAMLExporter`** — Export to YAML format.
- **`FlowRenderer`** — Renderer dla sekcji formatu flow.toon.
- **`BaseModel`** — Base class for models with automated serialization.
- **`FlowNode`** — Represents a node in the control flow graph.
- **`FlowEdge`** — Represents an edge in the control flow graph.
- **`FunctionInfo`** — Information about a function/method.
- **`ClassInfo`** — Information about a class.
- **`ModuleInfo`** — Information about a module/package.
- **`Pattern`** — Detected behavioral pattern.
- **`CodeSmell`** — Represents a detected code smell.
- **`Mutation`** — Represents a mutation of a variable/object.
- **`DataFlow`** — Represents data flow for a variable.
- **`AnalysisResult`** — Complete analysis result for a project.
- **`ToonViewGenerator`** — Generate project.toon.yaml from project.yaml data.
- **`FlowExporter`** — Export to flow.toon — data-flow focused format.
- **`DuplicatesMetricsComputer`** — Detects duplicate classes in the codebase.
- **`MetricsComputer`** — Computes all metrics for TOON export.
- **`ContextExporter`** — Export LLM-ready analysis summary with architecture and flows.
- **`ToonExporter`** — Export to toon v2 plain-text format — scannable, sorted by severity.
- **`HealthMetricsComputer`** — Computes health issues and quality alerts.
- **`ModuleDetailRenderer`** — Renders detailed module information.
- **`IndexHTMLGenerator`** — Generate index.html for browsing all generated files.
- **`HTMLRenderer`** — Render the index.html page with CSS and JavaScript.
- **`ProjectYAMLExporter`** — Export unified project.yaml — single source of truth for diagnostics.
- **`FileScanner`** — Scan output directory and collect file metadata.
- **`EvolutionExporter`** — Export evolution.toon.yaml — prioritized refactoring queue.
- **`CoreMetricsComputer`** — Computes core structural and complexity metrics.
- **`ToonRenderer`** — Renders all sections for TOON export.
- **`User`** — —
- **`UserService`** — —
- **`Order`** — —
- **`OrderService`** — —
- **`PatternDetector`** — Detect behavioral patterns in code.
- **`PromptEngine`** — Generate refactoring prompts from analysis results and detected smells.
- **`FuncSummary`** — —
- **`TemplateGenerator`** — Original - handles EVERYTHING: loading, matching, rendering, shell, docker, sql...
- **`CommandContext`** — Context for command generation.
- **`CommandResult`** — Result of command generation.
- **`EntityPreparer`** — Protocol for domain-specific entity preparation.
- **`ShellEntityPreparer`** — Prepares entities for shell commands.
- **`DockerEntityPreparer`** — Prepares entities for docker commands.
- **`SQLEntityPreparer`** — Prepares entities for SQL commands.
- **`KubernetesEntityPreparer`** — Prepares entities for kubernetes commands.
- **`EntityPreparationPipeline`** — Coordinates entity preparation across domains.
- **`Template`** — Command template.
- **`TemplateLoader`** — Loads templates from various sources.
- **`TemplateRenderer`** — Renders templates with entity substitution.
- **`CommandGenerator`** — Generates commands from natural language intents.
- **`CacheEntry`** — Single cache entry with evolution metadata.
- **`EvolutionaryCache`** — Cache that evolves based on usage patterns.
- **`NormalizationResult`** — Result of query normalization.
- **`QueryNormalizer`** — Normalize queries for consistent processing.
- **`IntentMatch`** — Single intent match result.
- **`IntentMatchingResult`** — Result of intent matching.
- **`IntentMatcher`** — Match queries to intents using fuzzy and keyword matching.
- **`NormalizationConfig`** — Configuration for query normalization.
- **`IntentMatchingConfig`** — Configuration for intent matching.
- **`EntityResolutionConfig`** — Configuration for entity resolution.
- **`MultilingualConfig`** — Configuration for multilingual processing.
- **`NLPConfig`** — Main NLP pipeline configuration.
- **`PipelineStage`** — Single pipeline stage result.
- **`NLPPipelineResult`** — Complete NLP pipeline result (4b-4e aggregation).
- **`NLPPipeline`** — Main NLP processing pipeline (4a-4e).
- **`Entity`** — Resolved entity.
- **`EntityResolutionResult`** — Result of entity resolution.
- **`EntityResolver`** — Resolve entities (functions, classes, etc.) from queries.
- **`AnalysisMode`** — Available analysis modes.
- **`PerformanceConfig`** — Performance optimization settings.
- **`FilterConfig`** — Filtering options to reduce analysis scope.
- **`DepthConfig`** — Depth limiting for control flow analysis.
- **`OutputConfig`** — Output formatting options.
- **`Config`** — Analysis configuration with performance optimizations.

### Functions

- `main()` — —
- `main()` — —
- `NewUserService()` — —
- `AddUser()` — —
- `GetUser()` — —
- `ProcessUsers()` — —
- `NewUserService()` — —
- `AddUser()` — —
- `read_readme()` — —
- `run_analysis(project_path)` — Run code2llm and return analysis outputs.
- `get_refactoring_advice(outputs, model)` — Send analysis to LLM and get refactoring advice.
- `main()` — —
- `validate_input(data)` — Validate input data.
- `format_output(data)` — Format output data.
- `calculate_metrics(data)` — Calculate metrics from data list.
- `filter_data(data, criteria)` — Filter data based on criteria.
- `transform_data(data, transformations)` — Transform data fields.
- `create_core_py(project)` — Utwórz core.py z god function, hub type, high fan-out i side-effect.
- `create_etl_py(project)` — Utwórz etl.py z funkcjami pipeline ETL.
- `create_validation_py(project)` — Utwórz validation.py z pipeline'em walidacji.
- `create_utils_py(project)` — Utwórz utils.py z duplikatem klasy Validator.
- `add_validator_to_core(project)` — Dodaj klasę Validator do core.py (tworzy duplikat).
- `create_ground_truth_project(base_dir)` — Utwórz projekt testowy ze znanymi, mierzalnymi problemami.
- `clear_caches(project_path)` — Clear all caches for clean benchmark.
- `run_analysis(project_path, config)` — Run analysis and return (time_seconds, file_count).
- `benchmark_cold_vs_warm(project_path, runs)` — Compare cold (no cache) vs warm (cached) runs.
- `print_summary(results)` — Print benchmark summary with speedup calculations.
- `main()` — —
- `print_results(scores)` — Wydrukuj sformatowane wyniki benchmarku.
- `build_report(scores)` — Zbuduj raport JSON do zapisu.
- `save_report(report, filename)` — Zapisz raport benchmarku do folderu reports.
- `parse_evolution_metrics(toon_content)` — Extract metrics from evolution.toon content.
- `load_previous(history_file)` — Load previous metrics from history file if present.
- `save_current(history_file, metrics)` — Save current metrics for next comparison.
- `run_benchmark(project_path)` — Run evolution analysis and print before/after table.
- `get_current_version()` — Get current version from pyproject.toml
- `parse_version(version_str)` — Parse version string into tuple of (major, minor, patch)
- `format_version(major, minor, patch)` — Format version tuple as string
- `bump_version(version_type)` — Bump version based on type (major, minor, patch)
- `update_pyproject_toml(new_version)` — Update version in pyproject.toml
- `update_version_file(new_version)` — Update VERSION file
- `main()` — —
- `load_yaml(filepath)` — Load YAML file safely.
- `load_file(filepath)` — Load file - auto-detect TOON vs YAML format.
- `extract_functions_from_yaml(yaml_data)` — Extract function list from standard YAML format.
- `extract_functions_from_toon(toon_data)` — Extract function list from parsed TOON data.
- `extract_classes_from_yaml(yaml_data)` — Extract class list from standard YAML format.
- `extract_classes_from_toon(toon_data)` — Extract class list from parsed TOON data.
- `analyze_class_differences(yaml_data, toon_data)` — Analyze why classes differ between formats.
- `extract_modules_from_yaml(yaml_data)` — Extract module list from standard YAML format.
- `extract_modules_from_toon(toon_data)` — Extract module list from parsed TOON data.
- `compare_basic_stats(yaml_data, toon_data)` — Compare basic statistics.
- `compare_functions(yaml_data, toon_data)` — Compare function lists.
- `compare_classes(yaml_data, toon_data)` — Compare class lists with detailed analysis.
- `compare_modules(yaml_data, toon_data)` — Compare module lists with detailed analysis.
- `validate_toon_completeness(toon_data)` — Validate toon format structure.
- `main()` — Main validation function.
- `get_shield_url(label, message, color)` — Generate a shields.io badge URL.
- `parse_evolution_metrics(toon_content)` — Extract metrics from evolution.toon content.
- `parse_format_quality_report(report_path)` — Parse format quality JSON report.
- `parse_performance_report(report_path)` — Parse performance JSON report.
- `generate_badges(metrics)` — Generate badge data from metrics.
- `generate_format_quality_badges(format_scores)` — Generate badges from format quality scores.
- `generate_performance_badges(performance_data)` — Generate badges from performance data.
- `create_html(badges, title)` — Create HTML page with badge table.
- `main()` — Main function to generate badges.
- `main()` — Main CLI entry point.
- `index()` — Serve the main badges page.
- `generate_badges()` — Generate badges by running the benchmark script.
- `get_badges()` — Get the generated badges HTML.
- `analyze(project_path, config)` — Analyze a Python project and return structured results.
- `analyze_file(file_path, config)` — Analyze a single Python file.
- `get_version()` — Read version from VERSION file.
- `create_parser()` — Create CLI argument parser.
- `main()` — Main entry point.
- `main()` — —
- `get_ast(filepath, registry)` — Return parsed AST for *filepath* using the shared registry.
- `find_function_node(tree, name, line)` — Locate a function/async-function node by name and line number.
- `ast_unparse(node, default_none)` — Convert an AST node to its source string via ast.unparse (Python 3.9+).
- `qualified_name(module_name, class_stack, name)` — Build a fully-qualified dotted name from module, optional class scope, and name.
- `expr_to_str(node)` — Convert an AST expression to a dotted string (for call-name extraction).
- `handle_special_commands()` — Handle special sub-commands (llm-flow, llm-context, report, cache).
- `handle_cache_command(args_list)` — Manage persistent cache (~/.code2llm/).
- `handle_report_command(args_list)` — Generate views from an existing project.yaml (legacy).
- `validate_and_setup(args)` — Validate source path and setup output directory.
- `print_start_info(args, source_path, output_dir)` — Print analysis start information if verbose.
- `validate_chunked_output(output_dir, args)` — Validate generated chunked output.
- `generate_llm_context(args_list)` — Quick command to generate LLM context only.
- `make_cache_key(file_path, content)` — Generate a cache key from file stem and MD5 of content.
- `demo_quick_strategy()` — Demonstrate quick strategy analysis.
- `demo_standard_strategy()` — Demonstrate standard strategy analysis.
- `demo_deep_strategy()` — Demonstrate deep strategy analysis.
- `demo_incremental_analysis()` — Demonstrate incremental analysis.
- `demo_memory_limited()` — Demonstrate memory-limited analysis.
- `demo_custom_progress()` — Demonstrate custom progress tracking.
- `main()` — Run all demos.
- `load_gitignore_patterns(project_path)` — Load gitignore patterns from project directory.
- `should_skip_file(file_str, project_path, gitignore_parser)` — Check if file should be skipped.
- `collect_files_in_dir(dir_path, project_path)` — Collect Python files recursively in a directory.
- `collect_root_files(project_path)` — Collect Python files at root level.
- `count_py_files(path)` — Count Python files (excluding tests/cache and gitignore patterns).
- `contains_python_files(dir_path)` — Check if directory contains any Python files.
- `get_level1_dirs(project_path)` — Get all level 1 directories (excluding hidden/cache).
- `calculate_priority(name, level)` — Calculate priority based on name and nesting level.
- `get_file_size_kb(filepath)` — Get file size in KB.
- `should_split_toon(filepath, max_kb)` — Check if TOON file exceeds size limit.
- `split_toon_file(source_file, output_dir, max_kb, prefix)` — Split large TOON file into chunks under size limit.
- `manage_toon_size(source_file, output_dir, max_kb, prefix)` — Main entry point: check and split TOON file if needed.
- `get_all_projects(cache_root)` — Return summary dicts for every cached project.
- `clear_all(cache_root)` — Delete entire ~/.code2llm/ cache.
- `analyze_rust(content, file_path, module_name, ext)` — Analyze Rust files using regex-based parsing.
- `analyze_cpp(content, file_path, module_name, ext)` — Analyze C++ files using shared C-family extraction.
- `analyze_ruby(content, file_path, module_name, ext)` — Analyze Ruby files using shared extraction.
- `extract_declarations_ts(tree, source_bytes, ext, file_path)` — Extract all declarations from a tree-sitter tree.
- `get_parser()` — Get global TreeSitterParser instance.
- `parse_source(content, ext)` — Convenience function: parse string content for given extension.
- `is_available()` — Check if tree-sitter is available.
- `register_language()` — Decorator to register a language parser.
- `get_parser(extension)` — Get parser for a file extension.
- `list_parsers()` — List all registered parsers.
- `analyze_csharp(content, file_path, module_name, ext)` — Analyze C# files using shared C-family extraction.
- `analyze_php(content, file_path, module_name, ext)` — —
- `analyze_go(content, file_path, module_name, ext)` — Analyze Go files. Uses tree-sitter when available, regex fallback.
- `analyze_java(content, file_path, module_name, ext)` — Analyze Java files using shared C-family extraction.
- `get_typescript_patterns()` — Returns regex patterns for TypeScript/JavaScript parsing.
- `get_typescript_lang_config()` — Returns language configuration for TypeScript/JavaScript.
- `analyze_typescript_js(content, file_path, module_name, ext)` — Analyze TypeScript/JavaScript files using shared extraction.
- `extract_function_body(content, start_line)` — Extract the body of a function between braces from a start line (1-indexed).
- `calculate_complexity_regex(content, result, lang)` — Estimate cyclomatic complexity for every function using regex keyword counting.
- `extract_calls_regex(content, module_name, result)` — Extract function calls from function bodies using regex.
- `analyze_c_family(content, file_path, module_name, stats)` — Shared analyzer for C-family languages (Java, C#, C++, etc.).
- `analyze_generic(content, file_path, module_name, ext)` — Basic structural analysis for unsupported languages.
- `evaluate_format(name, content, path)` — Oceń pojedynczy format względem ground truth.
- `export_format(name, description, extension, supports_project_yaml)` — Decorator to register an exporter with the EXPORT_REGISTRY.
- `get_exporter(name)` — Get exporter class by format name.
- `list_exporters()` — List all registered exporters with metadata.
- `save_report(results, filename)` — Save benchmark report to reports folder.
- `create_test_project(size)` — Create test project of specified size.
- `benchmark_original_analyzer(project_path, runs)` — Benchmark original ProjectAnalyzer.
- `benchmark_streaming_analyzer(project_path, runs)` — Benchmark new StreamingAnalyzer.
- `benchmark_with_strategies(project_path)` — Benchmark all strategies.
- `print_comparison(original, streaming)` — Print comparison table.
- `main()` — Run benchmark suite.
- `load_project_yaml(path)` — Load and validate project.yaml with detailed error reporting.
- `should_use_chunking(project_path, size_threshold_kb)` — Check if repository should use chunked analysis.
- `get_analysis_plan(project_path, size_limit_kb)` — Get analysis plan for project (auto-detect if chunking needed).
- `is_excluded_path(path)` — Return True if *path* matches any standard exclusion pattern (venv, cache, etc.).
- `validate_project_yaml(output_dir, verbose)` — Validate project.yaml against generated views in output_dir.
- `run_benchmark()` — Run the full format quality benchmark.
- `build_evolution(health, total_lines, prev_evolution)` — Build append-only evolution history.
- `load_previous_evolution(output_path)` — Load previous evolution entries from existing project.yaml.
- `build_hotspots(result)` — Build hotspots list (high fan-out functions).
- `hotspot_note(fi, fan_out)` — Generate descriptive note for a hotspot.
- `build_refactoring(result, modules, hotspots)` — Build prioritized refactoring actions.
- `generate_index_html(output_dir)` — Generate index.html in the specified directory.
- `build_modules(result, line_counts)` — Build module list with per-file metrics.
- `group_by_file(result)` — Group functions and classes by file path.
- `compute_module_entry(fpath, result, line_counts, file_funcs)` — Build a single module dict for the given file.
- `compute_inbound_deps(funcs, fpath, result)` — Count unique files that call into this module.
- `build_exports(funcs, classes, result)` — Build export list (classes + standalone functions) for a module.
- `build_class_export(ci, result)` — Build export entry for a single class.
- `build_function_exports(funcs, classes)` — Build export entries for standalone (non-method) functions.
- `dump_yaml(data)` — Shared YAML serialiser (sort_keys=False, unicode, width=100).
- `build_health(result, modules)` — Build health section with CC metrics, alerts, and issues.
- `build_alerts(result)` — Build list of health alerts for high CC and high fan-out.
- `count_duplicates(result)` — Count duplicate class names in different files.
- `get_file_types()` — Get file type configuration mapping.
- `get_default_file_info(ext)` — Get default file info for unknown extension.
- `normalize_llm_task(data)` — —
- `parse_llm_task_text(text)` — Parse LLM task text into structured data.
- `load_input(path)` — Load input file with detailed YAML/JSON error reporting.
- `create_parser()` — —
- `main(argv)` — —
- `parse_toon_content(content)` — Parse TOON v2 plain-text format.
- `is_toon_file(filepath)` — Check if file is TOON format based on extension or content.
- `load_toon(filepath)` — Parse TOON plain-text format into structured data.
- `main()` — —
- `NewUserService()` — —
- `AddUser()` — —
- `GetUser()` — —
- `ProcessUsers()` — —
- `validate_mermaid_file(mmd_path)` — Validate Mermaid file and return list of errors.
- `fix_mermaid_file(mmd_path)` — Attempt to fix common Mermaid syntax errors.
- `generate_pngs(input_dir, output_dir, timeout, max_workers)` — Generate PNG files from all .mmd files in input_dir (parallel).
- `generate_single_png(mmd_file, output_file, timeout)` — Generate PNG from single Mermaid file using available renderers.
- `generate_with_puppeteer(mmd_file, output_file, timeout, max_text_size)` — Generate PNG using Puppeteer with HTML template.
- `generate_llm_flow(analysis, max_functions, limit_decisions, limit_calls)` — —
- `render_llm_flow_md(flow)` — —
- `create_parser()` — —
- `main(argv)` — —
- `generate(query, intent, dry_run, cache_dir)` — Generate command from natural language query.


## Project Structure

📄 `badges.server` (3 functions)
📄 `benchmarks.benchmark_constants`
📄 `benchmarks.benchmark_evolution` (4 functions)
📄 `benchmarks.benchmark_format_quality` (5 functions)
📄 `benchmarks.benchmark_optimizations` (5 functions)
📄 `benchmarks.benchmark_performance` (7 functions)
📄 `benchmarks.format_evaluator` (5 functions, 1 classes)
📄 `benchmarks.project_generator` (6 functions)
📄 `benchmarks.reporting` (9 functions)
📦 `code2llm` (1 functions)
📄 `code2llm.__main__`
📦 `code2llm.analysis` (1 functions)
📄 `code2llm.analysis.call_graph` (12 functions, 1 classes)
📄 `code2llm.analysis.cfg` (16 functions, 1 classes)
📄 `code2llm.analysis.coupling` (5 functions, 1 classes)
📄 `code2llm.analysis.data_analysis` (28 functions, 3 classes)
📄 `code2llm.analysis.dfg` (12 functions, 1 classes)
📄 `code2llm.analysis.pipeline_classifier` (5 functions, 1 classes)
📄 `code2llm.analysis.pipeline_detector` (9 functions, 3 classes)
📄 `code2llm.analysis.pipeline_resolver` (5 functions, 1 classes)
📄 `code2llm.analysis.side_effects` (15 functions, 2 classes)
📄 `code2llm.analysis.smells` (9 functions, 1 classes)
📄 `code2llm.analysis.type_inference` (17 functions, 1 classes)
📦 `code2llm.analysis.utils`
📄 `code2llm.analysis.utils.ast_helpers` (5 functions)
📄 `code2llm.api` (2 functions)
📄 `code2llm.cli` (1 functions)
📄 `code2llm.cli_analysis` (11 functions)
📄 `code2llm.cli_commands` (13 functions)
📦 `code2llm.cli_exports`
📄 `code2llm.cli_exports.code2logic` (8 functions)
📄 `code2llm.cli_exports.formats` (16 functions)
📄 `code2llm.cli_exports.orchestrator` (20 functions)
📄 `code2llm.cli_exports.prompt` (18 functions)
📄 `code2llm.cli_parser` (2 functions)
📦 `code2llm.core` (1 functions)
📄 `code2llm.core.analyzer` (20 functions, 1 classes)
📄 `code2llm.core.ast_registry` (9 functions, 1 classes)
📄 `code2llm.core.config` (2 functions, 6 classes)
📄 `code2llm.core.export_pipeline` (5 functions, 2 classes)
📄 `code2llm.core.file_analyzer` (18 functions, 1 classes)
📄 `code2llm.core.file_cache` (10 functions, 1 classes)
📄 `code2llm.core.file_filter` (9 functions, 1 classes)
📄 `code2llm.core.gitignore` (7 functions, 2 classes)
📄 `code2llm.core.incremental` (10 functions, 1 classes)
📦 `code2llm.core.lang` (5 functions, 1 classes)
📄 `code2llm.core.lang.base` (14 functions)
📄 `code2llm.core.lang.cpp` (1 functions)
📄 `code2llm.core.lang.csharp` (1 functions)
📄 `code2llm.core.lang.generic` (1 functions)
📄 `code2llm.core.lang.go_lang` (2 functions)
📄 `code2llm.core.lang.java` (1 functions)
📄 `code2llm.core.lang.php` (4 functions)
📄 `code2llm.core.lang.ruby` (4 functions, 1 classes)
📄 `code2llm.core.lang.rust` (1 functions)
📄 `code2llm.core.lang.ts_extractors` (5 functions)
📄 `code2llm.core.lang.ts_parser` (9 functions, 1 classes)
📄 `code2llm.core.lang.typescript` (3 functions)
📄 `code2llm.core.large_repo` (20 functions, 2 classes)
📄 `code2llm.core.models` (6 functions, 11 classes)
📄 `code2llm.core.persistent_cache` (18 functions, 1 classes)
📄 `code2llm.core.refactoring` (11 functions, 1 classes)
📄 `code2llm.core.repo_files` (8 functions)
📦 `code2llm.core.streaming`
📄 `code2llm.core.streaming.cache` (5 functions, 1 classes)
📄 `code2llm.core.streaming.incremental` (5 functions, 1 classes)
📄 `code2llm.core.streaming.prioritizer` (4 functions, 2 classes)
📄 `code2llm.core.streaming.scanner` (6 functions, 1 classes)
📄 `code2llm.core.streaming.strategies` (1 classes)
📄 `code2llm.core.streaming_analyzer` (6 functions, 1 classes)
📄 `code2llm.core.toon_size_manager` (8 functions)
📦 `code2llm.exporters`
📄 `code2llm.exporters.article_view` (8 functions, 1 classes)
📄 `code2llm.exporters.base` (8 functions, 2 classes)
📄 `code2llm.exporters.context_exporter` (15 functions, 1 classes)
📄 `code2llm.exporters.context_view` (7 functions, 1 classes)
📄 `code2llm.exporters.dashboard_data` (9 functions, 1 classes)
📄 `code2llm.exporters.dashboard_renderer` (4 functions, 1 classes)
📄 `code2llm.exporters.evolution_exporter` (17 functions, 1 classes)
📄 `code2llm.exporters.flow_constants` (1 functions)
📄 `code2llm.exporters.flow_exporter` (14 functions, 1 classes)
📄 `code2llm.exporters.flow_renderer` (6 functions, 1 classes)
📄 `code2llm.exporters.html_dashboard` (3 functions, 1 classes)
📦 `code2llm.exporters.index_generator` (5 functions, 1 classes)
📄 `code2llm.exporters.index_generator.renderer` (1 functions, 1 classes)
📄 `code2llm.exporters.index_generator.scanner` (7 functions, 1 classes)
📄 `code2llm.exporters.json_exporter` (1 functions, 1 classes)
📄 `code2llm.exporters.llm_exporter`
📄 `code2llm.exporters.map_exporter` (24 functions, 1 classes)
📄 `code2llm.exporters.mermaid_exporter` (23 functions, 1 classes)
📄 `code2llm.exporters.mermaid_flow_helpers` (12 functions)
📦 `code2llm.exporters.project_yaml`
📄 `code2llm.exporters.project_yaml.constants`
📄 `code2llm.exporters.project_yaml.core` (3 functions, 1 classes)
📄 `code2llm.exporters.project_yaml.evolution` (2 functions)
📄 `code2llm.exporters.project_yaml.health` (3 functions)
📄 `code2llm.exporters.project_yaml.hotspots` (3 functions)
📄 `code2llm.exporters.project_yaml.modules` (7 functions)
📄 `code2llm.exporters.project_yaml_exporter`
📄 `code2llm.exporters.readme_exporter` (7 functions, 1 classes)
📄 `code2llm.exporters.report_generators` (1 functions)
📦 `code2llm.exporters.toon` (11 functions, 1 classes)
📄 `code2llm.exporters.toon.helpers` (7 functions)
📄 `code2llm.exporters.toon.metrics` (4 functions, 1 classes)
📄 `code2llm.exporters.toon.metrics_core` (16 functions, 1 classes)
📄 `code2llm.exporters.toon.metrics_duplicates` (4 functions, 1 classes)
📄 `code2llm.exporters.toon.metrics_health` (6 functions, 1 classes)
📄 `code2llm.exporters.toon.module_detail` (9 functions, 1 classes)
📄 `code2llm.exporters.toon.renderer` (26 functions, 1 classes)
📄 `code2llm.exporters.toon_view` (8 functions, 1 classes)
📄 `code2llm.exporters.validate_project` (3 functions)
📄 `code2llm.exporters.yaml_exporter` (24 functions, 1 classes)
📦 `code2llm.generators`
📄 `code2llm.generators._utils` (1 functions)
📄 `code2llm.generators.llm_flow` (23 functions, 1 classes)
📄 `code2llm.generators.llm_task` (14 functions)
📄 `code2llm.generators.mermaid` (21 functions)
📦 `code2llm.nlp`
📄 `code2llm.nlp.config` (2 functions, 5 classes)
📄 `code2llm.nlp.entity_resolution` (16 functions, 3 classes)
📄 `code2llm.nlp.intent_matching` (15 functions, 3 classes)
📄 `code2llm.nlp.normalization` (13 functions, 2 classes)
📄 `code2llm.nlp.pipeline` (20 functions, 3 classes)
📄 `code2llm.parsers.toon_parser` (10 functions)
📦 `code2llm.patterns`
📄 `code2llm.patterns.detector` (8 functions, 1 classes)
📦 `code2llm.refactor`
📄 `code2llm.refactor.prompt_engine` (7 functions, 1 classes)
📄 `demo_langs.valid.sample` (5 functions, 2 classes)
📄 `examples.functional_refactoring_example` (50 functions, 15 classes)
📄 `examples.litellm.run` (3 functions)
📄 `examples.streaming-analyzer.demo` (7 functions)
📦 `examples.streaming-analyzer.sample_project`
📄 `examples.streaming-analyzer.sample_project.api` (7 functions, 1 classes)
📄 `examples.streaming-analyzer.sample_project.auth` (10 functions, 1 classes)
📄 `examples.streaming-analyzer.sample_project.database` (13 functions, 1 classes)
📄 `examples.streaming-analyzer.sample_project.main` (9 functions, 2 classes)
📄 `examples.streaming-analyzer.sample_project.utils` (5 functions)
📄 `orchestrator`
📄 `project`
📄 `project2`
📄 `scripts.benchmark_badges` (9 functions)
📄 `scripts.bump_version` (7 functions)
📄 `setup` (1 functions)
📄 `test_langs.invalid.sample_bad` (3 functions, 1 classes)
📄 `test_langs.valid.sample` (5 functions, 2 classes)
📦 `test_python_only.invalid`
📦 `test_python_only.valid`
📄 `test_python_only.valid.sample` (5 functions, 2 classes)
📄 `validate_toon` (21 functions)

## Requirements

- Python >= >=3.8
- networkx >=2.6- matplotlib >=3.4- pyyaml >=5.4- numpy >=1.20- jinja2 >=3.0- radon >=5.1- astroid >=3.0- code2logic- vulture >=2.10- tiktoken >=0.5- tree-sitter >=0.21- tree-sitter-python >=0.21- tree-sitter-javascript >=0.21- tree-sitter-typescript >=0.21- tree-sitter-go >=0.21- tree-sitter-rust >=0.21- tree-sitter-java >=0.21- tree-sitter-c >=0.21- tree-sitter-cpp >=0.22- tree-sitter-c-sharp >=0.21- tree-sitter-php >=0.22- tree-sitter-ruby >=0.21

## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/wronai/code2flow
cd code2llm

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 📖 [Full Documentation](https://github.com/wronai/code2flow/tree/main/docs) — API reference, module docs, architecture
- 🚀 [Getting Started](https://github.com/wronai/code2flow/blob/main/docs/getting-started.md) — Quick start guide
- 📚 [API Reference](https://github.com/wronai/code2flow/blob/main/docs/api.md) — Complete API documentation
- 🔧 [Configuration](https://github.com/wronai/code2flow/blob/main/docs/configuration.md) — Configuration options
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `docs/api.md` | Consolidated API reference | [View](./docs/api.md) |
| `docs/modules.md` | Module reference with metrics | [View](./docs/modules.md) |
| `docs/architecture.md` | Architecture with diagrams | [View](./docs/architecture.md) |
| `docs/dependency-graph.md` | Dependency graphs | [View](./docs/dependency-graph.md) |
| `docs/coverage.md` | Docstring coverage report | [View](./docs/coverage.md) |
| `docs/getting-started.md` | Getting started guide | [View](./docs/getting-started.md) |
| `docs/configuration.md` | Configuration reference | [View](./docs/configuration.md) |
| `docs/api-changelog.md` | API change tracking | [View](./docs/api-changelog.md) |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples/` | Usage examples | [Browse](./examples) |
| `mkdocs.yml` | MkDocs configuration | — |

<!-- code2docs:end -->