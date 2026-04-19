"""README insights extraction — parse analysis files for health metrics."""

from pathlib import Path
from typing import Any, Dict


def extract_insights(output_dir: Path) -> Dict[str, Any]:
    """Extract insights from existing analysis files."""
    insights = {
        'critical_functions': 0,
        'god_modules': 0,
        'refactoring_actions': 0,
        'has_health_issues': False,
        'has_evolution_plan': False
    }
    
    # Check analysis.toon for health metrics
    analysis_toon = output_dir / 'analysis.toon'
    if analysis_toon.exists():
        try:
            content = analysis_toon.read_text(encoding='utf-8')
            # Extract critical functions count
            for line in content.split('\n'):
                if 'critical:' in line:
                    # Format: critical:57/537
                    parts = line.split('critical:')[1].split('/')[0]
                    insights['critical_functions'] = int(parts.strip())
                elif 'GOD' in line and '🔴' in line:
                    insights['god_modules'] += 1
                elif line.strip().startswith('🔴'):
                    insights['has_health_issues'] = True
        except Exception:
            pass
    
    # Check evolution.toon.yaml for refactoring plan
    evolution_toon = output_dir / 'evolution.toon.yaml'
    if evolution_toon.exists():
        try:
            content = evolution_toon.read_text(encoding='utf-8')
            if 'REFACTOR[' in content:
                # Count refactoring actions
                for line in content.split('\n'):
                    if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                        insights['refactoring_actions'] += 1
                insights['has_evolution_plan'] = True
        except Exception:
            pass
    
    return insights


__all__ = ['extract_insights']
