"""
Template Loading and Rendering - storage, retrieval and interpolation.

domain/command_generation/templates/loader.py
domain/command_generation/templates/renderer.py
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path
from string import Template as StringTemplate
from typing import Dict, Optional, Any


@dataclass
class Template:
    """Command template."""
    intent: str
    pattern: str
    template: str
    description: Optional[str] = None
    aliases: Optional[Dict[str, str]] = None


class TemplateLoader:
    """Loads templates from various sources."""

    def __init__(self, templates_dir: Optional[Path] = None):
        self._templates_dir = templates_dir or Path(__file__).parent / 'data'
        self._templates: Dict[str, Template] = {}
        self._defaults: Dict[str, Any] = {}

    def load(self) -> None:
        """Load all templates and defaults."""
        self._load_templates()
        self._load_defaults()

    def _load_templates(self) -> None:
        """Load templates from JSON files."""
        templates_file = self._templates_dir / 'templates.json'
        if templates_file.exists():
            data = json.loads(templates_file.read_text())
            for intent, template_data in data.items():
                self._templates[intent] = Template(
                    intent=intent,
                    pattern=template_data.get('pattern', ''),
                    template=template_data.get('template', ''),
                    description=template_data.get('description'),
                    aliases=template_data.get('aliases')
                )

    def _load_defaults(self) -> None:
        """Load default values from JSON."""
        defaults_file = self._templates_dir / 'defaults.json'
        if defaults_file.exists():
            self._defaults = json.loads(defaults_file.read_text())

    def get_template(self, intent: str) -> Optional[Template]:
        """Get template by intent."""
        return self._templates.get(intent)

    def get_default(self, key: str, fallback: Any = None) -> Any:
        """Get default value."""
        return self._defaults.get(key, fallback)

    def find_alternative_template(self, intent: str, entities: Dict[str, Any]) -> Optional[Template]:
        """Find alternative template based on entities."""
        return self._templates.get(intent)


class TemplateRenderer:
    """Renders templates with entity substitution."""

    def render(self, template: str, entities: Dict[str, Any]) -> str:
        """Render template with entities."""
        try:
            t = StringTemplate(template)
            return t.safe_substitute(entities)
        except Exception:
            return self._manual_render(template, entities)

    def _manual_render(self, template: str, entities: Dict[str, Any]) -> str:
        """Manual template rendering for complex cases."""
        result = template
        for key, value in entities.items():
            placeholder = f"${{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result

    def render_with_conditionals(self, template: str, entities: Dict[str, Any]) -> str:
        """Render template with conditional blocks."""
        result = template
        pattern = r'\$\{if:(\w+)\}(.*?)\$\{endif\}'

        def replace_conditional(match):
            condition_var = match.group(1)
            content = match.group(2)
            if entities.get(condition_var):
                return content
            return ''

        result = re.sub(pattern, replace_conditional, result, flags=re.DOTALL)
        return self.render(result, entities)
