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
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 332-352)

## Kod źródłowy do refaktoryzacji
```python
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
                'effort': f"{len(opportunity['types'])} types",
                'impact': f"Benefit: {opportunity['consolidation_benefit']:.2f}"
            })
        
        return actions
    
    def _prioritize_implementation(self, action_items: List[Dict]) -> List[Dict]:
        """Prioritize implementation order."""
        # Sort by priority and impact
        priority_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        
        return sorted(action_items, key=lambda x: (
            priority_order.get(x['priority'], 0),
            len(x['description'])  # Longer descriptions = more complex
        ), reverse=True)
    
    def _assess_risks(self, action_items: List[Dict]) -> Dict[str, Any]:
        """Assess risks for optimization actions."""
        high_priority_count = len([a for a in action_items if a['priority'] == 'HIGH'])
        total_count = len(action_items)

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.