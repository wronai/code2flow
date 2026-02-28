## Cel refaktoryzacji
Extract logic from `visualize_call_graph` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visualize_call_graph' is highly complex: CC=1, fan-out=21, mutations=0.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/visualizers/graph.py (linie 114+)

## Kod źródłowy do refaktoryzacji
```python
    def visualize_call_graph(self, filepath: str):
        """Visualize call graph."""
        # Build call graph
        call_graph = nx.DiGraph()
        
        for func_name, func_info in self.result.functions.items():
            short_name = func_name.split('.')[-1]
            call_graph.add_node(func_name, label=short_name)
            
            for callee in func_info.calls:
                call_graph.add_edge(func_name, callee)
                
        if len(call_graph.nodes()) == 0:
            return  # Nothing to visualize
            
        plt.figure(figsize=(14, 10))
        
        # Layout
        pos = nx.spring_layout(call_graph, k=1.5, iterations=50, seed=42)
        
        # Node sizes based on calls
        node_sizes = []
        for node in call_graph.nodes():
            out_degree = call_graph.out_degree(node)
            in_degree = call_graph.in_degree(node)
            size = 300 + (out_degree + in_degree) * 150
            node_sizes.append(size)
            
        # Draw
        nx.draw_networkx_nodes(
            call_graph, pos,
            node_color='#4CAF50',
            node_size=node_sizes,
            alpha=0.8,
            edgecolors='white',
            linewidths=2
        )
        
        nx.draw_networkx_edges(
            call_graph, pos,
            alpha=0.5,
            arrows=True,
            arrowsize=20,
            edge_color='#2196F3',
            width=2
        )
        
        # Labels
        labels = {n: (call_graph.nodes[n].get('label') or n)[:20] for n in call_graph.nodes()}
        nx.draw_networkx_labels(
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visualize_call_graph. Skup się na wydzieleniu operacji o największej liczbie mutacji.