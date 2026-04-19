"""Memory-efficient streaming cache with LRU eviction."""

import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from code2llm.core.file_cache import make_cache_key


class StreamingFileCache:
    """Memory-efficient cache with LRU eviction."""
    
    def __init__(self, max_size: int = 100, cache_dir: str = ".code2llm_cache"):
        self.max_size = max_size
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, tuple] = {}
        self._access_order: List[str] = []
    
    def _get_cache_key(self, file_path: str, content: str) -> str:
        return make_cache_key(file_path, content)
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache is full."""
        while len(self._memory_cache) >= self.max_size:
            if self._access_order:
                oldest = self._access_order.pop(0)
                if oldest in self._memory_cache:
                    del self._memory_cache[oldest]
    
    def get(self, file_path: str, content: str) -> Optional[Tuple[ast.AST, str]]:
        """Get from cache with LRU tracking."""
        key = self._get_cache_key(file_path, content)
        
        if key in self._memory_cache:
            # Move to end (most recently used)
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            return self._memory_cache[key]
        
        return None
    
    def put(self, file_path: str, content: str, data: Tuple[ast.AST, str]) -> None:
        """Store in cache with LRU management."""
        self._evict_if_needed()
        
        key = self._get_cache_key(file_path, content)
        self._memory_cache[key] = data
        self._access_order.append(key)
