import os
import json
import html

paths_to_scan = [
    "/home/cygel/c25-unified-platform",
    "/home/cygel/constellation25",
    "/home/cygel/videocourts"
]

print("Processing and compiling all 1,344 full-stack project code metrics...")
all_assets = []

for base_path in paths_to_scan:
    if not os.path.exists(base_path):
        continue
    for root, dirs, files in os.walk(base_path):
        # Filter out heavy git binaries and dependency directories to prevent bundle crashes
        if any(x in root for x in ['.git', 'node_modules', '.venv', '__pycache__']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ['.js', '.py', '.html', '.css', '.json', '.sh', '.java']:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        raw_code = f.read()
                    
                    # Convert source code into a safe format for browser rendering
                    escaped_code = html.escape(raw_code)
                    
                    all_assets.append({
                        "path": full_path.replace('/home/cygel/', ''),
                        "name": file,
                        "type": ext.replace('.', '').upper() if ext else 'TXT',
                        "content": escaped_code,
                        "size": os.path.getsize(full_path)
                    })
                except Exception:
                    pass

print(f"Extraction step complete. Successfully read {len(all_assets)} source assets.")
print("Assembling consolidated UI/UX control dashboard inside /docs/index.html...")

# Safely inject the data directly as a JavaScript payload matrix
json_db = json.dumps(all_assets)

html_layout = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C25 Complete Monorepo System Control Matrix</title>
    <style>
        :root {{
            --bg-dark: #090d16;
            --bg-panel: #111827;
            --border-color: #1f2937;
            --accent-color: #38bdf8;
            --text-light: #f8fafc;
            --text-dark: #64748b;
            --code-green: #34d399;
        }}
        body {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background-color: var(--bg-dark);
            color: var(--text-light);
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        header {{
            background-color: var(--bg-panel);
            border-bottom: 1px solid var(--border-color);
            padding: 15px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo-area h1 {{ margin: 0; font-size: 18px; color: var(--accent-color); letter-spacing: 0.05em; }}
        .logo-area p {{ margin: 3px 0 0 0; font-size: 12px; color: var(--text-dark); }}
        .badge-counter {{
            background: #1f2937;
            border: 1px solid var(--border-color);
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
        }}
        .search-container {{
            padding: 16px 24px;
            background-color: #0b0f19;
            border-bottom: 1px solid var(--border-color);
        }}
        .search-bar {{
            width: 100%;
            padding: 12px 16px;
            background: #030712;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-light);
            font-family: inherit;
            font-size: 14px;
            box-sizing: border-box;
        }}
        .search-bar:focus {{ outline: 1px solid var(--accent-color); }}
        .main-workspace {{
            display: grid;
            grid-template-columns: 450px 1fr;
            flex-grow: 1;
            overflow: hidden;
        }}
        .sidebar {{
            background: var(--bg-panel);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        .sidebar-header {{
            font-size: 11px;
            text-transform: uppercase;
            color: var(--accent-color);
            padding: 12px 16px;
            border-bottom: 1px solid #1f2937;
            font-weight: bold;
        }}
        .file-list {{
            overflow-y: auto;
            flex-grow: 1;
        }}
        .file-row {{
            padding: 10px 16px;
            border-bottom: 1px solid #111827;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .file-row:hover {{ background: #1f2937; }}
        .type-badge {{
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 3px;
            background: #030712;
            border: 1px solid #1f2937;
            font-weight: bold;
        }}
        .type-badge.JAVA {{ color: #f97316; }}
        .type-badge.JS {{ color: #eab308; }}
        .type-badge.PY {{ color: #3b82f6; }}
        .type-badge.HTML {{ color: #ef4444; }}
        .viewer-area {{
            display: flex;
            flex-direction: column;
            padding: 20px;
            overflow: hidden;
            background: #030712;
        }}
        .active-file-banner {{
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
            word-break: break-all;
        }}
        .code-sandbox {{
            background: #020617;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 20px;
            flex-grow: 1;
            overflow: auto;
            white-space: pre;
            font-size: 13px;
            color: var(--code-green);
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo-area">
            <h1>C25 Consolidated Monorepo System Control Matrix</h1>
            <p>Unified Project Platform Engine View</p>
        </div>
        <div class="badge-counter" id="total-badge">Compiled Files: 0</div>
    </header>

    <div class="search-container">
        <input type="text" class="search-bar" id="search-box" placeholder="Search and execute routing pipelines across all code files, models, configuration schemas, and subpages..." oninput="triggerSearch()">
    </div>

    <div class="main-workspace">
        <div class="sidebar">
            <div class="sidebar-header">Subpage Code Tree Index</div>
            <div class="file-list" id="list-target"></div>
        </div>
        <div class="viewer-area">
            <div class="active-file-banner" id="current-path">Active Context: No target file workspace open.</div>
            <div class="code-sandbox" id="code-canvas">// Select any code module asset from the architectural tree listing on the sidebar grid array to render contents live...</div>
        </div>
    </div>

    <script>
        // Main embedded database array holding every full-stack file layout directly in memory
        const monorepoData = {json_db};

        document.getElementById('total-badge').innerText = `Compiled Files: ${{monorepoData.length}}`;

        function buildFileTree(assets) {{
            const target = document.getElementById('list-target');
            target.innerHTML = '';
            assets.forEach(asset => {{
                const row = document.createElement('div');
                row.className = 'file-row';
                row.onclick = () => renderCodeView(asset.path, asset.content);
                row.innerHTML = `<span>${{asset.path}}</span><span class="type-badge ${{asset.type}}">${{asset.type}}</span>`;
                target.appendChild(row);
            }});
        }}

        function renderCodeView(path, codeText) {{
            document.getElementById('current-path').innerText = `Active Context: ${{path}}`;
            document.getElementById('code-canvas').innerHTML = codeText || '// Clean empty target code allocation schema.';
        }}

        function triggerSearch() {{
            const query = document.getElementById('search-box').value.toLowerCase();
            const filtered = monorepoData.filter(item => item.path.toLowerCase().includes(query) || item.content.toLowerCase().includes(query));
            buildFileTree(filtered);
        }}

        // Initialization routine call
        buildFileTree(monorepoData);
    </script>
</body>
</html>
"""

# Force create the directory if it was cleared out during git operations
os.makedirs("/home/cygel/c25-unified-platform/docs", exist_ok=True)

with open("/home/cygel/c25-unified-platform/docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("Success! Monolithic full-stack UI index file created successfully in /docs/index.html.")
