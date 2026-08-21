#!/usr/bin/env python3
"""
TrapTrace HTML Manual & Documentation Exporter.
Compiles all catalog markdown entries into a standalone, single-file offline HTML reference manual.
"""

import os
import glob
import re
import html

def parse_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_str, body = match.group(1), match.group(2)
    meta = {}
    for line in yaml_str.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("'\"")
    return meta, body

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries_pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = sorted(glob.glob(entries_pattern, recursive=True))
    
    entries = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            meta, body = parse_frontmatter(fh.read())
            entries.append((meta, body))
            
    html_content = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <title>TrapTrace Soroban Error Resolution Manual</title>",
        "  <style>",
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace; background: #F7F5F0; color: #1B1F23; margin: 40px auto; max-width: 900px; line-height: 1.6; }",
        "    h1 { color: #1B1F23; border-bottom: 2px solid #2FA98C; padding-bottom: 10px; }",
        "    .entry { background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }",
        "    .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #2FA98C; color: #FFF; }",
        "    pre { background: #1B1F23; color: #F7F5F0; padding: 14px; border-radius: 6px; overflow-x: auto; }",
        "    code { font-family: monospace; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>⚡ TrapTrace: Verified Soroban Error Knowledge Graph</h1>",
        f"  <p>Comprehensive offline diagnostic manual containing {len(entries)} testnet-verified smart contract error patterns.</p>"
    ]
    
    for meta, body in entries:
        title = html.escape(meta.get("title", meta.get("id", "Error Entry")))
        cat = html.escape(meta.get("category", "unknown"))
        code = html.escape(meta.get("error_code", "N/A"))
        summary = html.escape(meta.get("summary", ""))
        
        html_content.append(f"  <div class='entry'>")
        html_content.append(f"    <h2>{title}</h2>")
        html_content.append(f"    <p><span class='badge'>{cat}</span> <code>{code}</code></p>")
        html_content.append(f"    <p><strong>Summary:</strong> {summary}</p>")
        html_content.append(f"  </div>")
        
    html_content.extend(["</body>", "</html>"])
    
    out_dir = os.path.join(root_dir, "build")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "manual.html")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
        
    print(f"✅ Generated standalone HTML manual: {out_file} ({len(entries)} entries)")

if __name__ == "__main__":
    main()
