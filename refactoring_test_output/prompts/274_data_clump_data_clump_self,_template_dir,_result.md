## Cel refaktoryzacji
Extract logic from `self, template_dir, result` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, template_dir, result) are used together in multiple functions: code2flow.refactor.prompt_engine.PromptEngine.__init__, code2flow.refactor.prompt_engine.__init__.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py (linie 10-30)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, result: AnalysisResult, template_dir: Optional[str] = None):
        if template_dir is None:
            # Default to templates directory relative to this file
            template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
            
        self.result = result
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        
    def generate_prompts(self) -> Dict[str, str]:
        """Generate a prompt for each detected code smell."""
        prompts = {}
        
        for i, smell in enumerate(self.result.smells):
            prompt = self._generate_prompt_for_smell(smell)
            if prompt:
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
            "data_clump": "extract_method.md", # Placeholder until extract_class.md exists
            "shotgun_surgery": "extract_method.md" # Placeholder
        }
        return mapping.get(smell_type)
        
    def _build_context_for_smell(self, smell: CodeSmell) -> Dict[str, Any]:
        """Prepare context data for the Jinja2 template."""
        # Extract source code for context
        source_code = self._get_source_context(smell.file, smell.line)
        
        # Prepare metrics

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.