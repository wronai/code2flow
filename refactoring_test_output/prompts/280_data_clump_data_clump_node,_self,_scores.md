## Cel refaktoryzacji
Extract logic from `node, self, scores` to a new method/function.

## Powód (z analizy DFG)
- Arguments (node, self, scores) are used together in multiple functions: code2flow.optimization.advanced_optimizer.DataStructureOptimizer._generate_optimization_recommendation, code2flow.optimization.advanced_optimizer._generate_optimization_recommendation.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 239-259)

## Kod źródłowy do refaktoryzacji
```python
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
        clusters = []
        processed = set()
        
        for i, type1 in enumerate(type_data):
            if i in processed:
                continue
                
            cluster = [type1]
            processed.add(i)
            
            for j, type2 in enumerate(type_data[i+1:], i+1):
                if j in processed:
                    continue
                    
                # Check similarity
                similarity = self._calculate_type_similarity(type1, type2)
                if similarity > 0.7:  # High similarity threshold
                    cluster.append(type2)
                    processed.add(j)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_type_similarity(self, type1: Dict, type2: Dict) -> float:
        """Calculate similarity between two data types."""
        # Similarity based on detected types and usage patterns
        type_overlap = len(set(type1['detected_types']) & set(type2['detected_types']))
        total_types = len(set(type1['detected_types']) | set(type2['detected_types']))
        
        if total_types == 0:
            return 0.0
        

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.