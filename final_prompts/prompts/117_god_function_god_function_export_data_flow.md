## Cel refaktoryzacji
Extract logic from `export_data_flow` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'export_data_flow' is highly complex: CC=1, fan-out=10, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 332+)

## Kod źródłowy do refaktoryzacji
```python
    def export_data_flow(self, result: AnalysisResult, output_path: str, compact: bool = True) -> None:
        """Export detailed data flow analysis showing what happens in the project.
        
        Analyzes:
        - Data pipelines (input → transform → output)
        - State transitions and lifecycles
        - Cross-component data dependencies
        - Event/callback flows
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 1. Identify data transformation chains
        data_pipelines = self._find_data_pipelines(result)
        
        # 2. Identify state management patterns
        state_patterns = self._find_state_patterns(result)
        
        # 3. Identify data dependencies between modules
        data_deps = self._find_data_dependencies(result)
        
        # 4. Identify event/callback flows
        event_flows = self._find_event_flows(result)
        
        # Build data flow report
        flow_data = {
            'project_path': result.project_path,
            'analysis_type': 'data_flow',
            'summary': {
                'data_pipelines_count': len(data_pipelines),
                'state_managers_count': len(state_patterns),
                'cross_module_data_deps': len(data_deps),
                'event_flows_count': len(event_flows),
            },
            'data_pipelines': data_pipelines,
            'state_patterns': state_patterns,
            'data_dependencies': data_deps,
            'event_flows': event_flows,
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(flow_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✓ Data flow exported: {output_path}")
        print(f"  - Data pipelines: {len(data_pipelines)}")
        print(f"  - State patterns: {len(state_patterns)}")
        print(f"  - Data dependencies: {len(data_deps)}")
        print(f"  - Event flows: {len(event_flows)}")
    
    def _find_data_pipelines(self, result: AnalysisResult) -> list:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji export_data_flow. Skup się na wydzieleniu operacji o największej liczbie mutacji.