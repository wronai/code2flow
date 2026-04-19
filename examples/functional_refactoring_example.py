"""
Example Functional Refactoring for nlp2cmd generation module.

This shows how to split the 1202-line template_generator.py (100 methods)
into functional domains. See functional_refactoring/ package for the split.
"""

# ============================================================================
# BEFORE: Monolithic template_generator.py (1202 lines, 100 methods)
# ============================================================================

class TemplateGenerator:
    """Original - handles EVERYTHING: loading, matching, rendering, shell, docker, sql..."""

    def __init__(self, *args, **kwargs):
        self._load_templates_from_json()
        self._load_defaults_from_json()

    def generate(self, intent: str, entities: dict, context: dict):
        # 100+ lines of mixed logic
        if intent.startswith('shell_'):
            entities = self._prepare_shell_entities(intent, entities, context)
        elif intent.startswith('docker_'):
            entities = self._prepare_docker_entities(intent, entities)
        elif intent.startswith('sql_'):
            entities = self._prepare_sql_entities(intent, entities)
        template = self._find_alternative_template(intent, entities)
        rendered = self._render_template(template, entities)
        return rendered

    def _load_templates_from_json(self): pass
    def _load_defaults_from_json(self): pass
    def _prepare_shell_entities(self, *args, **kwargs): pass
    def _prepare_docker_entities(self, *args, **kwargs): pass
    def _prepare_sql_entities(self, *args, **kwargs): pass
    def _find_alternative_template(self, *args, **kwargs): pass
    def _render_template(self, *args, **kwargs): pass


# ============================================================================
# AFTER: Functional Domain Separation
# See functional_refactoring/ package:
#   models.py          — CommandContext, CommandResult
#   entity_preparers.py — ShellEntityPreparer, DockerEntityPreparer, ...
#   template_engine.py — TemplateLoader, TemplateRenderer
#   generator.py       — CommandGenerator (orchestrator)
#   cache.py           — EvolutionaryCache
#   cli.py             — generate() click command
# ============================================================================

from functional_refactoring.models import CommandContext, CommandResult
from functional_refactoring.entity_preparers import (
    EntityPreparationPipeline,
    ShellEntityPreparer,
    DockerEntityPreparer,
    SQLEntityPreparer,
    KubernetesEntityPreparer,
)
from functional_refactoring.template_engine import TemplateLoader, TemplateRenderer
from functional_refactoring.generator import CommandGenerator
from functional_refactoring.cache import EvolutionaryCache
