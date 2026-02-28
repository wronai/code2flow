## Cel refaktoryzacji
Move method `compact, output_dir, result, self` from module `base` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (compact, output_dir, result, self) are used together in multiple functions: code2flow.exporters.base.YAMLExporter.export_separated, code2flow.exporters.base.export_separated.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `base`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def export_separated(self, result: AnalysisResult, output_dir: str, compact: bool = True) -> dict:
        """Export analysis separating consolidated project from orphaned functions.
        
        Creates two folders:
        - consolidated/ - functions connected to the main project structure
        - orphans/ - isolated functions not connected to main flows
        
        Returns statistics about the separation.
        """
        from collections import defaultdict
        
        output_path = Path(output_dir)
        consolidated_dir = output_path / 'consolidated'
        orphans_dir = output_path / 'orphans'
        consolidated_dir.mkdir(parents=True, exist_ok=True)
        orphans_dir.mkdir(parents=True, exist_ok=True)
        
        # Identify orphan functions
        # Orphans = no calls AND not called by anyone (isolated)
        # Or = called but caller is also orphan (dead code chain)
        
        consolidated_funcs = {}
        orphan_funcs = {}
        
        # First pass: identify clearly connected functions
        for func_name, func in result.functions.items():
            has_calls = len(func.calls) > 0
            is_called = len(func.called_by) > 0
            is_entry = func_name in result.entry_points
            
            if is_entry:
                # Entry points are always consolidated
                consolidated_funcs[func_name] = func
            elif has_calls and is_called:
                # Functions that both call and are called = consolidated
                consolidated_funcs[func_name] = func
            elif is_called and not has_calls:
                # Leaf functions (called but don't call) = consolidated
                consolidated_funcs[func_name] = func
            elif has_calls and not is_called:
                # Functions that call but aren't called = check if they call consolidated
                calls_consolidated = any(c in consolidated_funcs for c in func.calls)
                if calls_consolidated:
                    consolidated_funcs[func_name] = func
                else:
                    orphan_funcs[func_name] = func
            else:
                # No calls, not called = orphan
                orphan_funcs[func_name] = func
        
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.