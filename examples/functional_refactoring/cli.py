"""
CLI interface for command generation.

interfaces/cli/generate_command.py
"""
import os
from pathlib import Path
from typing import Optional

import click

from .cache import EvolutionaryCache
from .generator import CommandGenerator
from .models import CommandContext


@click.command()
@click.argument('query')
@click.option('--intent', help='Force specific intent')
@click.option('--dry-run', is_flag=True, help='Show command without executing')
@click.option('--cache-dir', default='~/.nlp2cmd/cache', help='Cache directory')
def generate(query: str, intent: Optional[str], dry_run: bool, cache_dir: str):
    """Generate command from natural language query."""
    cache = EvolutionaryCache(cache_file=Path(cache_dir) / 'commands.json')
    generator = CommandGenerator()

    if not intent:
        cached = cache.get(query, {})
        if cached:
            click.echo(f"Cached: {cached}")
            return

    context = CommandContext(environment=dict(os.environ))
    result = generator.generate(
        intent=intent or 'auto',
        entities={'query': query},
        context=context
    )

    if result.command:
        click.echo(result.command)
        if not dry_run:
            cache.put(query, {}, result.command)
    else:
        click.echo(f"Error: {result.explanation}", err=True)
