## Cel refaktoryzacji
Move method `_quick_scan_file` from module `streaming_analyzer` to `func_info`.

## Powód (Głęboka Analiza)
- Function '_quick_scan_file' mutates multiple variables in other modules: func_info.calls, result['module'].classes, result['module'].functions.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `func_info` niż z `streaming_analyzer`.
- Obce Mutacje: func_info.calls, result['module'].classes, result['module'].functions

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in result['module'], func_info

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def _quick_scan_file(self, priority: FilePriority) -> Optional[Dict]:
        """Quick scan - extract functions and classes only (no CFG)."""
        try:
            content = Path(priority.file_path).read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return None
        
        # Try cache
        if self.cache:
            cached = self.cache.get(priority.file_path, content)
            if cached:
                tree, _ = cached
            else:
                try:
                    tree = ast.parse(content)
                    self.cache.put(priority.file_path, content, (tree, content))
                except SyntaxError:
                    return None
        else:
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return None
        
        result = {
            'module': ModuleInfo(
                name=priority.module_name,
                file=priority.file_path
            ),
            'functions': {},
            'classes': {},
            'nodes': {},
            'edges': []
        }
        
        lines = content.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                cls_info = ClassInfo(
                    name=node.name,
                    qualified_name=f"{priority.module_name}.{node.name}",
                    file=priority.file_path,
                    line=node.lineno,
                    module=priority.module_name
                )
                result['classes'][cls_info.qualified_name] = cls_info
                result['module'].classes.append(cls_info.qualified_name)
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
```

## Instrukcja
Przenieś metodę _quick_scan_file do modułu, który posiada większość używanych w niej danych. Zmniejsz coupling między modułami.