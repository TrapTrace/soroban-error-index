---
name: 📝 New Verified Error Entry
about: Submit a new testnet-verified Soroban error code and resolution guide
title: "entry: [category] <error_code_or_id>"
labels: ["new-entry", "needs-review"]
assignees: ''
---

### 1. Error Classification
- **Category:** [host-error | cli-error | rpc-error | sdk-error]
- **Exact Error Code/Identifier:** (e.g. `HostError::InvalidAction`)
- **Soroban Version:** (e.g. `21.0.0`)

### 2. Summary
<!-- A brief 1-2 sentence description of what triggered this error -->

### 3. Symptoms
<!-- CLI output, RPC error response, or log snippet -->
```
```

### 4. Root Causes
<!-- 2-3 specific root causes explaining why this occurs -->
1. 
2. 

### 5. Empirical Reproduction Steps (Testnet Verified)
<!-- Exact Rust snippet, CLI command, or RPC payload used to reproduce on testnet -->
```rust
```

### 6. Step-by-Step Solutions
<!-- Clear fix instructions and code snippets -->
1. 
2. 

### 7. Verification Checklist
- [ ] Tested on Stellar Testnet with a funded account
- [ ] Formatted with YAML frontmatter adhering to `schema/entry.schema.json`
- [ ] `python tools/validate_schema.py` passes with zero errors
