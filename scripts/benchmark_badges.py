#!/usr/bin/env python3
"""
Generate GitHub badges from code2llm benchmark results.

Usage:
    python scripts/benchmark_badges.py --output index.html
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Shields.io badge URL format
SHIELDS_URL = "https://img.shields.io/badge/{label}-{message}-{color}.svg"

def get_shield_url(label: str, message: str, color: str = "blue") -> str:
    """Generate a shields.io badge URL."""
    label = label.replace(" ", "%20")
    message = message.replace(" ", "%20")
    return SHIELDS_URL.format(label=label, message=message, color=color)

def parse_evolution_metrics(toon_content: str) -> Dict[str, str]:
    """Extract metrics from evolution.toon content."""
    metrics = {}
    for line in toon_content.splitlines():
        line = line.strip()
        if line.startswith("CC̄:"):
            m = re.search(r"([\d.]+)\s*→", line)
            if m:
                metrics["cc_avg"] = m.group(1)
        elif line.startswith("max-CC:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["max_cc"] = m.group(1)
        elif line.startswith("god-modules:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["god_modules"] = m.group(1)
        elif line.startswith("high-CC"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["high_cc"] = m.group(1)
        elif line.startswith("hub-types:"):
            m = re.search(r"(\d+)\s*→", line)
            if m:
                metrics["hub_types"] = m.group(1)

    # Also extract func count from header
    m = re.search(r"\| (\d+) func \|", toon_content)
    if m:
        metrics["total_funcs"] = m.group(1)

    return metrics

def parse_format_quality_report(report_path: Path) -> Optional[Dict[str, Dict]]:
    """Parse format quality JSON report."""
    if not report_path.exists():
        return None

    try:
        data = json.loads(report_path.read_text())
        return data.get("results", {})
    except Exception:
        return None

def parse_performance_report(report_path: Path) -> Optional[Dict]:
    """Parse performance JSON report."""
    if not report_path.exists():
        return None

    try:
        data = json.loads(report_path.read_text())
        return data
    except Exception:
        return None

def generate_badges(metrics: Dict[str, str]) -> List[Dict[str, str]]:
    """Generate badge data from metrics."""
    badges = []

    # Evolution metrics
    if "cc_avg" in metrics:
        badges.append({
            "label": "CC̄",
            "value": metrics["cc_avg"],
            "color": "blue"
        })
    if "max_cc" in metrics:
        badges.append({
            "label": "max-CC",
            "value": metrics["max_cc"],
            "color": "orange"
        })
    if "god_modules" in metrics:
        badges.append({
            "label": "god-modules",
            "value": metrics["god_modules"],
            "color": "red"
        })
    if "high_cc" in metrics:
        badges.append({
            "label": "high-CC",
            "value": metrics["high_cc"],
            "color": "yellow"
        })
    if "hub_types" in metrics:
        badges.append({
            "label": "hub-types",
            "value": metrics["hub_types"],
            "color": "green"
        })
    if "total_funcs" in metrics:
        badges.append({
            "label": "functions",
            "value": metrics["total_funcs"],
            "color": "purple"
        })

    return badges

def generate_format_quality_badges(format_scores: Dict[str, Dict]) -> List[Dict[str, str]]:
    """Generate badges from format quality scores."""
    badges = []

    if format_scores:
        # Get top 3 formats
        sorted_formats = sorted(
            format_scores.items(),
            key=lambda x: x[1].get("total_score", 0),
            reverse=True
        )[:3]

        for i, (format_name, scores) in enumerate(sorted_formats):
            rank = i + 1
            color = ["gold", "silver", "bronze"][i] if i < 3 else "blue"
            badges.append({
                "label": f"#{rank}",
                "value": format_name,
                "color": color
            })

        # Add total score
        total_score = sum(s.get("total_score", 0) for s in format_scores.values()) / len(format_scores) if format_scores else 0
        badges.append({
            "label": "Avg Score",
            "value": f"{total_score:.1f}/100",
            "color": "blue"
        })

    return badges

def generate_performance_badges(performance_data: Dict) -> List[Dict[str, str]]:
    """Generate badges from performance data."""
    badges = []

    if performance_data:
        # Quick strategy
        quick = performance_data.get("strategy_comparison", {}).get("Quick", {})
        if quick:
            badges.append({
                "label": "Quick",
                "value": f"{quick.get('time', 'N/A')}s",
                "color": "green"
            })

        # Standard strategy
        standard = performance_data.get("strategy_comparison", {}).get("Standard", {})
        if standard:
            badges.append({
                "label": "Standard",
                "value": f"{standard.get('time', 'N/A')}s",
                "color": "blue"
            })

        # Deep strategy
        deep = performance_data.get("strategy_comparison", {}).get("Deep", {})
        if deep:
            badges.append({
                "label": "Deep",
                "value": f"{deep.get('time', 'N/A')}s",
                "color": "purple"
            })

        # Memory estimates
        memory = performance_data.get("memory_estimates", {})
        if memory:
            badges.append({
                "label": "Memory",
                "value": f"Quick: {memory.get('quick_mb', 'N/A')}MB",
                "color": "gray"
            })

    return badges

def create_html(badges: List[List[Dict[str, str]]], title: str = "Code2LLM Benchmarks") -> str:
    """Create HTML page with badge table."""
    html = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f5f5;
                color: #333;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }}
            .badge-table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            .badge-table th {{
                background: #4a5568;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            .badge-table td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            .badge {{
                display: inline-block;
                margin: 2px;
                background: #f7fafc;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-family: 'Courier New', monospace;
                border: 1px solid #e2e8f0;
            }}
            .badge img {{
                vertical-align: middle;
                margin-right: 4px;
            }}
            .badge-title {{
                font-weight: 600;
                color: #2d3748;
            }}
            .badge-value {{
                color: #4a5568;
            }}
            .timestamp {{
                text-align: center;
                color: #718096;
                font-size: 14px;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
            }}
            .github-link {{
                text-align: center;
                margin-top: 10px;
            }}
            .github-link a {{
                color: #0366d6;
                text-decoration: none;
                font-weight: 500;
            }}
            .github-link a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
    """

    # Add tables for each category
    categories = [
        ("Evolution Metrics", badges[0]),
        ("Format Quality", badges[1]),
        ("Performance", badges[2])
    ]

    for category_name, category_badges in categories:
        if category_badges:
            html += f"""
            <h2 style="color: #2d3748; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">{category_name}</h2>
            <table class="badge-table">
                <tr>
                    <th>Badge</th>
                    <th>Label</th>
                    <th>Value</th>
                </tr>
            """
            for badge in category_badges:
                shield_url = get_shield_url(badge["label"], badge["value"], badge["color"])
                html += f"""
                <tr>
                    <td>
                        <div class="badge">
                            <img src="{shield_url}" alt="{badge['label']}: {badge['value']}">
                        </div>
                    </td>
                    <td><span class="badge-title">{badge['label']}</span></td>
                    <td><span class="badge-value">{badge['value']}</span></td>
                </tr>
                """
            html += "</table>"

    # Add timestamp and GitHub link
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html += f"""
        <div class="timestamp">
            Generated: {timestamp}
        </div>
        <div class="github-link">
            <a href="https://github.com/wronai/code2llm" target="_blank">
                View on GitHub
            </a>
        </div>
    </div>
    </body>
    </html>
    """

    return html

