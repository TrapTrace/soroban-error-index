#!/usr/bin/env python3
"""
CLI Helper tool to search and display Soroban error entries in soroban-error-index.
"""

import os
import sys
import glob
import re
import argparse
import json

def parse_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    
    yaml_str = match.group(1)
    body = match.group(2)
    
    metadata = {}
    for line in yaml_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.startswith("[") and val.endswith("]"):
                items = val[1:-1].split(",")
                val = [item.strip().strip("'\"") for item in items if item.strip()]
            elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            elif val.isdigit():
                val = int(val)
            metadata[key] = val

    return metadata, body

def load_all_entries(root_dir):
    entries_pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = glob.glob(entries_pattern, recursive=True)
    entries = []
    
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        meta, body = parse_frontmatter(content)
        meta["filepath"] = os.path.relpath(filepath, root_dir)
        meta["body"] = body
        entries.append(meta)
        
    return entries

def search_entries(entries, query=None, category=None, verified_only=False):
    results = []
    
    for entry in entries:
        if category and entry.get("category") != category:
            continue
        if verified_only and not entry.get("verified", False):
            continue
            
        if query:
            q = query.lower()
            title = str(entry.get("title", "")).lower()
            summary = str(entry.get("summary", "")).lower()
            code = str(entry.get("error_code", "")).lower()
            tags = " ".join(entry.get("tags", [])).lower()
            body = str(entry.get("body", "")).lower()
            
            if q not in title and q not in summary and q not in code and q not in tags and q not in body:
                continue
                
        results.append(entry)
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Search TrapTrace Soroban Error Index")
    parser.add_argument("query", nargs="?", default="", help="Search query (error code, text, or keyword)")
    parser.add_argument("-c", "--category", choices=["host-error", "cli-error", "rpc-error", "sdk-error"], help="Filter by category")
    parser.add_argument("-v", "--verified", action="store_true", help="Show verified entries only")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries = load_all_entries(root_dir)
    results = search_entries(entries, query=args.query, category=args.category, verified_only=args.verified)
    
    if args.json:
        # Strip body for concise output
        out = []
        for r in results:
            item = dict(r)
            item.pop("body", None)
            out.append(item)
        print(json.dumps(out, indent=2))
        return

    print(f"\n🔍 Found {len(results)} matching entries for query '{args.query}':\n")
    for r in results:
        verified_str = "✅ Verified" if r.get("verified") else "⚠️  Unverified"
        print(f"📌 [{r.get('id')}] {r.get('title')}")
        print(f"   Category: {r.get('category')} | Code: {r.get('error_code')} | Status: {verified_str}")
        print(f"   Summary:  {r.get('summary')}")
        print(f"   File:     {r.get('filepath')}\n")

if __name__ == "__main__":
    main()
