"""Evolution exporter exclusion logic — path filtering."""

from .constants import EXCLUDE_PATTERNS


def is_excluded(path: str) -> bool:
    """Check if path should be excluded (venv, site-packages, etc.)."""
    path_lower = path.lower().replace('\\', '/')
    for pattern in EXCLUDE_PATTERNS:
        if f'/{pattern}/' in path_lower or path_lower.startswith(f'{pattern}/'):
            return True
        if pattern in path_lower.split('/'):
            return True
    return False


__all__ = ['is_excluded']
