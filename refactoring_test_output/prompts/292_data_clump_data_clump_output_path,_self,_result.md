## Cel refaktoryzacji
Extract logic from `output_path, self, result` to a new method/function.

## Powód (z analizy DFG)
- Arguments (output_path, self, result) are used together in multiple functions: code2flow.exporters.base.YAMLExporter.export_grouped, code2flow.exporters.base.MermaidExporter.export, code2flow.exporters.base.MermaidExporter.export_call_graph, code2flow.exporters.base.MermaidExporter.export_compact, code2flow.exporters.base.LLMPromptExporter.export, code2flow.exporters.base.export, code2flow.exporters.base.export_grouped, code2flow.exporters.base.export_call_graph, code2flow.exporters.base.export_compact.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 911-931)

## Kod źródłowy do refaktoryzacji
```python
    def export_compact(self, result: AnalysisResult, output_path: str) -> None:
        """Export compact flowchart - same as call graph for now."""
        self.export_call_graph(result, output_path)
    
    def _safe_id(self, name: str) -> str:
        """Create Mermaid-safe node ID."""
        safe = name.replace('.', '_').replace('-', '_').replace(':', '_')
        if len(safe) > 40:
            safe = safe[:20] + '_' + str(hash(name) % 10000)
        return safe


class LLMPromptExporter:
    """Export LLM-ready analysis summary with architecture and flows."""
    
    def export(self, result: AnalysisResult, output_path: str) -> None:
        """Generate comprehensive LLM prompt with architecture description."""
        lines = [
            "# System Architecture Analysis",
            "",
            f"## Overview",
            f"",
            f"- **Project**: {result.project_path}",
            f"- **Analysis Mode**: {result.analysis_mode}",
            f"- **Total Functions**: {len(result.functions)}",
            f"- **Total Classes**: {len(result.classes)}",
            f"- **Modules**: {len(result.modules)}",
            f"- **Entry Points**: {len(result.entry_points)}",
            f"",
        ]
        
        # Architecture - Group by module
        lines.extend([
            "## Architecture by Module",
            "",
        ])
        
        # Get top modules by function count
        module_stats = []
        for mod_name, mod in result.modules.items():
            func_count = len(mod.functions)
            class_count = len(mod.classes)
            if func_count > 0 or class_count > 0:
                module_stats.append((mod_name, func_count, class_count, mod.file))
        
        module_stats.sort(key=lambda x: x[1], reverse=True)
        
        for mod_name, func_count, class_count, file_path in module_stats[:20]:
            lines.append(f"### {mod_name}")
            lines.append(f"- **Functions**: {func_count}")

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.