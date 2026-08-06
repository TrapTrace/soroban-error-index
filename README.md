# TrapTrace — Soroban Error Index (`soroban-error-index`)

![CI Validation](https://github.com/TrapTrace/soroban-error-index/actions/workflows/validate.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-teal.svg)
![Status](https://img.shields.io/badge/Status-Verified--Entries-orange.svg)

**TrapTrace Error Index** is a structured, contributor-extensible, searchable knowledge base of real Soroban host, CLI, RPC, and SDK errors mapped to root cause analysis, reproduction steps, and verified fixes.

---

## 🎯 Purpose

Soroban developers frequently encounter cryptic VM traps, RPC simulation failures, and CLI execution errors. Stellar's official documentation explains transaction flow models conceptually, but is not indexed or searchable by exact error strings.

`soroban-error-index` solves this gap by serving as a structured catalog containing:
- Exact error strings & codes.
- Honest verification status (`verified: true | false`).
- Reproducible contract and CLI snippets.
- Explicit step-by-step resolution steps.

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
