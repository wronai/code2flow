## Cel refaktoryzacji
Move method `template_dir, result, self` from module `prompt_engine` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (template_dir, result, self) are used together in multiple functions: code2flow.refactor.prompt_engine.PromptEngine.__init__, code2flow.refactor.prompt_engine.__init__.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `prompt_engine`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/refactor/prompt_engine.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def __init__(self, result: AnalysisResult, template_dir: Optional[str] = None):
        if template_dir is None:
            # Default to templates directory relative to this file
            template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
            
        self.result = result
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        
        # Initialize tiktoken for context management
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base") # GPT-4/3.5-turbo encoding
        except Exception:
            self.encoding = None
            
        # Initialize tree-sitter for precision extraction
        try:
            self.PY_LANGUAGE = Language(tree_sitter_python.language())
            self.parser = Parser(self.PY_LANGUAGE)
        except Exception:
            self.parser = None
        
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.