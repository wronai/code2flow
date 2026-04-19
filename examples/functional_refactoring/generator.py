"""
Main Command Generator - orchestrates the generation process.

domain/command_generation/generator.py
"""
from typing import Optional

from .entity_preparers import EntityPreparationPipeline
from .models import CommandResult
from .template_engine import TemplateLoader, TemplateRenderer


class CommandGenerator:
    """Generates commands from natural language intents."""

    def __init__(
        self,
        template_loader: Optional[TemplateLoader] = None,
        entity_preparer: Optional[EntityPreparationPipeline] = None,
        template_renderer: Optional[TemplateRenderer] = None,
    ):
        self._template_loader = template_loader or TemplateLoader()
        self._entity_preparer = entity_preparer or EntityPreparationPipeline()
        self._template_renderer = template_renderer or TemplateRenderer()
        self._template_loader.load()

    def generate(
        self,
        intent: str,
        entities: dict,
        context: Optional[dict] = None
    ) -> CommandResult:
        """
        Generate command from intent and entities.

        Args:
            intent: The command intent (e.g., 'shell_find_files')
            entities: Extracted entities from NL query
            context: Optional execution context

        Returns:
            CommandResult with generated command
        """
        context = context or {}
        prepared_entities = self._entity_preparer.prepare(intent, entities, context)
        template = self._template_loader.find_alternative_template(intent, prepared_entities)
        if not template:
            return CommandResult(
                command="",
                confidence=0.0,
                explanation=f"No template found for intent: {intent}"
            )
        command = self._template_renderer.render_with_conditionals(
            template.template,
            prepared_entities
        )
        return CommandResult(
            command=command,
            confidence=0.9,
            explanation=template.description
        )
