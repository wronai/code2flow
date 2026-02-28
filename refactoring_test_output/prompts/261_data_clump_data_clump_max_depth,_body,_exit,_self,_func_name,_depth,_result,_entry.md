## Cel refaktoryzacji
Extract logic from `max_depth, body, exit, self, func_name, depth, result, entry` to a new method/function.

## Powód (z analizy DFG)
- Arguments (max_depth, body, exit, self, func_name, depth, result, entry) are used together in multiple functions: code2flow.core.analyzer.FileAnalyzer._process_cfg_block, code2flow.core.analyzer._process_cfg_block.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 314-334)

## Kod źródłowy do refaktoryzacji
```python
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
                        stmt.orelse, node_id, exit, func_name, result, depth + 1, max_depth
                    )
                else:
                    else_exit = node_id
                
                # Merge point
                current = f"{func_name}_merge_{stmt.lineno}"
                result['nodes'][current] = FlowNode(
                    id=current, type='FUNC', label='merge', function=func_name
                )
                result['edges'].append(FlowEdge(source=then_exit, target=current))
                if else_exit != node_id:
                    result['edges'].append(FlowEdge(source=else_exit, target=current))
            
            elif isinstance(stmt, (ast.For, ast.While)):
                node_id = f"{func_name}_loop_{stmt.lineno}"
                loop_type = 'FOR' if isinstance(stmt, ast.For) else 'WHILE'
                result['nodes'][node_id] = FlowNode(
                    id=node_id, type=loop_type, label=loop_type.lower(), 
                    function=func_name, line=stmt.lineno
                )
                result['edges'].append(FlowEdge(source=current, target=node_id))
                
                # Limit loop body depth even more
                self._process_cfg_block(

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.