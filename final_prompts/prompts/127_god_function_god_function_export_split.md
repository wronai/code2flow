## Cel refaktoryzacji
Extract logic from `export_split` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'export_split' is highly complex: CC=1, fan-out=14, mutations=15.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 89+)

## Kod źródłowy do refaktoryzacji
```python
    def export_split(self, result: AnalysisResult, output_dir: str, compact: bool = True, include_defaults: bool = False) -> None:
        """Export analysis split into multiple files for large repositories.
        
        Creates:
        - summary.yaml - project overview and stats
        - functions.yaml - all functions with their calls
        - classes.yaml - all classes with methods
        - modules.yaml - all modules
        - cfg_nodes.yaml - control flow graph nodes (optional, can be large)
        - entry_points.yaml - main entry points
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        compact_mode = compact and not include_defaults
        
        # 1. Summary file
        summary = {
            'project': result.project_path,
            'analysis_mode': result.analysis_mode,
            'stats': result.stats,
            'overview': {
                'total_functions': len(result.functions),
                'total_classes': len(result.classes),
                'total_modules': len(result.modules),
                'total_nodes': len(result.nodes),
                'total_edges': len(result.edges),
                'entry_points_count': len(result.entry_points),
            }
        }
        with open(output_path / 'summary.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(summary, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 2. Functions file
        functions_data = {
            'count': len(result.functions),
            'functions': {k: v.to_dict(compact_mode) for k, v in result.functions.items()}
        }
        with open(output_path / 'functions.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(functions_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 3. Classes file
        classes_data = {
            'count': len(result.classes),
            'classes': {k: v.to_dict(compact_mode) for k, v in result.classes.items()}
        }
        with open(output_path / 'classes.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(classes_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 4. Modules file
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji export_split. Skup się na wydzieleniu operacji o największej liczbie mutacji.