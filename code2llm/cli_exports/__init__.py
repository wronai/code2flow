"""CLI export functions — split into thematic modules.

Thin re-export so existing ``from .cli_exports import ...`` continues to work.
"""

from .formats import (
    _export_simple_formats,
    _export_yaml,
    _export_mermaid,
    _export_evolution,
    _export_data_structures,
    _export_context_fallback,
    _export_readme,
    _export_refactor_prompts,
    _export_project_yaml,
    _run_report,
)
from .prompt import (
    _export_prompt_txt,
    _export_chunked_prompt_txt,
)
from .code2logic import (
    _export_code2logic,
)
from .orchestrator import (
    _run_exports,
    _export_single_project,
    _export_chunked_results,
)
from .orchestrator_chunked import (
    _get_filtered_subprojects,
    _process_subproject,
)

__all__ = [
    "_export_simple_formats",
    "_export_yaml",
    "_export_mermaid",
    "_export_evolution",
    "_export_data_structures",
    "_export_context_fallback",
    "_export_readme",
    "_export_refactor_prompts",
    "_export_project_yaml",
    "_run_report",
    "_export_prompt_txt",
    "_export_chunked_prompt_txt",
    "_export_code2logic",
    "_run_exports",
    "_export_single_project",
    "_export_chunked_results",
    "_get_filtered_subprojects",
    "_process_subproject",
]
