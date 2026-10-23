import os
import json
import re
import datetime

# CONFIG: Add your actual vault paths here
VAULT_PATHS = [
    os.path.expanduser("~/Obsidian"),
    os.path.expanduser("~/c25-unified-platform/compiled_total_recall"),
    os.path.expanduser("~/c25-unified-platform/legacy-archive")
]

INDEX_FILE = os.path.expanduser("~/c25-unified-platform/apps/frontend/public/vault_index.json")

def parse_frontmatter(content):
    """Extract YAML frontmatter from Markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        yaml_str = match.group(1)
        tags = re.findall(r'tags:\s*\[([^\]]+)\]', yaml_str)
        if tags:
            return [t.strip().strip('"').strip("'") for t in tags[0].split(',')]
    return []

def ingest_vaults():
    index = []
    total_files = 0
    
    print("🔍 Scanning vaults for Markdown and text files...")
    
    for vault in VAULT_PATHS:
        if not os.path.exists(vault):
            print(f"⚠️  Skipping {vault} (Not found)")
            continue
            
        print(f" Ingesting: {vault}")
        
        for root, dirs, files in os.walk(vault):
            # Ignore .git and node_modules
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '.obsidian']]
            
            for file in files:
                if file.endswith(('.md', '.txt', '.json', '.js', '.py', '.sh', '.html')):
                    total_files += 1
                    filepath = os.path.join(root, file)
                    
                    try:
                        stat = os.stat(filepath)
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(2000) # Read first 2000 chars for tags
                        
                        tags = parse_frontmatter(content)
                        
                        # Extract title from frontmatter or filename
                        title_match = re.search(r'title:\s*(.*)', content)
                        title = title_match.group(1).strip() if title_match else file.replace('.md', '')
                        
                        index.append({
                            "id": total_files,
                            "title": title,
                            "file": file,
                            "path": filepath.replace(os.path.expanduser("~"), "~"),
                            "type": file.split('.')[-1],
                            "tags": tags,
                            "size_kb": round(stat.st_size / 1024, 2),
                            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
                    except Exception as e:
                        pass # Skip unreadable files

    # Write the index
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
        
    print(f"\n✅ INGESTION COMPLETE!")
    print(f"📊 Total files indexed: {total_files}")
    print(f" Index saved to: {INDEX_FILE}")
    print(f"💾 Index size: {round(os.path.getsize(INDEX_FILE) / 1024, 2)} KB")

if __name__ == "__main__":
    ingest_vaults()
