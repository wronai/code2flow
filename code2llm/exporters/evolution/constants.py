"""Evolution exporter constants — thresholds and configuration."""

# Thresholds
CC_SPLIT_THRESHOLD = 15
FAN_OUT_THRESHOLD = 10
GOD_MODULE_LINES = 500
HUB_TYPE_THRESHOLD = 10


# Exclude patterns (mirrors ToonExporter)
EXCLUDE_PATTERNS = {
    'venv', '.venv', 'env', '.env', 'publish-env', 'test-env',
    'site-packages', 'node_modules', '__pycache__', '.git',
    'dist', 'build', 'egg-info', '.tox', '.mypy_cache',
    'examples', 'benchmarks', 'tests', 'scripts', 'demo_langs',
}


__all__ = [
    'CC_SPLIT_THRESHOLD',
    'FAN_OUT_THRESHOLD',
    'GOD_MODULE_LINES',
    'HUB_TYPE_THRESHOLD',
    'EXCLUDE_PATTERNS',
]
