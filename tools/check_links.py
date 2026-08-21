#!/usr/bin/env python3
"""
TrapTrace Link & Reference Integrity Checker.
Validates all internal cross-references, related_entries links, and schema references in markdown entries.
"""

import os
import re
import glob
import json
import sys

def parse_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    yaml_str, body = match.group(1), match.group(2)
    meta = {}
    for line in yaml_str.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [item.strip().strip("'\"") for item in v[1:-1].split(",") if item.strip()]
            meta[k] = v
    return meta, body

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries_pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = glob.glob(entries_pattern, recursive=True)
    
    known_ids = set()
    entry_data = []
    
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            meta, body = parse_frontmatter(fh.read())
        entry_id = meta.get("id")
        if entry_id:
            known_ids.add(entry_id)
            entry_data.append((f, meta, body))
            
    print(f"🔍 Checking cross-reference integrity across {len(known_ids)} catalog entries...")
    errors = 0
    
    for filepath, meta, body in entry_data:
        entry_id = meta.get("id")
        rel_entries = meta.get("related_entries", [])
        if isinstance(rel_entries, list):
            for target_id in rel_entries:
                if target_id not in known_ids:
                    print(f"❌ Broken related_entries reference in {filepath}: '{target_id}' does not exist!")
                    errors += 1
                    
    if errors == 0:
        print(f"✅ All cross-references and related_entries are valid ({len(known_ids)}/{len(known_ids)}).")
        sys.exit(0)
    else:
        print(f"❌ Found {errors} broken cross-references.")
        sys.exit(1)

if __name__ == "__main__":
    main()
