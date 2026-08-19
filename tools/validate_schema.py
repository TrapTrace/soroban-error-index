#!/usr/bin/env python3
"""
Schema Validator for TrapTrace soroban-error-index entries.
Validates YAML frontmatter against JSON Schema and verifies Markdown header structure.
"""

import sys
import os
import glob
import re
import json

def parse_frontmatter(content):
    """Simple parser for YAML frontmatter without requiring PyYAML."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    
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
            
            # Simple YAML parsing for types
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.startswith("[") and val.endswith("]"):
                # Array parsing
                items = val[1:-1].split(",")
                val = [item.strip().strip("'\"") for item in items if item.strip()]
            elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            elif val.isdigit():
                val = int(val)
            metadata[key] = val

    return metadata, body

REQUIRED_FIELDS = ["id", "title", "category", "error_code", "verified", "summary", "tags"]
ALLOWED_CATEGORIES = ["host-error", "cli-error", "rpc-error", "sdk-error"]
REQUIRED_SECTIONS = ["Symptoms", "Root Causes", "Solutions"]

def validate_file(filepath):
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)
    if frontmatter is None:
        errors.append("Missing or invalid YAML frontmatter delimiters ('---').")
        return errors

    # Check required frontmatter fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required frontmatter field: '{field}'")

    if "id" in frontmatter:
        if not re.match(r"^[a-z0-9-]+$", str(frontmatter["id"])):
            errors.append(f"Invalid 'id' format '{frontmatter['id']}': must be lowercase alphanumeric with hyphens.")

    if "category" in frontmatter and frontmatter["category"] not in ALLOWED_CATEGORIES:
        errors.append(f"Invalid category '{frontmatter['category']}': must be one of {ALLOWED_CATEGORIES}")

    if "verified" in frontmatter and not isinstance(frontmatter["verified"], bool):
        errors.append(f"Field 'verified' must be a boolean (true/false). Got: {frontmatter['verified']}")

    if "tags" in frontmatter and not isinstance(frontmatter["tags"], list):
        errors.append("Field 'tags' must be a list.")

    if "severity" in frontmatter and frontmatter["severity"] not in ["info", "warning", "critical"]:
        errors.append(f"Invalid 'severity' '{frontmatter['severity']}': must be one of ['info', 'warning', 'critical']")

    if "related_entries" in frontmatter:
        if not isinstance(frontmatter["related_entries"], list):
            errors.append("Field 'related_entries' must be a list of entry IDs.")
        else:
            for rel in frontmatter["related_entries"]:
                if not re.match(r"^[a-z0-9-]+$", str(rel)):
                    errors.append(f"Invalid related_entry ID format '{rel}': must be lowercase alphanumeric with hyphens.")

    # Check required markdown sections
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}", body, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required markdown section header: '## {section}'")

    return errors

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entries_pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = glob.glob(entries_pattern, recursive=True)

    if not files:
        print("❌ No markdown entries found in entries/")
        sys.exit(1)

    total_files = len(files)
    failed = 0

    print(f"🔍 Validating {total_files} entry files...")

    for filepath in sorted(files):
        rel_path = os.path.relpath(filepath, root_dir)
        errors = validate_file(filepath)
        if errors:
            failed += 1
            print(f"❌ {rel_path}:")
            for err in errors:
                print(f"   - {err}")
        else:
            print(f"✅ {rel_path}")

    if failed > 0:
        print(f"\n❌ Validation failed: {failed}/{total_files} files have errors.")
        sys.exit(1)

    print(f"\n🎉 Validation passed! All {total_files} entries match the schema.")
    sys.exit(0)

if __name__ == "__main__":
    main()
