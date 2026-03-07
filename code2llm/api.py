"""Stable public API for code2llm — primary entry point for external consumers.

This module provides a clean, stable interface for tools like code2docs
that depend on code2llm's analysis capabilities.
"""

from pathlib import Path
from typing import Optional

from .core.config import Config, FAST_CONFIG
from .core.models import (
    AnalysisResult,
    FunctionInfo,
    ClassInfo,
    ModuleInfo,
    Pattern,
    CodeSmell,
    FlowNode,
    FlowEdge,
    DataFlow,
    Mutation,
)


def analyze(project_path: str, config: Optional[Config] = None) -> AnalysisResult:
    """Analyze a Python project and return structured results.

    This is the main entry point for external consumers of code2llm.

    Args:
        project_path: Path to the project directory to analyze.
        config: Optional analysis configuration. Defaults to FAST_CONFIG.

    Returns:
        AnalysisResult with functions, classes, modules, call graph, patterns, etc.
    """
    from .core.analyzer import ProjectAnalyzer

    config = config or FAST_CONFIG
    analyzer = ProjectAnalyzer(config)
    return analyzer.analyze_project(project_path)


def analyze_file(file_path: str, config: Optional[Config] = None) -> AnalysisResult:
    """Analyze a single Python file.

    Args:
        file_path: Path to the Python file to analyze.
        config: Optional analysis configuration.

    Returns:
        AnalysisResult for the single file.
    """
    path = Path(file_path).resolve()
    return analyze(str(path.parent), config)


__all__ = [
    "analyze",
    "analyze_file",
    "Config",
    "FAST_CONFIG",
    "AnalysisResult",
    "FunctionInfo",
    "ClassInfo",
    "ModuleInfo",
    "Pattern",
    "CodeSmell",
    "FlowNode",
    "FlowEdge",
    "DataFlow",
    "Mutation",
]
