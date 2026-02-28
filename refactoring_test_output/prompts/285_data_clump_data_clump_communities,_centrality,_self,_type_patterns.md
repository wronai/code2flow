## Cel refaktoryzacji
Extract logic from `communities, centrality, self, type_patterns` to a new method/function.

## Powód (z analizy DFG)
- Arguments (communities, centrality, self, type_patterns) are used together in multiple functions: code2flow.optimization.advanced_optimizer.DataStructureOptimizer._calculate_overall_optimization_score, code2flow.optimization.advanced_optimizer.DataStructureOptimizer._generate_action_items, code2flow.optimization.advanced_optimizer._calculate_overall_optimization_score, code2flow.optimization.advanced_optimizer._generate_action_items.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 312-332)

## Kod źródłowy do refaktoryzacji
```python
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
        }
    
    def _generate_action_items(self, communities: Dict, centrality: Dict, type_patterns: Dict) -> List[Dict]:
        """Generate prioritized action items."""
        actions = []
        
        # Community consolidation actions
        for community in communities['communities'][:5]:
            actions.append({
                'type': 'community_consolidation',
                'priority': 'HIGH' if community['consolidation_score'] > 0.7 else 'MEDIUM',
                'description': community['recommendation'],
                'effort': f"{community['size']} functions",
                'impact': f"Score: {community['consolidation_score']:.2f}"
            })
        
        # Hub optimization actions
        for candidate in centrality['top_candidates'][:5]:
            actions.append({
                'type': 'hub_optimization',
                'priority': 'HIGH' if candidate['priority'] > 0.7 else 'MEDIUM',
                'description': candidate['recommendation'],
                'effort': f"Priority: {candidate['priority']:.2f}",
                'impact': f"Type: {candidate['optimization_type']}"
            })
        
        # Type consolidation actions
        for opportunity in type_patterns['consolidation_opportunities'][:3]:
            actions.append({
                'type': 'type_consolidation',
                'priority': 'MEDIUM',
                'description': opportunity['recommendation'],

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.