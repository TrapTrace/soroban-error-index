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

def calculate_relevance_score(entry, query):
    score = 0.0
    q = query.lower().strip()
    if not q:
        return 1.0

    id_str = str(entry.get("id", "")).lower()
    title = str(entry.get("title", "")).lower()
    code = str(entry.get("error_code", "")).lower()
    summary = str(entry.get("summary", "")).lower()
    tags = [t.lower() for t in entry.get("tags", [])]
    body = str(entry.get("body", "")).lower()

    # 1. Exact matches
    if q == code or q == id_str:
        score += 50.0
    elif q in code or q in id_str:
        score += 30.0

    if q in title:
        score += 20.0
    if any(q in t for t in tags):
        score += 15.0
    if q in summary:
        score += 10.0
    if q in body:
        score += 5.0

    # 2. Tokenized & fuzzy matching
    tokens = [t for t in re.split(r"[\s\:\(\)\_\-\,\#\.]+", q) if len(t) > 2]
    for tok in tokens:
        if tok in id_str or tok in code:
            score += 12.0
        elif tok in title:
            score += 8.0
        elif any(tok in t for t in tags):
            score += 6.0
        elif tok in summary:
            score += 4.0
        elif tok in body:
            score += 2.0
        else:
            # Check near-miss fuzzy similarity with words in title and id
            for word in re.split(r"[\s\_\-]+", f"{id_str} {title}"):
                if len(word) >= 4 and len(tok) >= 4:
                    # Simple char intersection / length ratio
                    common = set(tok) & set(word)
                    if len(common) >= len(tok) - 1:
                        score += 3.0
                        break

    return score

def search_entries(entries, query=None, category=None, verified_only=False, ranked=False, rank=False):
    is_ranked = ranked or rank
    scored = []
    for entry in entries:
        if category and entry.get("category") != category:
            continue
        if verified_only and not entry.get("verified", False):
            continue

        if not query:
            scored.append((entry, 1.0))
            continue

        score = calculate_relevance_score(entry, query)
        if score > 0.0:
            entry_copy = dict(entry)
            entry_copy["_score"] = score
            scored.append((entry_copy, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored]

def main():
    parser = argparse.ArgumentParser(description="Search TrapTrace Soroban Error Index")
    parser.add_argument("query", nargs="?", default="", help="Search query (error code, text, or keyword)")
    parser.add_argument("-c", "--category", choices=["host-error", "cli-error", "rpc-error", "sdk-error"], help="Filter by category")
    parser.add_argument("-v", "--verified", action="store_true", help="Show verified entries only")
    parser.add_argument("-r", "--rank", action="store_true", help="Display relevance score ranking for results")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries = load_all_entries(root_dir)
    results = search_entries(entries, query=args.query, category=args.category, verified_only=args.verified, ranked=args.rank)
    
    if args.json:
        # Strip body for concise output
        out = []
        for r in results:
            item = dict(r)
            item.pop("body", None)
            if not args.rank:
                item.pop("_score", None)
            out.append(item)
        print(json.dumps(out, indent=2))
        return

    print(f"\n🔍 Found {len(results)} matching entries for query '{args.query}':\n")
    for r in results:
        verified_str = "✅ Verified" if r.get("verified") else "⚠️  Unverified"
        score_str = f" | Score: {r.get('_score', 0):.1f}" if args.rank else ""
        print(f"📌 [{r.get('id')}] {r.get('title')}{score_str}")
        print(f"   Category: {r.get('category')} | Code: {r.get('error_code')} | Status: {verified_str}")
        print(f"   Summary:  {r.get('summary')}")
        print(f"   File:     {r.get('filepath')}\n")

if __name__ == "__main__":
    main()
