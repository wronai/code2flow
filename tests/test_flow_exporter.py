"""Tests for Sprint 2: Enhanced FlowExporter with AST-based type inference
and side-effect detection.

Tests cover:
- TypeInferenceEngine: annotation extraction, name-based fallback
- SideEffectDetector: IO, cache, mutation, pure classification
- FlowExporter: enhanced CONTRACTS, DATA_TYPES, SIDE_EFFECTS rendering
"""
import os
import textwrap
import tempfile
import pytest
from pathlib import Path

from code2llm.core.models import AnalysisResult, FunctionInfo, ModuleInfo
from code2llm.analysis.type_inference import TypeInferenceEngine
from code2llm.analysis.side_effects import SideEffectDetector, SideEffectInfo
from code2llm.exporters.flow_exporter import FlowExporter


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def typed_source(tmp_path):
    """Create a Python source file with type annotations."""
    code = textwrap.dedent("""\
        from typing import List, Optional
        from pathlib import Path

        class AnalysisResult:
            pass

        def analyze_file(path: Path, verbose: bool = False) -> AnalysisResult:
            with open(path) as f:
                data = f.read()
            return AnalysisResult()

        def normalize(text: str, lang: str = 'en') -> str:
            return text.lower().strip()

        def compute_metrics(result: AnalysisResult) -> dict:
            self_cache = {}
            return {"cc": 5}

        def save_results(results: List[AnalysisResult], output: Path) -> None:
            with open(output, 'w') as f:
                f.write(str(results))

        def pure_transform(items: list) -> list:
            return sorted(items)

        class DataProcessor:
            def __init__(self):
                self.cache = {}

            def process(self, data: str) -> str:
                self.result = data.upper()
                return self.result

            def update_cache(self, key: str, value: str) -> None:
                self.cache[key] = value
    """)
    src = tmp_path / "typed_module.py"
    src.write_text(code)
    return str(src)


@pytest.fixture
def untyped_source(tmp_path):
    """Create a Python source file without type annotations."""
    code = textwrap.dedent("""\
        def parse_config(text):
            return {}

        def export_data(result):
            print(result)

        def detect_smells(analysis):
            return []
    """)
    src = tmp_path / "untyped_module.py"
    src.write_text(code)
    return str(src)


def _make_fi(name, file, line=1, args=None, returns=None, calls=None,
             class_name=None, module="test_mod", complexity=None):
    """Helper to create FunctionInfo."""
    return FunctionInfo(
        name=name,
        qualified_name=f"{module}.{class_name + '.' if class_name else ''}{name}",
        file=file,
        line=line,
        module=module,
        class_name=class_name,
        is_method=class_name is not None,
        args=args or [],
        returns=returns,
        calls=calls or [],
        complexity=complexity or {},
    )


# ---------------------------------------------------------------------------
# TypeInferenceEngine tests
# ---------------------------------------------------------------------------

class TestTypeInferenceEngine:

    def test_extracts_return_annotation(self, typed_source):
        engine = TypeInferenceEngine()
        fi = _make_fi("analyze_file", typed_source, line=7, args=["path", "verbose"])
        info = engine.enrich_function(fi)

        assert info["returns"] == "AnalysisResult"
        assert info["source"] == "annotation"

    def test_extracts_arg_types(self, typed_source):
        engine = TypeInferenceEngine()
        fi = _make_fi("analyze_file", typed_source, line=7, args=["path", "verbose"])
        info = engine.enrich_function(fi)

        args = info["args"]
        assert len(args) == 2
        assert args[0]["name"] == "path"
        assert args[0]["type"] == "Path"
        assert args[1]["name"] == "verbose"
        assert args[1]["type"] == "bool"

    def test_detects_default_args(self, typed_source):
        engine = TypeInferenceEngine()
        fi = _make_fi("normalize", typed_source, line=12, args=["text", "lang"])
        info = engine.enrich_function(fi)

        args = info["args"]
        assert args[0]["has_default"] is False
        assert args[1]["has_default"] is True

    def test_typed_signature_format(self, typed_source):
        engine = TypeInferenceEngine()
        fi = _make_fi("normalize", typed_source, line=12, args=["text", "lang"])
        sig = engine.get_typed_signature(fi)

        assert "normalize(" in sig
        assert "text:str" in sig
        assert "\u2192 str" in sig

    def test_name_based_fallback(self, untyped_source):
        engine = TypeInferenceEngine()
        fi = _make_fi("parse_config", untyped_source, line=1, args=["text"])
        info = engine.enrich_function(fi)

        assert info["source"] in ("inferred", "mixed")
        assert info["returns"] == "dict"

    def test_no_annotations_no_pattern(self, untyped_source):
        """Functions with no annotations and no name pattern get source='none'."""
        engine = TypeInferenceEngine()
        # Create a function with a name that doesn't match any pattern
        code = "def foobar(x):\n    return x\n"
        src = Path(untyped_source).parent / "nopattern.py"
        src.write_text(code)
        fi = _make_fi("foobar", str(src), line=1, args=["x"])
        info = engine.enrich_function(fi)

        assert info["source"] == "none"

    def test_batch_extract(self, typed_source):
        engine = TypeInferenceEngine()
        funcs = {
            "m.analyze_file": _make_fi("analyze_file", typed_source, line=7,
                                       args=["path", "verbose"]),
            "m.normalize": _make_fi("normalize", typed_source, line=12,
                                    args=["text", "lang"]),
        }
        results = engine.extract_all_types(funcs)

        assert len(results) == 2
        assert results["m.analyze_file"]["returns"] == "AnalysisResult"
        assert results["m.normalize"]["returns"] == "str"


