## Cel refaktoryzacji
Extract logic from `_hierarchical_layout` to a new method/function.

## Powód (z analizy DFG)
- Function '_hierarchical_layout' has high complexity: fan-out=6, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/visualizers/graph.py (linie 175-195)

## Kod źródłowy do refaktoryzacji
```python
    def _hierarchical_layout(self) -> Dict:
        """Create hierarchical layout grouped by function."""
        from collections import defaultdict
        
        # Group nodes by function
        function_groups = defaultdict(list)
        for node_id, node in self.result.nodes.items():
            func = node.function or '__global__'
            function_groups[func].append(node_id)
            
        # Position nodes
        pos = {}
        y_offset = 0
        
        for func_name, nodes in sorted(function_groups.items()):
            for i, node_id in enumerate(nodes):
                x = i * 2
                y = -y_offset
                pos[node_id] = (x, y)
            y_offset += 3
            
        return pos

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _hierarchical_layout. Skup się na wydzieleniu operacji o największej liczbie mutacji.