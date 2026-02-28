## Cel refaktoryzacji
Extract logic from `export_data_structures` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'export_data_structures' is highly complex: CC=1, fan-out=12, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 539+)

## Kod źródłowy do refaktoryzacji
```python
    def export_data_structures(self, result: AnalysisResult, output_path: str, compact: bool = True) -> None:
        """Export data structure analysis focusing on data types, flows, and optimization opportunities.
        
        Analyzes:
        - Data types and their usage patterns
        - Data flow graphs (DFG) between functions
        - Process dependencies and data transformations
        - Optimization opportunities (type reduction, process consolidation)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 1. Analyze data types and structures
        data_types = self._analyze_data_types(result)
        
        # 2. Build data flow graph
        data_flow_graph = self._build_data_flow_graph(result)
        
        # 3. Identify process patterns
        process_patterns = self._identify_process_patterns(result)
        
        # 4. Calculate optimization opportunities
        optimization_analysis = self._analyze_optimization_opportunities(result, data_types, data_flow_graph)
        
        # Build comprehensive data structure report
        structure_data = {
            'project_path': result.project_path,
            'analysis_type': 'data_structures',
            'summary': {
                'unique_data_types': len(data_types),
                'data_flow_nodes': len(data_flow_graph.get('nodes', [])),
                'process_patterns': len(process_patterns),
                'optimization_potential': optimization_analysis.get('potential_score', 0),
            },
            'data_types': data_types,
            'data_flow_graph': data_flow_graph,
            'process_patterns': process_patterns,
            'optimization_analysis': optimization_analysis,
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(structure_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✓ Data structures exported: {output_path}")
        print(f"  - Data types: {len(data_types)}")
        print(f"  - Flow nodes: {len(data_flow_graph.get('nodes', []))}")
        print(f"  - Process patterns: {len(process_patterns)}")
        print(f"  - Optimization score: {optimization_analysis.get('potential_score', 0):.1f}")
    
    def _analyze_data_types(self, result: AnalysisResult) -> list:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji export_data_structures. Skup się na wydzieleniu operacji o największej liczbie mutacji.