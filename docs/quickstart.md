# ⚡ TrapTrace Index Quickstart & Contributor Guide

A step-by-step developer guide for querying the Soroban error index, executing live testnet verification, and submitting verified error entries.

---

## 1. Local Search & Ranked Querying

Search errors locally using the zero-dependency CLI tool:

```bash
# General search
python3 tools/search.py "auth failed"

# Ranked search with similarity scoring
python3 tools/search.py "overflow" --rank

# Filter by category
python3 tools/search.py --category host-error --verified
```

---

## 2. Schema Validation

Ensure all catalog files strictly adhere to `schema/entry.schema.json`:

```bash
python3 tools/validate_schema.py
```

Check internal cross-reference link integrity:
```bash
python3 tools/check_links.py
```

---

## 3. Live Testnet Verification Harness

To empirically verify reproduction payloads against Stellar Testnet RPC:

```bash
# Run verification harness against testnet
python3 tools/verify_entries.py

# Evidence logs are recorded in:
ls -la verification/
```

---

## 4. Exporting & Synchronizing

```bash
# Synchronize entries into the Web Explorer dataset
python3 tools/sync_explorer.py

# Export standalone offline HTML documentation
python3 tools/export_html.py
```
