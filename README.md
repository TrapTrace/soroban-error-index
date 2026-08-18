<div align="center">

# ⚡ TrapTrace — Soroban Error Index

**A structured, searchable knowledge base of Soroban host, CLI, RPC, and SDK errors mapped to root cause analysis and verified fixes.**

[![CI Validation](https://img.shields.io/github/actions/workflow/status/TrapTrace/soroban-error-index/validate.yml?branch=main&style=flat-square&color=2FA98C&label=CI%20Validation)](https://github.com/TrapTrace/soroban-error-index/actions)
[![Schema](https://img.shields.io/badge/Schema-Draft%2007-1B1F23?style=flat-square)](./schema/entry.schema.json)
[![Catalog Entries](https://img.shields.io/badge/Entries-10%20Cataloged-E2984B?style=flat-square)](#-repository-structure)
[![License](https://img.shields.io/badge/License-MIT-2FA98C?style=flat-square)](./LICENSE)
[![Stellar Wave](https://img.shields.io/badge/Drips%20Wave-8%20Target-E2984B?style=flat-square)](https://drips.network)

</div>

---

## 🎯 Purpose

Soroban smart contract developers frequently hit cryptic WASM execution traps, RPC simulation errors, and CLI authorization failures. Stellar's official documentation explains transaction flow concepts, but is not indexed or searchable by literal error strings.

`soroban-error-index` addresses this gap by serving as a structured catalog containing:
- **Exact Error Strings & Codes:** Machine-readable YAML frontmatter schema.
- **Verification Status (`verified: true`):** Empirical testnet/RPC verification logs.
- **Reproducible Snippets:** Contract Rust, CLI invocation, and RPC payload examples.
- **Step-by-Step Fixes:** Actionable resolution pathways.

---

## 📂 Repository Structure

```
soroban-error-index/
├── entries/
│   ├── host-errors/      # VM Traps, budget limits, state archival errors
│   ├── cli-errors/       # Soroban CLI identity, keypair, & sequence errors
│   ├── rpc-errors/       # RPC simulation, getLedgerEntries failures
│   └── sdk-errors/       # ScVal conversion & type-decoding errors
├── schema/
│   └── entry.schema.json # Strict JSON Schema for validation
├── tools/
│   ├── validate_schema.py# CI validator for Markdown & YAML frontmatter
│   └── search.py         # Search CLI helper
└── .github/
    └── workflows/
        └── validate.yml  # Automated CI workflow
```

---

## 🚀 Quick Search CLI Usage

You can query the catalog locally using the provided search tool:

```bash
# Search by keyword
python tools/search.py "budget"

# Filter by category
python tools/search.py -c host-error

# Show verified entries only
python tools/search.py -v

# Output JSON for integrations
python tools/search.py --json
```

---

## 🌐 The TrapTrace Ecosystem

`soroban-error-index` is the core content foundation of the **TrapTrace** developer diagnostics ecosystem:

| Repository / Tool | Purpose | Status |
|---|---|---|
| 📖 **[`soroban-error-index`](https://github.com/TrapTrace/soroban-error-index)** | Machine-readable error catalog with testnet-verified reproduction steps and fixes | **Active (10 verified entries)** |
| 🛠️ **[`soroban-error-cli`](https://github.com/TrapTrace/soroban-error-cli)** | Operational CLI tool (`traptrace`) with live RPC inspector, simulation debugger, and storage auditor | **Published** |
| ⚡ **[`soroban-error-explorer`](https://github.com/TrapTrace/soroban-error-explorer)** | Web search UI & Live Diagnostics Studio deployed at [traptrace-explorer.vercel.app](https://traptrace-explorer.vercel.app) | **Live on Vercel** |

---

## 🔄 Automated Index-to-Explorer Synchronization

To keep the web explorer in sync with newly contributed error entries:

```bash
# Regenerates src/data/entries.json in soroban-error-explorer
python tools/sync_explorer.py
```

---

## 🧪 Validating Entries

Run the built-in validator to check that all entries adhere to `schema/entry.schema.json`:

```bash
python tools/validate_schema.py
```

---

## 🤝 Contributing

We welcome community contributions! Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) for details on entry schema requirements, verification guidelines, and submitting pull requests.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.

