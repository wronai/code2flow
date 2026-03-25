#!/bin/bash
# orchestrator.sh — Generate all 5 TOON files for code2llm ecosystem
# Usage: ./orchestrator.sh [PROJECT_DIR] [OUTPUT_DIR]
# Generates: map.toon, analysis.toon, evolution.toon, validation.toon, duplication.toon

set -e

PROJECT_DIR="${1:-.}"
OUTPUT_DIR="${2:-$PROJECT_DIR/project}"

mkdir -p "$OUTPUT_DIR"

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
if command -v redup &> /dev/null; then
    redup scan "$PROJECT_DIR" -o "$OUTPUT_DIR/duplication.toon" 2>/dev/null || \
        echo "  [WARN] redup completed with warnings"
else
    echo "  [SKIP] redup not installed — run: pip install redup"
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
