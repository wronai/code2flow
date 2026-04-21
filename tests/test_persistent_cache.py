"""Tests for PersistentCache."""

import json
import os
import time
import tempfile
from pathlib import Path

import pytest

from code2llm.core.persistent_cache import PersistentCache, get_all_projects, clear_all, VERSION


@pytest.fixture()
def tmp_project(tmp_path):
    """A temporary project directory with a few source files."""
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    (tmp_path / "b.py").write_text("def bar(): pass\n")
    return tmp_path


@pytest.fixture()
def cache(tmp_project, tmp_path):
    """PersistentCache pointing at a separate temp cache root."""
    cache_root = tmp_path / "cache_root"
    return PersistentCache(str(tmp_project), cache_root=str(cache_root))


class TestContentHash:
    def test_same_content_same_hash(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        assert cache.content_hash(fp) == cache.content_hash(fp)

    def test_different_content_different_hash(self, tmp_project, cache):
        a = str(tmp_project / "a.py")
        b = str(tmp_project / "b.py")
        assert cache.content_hash(a) != cache.content_hash(b)


class TestFileResultRoundtrip:
    def test_put_then_get(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        payload = {"functions": {"foo": {"cc": 1}}, "file": fp}
        cache.put_file_result(fp, payload)
        retrieved = cache.get_file_result(fp)
        assert retrieved == payload

    def test_get_missing_returns_none(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        assert cache.get_file_result(fp) is None

    def test_manifest_updated_after_put(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        rel = os.path.relpath(fp, str(tmp_project))
        assert rel in cache._manifest["files"]

    def test_put_dataclass_payload(self, tmp_project, cache):
        """Regression: real analyzer results contain ModuleInfo/FunctionInfo
        dataclasses. The serializer must round-trip them — otherwise
        put_file_result silently fails and the manifest never grows, which
        in turn collapses the export-cache run-hash to md5("{}").
        """
        from code2llm.core.models import ModuleInfo, FunctionInfo

        fp = str(tmp_project / "a.py")
        payload = {
            "module": ModuleInfo(name="a", file=fp, is_package=False),
            "functions": {"a.foo": FunctionInfo(name="foo", qualified_name="a.foo", file=fp, line=1)},
            "classes": {},
            "nodes": {},
            "edges": [],
            "file": fp,
        }
        cache.put_file_result(fp, payload)
        rel = os.path.relpath(fp, str(tmp_project))
        assert rel in cache._manifest["files"], (
            "put_file_result must succeed on real analyzer payloads "
            "containing dataclasses (regression for msgpack serialization bug)"
        )
        retrieved = cache.get_file_result(fp)
        assert retrieved["module"].name == "a"
        assert "a.foo" in retrieved["functions"]


class TestAutoCleanup:
    def test_fresh_cache_no_removal(self, tmp_project, cache):
        """Nothing to clean on a fresh cache."""
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed == {"exports": 0, "files": 0}

    def test_stale_export_removed(self, tmp_project, cache):
        """Exports whose _complete stamp is older than TTL are purged."""
        d = cache.create_export_cache_dir({"fmt": "toon"})
        cache.mark_export_complete(d)
        # Back-date the _complete stamp by 2 days
        old_ts = time.time() - 2 * 86400
        (d / "_complete").write_text(str(old_ts))
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["exports"] == 1
        assert not d.exists()

    def test_fresh_export_kept(self, tmp_project, cache):
        """Exports younger than TTL survive cleanup."""
        d = cache.create_export_cache_dir({"fmt": "toon"})
        cache.mark_export_complete(d)
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["exports"] == 0
        assert d.exists()

    def test_abandoned_export_removed(self, tmp_project, cache):
        """Export dirs without _complete stamp are cleaned based on mtime."""
        d = cache.create_export_cache_dir({"fmt": "toon"})
        # Back-date the directory mtime
        old_ts = time.time() - 2 * 86400
        os.utime(d, (old_ts, old_ts))
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["exports"] == 1
        assert not d.exists()

    def test_referenced_file_entry_kept_even_if_old(self, tmp_project, cache):
        """File cache entries referenced by the manifest survive TTL cleanup."""
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        pkl_files = list(cache._files_dir.iterdir())
        assert pkl_files, "put_file_result should have created a cache file"
        # Back-date the pkl mtime
        old_ts = time.time() - 30 * 86400
        for p in pkl_files:
            os.utime(p, (old_ts, old_ts))
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["files"] == 0, "referenced entries must not be removed"
        assert all(p.exists() for p in pkl_files)

    def test_orphan_file_entry_removed(self, tmp_project, cache):
        """Orphaned file cache entries older than TTL are removed."""
        # Create a fake orphan pkl file
        orphan = cache._files_dir / "deadbeef12345678.pkl"
        orphan.write_bytes(b"x")
        old_ts = time.time() - 2 * 86400
        os.utime(orphan, (old_ts, old_ts))
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["files"] == 1
        assert not orphan.exists()

    def test_orphan_file_entry_kept_if_fresh(self, tmp_project, cache):
        """Orphan but fresh entries survive (might be in-flight writes)."""
        orphan = cache._files_dir / "cafebabe12345678.pkl"
        orphan.write_bytes(b"x")
        removed = cache.auto_cleanup(ttl_days=1.0)
        assert removed["files"] == 0
        assert orphan.exists()

    def test_auto_cleanup_triggered_on_init(self, tmp_project, tmp_path):
        """Fresh __init__ runs auto_cleanup (removes stale exports)."""
        cache_root = tmp_path / "cache_root"
        c1 = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        d = c1.create_export_cache_dir({"fmt": "toon"})
        c1.mark_export_complete(d)
        # Back-date
        old_ts = time.time() - 5 * 86400
        (d / "_complete").write_text(str(old_ts))
        # New instance should auto-clean
        PersistentCache(str(tmp_project), cache_root=str(cache_root))
        assert not d.exists(), "auto_cleanup should have removed stale export on init"

    def test_env_var_disables_auto_cleanup(self, tmp_project, tmp_path, monkeypatch):
        """CODE2LLM_AUTO_CLEANUP=0 disables the init-time cleanup."""
        cache_root = tmp_path / "cache_root"
        c1 = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        d = c1.create_export_cache_dir({"fmt": "toon"})
        c1.mark_export_complete(d)
        old_ts = time.time() - 5 * 86400
        (d / "_complete").write_text(str(old_ts))

        monkeypatch.setenv("CODE2LLM_AUTO_CLEANUP", "0")
        PersistentCache(str(tmp_project), cache_root=str(cache_root))
        assert d.exists(), "auto_cleanup should have been skipped"

    def test_env_var_sets_ttl(self, tmp_project, tmp_path, monkeypatch):
        """CODE2LLM_CACHE_TTL_DAYS=0.5 makes 1-day-old exports stale."""
        cache_root = tmp_path / "cache_root"
        c1 = PersistentCache(
            str(tmp_project), cache_root=str(cache_root), auto_cleanup=False
        )
        d = c1.create_export_cache_dir({"fmt": "toon"})
        c1.mark_export_complete(d)
        # 1 day old — within default (1d) but outside 0.5d
        old_ts = time.time() - 86400
        (d / "_complete").write_text(str(old_ts))

        monkeypatch.setenv("CODE2LLM_CACHE_TTL_DAYS", "0.5")
        PersistentCache(str(tmp_project), cache_root=str(cache_root))
        assert not d.exists(), "TTL=0.5d should have removed 1-day-old export"


class TestPruneMissing:
    def test_no_entries_no_op(self, tmp_project, cache):
        assert cache.prune_missing([str(tmp_project / "a.py")]) == []

    def test_removes_vanished_entries(self, tmp_project, cache):
        a = str(tmp_project / "a.py")
        b = str(tmp_project / "b.py")
        cache.put_file_result(a, {"file": a})
        cache.put_file_result(b, {"file": b})
        # simulate b.py being deleted from the project
        removed = cache.prune_missing([a])
        assert removed == ["b.py"]
        assert "b.py" not in cache._manifest["files"]
        assert "a.py" in cache._manifest["files"]

    def test_pruning_changes_run_hash(self, tmp_project, cache):
        """Regression: deleting a file must invalidate the export cache key."""
        a = str(tmp_project / "a.py")
        b = str(tmp_project / "b.py")
        cache.put_file_result(a, {"file": a})
        cache.put_file_result(b, {"file": b})
        hash_before = cache._compute_run_hash({"fmt": "toon"})
        cache.prune_missing([a])  # b deleted
        hash_after = cache._compute_run_hash({"fmt": "toon"})
        assert hash_before != hash_after, (
            "prune_missing must change the run hash so deleted files "
            "invalidate cached exports"
        )

    def test_pruning_sets_dirty_flag(self, tmp_project, cache):
        a = str(tmp_project / "a.py")
        cache.put_file_result(a, {"file": a})
        cache.save()
        assert cache._dirty is False
        cache.prune_missing([])  # a is now "deleted"
        assert cache._dirty is True


class TestGetChangedFiles:
    def test_new_files_are_changed(self, tmp_project, cache):
        files = [str(tmp_project / "a.py"), str(tmp_project / "b.py")]
        changed, cached = cache.get_changed_files(files)
        assert set(changed) == set(files)
        assert cached == []

    def test_cached_file_not_changed(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        changed, cached = cache.get_changed_files([fp])
        assert changed == []
        assert cached == [fp]

    def test_modified_file_is_changed(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        # Modify content
        time.sleep(0.01)
        Path(fp).write_text("def foo(): return 42\n")
        changed, cached = cache.get_changed_files([fp])
        assert fp in changed
        assert fp not in cached


class TestExportCache:
    def test_missing_export_returns_none(self, cache):
        assert cache.get_export_cache_dir({"fmt": "toon"}) is None

    def test_complete_export_returned(self, tmp_project, cache):
        # Populate manifest so export cache is allowed (see empty-manifest guard)
        cache.put_file_result(str(tmp_project / "a.py"), {"file": str(tmp_project / "a.py")})
        cfg = {"fmt": "toon", "verbose": False}
        d = cache.create_export_cache_dir(cfg)
        assert cache.get_export_cache_dir(cfg) is None  # not complete yet
        cache.mark_export_complete(d)
        assert cache.get_export_cache_dir(cfg) == d

    def test_different_config_different_dir(self, cache):
        d1 = cache.create_export_cache_dir({"fmt": "toon"})
        d2 = cache.create_export_cache_dir({"fmt": "json"})
        assert d1 != d2

    def test_empty_manifest_refuses_cache_hit(self, cache):
        """Regression: when the per-file manifest is empty, the run-hash
        collapses to md5("{}") and would otherwise propagate stale exports
        across unrelated runs (e.g. after upgrading code2llm).
        """
        cfg = {"fmt": "toon"}
        d = cache.create_export_cache_dir(cfg)
        cache.mark_export_complete(d)
        # Manifest still empty -> must NOT return a cache hit
        assert cache._manifest["files"] == {}
        assert cache.get_export_cache_dir(cfg) is None

    def test_populated_manifest_allows_cache_hit(self, tmp_project, cache):
        """Once the per-file manifest is populated, export caching works."""
        cfg = {"fmt": "toon"}
        d = cache.create_export_cache_dir(cfg)
        cache.mark_export_complete(d)
        cache.put_file_result(str(tmp_project / "a.py"), {"file": str(tmp_project / "a.py")})
        # After populating the manifest the run-hash changes, so the old
        # _complete export dir is no longer valid either.
        assert cache.get_export_cache_dir(cfg) is None
        # Mark the *new* run hash complete -> then a hit is allowed.
        d2 = cache.create_export_cache_dir(cfg)
        cache.mark_export_complete(d2)
        assert cache.get_export_cache_dir(cfg) == d2


class TestSaveAndReload:
    def test_save_creates_manifest(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        cache.save()
        assert cache._manifest_path.exists()

    def test_reload_preserves_entries(self, tmp_project, tmp_path):
        cache_root = tmp_path / "cache_root"
        fp = str(tmp_project / "a.py")
        c1 = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        c1.put_file_result(fp, {"file": fp, "data": 42})
        c1.save()

        c2 = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        result = c2.get_file_result(fp)
        assert result == {"file": fp, "data": 42}

    def test_version_mismatch_resets_manifest(self, tmp_project, tmp_path):
        cache_root = tmp_path / "cache_root"
        proj_hash = __import__('hashlib').md5(
            os.path.realpath(str(tmp_project)).encode()
        ).hexdigest()[:12]
        manifest_path = cache_root / "projects" / proj_hash / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({"version": 0, "files": {"stale": {}}}))

        c = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        assert c._manifest.get("version") == VERSION
        assert c._manifest["files"] == {}


class TestGC:
    def test_gc_removes_old_exports(self, tmp_project, cache):
        cfg = {"fmt": "toon"}
        d = cache.create_export_cache_dir(cfg)
        # Backdate _complete timestamp
        (d / "_complete").write_text(str(time.time() - 40 * 86400))
        removed = cache.gc(max_age_days=30)
        assert removed >= 1
        assert not d.exists()

    def test_gc_keeps_recent_exports(self, tmp_project, cache):
        cfg = {"fmt": "toon"}
        d = cache.create_export_cache_dir(cfg)
        cache.mark_export_complete(d)
        removed = cache.gc(max_age_days=30)
        assert removed == 0
        assert d.exists()


class TestClear:
    def test_clear_empties_manifest(self, tmp_project, cache):
        fp = str(tmp_project / "a.py")
        cache.put_file_result(fp, {"file": fp})
        cache.clear()
        assert cache._manifest["files"] == {}
        assert cache.get_file_result(fp) is None


class TestModuleLevelHelpers:
    def test_get_all_projects_empty(self, tmp_path):
        projects = get_all_projects(cache_root=str(tmp_path))
        assert projects == []

    def test_get_all_projects_after_save(self, tmp_project, tmp_path):
        cache_root = tmp_path / "root"
        c = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        fp = str(tmp_project / "a.py")
        c.put_file_result(fp, {"file": fp})
        c.save()
        projects = get_all_projects(cache_root=str(cache_root))
        assert len(projects) == 1
        assert projects[0]["project"] == os.path.realpath(str(tmp_project))

    def test_clear_all(self, tmp_project, tmp_path):
        cache_root = tmp_path / "root"
        c = PersistentCache(str(tmp_project), cache_root=str(cache_root))
        c.put_file_result(str(tmp_project / "a.py"), {"x": 1})
        c.save()
        clear_all(cache_root=str(cache_root))
        assert not cache_root.exists()
