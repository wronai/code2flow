## Cel refaktoryzacji
Extract logic from `_cluster_similar_types` to a new method/function.

## Powód (z analizy DFG)
- Function '_cluster_similar_types' has high complexity: fan-out=7, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 252-272)

## Kod źródłowy do refaktoryzacji
```python
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
        
        type_similarity = type_overlap / total_types
        
        # Factor in usage similarity
        usage_diff = abs(type1['usage_count'] - type2['usage_count'])
        max_usage = max(type1['usage_count'], type2['usage_count'])
        usage_similarity = 1.0 - (usage_diff / max_usage) if max_usage > 0 else 1.0
        
        return (type_similarity + usage_similarity) / 2.0
    
    def _calculate_consolidation_benefit(self, cluster: List[Dict]) -> float:
        """Calculate benefit of consolidating a type cluster."""
        total_usage = sum(t['usage_count'] for t in cluster)
        complexity_reduction = len(cluster) - 1  # Reduce by number of merged types

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _cluster_similar_types. Skup się na wydzieleniu operacji o największej liczbie mutacji.