## Cel refaktoryzacji
Move method `_process_function` from module `analyzer` to `func_info`.

## Powód (z analizy DFG)
- Function '_process_function' mutates multiple variables in other modules: func_info.calls, self.stats['functions_found'], result['module'].functions.
- Feature Envy: Accesses more data from `func_info` than `analyzer`.
- Foreign Mutatons: func_info.calls, self.stats['functions_found'], result['module'].functions

## Kontekst przepływu danych
- Zależności: 
- Mutacje w module docelowym: This code mutates state in result['module'], self, func_info

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def _process_function(self, node: ast.FunctionDef, file_path: str, module_name: str,
                          result: Dict, lines: List[str], class_name: Optional[str]) -> None:
        """Process function definition with limited CFG depth."""
        func_name = node.name
        if class_name:
            qualified_name = f"{module_name}.{class_name}.{func_name}"
        else:
            qualified_name = f"{module_name}.{func_name}"
        
        # Check filtering - use FastFileFilter for function-level filtering
        line_count = (node.end_lineno - node.lineno + 1) if node.end_lineno else 1
        is_private = func_name.startswith('_')
        is_property = any(
            isinstance(d, ast.Name) and d.id == 'property' 
            for d in node.decorator_list
        )
        
        filter_obj = FastFileFilter(self.config.filters)
        if filter_obj.should_skip_function(func_name, line_count, is_private, is_property):
            return
        
        # Create function info
        func_info = FunctionInfo(
            name=func_name,
            qualified_name=qualified_name,
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            module=module_name,
            class_name=class_name,
            is_method=class_name is not None,
            is_private=is_private,
            is_property=is_property,
            docstring=ast.get_docstring(node),
            args=[arg.arg for arg in node.args.args],
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
        )
        
        # Build simplified CFG with depth limit
        if not self.config.performance.skip_data_flow:
            self._build_cfg(node, qualified_name, func_info, result)
        
        # Find calls
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                called_name = self._get_call_name(child.func)
                if called_name:
                    func_info.calls.append(called_name)
        
        result['functions'][qualified_name] = func_info

```

## Instrukcja
Przenieś metodę _process_function do modułu, który posiada większość używanych w niej danych.