def main():
    """Main function to generate badges."""
    output_dir = Path("badges")
    output_dir.mkdir(exist_ok=True)

    # Parse benchmark data
    evolution_metrics = {}
    format_scores = {}
    performance_data = {}

    # Try to find evolution.toon
    for root, dirs, files in os.walk("."):
        if "evolution.toon" in files:
            toon_path = Path(root) / "evolution.toon"
            content = toon_path.read_text()
            evolution_metrics = parse_evolution_metrics(content)
            break

    # Try to find format quality report
    format_report_path = Path("reports") / "format_quality_*.json"
    for report_path in Path("reports").glob("format_quality_*.json"):
        format_scores = parse_format_quality_report(report_path)
        break

    # Try to find performance report
    performance_report_path = Path("reports") / "benchmark_*.json"
    for report_path in Path("reports").glob("benchmark_*.json"):
        performance_data = parse_performance_report(report_path)
        break

    # Generate badges
    badges = [
        generate_badges(evolution_metrics),
        generate_format_quality_badges(format_scores),
        generate_performance_badges(performance_data)
    ]

    # Create HTML
    html_content = create_html(badges)

    # Save HTML
    output_path = output_dir / "index.html"
    output_path.write_text(html_content)

    print(f"✓ Badges generated successfully!")
    print(f"✓ HTML page saved to: {output_path}")
    print(f"✓ Open in browser: file://{output_path.resolve()}")

if __name__ == "__main__":
    main()