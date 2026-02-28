## Cel refaktoryzacji
Extract logic from `render_llm_flow_md` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'render_llm_flow_md' is highly complex: CC=10, fan-out=12, mutations=30.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 332+)

## Kod źródłowy do refaktoryzacji
```python
def render_llm_flow_md(flow: Dict[str, Any]) -> str:
    app = _as_dict(flow.get("app"))
    entrypoints = _as_list(app.get("entrypoints"))
    selected = _as_list(_as_dict(flow.get("flow")).get("selected_functions"))

    lines: List[str] = []
    lines.append("# LLM Flow Summary")
    lines.append("")

    pkgs = _as_list(app.get("packages"))
    if pkgs:
        lines.append("## Packages")
        for p in pkgs:
            lines.append(f"- {p}")
        lines.append("")

    if entrypoints:
        lines.append("## Entrypoints")
        for ep in entrypoints:
            epd = _as_dict(ep)
            fn = epd.get("function")
            f = epd.get("file")
            ln = epd.get("line")
            lines.append(f"- {fn} ({f}:{ln})")
        lines.append("")

    lines.append("## Selected functions")
    for f in selected:
        fd = _as_dict(f)
        name = fd.get("name")
        file = fd.get("file")
        line = fd.get("line")
        lines.append(f"### {name}")
        lines.append(f"- Location: {file}:{line}")

        decisions = _as_list(fd.get("decisions"))
        if decisions:
            lines.append("- Decisions:")
            for d in decisions:
                lines.append(f"  - {_shorten(str(d), 180)}")

        calls = _as_list(fd.get("calls"))
        if calls:
            lines.append("- Calls:")
            for c in calls:
                lines.append(f"  - {c}")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji render_llm_flow_md. Skup się na wydzieleniu operacji o największej liczbie mutacji.