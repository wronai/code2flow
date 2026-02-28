## Cel refaktoryzacji
Move method `file_path, class_name, result, self, node, lines, module_name` from module `analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (file_path, class_name, result, self, node, lines, module_name) are used together in multiple functions: code2flow.core.analyzer.FileAnalyzer._process_function, code2flow.core.analyzer._process_function.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `analyzer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

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
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.