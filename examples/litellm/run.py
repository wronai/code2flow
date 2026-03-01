#!/usr/bin/env python3
"""
code2llm + LiteLLM: Automated refactoring advice from any LLM provider.

Usage:
    python examples/litellm/run.py /path/to/project [--model MODEL]

Examples:
    python examples/litellm/run.py .
    python examples/litellm/run.py . --model claude-3-5-sonnet-20241022
    python examples/litellm/run.py . --model ollama/llama3
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import litellm
except ImportError:
    print("ERROR: pip install litellm")
    sys.exit(1)


DEFAULT_MODEL = "gpt-4o-mini"


def run_analysis(project_path: str) -> dict:
    """Run code2llm and return analysis outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable, "-m", "code2llm",
            project_path, "-f", "evolution,context", "-o", tmpdir, "--no-png"
        ]
        print(f"🔍 Analyzing: {project_path}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            sys.exit(1)

        outputs = {}
        for name in ["evolution.toon", "context.md"]:
            path = Path(tmpdir) / name
            if path.exists():
                outputs[name] = path.read_text()

        return outputs


def get_refactoring_advice(outputs: dict, model: str) -> str:
    """Send analysis to LLM and get refactoring advice."""
    evolution = outputs.get("evolution.toon", "No evolution data")
    context = outputs.get("context.md", "No context data")

    # Truncate context if too large (keep first 3000 chars)
    if len(context) > 3000:
        context = context[:3000] + "\n... (truncated)"

    prompt = f"""You are a senior Python developer. Based on the following code analysis,
provide 3 concrete refactoring recommendations with estimated impact.

## Evolution Analysis (refactoring priorities)
```
{evolution}
```

## Architecture Context
```
{context}
```

For each recommendation:
1. What to refactor (file, function, line)
2. How to refactor (specific technique)
3. Expected impact (CC reduction, readability improvement)
4. Risk level (low/medium/high)

Be specific and actionable. Include code snippets where helpful."""

    print(f"🤖 Asking {model} for advice...")

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.3,
    )

    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="code2llm + LiteLLM refactoring advisor")
    parser.add_argument("project", help="Path to Python project")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LiteLLM model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    # Step 1: Analyze
    outputs = run_analysis(args.project)
    print(f"✅ Analysis complete: {', '.join(outputs.keys())}")

    # Step 2: Get advice
    advice = get_refactoring_advice(outputs, args.model)

    # Step 3: Print
    print("\n" + "=" * 60)
    print("  REFACTORING RECOMMENDATIONS")
    print("=" * 60 + "\n")
    print(advice)
    print("\n" + "=" * 60)
    print(f"  Model: {args.model}")
    print(f"  Project: {args.project}")
    print("=" * 60)


if __name__ == "__main__":
    main()
