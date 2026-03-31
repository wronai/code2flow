"""Centralny rejestr drzew AST — jeden ast.parse() per plik per przebieg.

Wszystkie moduły analizy (side_effects, type_inference, call_graph, cfg, dfg)
korzystają z tego singletona zamiast wywoływać ast.parse() niezależnie.
"""

import ast
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ASTRegistry:
    """Parse each file exactly once; share the AST across all analysis consumers.

    Usage (per-run singleton)::

        registry = ASTRegistry.get_global()
        tree = registry.get_ast("/path/to/file.py")

    Usage (explicit instance, e.g. in tests)::

        registry = ASTRegistry()
        tree = registry.get_ast(filepath)
    """

    _global: Optional["ASTRegistry"] = None

    def __init__(self) -> None:
        self._trees: Dict[str, Optional[ast.Module]] = {}
        self._sources: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @classmethod
    def get_global(cls) -> "ASTRegistry":
        """Return (or create) the process-wide singleton."""
        if cls._global is None:
            cls._global = cls()
        return cls._global

    @classmethod
    def reset_global(cls) -> None:
        """Discard the singleton (call between independent analysis runs)."""
        cls._global = None

    def get_ast(self, filepath: str) -> Optional[ast.Module]:
        """Return parsed AST for *filepath*, parsing at most once per instance."""
        if not filepath:
            return None
        if filepath in self._trees:
            return self._trees[filepath]

        source = self.get_source(filepath)
        if source is None:
            self._trees[filepath] = None
            return None

        try:
            tree = ast.parse(source, filename=filepath)
            self._trees[filepath] = tree
        except SyntaxError as exc:
            logger.debug("SyntaxError in %s: %s", filepath, exc)
            self._trees[filepath] = None

        return self._trees[filepath]

    def get_source(self, filepath: str) -> Optional[str]:
        """Return source text for *filepath*, reading at most once per instance."""
        if not filepath:
            return None
        if filepath in self._sources:
            return self._sources[filepath]

        try:
            source = Path(filepath).read_text(encoding="utf-8", errors="replace")
            self._sources[filepath] = source
        except (OSError, IOError) as exc:
            logger.debug("Cannot read %s: %s", filepath, exc)
            return None

        return self._sources.get(filepath)

    def invalidate(self, filepath: str) -> None:
        """Remove cached AST and source for *filepath* (e.g. after file write)."""
        self._trees.pop(filepath, None)
        self._sources.pop(filepath, None)

    def clear(self) -> None:
        """Remove all cached entries."""
        self._trees.clear()
        self._sources.clear()

    def __len__(self) -> int:
        return len(self._trees)

    def __repr__(self) -> str:
        return f"ASTRegistry({len(self._trees)} files cached)"
