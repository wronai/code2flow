"""HTML Renderer — generates index.html with CSS and JavaScript."""

import json
from typing import Any, Dict, List


class HTMLRenderer:
    """Render the index.html page with CSS and JavaScript."""

    def render(self, files: List[Dict[str, Any]]) -> str:
        """Render the index.html page."""
        files_json = json.dumps(files, ensure_ascii=False)
        return self._TEMPLATE.format(files_json=files_json)

    _TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>code2llm Analysis Results</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"></script>
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
            gap: 0.75rem;
            padding: 0.625rem 0.75rem;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: all 0.15s ease;
            margin-bottom: 0.125rem;
        }}

        .file-item:hover {{
            background: var(--surface-hover);
        }}

        .file-item.active {{
            background: var(--accent);
            color: white;
        }}

        .file-item.active .file-meta {{
            color: rgba(255, 255, 255, 0.7);
        }}

        .file-icon {{
            font-size: 1.25rem;
            flex-shrink: 0;
        }}

        .file-info {{
            flex: 1;
            min-width: 0;
        }}

        .file-name {{
            font-size: 0.875rem;
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

        /* Content */
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
            border-bottom: 1px solid var(--border);
            background: var(--surface);
        }}

        .content-title {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .content-title h2 {{
            font-size: 1.125rem;
            font-weight: 600;
        }}

        .content-actions {{
            display: flex;
            gap: 0.5rem;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.5rem 1rem;
            background: var(--surface-hover);
            color: var(--text);
            text-decoration: none;
            border-radius: 0.375rem;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.15s ease;
            border: none;
            cursor: pointer;
        }}

        .btn:hover {{
            background: var(--border);
        }}

        .btn-primary {{
            background: var(--accent);
            color: white;
        }}

        .btn-primary:hover {{
            background: var(--accent-hover);
        }}

        .content-body {{
            flex: 1;
            overflow: auto;
            padding: 1.5rem;
        }}

        /* Welcome */
        .welcome {{
            max-width: 800px;
        }}

        .welcome h2 {{
            font-size: 1.5rem;
            margin-bottom: 0.75rem;
        }}

        .welcome p {{
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }}

        .stat-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
        }}

        .stat-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--accent);
        }}

        .stat-label {{
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}

        /* Content Display */
        pre {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1rem;
            overflow-x: auto;
            font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            font-size: 0.875rem;
            line-height: 1.6;
        }}

        code {{
            font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
        }}

        .markdown-content {{
            line-height: 1.7;
        }}

        .markdown-content h1,
        .markdown-content h2,
        .markdown-content h3 {{
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}

        .markdown-content h1 {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }}

        .markdown-content p {{
            margin-bottom: 1rem;
        }}

        .markdown-content code {{
            background: var(--surface);
            padding: 0.125rem 0.375rem;
            border-radius: 0.25rem;
            font-size: 0.875em;
        }}

        .markdown-content pre code {{
            background: transparent;
            padding: 0;
        }}

        .markdown-content ul,
        .markdown-content ol {{
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }}

        .markdown-content li {{
            margin-bottom: 0.25rem;
        }}

        .markdown-content blockquote {{
            border-left: 4px solid var(--accent);
            padding-left: 1rem;
            margin-left: 0;
            color: var(--text-muted);
        }}

        .markdown-content table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 1rem;
        }}

        .markdown-content th,
        .markdown-content td {{
            border: 1px solid var(--border);
            padding: 0.5rem;
            text-align: left;
        }}

        .markdown-content th {{
            background: var(--surface);
        }}

        .markdown-content img {{
            max-width: 100%;
            border-radius: 0.5rem;
        }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
        }}

        /* Mermaid */
        .mermaid-content {{
            background: var(--surface);
            border-radius: 0.5rem;
            padding: 1rem;
        }}

        .mermaid-content pre {{
            background: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }}

        /* Image Preview */
        .image-preview {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            background: var(--surface);
            border-radius: 0.5rem;
            padding: 1rem;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
            }}

            .sidebar {{
                display: none;
            }}

            .sidebar.open {{
                display: flex;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: 100;
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
        // Initialize mermaid
        mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});

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
            if (file.type === 'markdown') {{
                // Render markdown as HTML using marked.js
                body.innerHTML = `<div class="markdown-content">${{marked.parse(file.content)}}</div>`;
            }} else if (file.type === 'html') {{
                // For HTML files, show in iframe for safety
                body.innerHTML = `<iframe src="${{file.rel_path}}" style="width:100%;height:100%;border:none;border-radius:0.5rem;"></iframe>`;
            }} else if (file.type === 'image') {{
                // For images, display the actual image
                body.innerHTML = `<div class="image-preview"><img src="${{file.rel_path}}" alt="${{file.name}}" style="max-width:100%;max-height:100%;object-fit:contain;border-radius:0.5rem;"></div>`;
            }} else if (file.type === 'mermaid') {{
                // Render mermaid diagram
                const diagramId = 'mermaid-diagram-' + Date.now();
                body.innerHTML = `<div class="mermaid-content"><pre class="mermaid" id="${{diagramId}}">${{file.content}}</pre></div>`;
                // Initialize mermaid on the new element
                setTimeout(() => {{
                    mermaid.init(undefined, document.getElementById(diagramId));
                }}, 0);
            }} else if (file.type === 'json') {{
                try {{
                    const json = JSON.parse(file.content.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'));
                    const formatted = JSON.stringify(json, null, 2);
                    body.innerHTML = `<pre><code class="language-json">${{formatted.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</code></pre>`;
                    hljs.highlightElement(body.querySelector('code'));
                }} catch {{
                    body.innerHTML = `<pre>${{file.content}}</pre>`;
                }}
            }} else if (file.type === 'yaml') {{
                // YAML with syntax highlighting
                body.innerHTML = `<pre><code class="language-yaml">${{file.content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</code></pre>`;
                hljs.highlightElement(body.querySelector('code'));
            }} else if (file.type === 'toon') {{
                // TOON with simple highlighting (use ini as closest match for key: value format)
                body.innerHTML = `<pre><code class="language-ini">${{file.content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</code></pre>`;
                hljs.highlightElement(body.querySelector('code'));
            }} else if (file.type === 'code') {{
                // Code files with auto-highlighting
                body.innerHTML = `<pre><code>${{file.content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</code></pre>`;
                hljs.highlightElement(body.querySelector('code'));
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
