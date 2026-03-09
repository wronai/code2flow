"""Language-specific analyzers for non-Python source files."""

from .typescript import analyze_typescript_js
from .go_lang import analyze_go
from .rust import analyze_rust
from .java import analyze_java
from .cpp import analyze_cpp
from .csharp import analyze_csharp
from .php import analyze_php
from .ruby import analyze_ruby
from .generic import analyze_generic
