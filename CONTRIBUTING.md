# Contributing to TrapTrace Soroban Error Index

Thank you for helping improve the Soroban developer experience!

## Submission Guidelines

1. **Category Selection:** Choose one of `host-error`, `cli-error`, `rpc-error`, or `sdk-error`.
2. **File Naming:** Name your file using kebab-case matching its `id` frontmatter (e.g. `entries/host-errors/budget-exceeded.md`).
3. **Required Frontmatter:**
   ```yaml
   ---
   id: my-error-id
   title: Host Error - Short Description
   category: host-error
   error_code: ErrorCodeString
   verified: false
   summary: Concise 1-2 sentence description.
   tags: [tag1, tag2]
   soroban_version: "21.0.0"
   ---
   ```
4. **Required Markdown Sections:**
   - `## Symptoms`
   - `## Root Causes`
   - `## Reproduction Steps`
   - `## Solutions`
   - `## References`

5. **Validation:** Run `python tools/validate_schema.py` before committing.
