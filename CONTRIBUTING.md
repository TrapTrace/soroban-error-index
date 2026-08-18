# Contributing to TrapTrace — Soroban Error Index

Thank you for contributing to TrapTrace! High-quality, verified error entries and robust tooling make building on Stellar Soroban smoother for the entire developer community.

---

## 📋 Standards for Error Catalog Entries

Every entry in the catalog must adhere to strict schema rules and empirical reproducibility guidelines:

1. **Category Mapping:**
   - `host-error`: WASM traps, execution budget limits, state archival / TTL errors.
   - `cli-error`: Soroban CLI identity, keypair, network configuration, and sequence errors.
   - `rpc-error`: Simulation failures, invalid authorization signatures, missing footprint keys.
   - `sdk-error`: ScVal type decoding, conversion, and environment mismatch errors.

2. **File Naming & Path:**
   - Files must be placed under `entries/<category>/<id>.md`.
   - `<id>` must match the `id` field in frontmatter using lowercase alphanumeric characters and hyphens (`kebab-case`).

3. **Required Frontmatter (YAML):**
   ```yaml
   ---
   id: entry-archived-ttl-expired
   title: Host Error - Storage Entry Archived or TTL Expired
   category: host-error
   error_code: HostError::EntryArchived
   verified: true
   summary: Attempted access to a persistent or instance storage entry whose Time-To-Live (TTL) has expired.
   tags: [storage, ttl, archive, state-archival, host-error]
   soroban_version: "21.0.0"
   ---
   ```

4. **Required Markdown Sections:**
   - `## Symptoms`: Exact error logs, RPC payloads, or terminal output observed by developers.
   - `## Root Causes`: Bulleted technical explanation of what caused the failure.
   - `## Reproduction Steps`: Verifiable Rust snippet, CLI command, or RPC request payload.
   - `## Solutions`: Step-by-step resolution pathways and remediation code.
   - `## References`: Links to official Stellar docs, CAP specifications, or SDK references.

---

## 🧪 Local Testing & Validation Workflow

Before opening a pull request:

```bash
# 1. Validate all markdown entries against entry.schema.json
python tools/validate_schema.py

# 2. Test search CLI
python tools/search.py "your-error-code"

# 3. Synchronize with the web explorer
python tools/sync_explorer.py
```

---

## 🚀 Pull Request Workflow

1. Fork the repository and create a feature branch (`git checkout -b entry/your-error-id`).
2. Add your entry under `entries/<category>/`.
3. Verify that `python tools/validate_schema.py` passes with zero errors.
4. Push your branch and submit a Pull Request describing your testnet reproduction setup.
5. All PRs require passing GitHub Actions CI before merge.

---

## ⚖️ Code of Conduct
Please be respectful and collaborative. We uphold a zero-tolerance policy against harassment or toxic behavior.
