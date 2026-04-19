"""
Evolutionary Cache - stores and evolves command templates based on usage.

infrastructure/caching/evolutionary_cache.py
"""
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class CacheEntry:
    """Single cache entry with evolution metadata."""
    intent: str
    entities: Dict[str, Any]
    result: str
    success_count: int = 0
    failure_count: int = 0
    last_used: Optional[datetime] = None
    evolution_score: float = 0.0


class EvolutionaryCache:
    """
    Cache that evolves based on usage patterns.

    Unlike simple LRU cache, this tracks success/failure rates
    and prioritizes entries that work well.
    """

    def __init__(self, cache_file: Optional[Path] = None, max_size: int = 1000):
        self._cache_file = cache_file
        self._max_size = max_size
        self._entries: Dict[str, CacheEntry] = {}
        self._load()

    def _load(self) -> None:
        """Load cache from disk."""
        if self._cache_file and self._cache_file.exists():
            try:
                data = json.loads(self._cache_file.read_text())
                for key, entry_data in data.items():
                    self._entries[key] = CacheEntry(**entry_data)
            except Exception:
                pass

    def _save(self) -> None:
        """Save cache to disk."""
        if self._cache_file:
            data = {k: asdict(v) for k, v in self._entries.items()}
            self._cache_file.parent.mkdir(parents=True, exist_ok=True)
            self._cache_file.write_text(json.dumps(data, default=str, indent=2))

    def get(self, intent: str, entities: Dict[str, Any]) -> Optional[str]:
        """Get cached result if available."""
        key = self._make_key(intent, entities)
        entry = self._entries.get(key)
        if entry:
            entry.last_used = datetime.now()
            return entry.result
        return None

    def put(self, intent: str, entities: Dict[str, Any], result: str) -> None:
        """Store result in cache."""
        key = self._make_key(intent, entities)
        if key in self._entries:
            self._entries[key].result = result
            self._entries[key].last_used = datetime.now()
        else:
            if len(self._entries) >= self._max_size:
                self._evict_worst()
            self._entries[key] = CacheEntry(
                intent=intent,
                entities=entities,
                result=result,
                last_used=datetime.now()
            )
        self._save()

    def report_success(self, intent: str, entities: Dict[str, Any]) -> None:
        """Report successful command execution."""
        key = self._make_key(intent, entities)
        if key in self._entries:
            self._entries[key].success_count += 1
            self._entries[key].evolution_score = self._calculate_score(self._entries[key])
            self._save()

    def report_failure(self, intent: str, entities: Dict[str, Any]) -> None:
        """Report failed command execution."""
        key = self._make_key(intent, entities)
        if key in self._entries:
            self._entries[key].failure_count += 1
            self._entries[key].evolution_score = self._calculate_score(self._entries[key])
            self._save()

    def _make_key(self, intent: str, entities: Dict[str, Any]) -> str:
        """Create cache key from intent and entities."""
        entity_str = json.dumps(entities, sort_keys=True)
        return f"{intent}:{hash(entity_str)}"

    def _calculate_score(self, entry: CacheEntry) -> float:
        """Calculate evolution score based on success rate and recency."""
        total = entry.success_count + entry.failure_count
        if total == 0:
            return 0.5
        success_rate = entry.success_count / total
        recency_boost = 0.0
        if entry.last_used:
            days_since = (datetime.now() - entry.last_used).days
            recency_boost = max(0, 0.1 - days_since * 0.01)
        return success_rate + recency_boost

    def _evict_worst(self) -> None:
        """Remove lowest-scored entry when cache is full."""
        if not self._entries:
            return
        worst_key = min(self._entries.keys(),
                        key=lambda k: self._entries[k].evolution_score)
        del self._entries[worst_key]
