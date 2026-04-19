"""
Shared domain models for command generation.

domain/command_generation/__init__.py
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class CommandContext:
    """Context for command generation."""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    environment: Dict[str, str] = None
    history: list = None


@dataclass
class CommandResult:
    """Result of command generation."""
    command: str
    confidence: float
    explanation: Optional[str] = None
    alternatives: list = None
