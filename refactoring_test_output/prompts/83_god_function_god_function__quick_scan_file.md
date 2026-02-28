## Cel refaktoryzacji
Extract logic from `_quick_scan_file` to a new method/function.

## Powód (z analizy DFG)
- Function '_quick_scan_file' has high complexity: fan-out=15, mutations=19.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 383-403)

## Kod źródłowy do refaktoryzacji
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
Wyekstrahuj mniejsze, spójne metody z funkcji _quick_scan_file. Skup się na wydzieleniu operacji o największej liczbie mutacji.