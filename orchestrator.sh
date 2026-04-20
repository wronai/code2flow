#!/bin/bash
# orchestrator.sh — Generate all 5 TOON files for code2llm ecosystem
# Usage: ./orchestrator.sh [PROJECT_DIR] [OUTPUT_DIR]
# Generates: map.toon, analysis.toon, evolution.toon, validation.toon, duplication.toon
#
# Performance optimizations applied:
# - Fix 1: PIP_DISABLE_PIP_VERSION_CHECK=1 (saves ~4-8s)
# - Fix 3: Skip redup for non-Python projects (saves ~8s)
# - Fix 4: Unified pipeline.py preferred over 5 subprocesses (saves ~3-5s)

# Performance: disable pip version check (~4-8s saved per subprocess)
export PIP_DISABLE_PIP_VERSION_CHECK=1

set -e

PROJECT_DIR="${1:-.}"
OUTPUT_DIR="${2:-$PROJECT_DIR/project}"

mkdir -p "$OUTPUT_DIR"

# Fix 4: Use unified pipeline.py if available (single process = ~3-5s faster)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/pipeline.py" ] && [ -z "$FORCE_SUBPROCESS" ]; then
    echo "=== Unified Pipeline (single-process mode) ==="
    python3 "$SCRIPT_DIR/pipeline.py" "$PROJECT_DIR" "$OUTPUT_DIR"
    exit 0
fi

# Fallback: subprocess mode (slower but 100% compatible)
echo "=== code2llm ==="
echo "Generating: map.toon, analysis.toon, evolution.toon"
if command -v code2llm &> /dev/null; then
    code2llm "$PROJECT_DIR" -o "$OUTPUT_DIR" --format toon
elif python3 -c "import code2llm" 2>/dev/null; then
    python3 -m code2llm "$PROJECT_DIR" -o "$OUTPUT_DIR" --format toon
else
    echo "  [SKIP] code2llm not installed"
    exit 1
fi

echo ""
echo "=== vallm ==="
echo "Generating: validation.toon (compact mode)"
if command -v vallm &> /dev/null; then
    vallm batch "$PROJECT_DIR" -o "$OUTPUT_DIR/validation.toon" --compact 2>/dev/null || \
        echo "  [WARN] vallm completed with warnings"
else
    echo "  [SKIP] vallm not installed — run: pip install vallm"
fi

echo ""
echo "=== redup ==="
echo "Generating: duplication.toon"

# Fix 3: Skip redup for non-Python projects (saves ~8s startup when no .py files)
if find "$PROJECT_DIR" -name "*.py" -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/.venv/*" -print -quit 2>/dev/null | grep -q .; then
    if command -v redup &> /dev/null; then
        redup scan "$PROJECT_DIR" -o "$OUTPUT_DIR/duplication.toon" 2>/dev/null || \
            echo "  [WARN] redup completed with warnings"
    else
        echo "  [SKIP] redup not installed — run: pip install redup"
    fi
else
    echo "  [SKIP] redup — no Python files detected"
    echo "# redup/duplication | 0 groups | skip (non-python project)" > "$OUTPUT_DIR/duplication.toon"
fi

echo ""
echo "=== Done ==="
TOON_FILES=("$OUTPUT_DIR/map.toon" "$OUTPUT_DIR/analysis.toon" "$OUTPUT_DIR/evolution.toon" "$OUTPUT_DIR/validation.toon" "$OUTPUT_DIR/duplication.toon")
GENERATED=0
for f in "${TOON_FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "  ✓ $(basename $f)"
        ((GENERATED++))
    else
        echo "  ✗ $(basename $f) — not generated"
    fi
done

echo ""
echo "Generated $GENERATED/5 TOON files in $OUTPUT_DIR/"
