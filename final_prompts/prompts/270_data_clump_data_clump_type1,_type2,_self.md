## Cel refaktoryzacji
Move method `type1, type2, self` from module `advanced_optimizer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (type1, type2, self) are used together in multiple functions: code2flow.optimization.advanced_optimizer.DataStructureOptimizer._calculate_type_similarity, code2flow.optimization.advanced_optimizer._calculate_type_similarity.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `advanced_optimizer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
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
        
        return (total_usage / 100.0) * complexity_reduction
    
    def _generate_type_consolidation_recommendation(self, cluster: List[Dict]) -> str:
        """Generate type consolidation recommendation."""
        type_names = [t['type_name'] for t in cluster]
        total_usage = sum(t['usage_count'] for t in cluster)
        
        return f"MERGE {len(cluster)} types ({', '.join(type_names[:3])}...) - {total_usage} total usages"
    
    def _calculate_overall_optimization_score(self, communities: Dict, centrality: Dict, type_patterns: Dict) -> float:
        """Calculate overall optimization score."""
        community_score = communities['analyzed_communities'] * 0.1
        centrality_score = centrality['candidates'] * 0.05
        type_score = len(type_patterns['consolidation_opportunities']) * 0.15
        
        return min(10.0, community_score + centrality_score + type_score)
    
    def _estimate_impact(self, action_items: List[Dict]) -> Dict[str, Any]:
        """Estimate impact of optimization actions."""
        total_items = len(action_items)
        high_priority = len([a for a in action_items if a['priority'] == 'HIGH'])
        
        return {
            'total_actions': total_items,
            'high_priority_actions': high_priority,
            'estimated_complexity_reduction': f"{total_items * 5}%",
            'estimated_performance_improvement': f"{high_priority * 10}%"
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.