"""Regression tests for FileAnalyzer result tagging.

Covers the bug where analyze_file() returned a result dict without a
'file' key, causing ProjectAnalyzer._store_to_persistent_cache to never
match results back to source paths. Consequence: the persistent manifest
stayed empty, the export-level cache key collapsed to md5("{}"), and
stale exports were copied across unrelated runs (including after
`pip install --upgrade code2llm`).

This file pins the contract: every non-empty analyze_file() result must
carry a 'file' key equal to the input file_path, regardless of language.
"""

import pytest

from code2llm.core.config import Config
from code2llm.core.file_analyzer import FileAnalyzer


@pytest.fixture()
def analyzer():
    return FileAnalyzer(Config(), cache=None)


@pytest.mark.parametrize(
    "filename,content",
    [
        ("sample.py", "def foo():\n    return 1\n"),
        ("sample.ts", "export function foo(): number { return 1; }\n"),
        ("sample.go", "package main\nfunc Foo() int { return 1 }\n"),
        ("sample.rs", "pub fn foo() -> i32 { 1 }\n"),
        ("sample.java", "class A { int foo() { return 1; } }\n"),
        ("sample.rb", "def foo\n  1\nend\n"),
        ("sample.php", "<?php\nfunction foo() { return 1; }\n"),
    ],
)
def test_analyze_file_tags_result_with_path(tmp_path, analyzer, filename, content):
    fp = tmp_path / filename
    fp.write_text(content)
    result = analyzer.analyze_file(str(fp), "sample")
    assert result, f"expected non-empty result for {filename}"
    assert result.get("file") == str(fp), (
        f"{filename}: analyze_file must tag result with 'file' key so "
        f"ProjectAnalyzer._store_to_persistent_cache can match it back "
        f"to the source path (got {result.get('file')!r})"
    )


def test_nonexistent_file_returns_empty(analyzer, tmp_path):
    result = analyzer.analyze_file(str(tmp_path / "missing.py"), "missing")
    assert result == {}


def test_cached_result_also_tagged(tmp_path):
    """The fast in-memory cache path must also return a tagged result."""
    from code2llm.core.file_cache import FileCache

    fp = tmp_path / "a.py"
    fp.write_text("def foo(): return 1\n")

    cache = FileCache(str(tmp_path / ".c2l_cache"), ttl_hours=1)
    analyzer = FileAnalyzer(Config(), cache=cache)

    first = analyzer.analyze_file(str(fp), "a")
    assert first.get("file") == str(fp)

    # Second call hits the fast cache; 'file' must still be present.
    second = analyzer.analyze_file(str(fp), "a")
    assert second.get("file") == str(fp)
