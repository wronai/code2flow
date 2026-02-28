## Cel refaktoryzacji
Move method `project_path, files, self` from module `streaming_analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (project_path, files, self) are used together in multiple functions: code2flow.core.streaming_analyzer.SmartPrioritizer.prioritize_files, code2flow.core.streaming_analyzer.SmartPrioritizer._build_import_graph, code2flow.core.streaming_analyzer.prioritize_files, code2flow.core.streaming_analyzer._build_import_graph.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `streaming_analyzer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def prioritize_files(
        self,
        files: List[Tuple[str, str]],
        project_path: Path
    ) -> List[FilePriority]:
        """Score and sort files by importance."""
        scored = []
        
        # First pass: gather import relationships
        import_graph = self._build_import_graph(files, project_path)
        
        for file_path, module_name in files:
            score = 0.0
            reasons = []
            
            # Check if has main
            has_main = self._check_has_main(file_path)
            if has_main:
                score += 100.0
                reasons.append("has_main")
            
            # Check if entry point (not imported by others)
            is_entry = module_name not in import_graph or len(import_graph[module_name]) == 0
            if is_entry:
                score += 50.0
                reasons.append("entry_point")
            
            # Check if public API (no underscore prefix)
            is_public = not any(part.startswith('_') for part in module_name.split('.'))
            if is_public:
                score += 20.0
                reasons.append("public_api")
            
            # Import count (more imports = more central)
            import_count = len(import_graph.get(module_name, []))
            score += import_count * 5.0
            
            # File size (prefer smaller files first for quick wins)
            try:
                loc = len(Path(file_path).read_text().split('\n'))
                if loc < 100:
                    score += 10.0
                    reasons.append("small_file")
            except:
                loc = 0
            
            priority = FilePriority(
                file_path=file_path,
                module_name=module_name,
                priority_score=score,
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.