import os
import json
import html

paths_to_scan = [
    "/home/cygel/c25-unified-platform",
    "/home/cygel/constellation25",
    "/home/cygel/videocourts"
]

print("Mining monorepo code structures to extract system logic...")
all_modules = []

for base_path in paths_to_scan:
    if not os.path.exists(base_path):
        continue
    project_group = os.path.basename(base_path)
    for root, dirs, files in os.walk(base_path):
        if any(x in root for x in ['.git', 'node_modules', '.venv', '__pycache__', 'artifacts']):
            continue
        for file in files:
            name, ext = os.path.splitext(file)[1], os.path.splitext(file)[1]
            if ext in ['.js', '.py', '.html', '.css', '.json', '.sh', '.java']:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        raw_content = f.read()
                    
                    intent = "General Configuration Asset"
                    if ext == '.py':
                        intent = "FastAPI Backend API Router / Logic Node" if "FastAPI" in raw_content or "router" in raw_content else "Python Automation Handler"
                    elif ext == '.js':
                        intent = "Node.js Core Microservice Controller" if "require" in raw_content or "express" in raw_content else "Client Interface Script"
                    elif ext == '.java':
                        intent = "Java Compiled Class Module / JAXP Context"
                    elif ext == '.html':
                        intent = "UI Application Presentation Subpage"
                    elif ext == '.sh':
                        intent = "System Shell Automated Deployment Vector"

                    escaped_code = html.escape(raw_content)
                    display_path = full_path.replace('/home/cygel/', '')
                    
                    all_modules.append({
                        "path": display_path,
                        "filename": file,
                        "project": project_group,
                        "type": ext.replace('.', '').upper(),
                        "intent": intent,
                        "code": escaped_code,
                        "lines": len(raw_content.splitlines())
                    })
                except Exception:
                    pass

print(f"Successfully processed {len(all_modules)} files. Assembling monolithic HTML Dashboard...")

json_payload = json.dumps(all_modules)

html_layout = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C25 Complete Fullstack Interface Matrix</title>
    <style>
        :root {
            --bg-dark: #030712;
            --bg-card: #0f172a;
            --border: #1e293b;
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #64748b;
            --terminal-green: #10b981;
        }
        body {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background-color: var(--bg-dark);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        header {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .brand h1 { margin: 0; font-size: 20px; color: var(--accent); letter-spacing: 0.05em; }
        .brand p { margin: 4px 0 0 0; font-size: 12px; color: var(--text-muted); }
        .badge { background: #1e293b; border: 1px solid var(--border); padding: 6px 12px; border-radius: 4px; font-size: 13px; font-weight: bold; }
        .search-area { padding: 16px 24px; background: #0b0f19; border-bottom: 1px solid var(--border); }
        .search-input {
            width: 100%; padding: 14px; background: #030712; border: 1px solid var(--border); border-radius: 6px;
            color: var(--text-main); font-family: inherit; font-size: 14px; box-sizing: border-box;
        }
        .search-input:focus { outline: 1px solid var(--accent); }
        .workspace { display: grid; grid-template-columns: 480px 1fr; flex-grow: 1; overflow: hidden; }
        .sidebar { background: var(--bg-card); border-right: 1px solid var(--border); display: flex; flex-direction: column; overflow: hidden; }
        .sidebar-title { font-size: 11px; text-transform: uppercase; color: var(--accent); padding: 12px 16px; border-bottom: 1px solid var(--border); font-weight: bold; }
        .file-scroller { overflow-y: auto; flex-grow: 1; }
        .file-item { padding: 12px 16px; border-bottom: 1px solid #111827; font-size: 12px; cursor: pointer; display: flex; flex-direction: column; gap: 4px; }
        .file-item:hover { background: #1e293b; }
        .file-meta { display: flex; justify-content: space-between; align-items: center; }
        .intent-tag { font-size: 11px; color: #a855f7; display: block; margin-top: 2px; }
        .lang-badge { font-size: 10px; padding: 2px 6px; border-radius: 3px; background: #030712; border: 1px solid var(--border); font-weight: bold; }
        .lang-badge.PY { color: #3b82f6; }
        .lang-badge.JS { color: #eab308; }
        .lang-badge.JAVA { color: #f97316; }
        .lang-badge.HTML { color: #ef4444; }
        .display-area { display: flex; flex-direction: column; padding: 24px; overflow: hidden; background: #020617; }
        .active-banner { font-size: 13px; color: #94a3b8; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
        .code-container { background: #030712; border: 1px solid var(--border); border-radius: 6px; padding: 20px; flex-grow: 1; overflow: auto; white-space: pre; font-size: 13px; color: var(--terminal-green); line-height: 1.6; }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <h1>C25 Fullstack Functional Interface Matrix</h1>
            <p>Automated Operational Core Module Controller</p>
        </div>
        <div class="badge" id="runtime-counter">Assets Loaded: 0 Modules</div>
    </header>

    <div class="search-area">
        <input type="text" class="search-input" id="search-field" placeholder="Filter by system intent, vendor routes, components, subpages, or code definitions..." oninput="filterWorkspace()">
    </div>

    <div class="workspace">
        <div class="sidebar">
            <div class="sidebar-title">Monorepo System Map Directory</div>
            <div class="file-scroller" id="tree-target"></div>
        </div>
        <div class="display-area">
            <div class="active-banner" id="current-module">Selected Target: No fullstack code module active.</div>
            <div class="code-container" id="terminal-canvas">// Click on any infrastructure module node on the sidebar directory to trigger the interactive fullstack view layout...</div>
        </div>
    </div>

    <script>
        const runtimeDatabase = __PAYLOAD_DATA__;

        document.getElementById('runtime-counter').innerText = `Assets Loaded: ${runtimeDatabase.length} Modules`;

        function drawWorkspaceList(modules) {
            const container = document.getElementById('tree-target');
            container.innerHTML = '';
            modules.forEach(m => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.onclick = () => mountCodeScreen(m.path, m.intent, m.code);
                item.innerHTML = `
                    <div class="file-meta">
                        <strong>${m.filename}</strong>
                        <span class="lang-badge ${m.type}">${m.type}</span>
                    </div>
                    <div style="font-size:11px; color:#94a3b8;">${m.path}</div>
                    <span class="intent-tag">${m.intent} (${m.lines} lines)</span>
                `;
                container.appendChild(item);
            });
        }

        function mountCodeScreen(path, intent, sourceText) {
            document.getElementById('current-module').innerText = `Active Component: ${path} | Intent Group: ${intent}`;
            document.getElementById('terminal-canvas').innerHTML = sourceText || '// Empty operational code descriptor block.';
        }

        function filterWorkspace() {
            const query = document.getElementById('search-field').value.toLowerCase();
            const results = runtimeDatabase.filter(m => m.path.toLowerCase().includes(query) || m.intent.toLowerCase().includes(query) || m.code.toLowerCase().includes(query));
            drawWorkspaceList(results);
        }

        drawWorkspaceList(runtimeDatabase);
    </script>
</body>
</html>
"""

# Embed database payloads safely into the target hook position without using f-string braces
final_output = html_layout.replace("__PAYLOAD_DATA__", json_payload)

os.makedirs("/home/cygel/c25-unified-platform/docs", exist_ok=True)
with open("/home/cygel/c25-unified-platform/docs/fullstack_app_ui.html", "w", encoding="utf-8") as f:
    f.write(final_output)

print("Success! Standalone UI/UX file generated safely inside /docs/fullstack_app_ui.html.")
