"""
Entity Preparation - converts raw entities to command-specific format.

domain/command_generation/entities/preparer.py
"""
from typing import Dict, Any, Protocol
from abc import ABC, abstractmethod


class EntityPreparer(Protocol):
    """Protocol for domain-specific entity preparation."""

    def supports(self, intent: str) -> bool: ...
    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]: ...


class ShellEntityPreparer:
    """Prepares entities for shell commands."""

    SUPPORTED_PREFIXES = ('shell_', 'find_', 'grep_', 'awk_')

    def supports(self, intent: str) -> bool:
        return any(intent.startswith(p) for p in self.SUPPORTED_PREFIXES)

    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(entities)
        self._apply_path_defaults(intent, entities, result, context)
        self._apply_pattern_defaults(entities, result)
        self._apply_find_flags(intent, entities, result)
        return result

    def _apply_path_defaults(self, intent: str, entities: Dict, result: Dict, context: Dict) -> None:
        """Apply shell path defaults."""
        if 'path' not in result:
            result['path'] = context.get('current_directory', '.')

    def _apply_pattern_defaults(self, entities: Dict, result: Dict) -> None:
        """Apply pattern defaults for file operations."""
        if 'pattern' in entities and '*' not in entities['pattern']:
            result['pattern'] = f"*{entities['pattern']}*"

    def _apply_find_flags(self, intent: str, entities: Dict, result: Dict) -> None:
        """Build find command flags."""
        flags = []
        if 'target_type' in entities:
            flags.append(f"-type {entities['target_type']}")
        if 'pattern' in entities:
            flags.append(f"-name '{entities['pattern']}'")
        if 'size' in entities:
            flags.append(f"-size {entities['size']}")
        if 'mtime' in entities:
            flags.append(f"-mtime {entities['mtime']}")
        result['find_flags'] = ' '.join(flags)


class DockerEntityPreparer:
    """Prepares entities for docker commands."""

    def supports(self, intent: str) -> bool:
        return intent.startswith('docker_')

    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(entities)
        if 'container' in entities and not entities['container'].startswith(('container_', 'id:')):
            result['container'] = self._resolve_container_name(entities['container'])
        return result

    def _resolve_container_name(self, name: str) -> str:
        """Resolve container name to ID if needed."""
        return name


class SQLEntityPreparer:
    """Prepares entities for SQL commands."""

    def supports(self, intent: str) -> bool:
        return intent.startswith('sql_')

    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(entities)
        if 'table' in entities:
            result['table'] = self._sanitize_identifier(entities['table'])
        if 'columns' in entities:
            result['columns'] = self._sanitize_columns(entities['columns'])
        return result

    def _sanitize_identifier(self, identifier: str) -> str:
        """Sanitize SQL identifier."""
        return ''.join(c for c in identifier if c.isalnum() or c == '_')

    def _sanitize_columns(self, columns: Any) -> str:
        """Sanitize column list."""
        if isinstance(columns, str):
            columns = [c.strip() for c in columns.split(',')]
        return ', '.join(self._sanitize_identifier(c) for c in columns)


class KubernetesEntityPreparer:
    """Prepares entities for kubernetes commands."""

    def supports(self, intent: str) -> bool:
        return intent.startswith(('kubectl_', 'kubernetes_', 'k8s_'))

    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(entities)
        if 'namespace' not in result:
            result['namespace'] = context.get('kubernetes_namespace', 'default')
        if 'context' not in result:
            result['context'] = context.get('kubernetes_context')
        return result


class EntityPreparationPipeline:
    """Coordinates entity preparation across domains."""

    def __init__(self):
        self._preparers = [
            ShellEntityPreparer(),
            DockerEntityPreparer(),
            SQLEntityPreparer(),
            KubernetesEntityPreparer(),
        ]

    def prepare(self, intent: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate preparer based on intent."""
        for preparer in self._preparers:
            if preparer.supports(intent):
                return preparer.prepare(intent, entities, context)
        return entities
