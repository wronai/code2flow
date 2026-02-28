## Cel refaktoryzacji
Extract logic from `analyze_communities` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'analyze_communities' is highly complex: CC=1, fan-out=10, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/optimization/advanced_optimizer.py (linie 40+)

## Kod źródłowy do refaktoryzacji
```python
    def analyze_communities(self) -> Dict[str, Any]:
        """Detect communities for process consolidation using Louvain algorithm."""
        # Convert to undirected for community detection
        G_undirected = self.graph.to_undirected()
        
        # Detect communities
        communities = nx.community.louvain_communities(G_undirected, seed=42)
        
        # Analyze each community
        community_analysis = []
        for i, community in enumerate(communities):
            if len(community) < 3:  # Skip very small communities
                continue
                
            # Get process patterns in this community
            community_patterns = self._get_community_patterns(community)
            
            # Calculate consolidation potential
            consolidation_score = self._calculate_consolidation_potential(community)
            
            community_analysis.append({
                'community_id': i,
                'size': len(community),
                'functions': list(community)[:10],  # Limit for readability
                'process_patterns': community_patterns,
                'consolidation_score': consolidation_score,
                'recommendation': self._generate_consolidation_recommendation(community, consolidation_score)
            })
        
        return {
            'total_communities': len(communities),
            'analyzed_communities': len(community_analysis),
            'communities': sorted(community_analysis, key=lambda x: x['consolidation_score'], reverse=True)
        }
    
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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji analyze_communities. Skup się na wydzieleniu operacji o największej liczbie mutacji.