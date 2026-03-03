"""Large repository analyzer with hierarchical chunking.

Splitting strategy:
1. Check total project size
2. Split by level 1 folders first
3. If level 1 folder >256KB, split by level 2 subfolders
4. If still too big, use file count chunking
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class SubProject:
    """Represents a sub-project within a larger repository."""
    name: str
    path: Path
    relative_path: str
    files: List[Tuple[str, str]] = field(default_factory=list)  # (file_path, module_name)
    level: int = 1  # Nesting level (1=root dirs, 2=subdirs)
    priority: int = 0
    
    @property
    def estimated_size_kb(self) -> int:
        """Estimate output size based on file count."""
        # Rough estimate: ~3KB per file in TOON format
        file_count = len(self.files)
        return max(1, file_count * 3)
    
    @property
    def file_count(self) -> int:
        return len(self.files)


class HierarchicalRepoSplitter:
    """Splits large repositories using hierarchical approach.
    
    Strategy:
    1. First pass: level 1 folders
    2. If any level 1 folder > limit, split into level 2 subfolders
    3. Continue until all chunks under limit
    """
    
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
        
    def get_analysis_plan(self, project_path: Path) -> List[SubProject]:
        """Get complete hierarchical analysis plan.
        
        Returns list of subprojects respecting size limits.
        """
        # First, check total project
        total_files = self._count_py_files(project_path)
        total_estimated_kb = total_files * 3
        
        if total_estimated_kb <= self.size_limit_kb:
            # Small project - analyze as single unit
            files = self._collect_files_recursive(project_path, project_path)
            return [SubProject(
                name='root',
                path=project_path,
                relative_path='.',
                files=files,
                level=0,
                priority=100
            )]
        
        # Large project - need hierarchical splitting
        return self._split_hierarchically(project_path)
    
    def _split_hierarchically(self, project_path: Path) -> List[SubProject]:
        """Split project hierarchically by level 1, then level 2 if needed."""
        subprojects = []
        
        # First pass: level 1 directories
        level1_dirs = self._get_level1_dirs(project_path)
        
        for dir_path in level1_dirs:
            files = self._collect_files_in_dir(dir_path, project_path)
            if not files:
                continue
                
            estimated_kb = len(files) * 3
            
            if estimated_kb <= self.size_limit_kb:
                # Level 1 dir fits in limit
                subprojects.append(SubProject(
                    name=dir_path.name,
                    path=dir_path,
                    relative_path=str(dir_path.relative_to(project_path)),
                    files=files,
                    level=1,
                    priority=self._calculate_priority(dir_path.name, 1)
                ))
            else:
                # Level 1 too big - split into level 2
                level2_chunks = self._split_level2(dir_path, project_path)
                subprojects.extend(level2_chunks)
        
        # Add root-level files
        root_files = self._collect_root_files(project_path)
        if root_files:
            subprojects.append(SubProject(
                name='root',
                path=project_path,
                relative_path='.',
                files=root_files,
                level=0,
                priority=100
            ))
        
        # Sort by priority (highest first)
        subprojects.sort(key=lambda x: x.priority, reverse=True)
        
        return subprojects
    
    def _get_level1_dirs(self, project_path: Path) -> List[Path]:
        """Get all level 1 directories (excluding hidden/cache)."""
        dirs = []
        
        for entry in project_path.iterdir():
            if not entry.is_dir():
                continue
            
            dir_name = entry.name.lower()
            
            # Skip hidden and cache directories
            skip_dirs = {
                '.git', '.github', '.vscode', '.idea',
                '__pycache__', 'node_modules', '.venv', 'venv', 'fresh_env', 'test-env',
                '.tox', '.pytest_cache', '.mypy_cache',
                'build', 'dist', 'egg-info', '.eggs',
                'htmlcov', '.coverage', '.cache',
                'lib', 'lib64', 'site-packages', 'include', 'bin', 'share',  # venv internals
            }
            
            if dir_name.startswith('.') or dir_name in skip_dirs:
                continue
            
            # Check if directory contains Python files
            if self._contains_python_files(entry):
                dirs.append(entry)
        
        return sorted(dirs, key=lambda d: d.name.lower())
    
    def _split_level2(self, level1_path: Path, project_path: Path) -> List[SubProject]:
        """Split level 1 directory into level 2 subdirectories with merging."""
        chunks = []
        
        # Get and categorize subdirectories
        small_dirs, large_dirs = self._categorize_subdirs(level1_path, project_path)
        
        # Process large directories (need file-level chunking)
        chunks.extend(self._process_large_dirs(large_dirs, level1_path, project_path))
        
        # Merge and process small directories
        if small_dirs:
            chunks.extend(self._merge_small_dirs(small_dirs, level1_path, project_path))
        
        # Process files directly in level1
        chunks.extend(self._process_level1_files(level1_path, project_path))
        
        return chunks
    
    def _categorize_subdirs(
        self, level1_path: Path, project_path: Path
    ) -> Tuple[List, List]:
        """Categorize subdirectories into small and large based on size."""
        level2_dirs = [d for d in level1_path.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
        level2_dirs.sort(key=lambda d: self._calculate_priority(d.name, 2), reverse=True)
        
        small_dirs = []
        large_dirs = []
        
        for dir_path in level2_dirs:
            files = self._collect_files_in_dir(dir_path, project_path)
            if not files:
                continue
            
            estimated_kb = len(files) * 3
            priority = self._calculate_priority(dir_path.name, 2)
            
            if estimated_kb > self.size_limit_kb:
                large_dirs.append((dir_path, files, estimated_kb, priority))
            else:
                small_dirs.append((dir_path, files, estimated_kb, priority))
        
        return small_dirs, large_dirs
    
    def _process_large_dirs(
        self, large_dirs: List, level1_path: Path, project_path: Path
    ) -> List[SubProject]:
        """Process large directories with file-level chunking."""
        chunks = []
        for dir_path, files, estimated_kb, priority in large_dirs:
            file_chunks = self._chunk_by_files(
                files, level1_path.name, dir_path.name, 
                dir_path, project_path
            )
            chunks.extend(file_chunks)
        return chunks
    
    def _process_level1_files(self, level1_path: Path, project_path: Path) -> List[SubProject]:
        """Process Python files directly in level1 directory."""
        chunks = []
        
        level1_direct_files = [
            (str(f), f"{level1_path.name}.{f.stem}")
            for f in level1_path.glob("*.py")
            if not self._should_skip_file(str(f))
        ]
        
        if not level1_direct_files:
            return chunks
        
        estimated_kb = len(level1_direct_files) * 3
        
        if estimated_kb <= self.size_limit_kb:
            chunks.append(SubProject(
                name=f"{level1_path.name}._root",
                path=level1_path,
                relative_path=str(level1_path.relative_to(project_path)),
                files=level1_direct_files,
                level=2,
                priority=self._calculate_priority(level1_path.name, 2) - 10
            ))
        else:
            file_chunks = self._chunk_by_files(
                level1_direct_files, level1_path.name, "_root",
                level1_path, project_path
            )
            chunks.extend(file_chunks)
        
        return chunks
    
    def _merge_small_dirs(
        self,
        small_dirs: List[Tuple[Path, List, int, int]],
        level1_path: Path,
        project_path: Path
    ) -> List[SubProject]:
        """Merge small subdirectories into combined chunks up to size limit."""
        chunks = []
        
        # Sort by priority (highest first)
        small_dirs.sort(key=lambda x: x[3], reverse=True)
        
        current_chunk_files = []
        current_chunk_names = []
        current_size = 0
        
        for dir_path, files, estimated_kb, priority in small_dirs:
            # Check if adding this dir would exceed limit
            if current_chunk_files and (current_size + estimated_kb > self.size_limit_kb):
                # Flush current chunk
                chunk_name = f"{level1_path.name}.{'_'.join(current_chunk_names)}"
                if len(current_chunk_names) > 3:
                    chunk_name = f"{level1_path.name}.batch_{len(chunks)+1}"
                
                chunks.append(SubProject(
                    name=chunk_name,
                    path=level1_path,
                    relative_path=str(level1_path.relative_to(project_path)),
                    files=current_chunk_files.copy(),
                    level=2,
                    priority=priority
                ))
                
                # Start new chunk
                current_chunk_files = []
                current_chunk_names = []
                current_size = 0
            
            # Add to current chunk
            current_chunk_files.extend(files)
            current_chunk_names.append(dir_path.name)
            current_size += estimated_kb
        
        # Flush remaining chunk
        if current_chunk_files:
            chunk_name = f"{level1_path.name}.{'_'.join(current_chunk_names)}"
            if len(current_chunk_names) > 3:
                chunk_name = f"{level1_path.name}.batch_{len(chunks)+1}"
            
            chunks.append(SubProject(
                name=chunk_name,
                path=level1_path,
                relative_path=str(level1_path.relative_to(project_path)),
                files=current_chunk_files,
                level=2,
                priority=30  # Default priority for merged batch
            ))
        
        return chunks
    
    def _chunk_by_files(
        self,
        files: List[Tuple[str, str]],
        level1_name: str,
        level2_name: str,
        path: Path,
        project_path: Path
    ) -> List[SubProject]:
        """Chunk large file list by max_files_per_chunk."""
        chunks = []
        chunk_num = 1
        
        remaining_files = files.copy()
        
        while remaining_files:
            chunk_files = remaining_files[:self.max_files_per_chunk]
            remaining_files = remaining_files[self.max_files_per_chunk:]
            
            chunks.append(SubProject(
                name=f"{level1_name}.{level2_name}_part{chunk_num}",
                path=path,
                relative_path=str(path.relative_to(project_path)),
                files=chunk_files,
                level=3,
                priority=30 - chunk_num  # Lower priority for chunked parts
            ))
            chunk_num += 1
        
        return chunks
    
    def _collect_files_in_dir(
        self,
        dir_path: Path,
        project_path: Path
    ) -> List[Tuple[str, str]]:
        """Collect Python files recursively in a directory."""
        files = []
        
        for py_file in dir_path.rglob("*.py"):
            file_str = str(py_file)
            
            if self._should_skip_file(file_str):
                continue
            
            # Calculate module name
            try:
                rel_path = py_file.relative_to(project_path)
                parts = list(rel_path.parts)[:-1]
                
                if py_file.name == '__init__.py':
                    module_name = '.'.join(parts) if parts else dir_path.name
                else:
                    module_name = '.'.join(parts + [py_file.stem])
                
                files.append((file_str, module_name))
            except ValueError:
                # File not relative to project_path
                files.append((file_str, py_file.stem))
        
        return files
    
    def _collect_files_recursive(
        self,
        dir_path: Path,
        project_path: Path
    ) -> List[Tuple[str, str]]:
        """Collect all Python files recursively."""
        return self._collect_files_in_dir(dir_path, project_path)
    
    def _collect_root_files(self, project_path: Path) -> List[Tuple[str, str]]:
        """Collect Python files at root level."""
        files = []
        
        for py_file in project_path.glob("*.py"):
            file_str = str(py_file)
            
            if self._should_skip_file(file_str):
                continue
            
            module_name = py_file.stem
            files.append((file_str, module_name))
        
        return files
    
    def _count_py_files(self, path: Path) -> int:
        """Count Python files (excluding tests/cache)."""
        count = 0
        for py_file in path.rglob("*.py"):
            if not self._should_skip_file(str(py_file)):
                count += 1
        return count
    
    def _contains_python_files(self, dir_path: Path) -> bool:
        """Check if directory contains any Python files."""
        for py_file in dir_path.rglob("*.py"):
            if not self._should_skip_file(str(py_file)):
                return True
        return False
    
    def _should_skip_file(self, file_str: str) -> bool:
        """Check if file should be skipped."""
        lower_path = file_str.lower()
        skip_patterns = [
            'test', '_test', 'conftest',
            '__pycache__', '.venv', 'venv', 'fresh_env', 'test-env',
            'node_modules', '.git',
            '/lib/', '/lib64/', '/site-packages/',  # venv internals
            '/include/', '/bin/python', '/share/',
        ]
        return any(pattern in lower_path for pattern in skip_patterns)
    
    def _calculate_priority(self, name: str, level: int) -> int:
        """Calculate priority based on name and nesting level.
        
        Higher priority = analyzed first
        """
        name_lower = name.lower()
        base_priority = 50
        
        # Core code
        if name_lower in {'src', 'source', 'lib', 'core', 'app', 'application'}:
            base_priority = 100
        elif name_lower in {'api', 'cli', 'cmd', 'commands', 'server', 'backend'}:
            base_priority = 80
        elif name_lower in {'utils', 'util', 'tools', 'scripts'}:
            base_priority = 60
        elif name_lower in {'docs', 'doc', 'documentation'}:
            base_priority = 40
        elif name_lower in {'examples', 'example', 'demo', 'demos', 'samples'}:
            base_priority = 30
        elif name_lower in {'tests', 'test', 'testing'}:
            base_priority = 20
        
        # Deeper nesting = slightly lower priority
        level_penalty = level * 5
        
        return base_priority - level_penalty


def should_use_chunking(project_path: Path, size_threshold_kb: int = 256) -> bool:
    """Check if repository should use chunked analysis.
    
    Estimates size based on file count.
    """
    splitter = HierarchicalRepoSplitter(size_limit_kb=size_threshold_kb)
    total_files = splitter._count_py_files(project_path)
    estimated_kb = total_files * 3
    return estimated_kb > size_threshold_kb


def get_analysis_plan(project_path: Path, size_limit_kb: int = 256) -> List[SubProject]:
    """Get analysis plan for project (auto-detect if chunking needed)."""
    splitter = HierarchicalRepoSplitter(size_limit_kb=size_limit_kb)
    return splitter.get_analysis_plan(project_path)


# Backward compatibility
LargeRepoSplitter = HierarchicalRepoSplitter
