## Cel refaktoryzacji
Extract logic from `to_dict` to a new method/function.

## Powód (z analizy DFG)
- Function 'to_dict' has high complexity: fan-out=10, mutations=46.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/models.py (linie 350-370)

## Kod źródłowy do refaktoryzacji
```python
    def to_dict(self, compact: bool = True) -> dict:
        """Convert entire result to dictionary."""
        return {
            "project_path": self.project_path,
            "analysis_mode": self.analysis_mode,
            "stats": self.stats,
            "nodes": {k: v.to_dict(compact) for k, v in self.nodes.items()} if self.nodes else {},
            "edges": [e.to_dict(compact) for e in self.edges] if self.edges else [],
            "modules": {k: v.to_dict(compact) for k, v in self.modules.items()} if self.modules else {},
            "classes": {k: v.to_dict(compact) for k, v in self.classes.items()} if self.classes else {},
            "functions": {k: v.to_dict(compact) for k, v in self.functions.items()} if self.functions else {},
            "patterns": [p.to_dict(compact) for p in self.patterns] if self.patterns else [],
            "call_graph": self.call_graph,
            "entry_points": self.entry_points,
            "data_flows": {k: v.to_dict() for k, v in self.data_flows.items()} if self.data_flows else {},
            "metrics": self.metrics if self.metrics else {},
            "smells": [s.to_dict() for s in self.smells] if self.smells else [],
            "coupling": self.coupling if self.coupling else {},
            "mutations": [m.to_dict() for m in self.mutations] if self.mutations else [],
        }
    
    def get_function_count(self) -> int:
        """Get total function count."""
        return len(self.functions)
    
    def get_class_count(self) -> int:
        """Get total class count."""
        return len(self.classes)
    
    def get_node_count(self) -> int:
        """Get total CFG node count."""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """Get total edge count."""
        return len(self.edges)

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji to_dict. Skup się na wydzieleniu operacji o największej liczbie mutacji.