#!/usr/bin/env python3
"""
TrapTrace Automated Index -> Explorer Synchronizer
Parses all Markdown catalog entries, extracts frontmatter and structured body sections,
and generates the production entries.json bundle for soroban-error-explorer.
"""

import sys
import os
import glob
import re
import json

def parse_entry_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split YAML frontmatter and body
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None

    yaml_str = match.group(1)
    body = match.group(2)

    # Parse YAML frontmatter
    meta = {}
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
            meta[key] = val

    # Extract Markdown Sections
    sections = {}
    current_section = None
    current_lines = []

    for line in body.splitlines():
        sec_match = re.match(r"^##\s+(.*)$", line)
        if sec_match:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = sec_match.group(1).strip().lower().replace(" ", "_")
            current_lines = []
        else:
            if current_section:
                current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    # Clean code blocks in reproduction steps if wrapped in ```rust ... ```
    repro = sections.get("reproduction_steps", "")
    code_match = re.search(r"```(?:rust|bash|json)?\s*\n(.*?)\n```", repro, re.DOTALL)
    if code_match:
        repro_clean = code_match.group(1).strip()
    else:
        repro_clean = repro

    return {
        "id": meta.get("id"),
        "title": meta.get("title"),
        "category": meta.get("category"),
        "error_code": meta.get("error_code"),
        "verified": meta.get("verified", False),
        "summary": meta.get("summary", ""),
        "tags": meta.get("tags", []),
        "soroban_version": meta.get("soroban_version", "21.0.0"),
        "symptoms": sections.get("symptoms", ""),
        "root_causes": sections.get("root_causes", ""),
        "reproduction_steps": repro_clean,
        "solutions": sections.get("solutions", ""),
        "references": sections.get("references", "")
    }

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries_pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = sorted(glob.glob(entries_pattern, recursive=True))

    if not files:
        print("❌ No entries found in entries/")
        sys.exit(1)

    print(f"🔄 Parsing {len(files)} markdown catalog entries...")
    entries = []
    for f in files:
        entry = parse_entry_file(f)
        if entry and entry.get("id"):
            entries.append(entry)
            print(f"  ✓ Processed [{entry['id']}] ({entry['category']})")

    # Output paths
    explorer_data_path = os.path.abspath(os.path.join(root_dir, "..", "soroban-error-explorer", "src", "data", "entries.json"))
    local_build_dir = os.path.join(root_dir, "build")
    os.makedirs(local_build_dir, exist_ok=True)
    local_data_path = os.path.join(local_build_dir, "entries.json")

    # Write local bundle
    with open(local_data_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    print(f"✅ Generated local build index: {local_data_path}")

    # Write explorer bundle if directory exists
    if os.path.exists(os.path.dirname(explorer_data_path)):
        with open(explorer_data_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        print(f"✅ Synchronized web explorer data: {explorer_data_path}")

    print(f"🎉 Successfully synchronized {len(entries)} catalog entries.")

if __name__ == "__main__":
    main()
