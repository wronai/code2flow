## Cel refaktoryzacji
Extract logic from `filepath, self, layout` to a new method/function.

## Powód (z analizy DFG)
- Arguments (filepath, self, layout) are used together in multiple functions: code2flow.visualizers.graph.GraphVisualizer.visualize_cfg, code2flow.visualizers.graph.visualize_cfg.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/visualizers/graph.py (linie 43-63)

## Kod źródłowy do refaktoryzacji
```python
    def visualize_cfg(self, filepath: str, layout: str = 'spring'):
        """Create control flow visualization."""
        plt.figure(figsize=(16, 12))
        
        # Choose layout
        if layout == 'spring':
            pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)
        elif layout == 'hierarchical':
            pos = self._hierarchical_layout()
        elif layout == 'kamada':
            pos = nx.kamada_kawai_layout(self.graph)
        else:
            pos = nx.shell_layout(self.graph)
            
        # Get node colors
        node_colors = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get('type', 'DEFAULT')
            node_colors.append(NODE_COLORS.get(node_type, '#757575'))
            
        # Draw graph
        nx.draw_networkx_nodes(
            self.graph, pos,
            node_color=node_colors,
            node_size=600,
            alpha=0.8,
            edgecolors='white',
            linewidths=2
        )
        
        nx.draw_networkx_edges(
            self.graph, pos,
            alpha=0.4,
            arrows=True,
            arrowsize=15,
            arrowstyle='->',
            edge_color='#666666',
            width=1.5
        )
        
        # Draw labels for important nodes
        labels = {}
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            if node_data.get('type') in ['FUNC', 'IF', 'CALL']:
                label = node_data.get('label', '') or ''
                labels[node_id] = label[:25]
                
        nx.draw_networkx_labels(
            self.graph, pos, labels,

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.