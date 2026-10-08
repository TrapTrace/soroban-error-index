---
id: contract-spec-missing
title: "CLI Error - WASM Contract Specification (ABI) Metadata Missing or Stripped"
category: cli-error
error_code: "CLI::ContractSpecMissing"
verified: false
summary: "Contract WASM file deployed without embedded contract specification custom sections, preventing automated ABI decoding, binding generation, and CLI inspection."
tags: [cli-error, abi, wasm, spec, tooling]
soroban_version: "21.0.0"
severity: warning
related_entries: [wasm-verification-failed, host-invalid-action]
---

## Symptoms
- `stellar contract bindings` or `soroban contract bindings typescript` fails with `Error: Contract has no spec`.
- `traptrace abi <contract_id>` or the Web Studio WASM ABI tab indicates `No exported contract functions found`.
- Block explorers cannot render human-readable method signatures or argument input fields.

## Root Causes
1. **Aggressive WASM Optimization Stripping Custom Sections:** Compiling with `wasm-opt --strip-all` or `wasm-strip` instead of preserving the `.soroban_spec` custom section.
2. **Missing `contractimpl` Macro Attribute:** Writing Rust methods without decorating the `impl` block with `#[contractimpl]`.
3. **Manual WASM Assembly:** Compiling raw WASM bytecode without the Soroban SDK build target.

## Reproduction Steps
```bash
wasm-opt -Oz --strip-all contract.wasm -o contract_stripped.wasm
stellar contract bindings typescript --wasm contract_stripped.wasm --output-dir ./bindings
```

## Solutions
1. **Preserve Custom Sections in `wasm-opt`:** When running `wasm-opt`, use `--strip-debug` instead of `--strip-all` to keep `.soroban_spec`:
   ```bash
   wasm-opt -Oz --strip-debug target/wasm32-unknown-unknown/release/contract.wasm -o contract.optimized.wasm
   ```
2. **Use `stellar contract build`:** Prefer the official Stellar CLI build command which automatically optimizes while preserving metadata:
   ```bash
   stellar contract build
   ```
3. **Verify with TrapTrace WASM Inspector:** Use `traptrace abi <contract_id>` to confirm your deployed contract exports valid method specifications.

## References
- [Soroban CLI Contract Build & Optimization](https://developers.stellar.org/docs/tools/developer-tools/cli/stellar-cli)
- [Soroban Contract Specification Format](https://developers.stellar.org/docs/learn/smart-contract-internals/types#contract-spec)
