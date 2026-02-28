## Cel refaktoryzacji
Extract logic from `__init__` to a new method/function.

## Powód (Głęboka Analiza)
- Function '__init__' is highly complex: CC=1, fan-out=1, mutations=9.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/cfg.py (linie 14+)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, config: Config):
        self.config = config
        self.result = AnalysisResult()
        self.module_name = ""
        self.file_path = ""
        self.node_counter = 0
        
        # Context tracking
        self.function_stack = []
        self.class_stack = []
        self.current_node = None
        self.entry_nodes = {}  # Function -> entry node ID
        
    def extract(self, tree: ast.AST, module_name: str, file_path: str) -> AnalysisResult:
        """Extract CFG from AST."""
        self.result = AnalysisResult()
        self.module_name = module_name
        self.file_path = file_path
        self.node_counter = 0
        
        self.visit(tree)
        return self.result
        
    def new_node(self, node_type: str, label: str, **kwargs) -> int:
        """Create new flow node."""
        node_id = self.node_counter
        self.node_counter += 1
        
        node = FlowNode(
            id=node_id,
            type=node_type,
            label=label,
            function=self.function_stack[-1] if self.function_stack else None,
            file=self.file_path,
            line=kwargs.get('line'),
            column=kwargs.get('column'),
            conditions=kwargs.get('conditions', []),
            data_flow=kwargs.get('data_flow', [])
        )
        
        self.result.nodes[node_id] = node
        return node_id
        
    def connect(self, source: Optional[int], target: Optional[int], 
                edge_type: str = "control", condition: Optional[str] = None):
        """Create edge between nodes."""
        if source is not None and target is not None:
            edge = FlowEdge(
                source=source,
                target=target,
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji __init__. Skup się na wydzieleniu operacji o największej liczbie mutacji.