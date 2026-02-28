## Cel refaktoryzacji
Extract logic from `analyze_centrality` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'analyze_centrality' is highly complex: CC=1, fan-out=13, mutations=5.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 75+)

## Kod źródłowy do refaktoryzacji
```python
    def analyze_centrality(self) -> Dict[str, Any]:
        """Analyze centrality measures for hub optimization."""
        centrality_measures = {
            'betweenness': nx.betweenness_centrality(self.graph),
            'closeness': nx.closeness_centrality(self.graph),
            'pagerank': nx.pagerank(self.graph),
            'in_degree': dict(self.graph.in_degree()),
            'out_degree': dict(self.graph.out_degree())
        }
        
        # Find optimization candidates
        optimization_candidates = []
        
        for node in self.graph.nodes():
            scores = {
                'betweenness': centrality_measures['betweenness'][node],
                'closeness': centrality_measures['closeness'][node],
                'pagerank': centrality_measures['pagerank'][node],
                'in_degree': centrality_measures['in_degree'][node],
                'out_degree': centrality_measures['out_degree'][node]
            }
            
            # Calculate optimization priority
            priority = self._calculate_optimization_priority(scores)
            
            if priority > 0.5:  # Only include significant candidates
                optimization_candidates.append({
                    'function': node,
                    'scores': scores,
                    'priority': priority,
                    'optimization_type': self._determine_optimization_type(scores),
                    'recommendation': self._generate_optimization_recommendation(node, scores)
                })
        
        return {
            'total_nodes': len(self.graph.nodes()),
            'candidates': len(optimization_candidates),
            'top_candidates': sorted(optimization_candidates, key=lambda x: x['priority'], reverse=True)[:10]
        }
    
    def analyze_type_patterns(self) -> Dict[str, Any]:
        """Analyze type patterns for consolidation opportunities."""
        type_data = self.analysis_data['data_types']
        
        # Find similar types
        type_clusters = self._cluster_similar_types(type_data)
        
        # Generate consolidation recommendations
        consolidation_opportunities = []
        
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji analyze_centrality. Skup się na wydzieleniu operacji o największej liczbie mutacji.