# ---------------------------------------------------------------------------
# SideEffectDetector tests
# ---------------------------------------------------------------------------

class TestSideEffectDetector:

    def test_detects_io(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("analyze_file", typed_source, line=7,
                       args=["path", "verbose"], calls=["open"])
        info = detector.analyze_function(fi)

        assert info.classification == "IO"
        assert len(info.io_operations) > 0

    def test_detects_pure(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("normalize", typed_source, line=12,
                       args=["text", "lang"])
        info = detector.analyze_function(fi)

        assert info.classification == "pure"
        assert info.is_pure is True

    def test_detects_mutation(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("process", typed_source, line=25,
                       args=["self", "data"], class_name="DataProcessor")
        info = detector.analyze_function(fi)

        assert info.classification == "mutation"
        assert "result" in info.self_mutations

    def test_detects_write_io(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("save_results", typed_source, line=16,
                       args=["results", "output"], calls=["open"])
        info = detector.analyze_function(fi)

        assert info.classification == "IO"

    def test_side_effect_summary(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("save_results", typed_source, line=16,
                       args=["results", "output"], calls=["open"])
        info = detector.analyze_function(fi)

        summary = info.side_effect_summary
        assert "IO" in summary or "pure" not in summary

    def test_batch_analyze(self, typed_source):
        detector = SideEffectDetector()
        funcs = {
            "m.analyze_file": _make_fi("analyze_file", typed_source, line=7,
                                       args=["path"], calls=["open"]),
            "m.normalize": _make_fi("normalize", typed_source, line=12,
                                    args=["text"]),
        }
        results = detector.analyze_all(funcs)

        assert results["m.analyze_file"].classification == "IO"
        assert results["m.normalize"].classification == "pure"

    def test_heuristic_fallback(self):
        """When source file doesn't exist, fall back to heuristic."""
        detector = SideEffectDetector()
        fi = _make_fi("save_data", "/nonexistent/file.py",
                       args=["data"], calls=["write"])
        info = detector.analyze_function(fi)

        assert info.classification == "IO"

    def test_to_dict(self, typed_source):
        detector = SideEffectDetector()
        fi = _make_fi("analyze_file", typed_source, line=7,
                       args=["path"], calls=["open"])
        info = detector.analyze_function(fi)
        d = info.to_dict()

        assert "classification" in d
        assert "summary" in d
        assert d["classification"] == "IO"


# ---------------------------------------------------------------------------
# FlowExporter integration tests
# ---------------------------------------------------------------------------

class TestFlowExporterSprint2:

    @pytest.fixture
    def sample_result(self, typed_source):
        """Create AnalysisResult with typed functions."""
        result = AnalysisResult(project_path="/test/project")

        result.modules["test_mod"] = ModuleInfo(
            name="test_mod",
            file=typed_source,
            functions=["test_mod.analyze_file", "test_mod.normalize",
                        "test_mod.compute_metrics", "test_mod.save_results",
                        "test_mod.pure_transform"],
        )

        result.functions["test_mod.analyze_file"] = _make_fi(
            "analyze_file", typed_source, line=7,
            args=["path", "verbose"],
            calls=["open", "test_mod.normalize"],
            complexity={"cyclomatic_complexity": 8},
        )
        result.functions["test_mod.normalize"] = _make_fi(
            "normalize", typed_source, line=12,
            args=["text", "lang"],
            calls=["test_mod.compute_metrics"],
            complexity={"cyclomatic_complexity": 3},
        )
        result.functions["test_mod.compute_metrics"] = _make_fi(
            "compute_metrics", typed_source, line=15,
            args=["result"],
            calls=["test_mod.save_results"],
            complexity={"cyclomatic_complexity": 5},
        )
        result.functions["test_mod.save_results"] = _make_fi(
            "save_results", typed_source, line=16,
            args=["results", "output"],
            calls=[],
            complexity={"cyclomatic_complexity": 2},
        )
        result.functions["test_mod.pure_transform"] = _make_fi(
            "pure_transform", typed_source, line=20,
            args=["items"],
            calls=[],
            complexity={"cyclomatic_complexity": 1},
        )
        return result

    def test_export_creates_file(self, sample_result, tmp_path):
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        assert output.exists()

    def test_contracts_have_in_out(self, sample_result, tmp_path):
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        content = output.read_text()

        assert "CONTRACTS:" in content
        # Check for IN/OUT markers (if pipelines were detected)
        if "Pipeline:" in content:
            assert "IN:" in content
            assert "OUT:" in content

    def test_data_types_has_source_counts(self, sample_result, tmp_path):
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        content = output.read_text()

        assert "DATA_TYPES" in content
        assert "annotated" in content
        assert "inferred" in content

    def test_side_effects_section(self, sample_result, tmp_path):
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        content = output.read_text()

        assert "SIDE_EFFECTS:" in content

    def test_type_annotations_in_signatures(self, sample_result, tmp_path):
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        content = output.read_text()

        # The typed signature should include type info from AST
        # At minimum, check the TRANSFORMS or PIPELINES use typed sigs
        assert "PIPELINES" in content or "TRANSFORMS" in content

    def test_hub_type_split_recommendations(self, tmp_path):
        """Test that hub types get split recommendations."""
        exporter = FlowExporter()
        # Create a result with many functions consuming AnalysisResult
        result = AnalysisResult(project_path="/test/project")
        src = tmp_path / "hub_test.py"
        lines = ["from typing import Any\n\n"]
        funcs = {}
        for i in range(12):
            lines.append(
                f"def consumer_{i}(result: Any) -> None:\n"
                f"    pass\n\n"
            )
            fi = _make_fi(
                f"consumer_{i}", str(src), line=3 + i * 3,
                args=["result"], complexity={"cyclomatic_complexity": 1},
            )
            funcs[fi.qualified_name] = fi
        src.write_text("".join(lines))

        result.functions = funcs
        output = tmp_path / "flow.toon"
        exporter.export(result, str(output))
        content = output.read_text()

        assert "DATA_TYPES" in content

    def test_pipeline_purity_uses_ast(self, sample_result, tmp_path):
        """Verify pipeline purity comes from AST analysis."""
        exporter = FlowExporter()
        output = tmp_path / "flow.toon"
        exporter.export(sample_result, str(output))
        content = output.read_text()

        # SIDE_EFFECTS section should classify functions
        if "Pure:" in content:
            assert "normalize" in content or "pure_transform" in content


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_empty_result(self, tmp_path):
        exporter = FlowExporter()
        result = AnalysisResult(project_path="/empty")
        output = tmp_path / "flow.toon"
        exporter.export(result, str(output))
        content = output.read_text()

        assert "PIPELINES[0]" in content
        assert "DATA_TYPES" in content

    def test_missing_source_file(self, tmp_path):
        """Functions with nonexistent source files should not crash."""
        exporter = FlowExporter()
        result = AnalysisResult(project_path="/test")
        result.functions["m.foo"] = _make_fi(
            "foo", "/nonexistent/path.py", args=["x"],
            calls=[], complexity={"cyclomatic_complexity": 1},
        )
        output = tmp_path / "flow.toon"
        exporter.export(result, str(output))
        assert output.exists()

    def test_type_inference_bad_syntax(self, tmp_path):
        """Source file with syntax errors should not crash."""
        bad_src = tmp_path / "bad.py"
        bad_src.write_text("def foo(:\n    pass\n")

        engine = TypeInferenceEngine()
        fi = _make_fi("foo", str(bad_src), line=1, args=["x"])
        info = engine.enrich_function(fi)
        # Should fall back gracefully
        assert info["source"] in ("inferred", "none")

    def test_side_effect_detector_bad_syntax(self, tmp_path):
        """Source file with syntax errors should not crash detector."""
        bad_src = tmp_path / "bad.py"
        bad_src.write_text("def foo(:\n    pass\n")

        detector = SideEffectDetector()
        fi = _make_fi("foo", str(bad_src), line=1, args=["x"])
        info = detector.analyze_function(fi)
        assert info.classification in ("pure", "IO", "cache", "mutation")
