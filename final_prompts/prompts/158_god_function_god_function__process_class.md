## Cel refaktoryzacji
Extract logic from `_process_class` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_process_class' is highly complex: CC=1, fan-out=7, mutations=10.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 231+)

## Kod źródłowy do refaktoryzacji
```python
    def _process_class(self, node: ast.ClassDef, file_path: str, module_name: str, 
                       result: Dict, lines: List[str]) -> None:
        """Process class definition."""
        class_name = node.name
        qualified_name = f"{module_name}.{class_name}"
        
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
                method_name = item.name
                qualified_method = f"{qualified_name}.{method_name}"
                methods.append(qualified_method)
                self._process_function(item, file_path, module_name, result, lines, class_name)
        
        result['classes'][qualified_name] = ClassInfo(
            name=class_name,
            qualified_name=qualified_name,
            file=file_path,
            line=node.lineno,
            module=module_name,
            bases=[self._get_base_name(b) for b in node.bases],
            methods=methods,
            docstring=ast.get_docstring(node),
        )
        result['module'].classes.append(qualified_name)
        self.stats['classes_found'] += 1
    
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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _process_class. Skup się na wydzieleniu operacji o największej liczbie mutacji.