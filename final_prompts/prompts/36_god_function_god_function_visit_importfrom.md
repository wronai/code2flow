## Cel refaktoryzacji
Extract logic from `visit_ImportFrom` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'visit_ImportFrom' is highly complex: CC=1, fan-out=0, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/call_graph.py (linie 71+)

## Kod źródłowy do refaktoryzacji
```python
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Track from imports."""
        module = node.module or ""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports[name] = full_name
            self.result.imports[name] = full_name
            
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definition."""
        self.class_stack.append(node.name)
        
        # Store class info
        self.result.classes[node.name] = {
            'file': self.file_path,
            'line': node.lineno,
            'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
            'bases': [self._expr_to_str(b) for b in node.bases]
        }
        
        for stmt in node.body:
            self.visit(stmt)
            
        self.class_stack.pop()
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definition and track calls within it."""
        func_name = self._qualified_name(node.name)
        self.function_stack.append(func_name)
        
        # Visit body to find calls
        for stmt in node.body:
            self.visit(stmt)
            
        self.function_stack.pop()
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visit async function."""
        self.visit_FunctionDef(node)
        
    def visit_Call(self, node: ast.Call):
        """Track function calls."""
        if not self.function_stack:
            self.generic_visit(node)
            return
            
        caller = self.function_stack[-1]
        callee = self._resolve_call(node.func)
        
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji visit_ImportFrom. Skup się na wydzieleniu operacji o największej liczbie mutacji.