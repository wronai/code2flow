## Cel refaktoryzacji
Move method `output_path, result, self` from module `base` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (output_path, result, self) are used together in multiple functions: code2flow.exporters.base.YAMLExporter.export_grouped, code2flow.exporters.base.MermaidExporter.export, code2flow.exporters.base.MermaidExporter.export_call_graph, code2flow.exporters.base.MermaidExporter.export_compact, code2flow.exporters.base.LLMPromptExporter.export, code2flow.exporters.base.export, code2flow.exporters.base.export_grouped, code2flow.exporters.base.export_call_graph, code2flow.exporters.base.export_compact.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `base`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
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
            if class_count > 0:
                lines.append(f"- **Classes**: {class_count}")
            if file_path:
                lines.append(f"- **File**: `{file_path.split('/')[-1]}`")
            lines.append("")
        
        # Key Entry Points - limit to most important
        lines.extend([
            "## Key Entry Points",
            "",
            "Main execution flows into the system:",
            "",
        ])
        
        # Filter and prioritize entry points
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.