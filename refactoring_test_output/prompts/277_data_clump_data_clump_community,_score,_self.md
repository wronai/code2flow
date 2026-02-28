## Cel refaktoryzacji
Extract logic from `community, score, self` to a new method/function.

## Powód (z analizy DFG)
- Arguments (community, score, self) are used together in multiple functions: code2flow.optimization.advanced_optimizer.DataStructureOptimizer._generate_consolidation_recommendation, code2flow.optimization.advanced_optimizer._generate_consolidation_recommendation.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 205-225)

## Kod źródłowy do refaktoryzacji
```python
    def _generate_consolidation_recommendation(self, community: set, score: float) -> str:
        """Generate consolidation recommendation for a community."""
        if score > 0.8:
            return f"HIGH PRIORITY: Consolidate {len(community)} functions into unified framework"
        elif score > 0.5:
            return f"MEDIUM PRIORITY: Merge similar functions in {len(community)}-function group"
        else:
            return f"LOW PRIORITY: Consider refactoring {len(community)} functions"
    
    def _calculate_optimization_priority(self, scores: Dict[str, float]) -> float:
        """Calculate optimization priority from centrality scores."""
        # Weight different measures
        weights = {
            'betweenness': 0.3,
            'closeness': 0.2,
            'pagerank': 0.2,
            'out_degree': 0.2,
            'in_degree': 0.1
        }
        
        priority = sum(scores[measure] * weight for measure, weight in weights.items())
        return min(1.0, priority)
    
    def _determine_optimization_type(self, scores: Dict[str, float]) -> str:
        """Determine optimization type based on scores."""
        if scores['out_degree'] > 10:
            return 'split'
        elif scores['in_degree'] > 10:
            return 'cache'
        elif scores['betweenness'] > 0.1:
            return 'optimize_path'
        else:
            return 'monitor'
    
    def _generate_optimization_recommendation(self, node: str, scores: Dict[str, float]) -> str:
        """Generate optimization recommendation for a node."""
        opt_type = self._determine_optimization_type(scores)
        
        recommendations = {
            'split': f"SPLIT {node.split('.')[-1]} into {int(scores['out_degree']/5)} specialized functions",
            'cache': f"CACHE results for {node.split('.')[-1]} (called {int(scores['in_degree'])} times)",
            'optimize_path': f"OPTIMIZE critical path through {node.split('.')[-1]}",
            'monitor': f"MONITOR {node.split('.')[-1]} for performance issues"
        }
        
        return recommendations[opt_type]
    
    def _cluster_similar_types(self, type_data: List[Dict]) -> List[List[Dict]]:
        """Cluster similar data types."""
        # Simple clustering based on detected types and usage patterns

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.