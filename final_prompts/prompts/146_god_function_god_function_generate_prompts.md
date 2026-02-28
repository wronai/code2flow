## Cel refaktoryzacji
Extract logic from `generate_prompts` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'generate_prompts' is highly complex: CC=1, fan-out=7, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py (linie 34+)

## Kod źródłowy do refaktoryzacji
```python
    def generate_prompts(self) -> Dict[str, str]:
        """Generate a prompt for each detected code smell."""
        prompts = {}
        
        for i, smell in enumerate(self.result.smells):
            prompt = self._generate_prompt_for_smell(smell)
            if prompt:
                # Truncate prompt if it exceeds token limit (e.g., 4000 tokens)
                if self.encoding:
                    tokens = self.encoding.encode(prompt)
                    if len(tokens) > 4000:
                        prompt = self.encoding.decode(tokens[:3800]) + "\n\n... (prompt truncated due to length) ..."
                
                # Use a unique name for each prompt
                filename = f"{i+1:02d}_{smell.type}_{smell.name.lower().replace(' ', '_').replace(':', '')}.md"
                prompts[filename] = prompt
        return prompts
        
    def _generate_prompt_for_smell(self, smell: CodeSmell) -> Optional[str]:
        """Generate a single prompt from a CodeSmell."""
        template_name = self._get_template_for_type(smell.type)
        if not template_name:
            return None
            
        try:
            template = self.env.get_template(template_name)
            context = self._build_context_for_smell(smell)
            return template.render(**context)
        except Exception as e:
            print(f"Error generating prompt for {smell.name}: {e}")
            return None
            
    def _get_template_for_type(self, smell_type: str) -> Optional[str]:
        """Map smell type to Jinja2 template filename."""
        mapping = {
            "god_function": "extract_method.md",
            "feature_envy": "move_method.md",
            "data_clump": "move_method.md", 
            "shotgun_surgery": "extract_method.md",
            "bottleneck": "extract_method.md",
            "circular_dependency": "move_method.md"
        }
        return mapping.get(smell_type)
        
    def _build_context_for_smell(self, smell: CodeSmell) -> Dict[str, Any]:
        """Prepare context data for the Jinja2 template."""
        # Extract source code for context
        source_code = self._get_source_context(smell.file, smell.line)
        
        # Prepare metrics
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji generate_prompts. Skup się na wydzieleniu operacji o największej liczbie mutacji.