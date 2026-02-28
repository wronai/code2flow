## Cel refaktoryzacji
Extract logic from `analyze_type_patterns` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'analyze_type_patterns' is highly complex: CC=1, fan-out=7, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 115+)

## Kod źródłowy do refaktoryzacji
```python
    def analyze_type_patterns(self) -> Dict[str, Any]:
        """Analyze type patterns for consolidation opportunities."""
        type_data = self.analysis_data['data_types']
        
        # Find similar types
        type_clusters = self._cluster_similar_types(type_data)
        
        # Generate consolidation recommendations
        consolidation_opportunities = []
        
        for cluster_id, cluster in enumerate(type_clusters):
            if len(cluster) > 1:  # Only clusters with multiple types
                total_usage = sum(t['usage_count'] for t in cluster)
                cross_module_usage = sum(t['cross_module_usage'] for t in cluster)
                
                consolidation_opportunities.append({
                    'cluster_id': cluster_id,
                    'types': [t['type_name'] for t in cluster],
                    'total_usage': total_usage,
                    'cross_module_usage': cross_module_usage,
                    'consolidation_benefit': self._calculate_consolidation_benefit(cluster),
                    'recommendation': self._generate_type_consolidation_recommendation(cluster)
                })
        
        return {
            'total_types': len(type_data),
            'clusters_found': len(type_clusters),
            'consolidation_opportunities': consolidation_opportunities
        }
    
    def generate_refactoring_plan(self) -> Dict[str, Any]:
        """Generate comprehensive refactoring plan."""
        communities = self.analyze_communities()
        centrality = self.analyze_centrality()
        type_patterns = self.analyze_type_patterns()
        
        # Calculate overall optimization score
        overall_score = self._calculate_overall_optimization_score(
            communities, centrality, type_patterns
        )
        
        # Generate prioritized action items
        action_items = self._generate_action_items(communities, centrality, type_patterns)
        
        return {
            'overall_optimization_score': overall_score,
            'estimated_impact': self._estimate_impact(action_items),
            'action_items': action_items,
            'implementation_order': self._prioritize_implementation(action_items),
            'risk_assessment': self._assess_risks(action_items)
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji analyze_type_patterns. Skup się na wydzieleniu operacji o największej liczbie mutacji.