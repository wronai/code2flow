"""Tree-sitter parser wrapper — fast CST parsing for all supported languages.

Replaces regex-based parsing with tree-sitter for 10× speedup and better accuracy.
Falls back to regex parsing if tree-sitter grammar is unavailable.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Lazy-loaded language modules
_LANGUAGE_MODULES: Dict[str, Any] = {}
_PARSERS: Dict[str, Any] = {}
_TS_AVAILABLE = False

# Extension -> (grammar module name, language getter)
EXTENSION_MAP = {
    '.py': ('tree_sitter_python', 'language'),
    '.js': ('tree_sitter_javascript', 'language'),
    '.jsx': ('tree_sitter_javascript', 'language'),
    '.mjs': ('tree_sitter_javascript', 'language'),
    '.cjs': ('tree_sitter_javascript', 'language'),
    '.ts': ('tree_sitter_typescript', 'language_typescript'),
    '.tsx': ('tree_sitter_typescript', 'language_tsx'),
    '.go': ('tree_sitter_go', 'language'),
    '.rs': ('tree_sitter_rust', 'language'),
    '.java': ('tree_sitter_java', 'language'),
    '.c': ('tree_sitter_c', 'language'),
    '.h': ('tree_sitter_c', 'language'),
    '.cpp': ('tree_sitter_cpp', 'language'),
    '.cc': ('tree_sitter_cpp', 'language'),
    '.cxx': ('tree_sitter_cpp', 'language'),
    '.hpp': ('tree_sitter_cpp', 'language'),
    '.hxx': ('tree_sitter_cpp', 'language'),
    '.cs': ('tree_sitter_c_sharp', 'language'),
    '.php': ('tree_sitter_php', 'language_php'),
    '.rb': ('tree_sitter_ruby', 'language'),
}


def _init_tree_sitter() -> bool:
    """Initialize tree-sitter. Returns True if available."""
    global _TS_AVAILABLE
    try:
        import tree_sitter
        _TS_AVAILABLE = True
        return True
    except ImportError:
        logger.debug("tree-sitter not installed, using regex fallback")
        return False


def _get_language(ext: str) -> Optional[Any]:
    """Get tree-sitter Language for file extension."""
    if not _TS_AVAILABLE and not _init_tree_sitter():
        return None

    if ext not in EXTENSION_MAP:
        return None

    module_name, lang_attr = EXTENSION_MAP[ext]

    if module_name in _LANGUAGE_MODULES:
        return _LANGUAGE_MODULES[module_name]

    try:
        import importlib
        mod = importlib.import_module(module_name)
        lang_fn = getattr(mod, lang_attr, None)
        if callable(lang_fn):
            lang = lang_fn()
            _LANGUAGE_MODULES[module_name] = lang
            return lang
    except (ImportError, AttributeError) as e:
        logger.debug("Cannot load %s: %s", module_name, e)
        _LANGUAGE_MODULES[module_name] = None

    return None


def _get_parser(ext: str) -> Optional[Any]:
    """Get or create tree-sitter Parser for file extension."""
    if ext in _PARSERS:
        return _PARSERS[ext]

    lang = _get_language(ext)
    if not lang:
        _PARSERS[ext] = None
        return None

    try:
        from tree_sitter import Parser
        parser = Parser(lang)
        _PARSERS[ext] = parser
        return parser
    except Exception as e:
        logger.debug("Cannot create parser for %s: %s", ext, e)
        _PARSERS[ext] = None
        return None


class TreeSitterParser:
    """Unified tree-sitter parser for all supported languages.

    Usage::

        parser = TreeSitterParser()
        tree = parser.parse(source_bytes, ".ts")
        if tree:
            # Use tree.root_node for traversal
            for node in tree.root_node.children:
                ...
    """

    def __init__(self):
        self._initialized = _init_tree_sitter()

    @property
    def available(self) -> bool:
        return self._initialized

    def parse(self, source: bytes, ext: str) -> Optional[Any]:
        """Parse source code and return tree, or None if unavailable."""
        parser = _get_parser(ext)
        if not parser:
            return None
        try:
            return parser.parse(source)
        except Exception as e:
            logger.debug("Parse error for %s: %s", ext, e)
            return None

    def supports(self, ext: str) -> bool:
        """Check if extension is supported by tree-sitter."""
        return ext in EXTENSION_MAP and _get_language(ext) is not None


# Singleton instance
_parser_instance: Optional[TreeSitterParser] = None


def get_parser() -> TreeSitterParser:
    """Get global TreeSitterParser instance."""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = TreeSitterParser()
    return _parser_instance


def parse_source(content: str, ext: str) -> Optional[Any]:
    """Convenience function: parse string content for given extension."""
    return get_parser().parse(content.encode('utf-8'), ext)


def is_available() -> bool:
    """Check if tree-sitter is available."""
    return get_parser().available
