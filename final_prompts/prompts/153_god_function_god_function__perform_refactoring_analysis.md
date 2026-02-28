## Cel refaktoryzacji
Extract logic from `_perform_refactoring_analysis` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_perform_refactoring_analysis' is highly complex: CC=1, fan-out=22, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 639+)

## Kod źródłowy do refaktoryzacji
```python
    def _perform_refactoring_analysis(self, result: AnalysisResult) -> None:
        """Perform deep analysis and detect code smells."""
        if self.config.verbose:
            print("Performing refactoring analysis...")
            
        # 1. Calculate metrics (fan-in/fan-out)
        cg_ext = CallGraphExtractor(self.config)
        cg_ext.result = result
        cg_ext._calculate_metrics()
        
        # 2. Build networkx graph for project-level analysis
        G = nx.DiGraph()
        for func_name, func_info in result.functions.items():
            G.add_node(func_name)
            for callee in func_info.calls:
                G.add_edge(func_name, callee)
        
        # 3. Calculate Betweenness Centrality (Bottlenecks)
        if len(G) > 0:
            try:
                centrality = nx.betweenness_centrality(G)
                for func_name, score in centrality.items():
                    if func_name in result.functions:
                        result.functions[func_name].centrality = score
            except Exception as e:
                if self.config.verbose:
                    print(f"Error calculating centrality: {e}")
            
            # 4. Detect Circular Dependencies
            try:
                cycles = list(nx.simple_cycles(G))
                if cycles:
                    result.metrics["project"] = result.metrics.get("project", {})
                    result.metrics["project"]["circular_dependencies"] = cycles
            except Exception as e:
                if self.config.verbose:
                    print(f"Error detecting cycles: {e}")

            # 5. Community Detection (Module groups)
            try:
                from networkx.algorithms import community
                # Using Louvain if available, otherwise greedy modularity
                if hasattr(community, 'louvain_communities'):
                    communities = community.louvain_communities(G.to_undirected())
                else:
                    communities = community.greedy_modularity_communities(G.to_undirected())
                
                result.coupling["communities"] = [list(c) for c in communities]
            except Exception as e:
                if self.config.verbose:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _perform_refactoring_analysis. Skup się na wydzieleniu operacji o największej liczbie mutacji.