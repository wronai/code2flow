## Cel refaktoryzacji
Extract logic from `self, func_info, func_name, result, node` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, func_info, func_name, result, node) are used together in multiple functions: code2flow.core.analyzer.FileAnalyzer._build_cfg, code2flow.core.analyzer._build_cfg.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 289-309)

## Kod źródłowy do refaktoryzacji
```python
    def _build_cfg(self, node: ast.FunctionDef, func_name: str, 
                   func_info: FunctionInfo, result: Dict) -> None:
        """Build simplified control flow graph with depth limit."""
        max_depth = self.config.depth.max_cfg_depth
        
        entry_id = f"{func_name}_entry"
        exit_id = f"{func_name}_exit"
        
        # Create entry/exit nodes
        result['nodes'][entry_id] = FlowNode(
            id=entry_id, type='ENTRY', label='entry', function=func_name
        )
        result['nodes'][exit_id] = FlowNode(
            id=exit_id, type='EXIT', label='exit', function=func_name
        )
        
        func_info.cfg_entry = entry_id
        func_info.cfg_exit = exit_id
        
        # Build CFG with depth limiting
        self._process_cfg_block(node.body, entry_id, exit_id, func_name, 
                               result, depth=0, max_depth=max_depth)
        
        self.stats['nodes_created'] += len(result['nodes'])
    
    def _process_cfg_block(self, body: List[ast.stmt], entry: str, exit: str,
                            func_name: str, result: Dict, depth: int, max_depth: int) -> str:
        """Process a block of statements for CFG with depth limiting."""
        if depth >= max_depth:
            # Connect directly to exit if depth exceeded
            result['edges'].append(FlowEdge(source=entry, target=exit))
            return exit
        
        current = entry
        for stmt in body:
            if isinstance(stmt, ast.If):
                # Create branch node
                node_id = f"{func_name}_if_{stmt.lineno}"
                result['nodes'][node_id] = FlowNode(
                    id=node_id, type='IF', label='if', function=func_name,
                    line=stmt.lineno
                )
                result['edges'].append(FlowEdge(source=current, target=node_id))
                
                # Process branches
                then_exit = self._process_cfg_block(
                    stmt.body, node_id, exit, func_name, result, depth + 1, max_depth
                )
                if stmt.orelse:
                    else_exit = self._process_cfg_block(

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.