"""HTML Dashboard Generator — web visualization with trend charts.

Generates dashboard.html from project.yaml data.
Includes: metric cards, evolution chart, module CC bar chart,
alerts table, hotspots table, refactoring priorities.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class HTMLDashboardGenerator:
    """Generate dashboard.html from project.yaml data."""

    def generate(self, data: Dict[str, Any], output_path: str) -> None:
        html = self._render(data)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def _render(self, data: Dict[str, Any]) -> str:
        proj = data.get("project", {})
        health = data.get("health", {})
        modules = data.get("modules", [])
        hotspots = data.get("hotspots", [])
        refactoring = data.get("refactoring", {})
        evolution = data.get("evolution", [])
        stats = proj.get("stats", {})

        health_color, health_label = self._health_verdict(health)
        evo_chart = self._build_evolution_section(evolution)
        mod_chart = self._build_module_chart_data(modules)
        alerts_html = self._build_alerts_html(health)
        hotspots_html = self._build_hotspots_html(hotspots)
        refactor_html = self._build_refactoring_html(refactoring)

        cc_avg = health.get("cc_avg", 0)

        return self._assemble_html(
            proj=proj, stats=stats, health=health,
            cc_avg=cc_avg, health_color=health_color, health_label=health_label,
            evo_chart=evo_chart, mod_chart=mod_chart,
            alerts_html=alerts_html, hotspots_html=hotspots_html,
            hotspots=hotspots, refactor_html=refactor_html,
            refactoring=refactoring,
        )

    # ------------------------------------------------------------------
    # data builders
    # ------------------------------------------------------------------
    @staticmethod
    def _health_verdict(health: Dict) -> tuple:
        cc_avg = health.get("cc_avg", 0)
        if cc_avg <= 5:
            return "#22c55e", "Good"
        elif cc_avg <= 8:
            return "#eab308", "Warning"
        return "#ef4444", "Critical"

    @staticmethod
    def _build_evolution_section(evolution: List[Dict]) -> Dict[str, Any]:
        """Build evolution chart data, or metric cards if <3 data points."""
        evo_dates = [e.get("date", "") for e in evolution]
        evo_cc = [e.get("cc_avg", 0) for e in evolution]
        evo_crit = [e.get("critical", 0) for e in evolution]
        use_chart = len(evolution) >= 3
        return {
            "dates": evo_dates, "cc": evo_cc, "crit": evo_crit,
            "use_chart": use_chart, "entries": evolution,
        }

    @staticmethod
    def _build_module_chart_data(modules: List[Dict]) -> Dict[str, Any]:
        top = sorted(modules, key=lambda m: m.get("cc_max", 0), reverse=True)[:15]
        return {
            "names": [Path(m.get("path", "")).name for m in top],
            "cc": [m.get("cc_max", 0) for m in top],
        }

    @staticmethod
    def _build_alerts_html(health: Dict) -> str:
        html = ""
        for a in health.get("alerts", [])[:15]:
            sev = a.get("severity", "warning")
            sev_class = sev if sev in ("critical", "error", "warning") else "warning"
            html += f"""
            <tr class="{sev_class}">
                <td><span class="badge {sev_class}">{sev}</span></td>
                <td>{a.get('target', '?')}</td>
                <td>{a.get('type', '?')}</td>
                <td>{a.get('value', '?')}</td>
                <td>{a.get('limit', '?')}</td>
            </tr>"""
        return html

    @staticmethod
    def _build_hotspots_html(hotspots: List[Dict]) -> str:
        html = ""
        for h in hotspots[:10]:
            html += f"""
            <tr>
                <td><strong>{h.get('name', '?')}</strong></td>
                <td>{h.get('fan_out', 0)}</td>
                <td>{h.get('note', '')}</td>
            </tr>"""
        return html

    @staticmethod
    def _build_refactoring_html(refactoring: Dict) -> str:
        html = ""
        for i, p in enumerate(refactoring.get("priorities", [])[:10], 1):
            impact_class = p.get("impact", "low")
            html += f"""
            <tr>
                <td>{i}</td>
                <td>{p.get('action', '?')}</td>
                <td><span class="badge {impact_class}">{p.get('impact', '?')}</span></td>
                <td>{p.get('effort', '?')}</td>
            </tr>"""
        return html

    # ------------------------------------------------------------------
    # HTML assembly
    # ------------------------------------------------------------------
    def _assemble_html(self, **ctx) -> str:
        proj = ctx["proj"]
        stats = ctx["stats"]
        health = ctx["health"]
        cc_avg = ctx["cc_avg"]
        health_color = ctx["health_color"]
        health_label = ctx["health_label"]
        evo = ctx["evo_chart"]
        mod = ctx["mod_chart"]
        alerts_html = ctx["alerts_html"]
        hotspots_html = ctx["hotspots_html"]
        hotspots = ctx["hotspots"]
        refactor_html = ctx["refactor_html"]
        refactoring = ctx["refactoring"]

        evo_section = self._render_evolution_section(evo)
        evo_script = self._render_evolution_script(evo)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{proj.get('name', 'Project')} — Health Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
  :root {{
    --bg: #0f172a; --surface: #1e293b; --border: #334155;
    --text: #e2e8f0; --muted: #94a3b8;
    --green: #22c55e; --yellow: #eab308; --red: #ef4444; --blue: #3b82f6;
    --orange: #f97316;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{
      --bg: #f8fafc; --surface: #ffffff; --border: #e2e8f0;
      --text: #1e293b; --muted: #64748b;
    }}
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: 'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--text); padding:2rem; }}
  h1 {{ font-size:1.5rem; margin-bottom:.5rem; }}
  h2 {{ font-size:1.1rem; color:var(--muted); margin:1.5rem 0 .75rem; border-bottom:1px solid var(--border); padding-bottom:.25rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1rem; margin:1rem 0; }}
  .card {{ background:var(--surface); border:1px solid var(--border); border-radius:.5rem; padding:1rem; }}
  .card .value {{ font-size:1.8rem; font-weight:700; }}
  .card .label {{ color:var(--muted); font-size:.8rem; text-transform:uppercase; }}
  .chart-container {{ background:var(--surface); border:1px solid var(--border); border-radius:.5rem; padding:1rem; margin:1rem 0; }}
  .table-wrap {{ overflow-x:auto; }}
  table {{ width:100%; border-collapse:collapse; font-size:.85rem; }}
  th {{ text-align:left; color:var(--muted); padding:.5rem; border-bottom:1px solid var(--border); white-space:nowrap; }}
  td {{ padding:.5rem; border-bottom:1px solid var(--border); }}
  .badge {{ padding:.15rem .5rem; border-radius:.25rem; font-size:.75rem; font-weight:600; }}
  .badge.critical {{ background:var(--red); color:#fff; }}
  .badge.error {{ background:var(--orange); color:#fff; }}
  .badge.warning {{ background:var(--yellow); color:#000; }}
  .badge.high {{ background:var(--red); color:#fff; }}
  .badge.medium {{ background:var(--yellow); color:#000; }}
  .badge.low {{ background:var(--green); color:#fff; }}
  tr.critical td {{ background:rgba(239,68,68,.08); }}
  tr.error td {{ background:rgba(249,115,22,.06); }}
  tr.warning td {{ background:rgba(234,179,8,.05); }}
  .health-indicator {{ display:inline-block; width:12px; height:12px; border-radius:50%; margin-right:.5rem; }}
  .two-col {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }}
  .evo-cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:.75rem; }}
  .evo-cards .card {{ text-align:center; }}
  .trend {{ font-size:.75rem; color:var(--muted); }}
  @media (max-width:768px) {{ .two-col {{ grid-template-columns:1fr; }} }}
  footer {{ margin-top:2rem; color:var(--muted); font-size:.75rem; text-align:center; }}
</style>
</head>
<body>
<h1>
  <span class="health-indicator" style="background:{health_color}"></span>
  {proj.get('name', 'Project')} — {health_label}
</h1>
<p style="color:var(--muted);font-size:.85rem;">
  Analyzed {proj.get('analyzed_at', '?')[:10]} by code2llm
</p>

<div class="grid">
  <div class="card"><div class="value">{cc_avg}</div><div class="label">Avg CC</div></div>
  <div class="card"><div class="value">{health.get('critical_count', 0)}</div><div class="label">Critical (CC≥{health.get('critical_limit', 10)})</div></div>
  <div class="card"><div class="value">{stats.get('functions', 0)}</div><div class="label">Functions</div></div>
  <div class="card"><div class="value">{stats.get('classes', 0)}</div><div class="label">Classes</div></div>
  <div class="card"><div class="value">{stats.get('files', 0)}</div><div class="label">Files</div></div>
  <div class="card"><div class="value">{stats.get('lines', 0)}</div><div class="label">Lines</div></div>
  <div class="card"><div class="value">{health.get('duplicates', 0)}</div><div class="label">Duplicates</div></div>
  <div class="card"><div class="value">{health.get('cycles', 0)}</div><div class="label">Cycles</div></div>
</div>

<div class="two-col">
  {evo_section}
  <div class="chart-container">
    <h2 style="border:none;margin:0 0 .5rem;">Module CC (top 15)</h2>
    <canvas id="modChart" height="200"></canvas>
  </div>
</div>

<h2>Alerts ({len(health.get('alerts', []))})</h2>
<div class="card"><div class="table-wrap">
<table>
  <thead><tr><th>Severity</th><th>Target</th><th>Type</th><th>Value</th><th>Limit</th></tr></thead>
  <tbody>{alerts_html if alerts_html else '<tr><td colspan="5" style="color:var(--muted)">No alerts</td></tr>'}</tbody>
</table>
</div></div>

<div class="two-col">
<div>
<h2>Hotspots ({len(hotspots)})</h2>
<div class="card"><div class="table-wrap">
<table>
  <thead><tr><th>Function</th><th>Fan-out</th><th>Note</th></tr></thead>
  <tbody>{hotspots_html if hotspots_html else '<tr><td colspan="3" style="color:var(--muted)">No hotspots</td></tr>'}</tbody>
</table>
</div></div>
</div>

<div>
<h2>Refactoring Priorities ({len(refactoring.get('priorities', []))})</h2>
<div class="card"><div class="table-wrap">
<table>
  <thead><tr><th>#</th><th>Action</th><th>Impact</th><th>Effort</th></tr></thead>
  <tbody>{refactor_html if refactor_html else '<tr><td colspan="4" style="color:var(--muted)">No refactoring needed</td></tr>'}</tbody>
</table>
</div></div>
</div>
</div>

<footer>Generated by code2llm on {datetime.now().strftime('%Y-%m-%d %H:%M')}</footer>

<script>
{evo_script}

const modCtx = document.getElementById('modChart').getContext('2d');
new Chart(modCtx, {{
  type: 'bar',
  data: {{
    labels: {mod["names"]},
    datasets: [{{ label: 'Max CC', data: {mod["cc"]},
      backgroundColor: {mod["cc"]}.map(v => v >= 15 ? '#ef4444' : v >= 10 ? '#eab308' : '#22c55e')
    }}]
  }},
  options: {{
    responsive: true, indexAxis: 'y',
    scales: {{
      x: {{ grid:{{color:'#334155'}}, ticks:{{color:'#94a3b8'}} }},
      y: {{ grid:{{color:'#334155'}}, ticks:{{color:'#94a3b8',font:{{size:10}}}} }}
    }},
    plugins: {{ legend: {{ display:false }} }}
  }}
}});
</script>
</body>
</html>"""

    # ------------------------------------------------------------------
    # evolution section: chart (≥3 points) or metric cards (<3 points)
    # ------------------------------------------------------------------
    @staticmethod
    def _render_evolution_section(evo: Dict) -> str:
        if evo["use_chart"]:
            return """<div class="chart-container">
    <h2 style="border:none;margin:0 0 .5rem;">Evolution</h2>
    <canvas id="evoChart" height="200"></canvas>
  </div>"""

        # <3 data points — show metric cards with trend arrows
        entries = evo["entries"]
        if not entries:
            return """<div class="chart-container">
    <h2 style="border:none;margin:0 0 .5rem;">Evolution</h2>
    <p style="color:var(--muted);">No history yet. Run analysis again to build trend data.</p>
  </div>"""

        last = entries[-1]
        prev = entries[-2] if len(entries) >= 2 else None
        cc = last.get("cc_avg", 0)
        crit = last.get("critical", 0)
        lines = last.get("lines", 0)

        def trend(cur, prv_val):
            if prv_val is None:
                return "→"
            if cur < prv_val:
                return "↓"
            if cur > prv_val:
                return "↑"
            return "→"

        cc_trend = trend(cc, prev.get("cc_avg") if prev else None)
        crit_trend = trend(crit, prev.get("critical") if prev else None)

        return f"""<div class="chart-container">
    <h2 style="border:none;margin:0 0 .5rem;">Evolution ({last.get('date', '?')})</h2>
    <div class="evo-cards">
      <div class="card"><div class="value">{cc}</div><div class="label">CC̄ {cc_trend}</div></div>
      <div class="card"><div class="value">{crit}</div><div class="label">Critical {crit_trend}</div></div>
      <div class="card"><div class="value">{lines}</div><div class="label">Lines</div></div>
    </div>
    <p class="trend" style="margin-top:.5rem;">Run analysis multiple times to build a trend chart (≥3 data points needed).</p>
  </div>"""

    @staticmethod
    def _render_evolution_script(evo: Dict) -> str:
        if not evo["use_chart"]:
            return "// Evolution chart disabled — fewer than 3 data points"
        return f"""const evoCtx = document.getElementById('evoChart').getContext('2d');
new Chart(evoCtx, {{
  type: 'line',
  data: {{
    labels: {evo["dates"]},
    datasets: [
      {{ label: 'CC avg', data: {evo["cc"]}, borderColor: '#3b82f6', tension: .3, yAxisID: 'y' }},
      {{ label: 'Critical', data: {evo["crit"]}, borderColor: '#ef4444', tension: .3, yAxisID: 'y1' }}
    ]
  }},
  options: {{
    responsive: true,
    scales: {{
      y: {{ position:'left', grid:{{color:'#334155'}}, ticks:{{color:'#94a3b8'}} }},
      y1: {{ position:'right', grid:{{drawOnChartArea:false}}, ticks:{{color:'#94a3b8'}} }},
      x: {{ ticks:{{color:'#94a3b8'}}, grid:{{color:'#334155'}} }}
    }},
    plugins: {{ legend: {{ labels: {{ color:'#e2e8f0' }} }} }}
  }}
}});"""
