"""Large repository analyzer with automatic chunking and size limits.

Automatically splits large repositories into smaller sub-projects based on:
1. Output size limit (256KB default for TOON files)
2. Module boundaries (examples/, tests/, src/, etc.)
3. File count thresholds
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SubProject:
    """Represents a sub-project within a larger repository."""
    name: str
    path: Path
    relative_path: str
    files: List[Tuple[str, str]]  # (file_path, module_name)
    priority: int = 0
    
    @property
    def estimated_size_kb(self) -> int:
        """Estimate output size based on file count and average metrics."""
        # Rough estimate: ~2KB per function, ~1KB per class
        # Plus overhead for structure
        file_count = len(self.files)
        base_size = file_count * 3  # 3KB per file estimate
        return base_size
    
    @property
    def file_count(self) -> int:
        return len(self.files)


class LargeRepoSplitter:
    """Splits large repositories into manageable sub-projects."""
    
    # Default subproject directories
    SUBPROJECT_DIRS = {
        'src', 'source', 'lib', 'core', 'app', 'application',
        'tests', 'test', 'testing',
        'examples', 'example', 'demo', 'demos', 'samples',
        'docs', 'documentation', 'doc',
        'scripts', 'tools', 'util', 'utils', 'utilities',
        'benchmarks', 'perf', 'performance',
        'cli', 'cmd', 'commands',
        'api', 'web', 'server', 'client',
        'frontend', 'backend', 'ui', 'gui',
    }
    
    # Size limits
    DEFAULT_SIZE_LIMIT_KB = 256
    MAX_FILES_PER_CHUNK = 50
    
    def __init__(
        self,
        size_limit_kb: int = DEFAULT_SIZE_LIMIT_KB,
        max_files_per_chunk: int = MAX_FILES_PER_CHUNK
    ):
        self.size_limit_kb = size_limit_kb
        self.max_files_per_chunk = max_files_per_chunk
        
    def detect_subprojects(self, project_path: Path) -> List[SubProject]:
        """Detect natural subproject boundaries in repository."""
        subprojects = []
        root_files = []
        
        # First pass: look for known subproject directories
        for entry in project_path.iterdir():
            if not entry.is_dir():
                continue
                
            dir_name = entry.name.lower()
            
            # Skip hidden and cache directories
            if dir_name.startswith('.') or dir_name in {'__pycache__', 'node_modules', 'venv', '.venv'}:
                continue
            
            # Check if it's a known subproject directory
            if dir_name in self.SUBPROJECT_DIRS or self._is_python_package(entry):
                files = self._collect_files_in_dir(entry, project_path)
                if files:
                    subprojects.append(SubProject(
                        name=entry.name,
                        path=entry,
                        relative_path=str(entry.relative_to(project_path)),
                        files=files,
                        priority=self._calculate_priority(entry.name, files)
                    ))
        
        # Collect root-level files (not in any subproject)
        root_files = self._collect_root_files(project_path, subprojects)
        if root_files:
            subprojects.append(SubProject(
                name='root',
                path=project_path,
                relative_path='.',
                files=root_files,
                priority=100  # High priority for root
            ))
        
        # Sort by priority (highest first)
        subprojects.sort(key=lambda x: x.priority, reverse=True)
        
        return subprojects
    
    def _is_python_package(self, path: Path) -> bool:
        """Check if directory is a Python package."""
        return (path / '__init__.py').exists() or len(list(path.glob('*.py'))) > 0
    
    def _collect_files_in_dir(
        self,
        dir_path: Path,
        project_path: Path
    ) -> List[Tuple[str, str]]:
        """Collect Python files in a directory."""
        files = []
        
        for py_file in dir_path.rglob("*.py"):
            file_str = str(py_file)
            
            # Skip test files and cache
            if self._should_skip_file(file_str):
                continue
            
            # Calculate module name
            rel_path = py_file.relative_to(project_path)
            parts = list(rel_path.parts)[:-1]
            if py_file.name == '__init__.py':
                module_name = '.'.join(parts) if parts else dir_path.name
            else:
                module_name = '.'.join(parts + [py_file.stem])
            
            files.append((file_str, module_name))
        
        return files
    
    def _collect_root_files(
        self,
        project_path: Path,
        subprojects: List[SubProject]
    ) -> List[Tuple[str, str]]:
        """Collect files at root level not in any subproject."""
        subproject_paths = {sp.path for sp in subprojects}
        files = []
        
        for py_file in project_path.glob("*.py"):
            file_str = str(py_file)
            
            if self._should_skip_file(file_str):
                continue
            
            # Check if file is inside any subproject directory
            is_in_subproject = any(
                str(py_file).startswith(str(sp_path))
                for sp_path in subproject_paths
            )
            
            if not is_in_subproject:
                module_name = py_file.stem
                files.append((file_str, module_name))
        
        return files
    
    def _should_skip_file(self, file_str: str) -> bool:
        """Check if file should be skipped."""
        lower_path = file_str.lower()
        skip_patterns = [
            'test', '_test', 'conftest',
            '__pycache__', '.venv', 'venv',
            'node_modules', '.git',
        ]
        return any(pattern in lower_path for pattern in skip_patterns)
    
    def _calculate_priority(self, name: str, files: List) -> int:
        """Calculate priority for subproject ordering."""
        name_lower = name.lower()
        
        # Core code has highest priority
        if name_lower in {'src', 'source', 'lib', 'core', 'app'}:
            return 100
        
        # API/CLI next
        if name_lower in {'api', 'cli', 'cmd', 'commands', 'server'}:
            return 80
        
        # Tools and utilities
        if name_lower in {'utils', 'util', 'tools', 'scripts'}:
            return 60
        
        # Documentation
        if name_lower in {'docs', 'doc'}:
            return 40
        
        # Examples and tests lower priority
        if name_lower in {'examples', 'example', 'demo', 'samples'}:
            return 20
        
        if name_lower in {'tests', 'test', 'testing'}:
            return 10
        
        return 50  # Default
    
    def chunk_large_subproject(self, subproject: SubProject) -> List[SubProject]:
        """Split a large subproject into smaller chunks."""
        if len(subproject.files) <= self.max_files_per_chunk:
            return [subproject]
        
        chunks = []
        files = subproject.files.copy()
        chunk_num = 1
        
        while files:
            chunk_files = files[:self.max_files_per_chunk]
            files = files[self.max_files_per_chunk:]
            
            chunks.append(SubProject(
                name=f"{subproject.name}_part{chunk_num}",
                path=subproject.path,
                relative_path=subproject.relative_path,
                files=chunk_files,
                priority=subproject.priority - chunk_num  # Lower priority for later chunks
            ))
            chunk_num += 1
        
        return chunks
    
    def get_analysis_plan(self, project_path: Path) -> List[SubProject]:
        """Get complete analysis plan for large repository."""
        subprojects = self.detect_subprojects(project_path)
        
        # Chunk large subprojects
        final_plan = []
        for sp in subprojects:
            chunks = self.chunk_large_subproject(sp)
            final_plan.extend(chunks)
        
        return final_plan


def should_use_chunking(project_path: Path, file_threshold: int = 100) -> bool:
    """Check if repository should use chunked analysis."""
    py_file_count = len(list(Path(project_path).rglob("*.py")))
    return py_file_count > file_threshold


def estimate_output_size(file_count: int, function_count: int) -> int:
    """Estimate output size in KB."""
    # TOON format: ~1KB per 3-4 functions + overhead
    base_overhead = 5  # Header, metadata
    per_function = 0.3  # ~300 bytes per function
    per_file = 0.5  # File overhead
    
    estimated_kb = base_overhead + (function_count * per_function) + (file_count * per_file)
    return int(estimated_kb)
