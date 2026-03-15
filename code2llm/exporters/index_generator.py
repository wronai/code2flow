"""Index HTML Generator — web-based file browser for all generated outputs.

Generates index.html that provides a GitHub Pages-ready interface
for browsing all generated analysis files (toon, md, yaml, json, etc.)
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class IndexHTMLGenerator:
    """Generate index.html for browsing all generated files."""

    # File type detection and icons
    FILE_TYPES = {
        '.toon': {'icon': '📊', 'type': 'toon', 'name': 'TOON'},
        '.md': {'icon': '📝', 'type': 'markdown', 'name': 'Markdown'},
        '.yaml': {'icon': '⚙️', 'type': 'yaml', 'name': 'YAML'},
        '.yml': {'icon': '⚙️', 'type': 'yaml', 'name': 'YAML'},
        '.json': {'icon': '📋', 'type': 'json', 'name': 'JSON'},
        '.mmd': {'icon': '📈', 'type': 'mermaid', 'name': 'Mermaid'},
        '.txt': {'icon': '📄', 'type': 'text', 'name': 'Text'},
        '.html': {'icon': '🌐', 'type': 'html', 'name': 'HTML'},
        '.py': {'icon': '🐍', 'type': 'code', 'name': 'Python'},
        '.js': {'icon': '📜', 'type': 'code', 'name': 'JavaScript'},
        '.ts': {'icon': '📘', 'type': 'code', 'name': 'TypeScript'},
        '.go': {'icon': '🐹', 'type': 'code', 'name': 'Go'},
        '.rs': {'icon': '🦀', 'type': 'code', 'name': 'Rust'},
        '.java': {'icon': '☕', 'type': 'code', 'name': 'Java'},
    }

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir.resolve()

    def generate(self) -> Path:
        """Generate index.html in the output directory."""
        files = self._scan_files()
        html = self._render(files)
        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return index_path

    def _scan_files(self) -> List[Dict[str, Any]]:
        """Scan output directory for all generated files."""
        files = []
        
        for path in self.output_dir.rglob('*'):
            if not path.is_file():
                continue
            if path.name == 'index.html':
                continue
            
            rel_path = path.relative_to(self.output_dir)
            ext = path.suffix.lower()
            file_info = self.FILE_TYPES.get(ext, {'icon': '📄', 'type': 'unknown', 'name': ext[1:].upper() if ext else 'File'})
            
            # Read file content for preview
            content = self._read_file_content(path, file_info['type'])
            
            files.append({
                'name': path.name,
                'rel_path': str(rel_path),
                'path': str(rel_path).replace('/', ' / '),
                'size': self._format_size(path.stat().st_size),
                'icon': file_info['icon'],
                'type': file_info['type'],
                'type_name': file_info['name'],
                'content': content,
                'is_subdir': '/' in str(rel_path),
            })
        
        # Sort: root files first, then by type and name
        files.sort(key=lambda f: (f['is_subdir'], f['type'], f['name']))
        return files

    def _read_file_content(self, path: Path, file_type: str) -> str:
        """Read and escape file content for display."""
        try:
            if file_type in ('toon', 'markdown', 'yaml', 'json', 'text', 'mermaid', 'code'):
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    # Limit size
                    if len(content) > 100000:
                        content = content[:100000] + '\n\n... [truncated - file too large]'
                    return self._escape_html(content)
            return '[Binary file]'
        except Exception as e:
            return f'[Error reading file: {e}]'

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

    def _format_size(self, size: int) -> str:
        """Format file size for display."""
        if size < 1024:
            return f'{size}B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.1f}KB'
        else:
            return f'{size / (1024 * 1024):.1f}MB'

    def _render(self, files: List[Dict[str, Any]]) -> str:
        """Render the index.html page."""
        files_json = json.dumps(files, ensure_ascii=False)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>code2llm Analysis Results</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-hover: #334155;
            --border: #475569;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --success: #22c55e;
            --warning: #eab308;
            --error: #ef4444;
        }}
        
        @media (prefers-color-scheme: light) {{
            :root {{
                --bg: #f8fafc;
                --surface: #ffffff;
                --surface-hover: #f1f5f9;
                --border: #e2e8f0;
                --text: #1e293b;
                --text-muted: #64748b;
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            height: 100vh;
            overflow: hidden;
        }}
        
        .container {{
            display: grid;
            grid-template-columns: 320px 1fr;
            height: 100vh;
        }}
        
        /* Sidebar */
        .sidebar {{
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .header {{
            padding: 1.25rem;
            border-bottom: 1px solid var(--border);
        }}
        
        .header h1 {{
            font-size: 1.1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .header p {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}
        
        .search {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
        }}
        
        .search input {{
            width: 100%;
            padding: 0.5rem 0.75rem;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            color: var(--text);
            font-size: 0.875rem;
            outline: none;
        }}
        
        .search input:focus {{
            border-color: var(--accent);
        }}
        
        .search input::placeholder {{
            color: var(--text-muted);
        }}
        
        .file-list {{
            flex: 1;
            overflow-y: auto;
            padding: 0.5rem;
        }}
        
        .file-group {{
            margin-bottom: 1rem;
        }}
        
        .file-group-title {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            padding: 0.5rem 0.75rem;
            font-weight: 600;
        }}
        
        .file-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: background 0.15s;
            font-size: 0.875rem;
        }}
        
        .file-item:hover {{
            background: var(--surface-hover);
        }}
        
        .file-item.active {{
            background: var(--accent);
            color: white;
        }}
        
        .file-item.active .file-meta {{
            color: rgba(255,255,255,0.7);
        }}
        
        .file-icon {{
            font-size: 1rem;
            flex-shrink: 0;
        }}
        
        .file-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .file-name {{
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .file-meta {{
            font-size: 0.75rem;
            color: var(--text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .file-size {{
            font-size: 0.75rem;
            color: var(--text-muted);
            flex-shrink: 0;
        }}
        
        .empty-state {{
            padding: 2rem;
            text-align: center;
            color: var(--text-muted);
        }}
        
        /* Main content */
        .content {{
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .content-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.5rem;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
        }}
        
        .content-title {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .content-title h2 {{
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .content-actions {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .btn {{
            padding: 0.5rem 1rem;
            background: var(--surface-hover);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            color: var(--text);
            font-size: 0.875rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.15s;
        }}
        
        .btn:hover {{
            background: var(--border);
        }}
        
        .btn-primary {{
            background: var(--accent);
            border-color: var(--accent);
        }}
        
        .btn-primary:hover {{
            background: var(--accent-hover);
        }}
        
        .content-body {{
            flex: 1;
            overflow: auto;
            padding: 1.5rem;
        }}
        
        .welcome {{
            max-width: 600px;
            margin: 2rem auto;
            text-align: center;
        }}
        
        .welcome h2 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .welcome p {{
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            max-width: 400px;
            margin: 0 auto;
        }}
        
        .stat-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        
        pre {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1rem;
            overflow-x: auto;
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            font-size: 0.875rem;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        
        /* Mobile responsive */
        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
                grid-template-rows: auto 1fr;
            }}
            
            .sidebar {{
                border-right: none;
                border-bottom: 1px solid var(--border);
                max-height: 40vh;
            }}
            
            .file-list {{
                display: flex;
                flex-wrap: nowrap;
                overflow-x: auto;
                gap: 0.25rem;
                padding: 0.5rem;
            }}
            
            .file-group {{
                display: flex;
                flex-direction: row;
                margin: 0;
            }}
            
            .file-group-title {{
                display: none;
            }}
            
            .file-item {{
                flex-direction: column;
                min-width: 80px;
                padding: 0.5rem;
                text-align: center;
            }}
            
            .file-info {{
                display: none;
            }}
            
            .file-size {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="header">
                <h1>🔍 code2llm</h1>
                <p>Analysis Results Browser</p>
            </div>
            <div class="search">
                <input type="text" id="search" placeholder="Search files..." oninput="filterFiles(this.value)">
            </div>
            <div class="file-list" id="fileList">
                <!-- Files will be rendered here -->
            </div>
        </aside>
        
        <main class="content">
            <div class="content-header">
                <div class="content-title">
                    <span id="contentIcon">📁</span>
                    <h2 id="contentTitle">Welcome</h2>
                </div>
                <div class="content-actions" id="contentActions">
                    <!-- Actions will be rendered here -->
                </div>
            </div>
            <div class="content-body" id="contentBody">
                <div class="welcome">
                    <h2>Analysis Results</h2>
                    <p>Select a file from the sidebar to view its contents. This interface works on GitHub Pages without any server required.</p>
                    <div class="stats-grid" id="statsGrid">
                        <!-- Stats will be rendered here -->
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const files = {files_json};
        let currentFile = null;

        function renderFileList(filter = '') {{
            const list = document.getElementById('fileList');
            const filtered = files.filter(f => 
                f.name.toLowerCase().includes(filter.toLowerCase()) ||
                f.path.toLowerCase().includes(filter.toLowerCase())
            );
            
            if (filtered.length === 0) {{
                list.innerHTML = '<div class="empty-state">No files found</div>';
                return;
            }}
            
            // Group by type
            const groups = {{}};
            for (const file of filtered) {{
                const type = file.type_name;
                if (!groups[type]) groups[type] = [];
                groups[type].push(file);
            }}
            
            let html = '';
            for (const [typeName, groupFiles] of Object.entries(groups)) {{
                html += `
                    <div class="file-group">
                        <div class="file-group-title">${{typeName}} Files (${{groupFiles.length}})</div>
                        ${{groupFiles.map(f => `
                            <div class="file-item ${{currentFile?.name === f.name ? 'active' : ''}}" 
                                 onclick="selectFile('${{f.name}}')">
                                <span class="file-icon">${{f.icon}}</span>
                                <div class="file-info">
                                    <div class="file-name">${{f.name}}</div>
                                    <div class="file-meta">${{f.path}}</div>
                                </div>
                                <span class="file-size">${{f.size}}</span>
                            </div>
                        `).join('')}}
                    </div>
                `;
            }}
            
            list.innerHTML = html;
        }}

        function selectFile(name) {{
            const file = files.find(f => f.name === name);
            if (!file) return;
            
            currentFile = file;
            
            document.getElementById('contentIcon').textContent = file.icon;
            document.getElementById('contentTitle').textContent = file.name;
            
            // Actions
            const actions = document.getElementById('contentActions');
            actions.innerHTML = `
                <a href="${{file.rel_path}}" download class="btn">⬇ Download</a>
                <a href="${{file.rel_path}}" target="_blank" class="btn btn-primary">↗ Open Raw</a>
            `;
            
            // Content
            const body = document.getElementById('contentBody');
            if (file.type === 'markdown' || file.type === 'html') {{
                // For markdown, show formatted but also offer raw view
                body.innerHTML = `<pre>${{file.content}}</pre>`;
            }} else if (file.type === 'json') {{
                try {{
                    const json = JSON.parse(file.content.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'));
                    body.innerHTML = `<pre>${{JSON.stringify(json, null, 2)}}</pre>`;
                }} catch {{
                    body.innerHTML = `<pre>${{file.content}}</pre>`;
                }}
            }} else {{
                body.innerHTML = `<pre>${{file.content}}</pre>`;
            }}
            
            renderFileList(document.getElementById('search').value);
        }}

        function filterFiles(query) {{
            renderFileList(query);
        }}

        function renderStats() {{
            const stats = {{}};
            for (const f of files) {{
                stats[f.type_name] = (stats[f.type_name] || 0) + 1;
            }}
            
            const grid = document.getElementById('statsGrid');
            grid.innerHTML = Object.entries(stats)
                .sort((a, b) => b[1] - a[1])
                .map(([type, count]) => `
                    <div class="stat-card">
                        <div class="stat-value">${{count}}</div>
                        <div class="stat-label">${{type}}</div>
                    </div>
                `).join('');
        }}

        // Initialize
        renderStats();
        renderFileList();
        
        // Select first file if available
        if (files.length > 0) {{
            selectFile(files[0].name);
        }}
    </script>
</body>
</html>'''
