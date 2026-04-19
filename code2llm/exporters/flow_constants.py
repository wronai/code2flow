"""Stałe dla FlowExporter.

Zawiera progi, wzorce wykluczeń i rekomendacje dotyczące podziału typów hub.
"""

# Progi dla wykrywania problemów
CC_HIGH = 15
FAN_OUT_THRESHOLD = 10
HUB_TYPE_THRESHOLD = 10

# Wzorce do wykluczenia (venv, cache, etc.)
EXCLUDE_PATTERNS = {
    'venv', '.venv', 'env', '.env', 'publish-env', 'test-env',
    'site-packages', 'node_modules', '__pycache__', '.git',
    'dist', 'build', 'egg-info', '.tox', '.mypy_cache',
    # Backup directories that often contain nested venvs
    '.algitex', '.backup', 'backups', '.bak',
    # Additional venv patterns  
    'virtualenv', '.virtualenv', 'envs', '.envs',
}

def is_excluded_path(path: str) -> bool:
    """Return True if *path* matches any standard exclusion pattern (venv, cache, etc.)."""
    if not path:
        return False
    path_lower = path.lower().replace('\\', '/')
    for pattern in EXCLUDE_PATTERNS:
        if f'/{pattern}/' in path_lower or path_lower.startswith(f'{pattern}/'):
            return True
        if pattern in path_lower.split('/'):
            return True
    return False


# Rekomendacje podziału typów hub: typ -> sugerowane pod-interfejsy
HUB_SPLIT_RECOMMENDATIONS = {
    "AnalysisResult": [
        "StructureResult (modules, classes, functions)",
        "MetricsResult (complexity, coupling)",
        "FlowResult (call_graph, cfg, dfg)",
    ],
    "dict": ["replace with typed alternatives (dataclass/TypedDict)"],
    "str": [],  # primitive, expected to be ubiquitous
    "list": [],
    "Any": [],
}
