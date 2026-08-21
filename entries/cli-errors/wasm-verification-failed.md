---
id: wasm-verification-failed
title: CLI Error - Contract WASM Module Bytecode Verification Failed
category: cli-error
error_code: CLI::WasmVerificationFailed
verified: true
summary: Contract upload or installation failed because the compiled WASM binary violates Soroban VM constraints, contains unsupported floating-point operations, or imports unexported host interfaces.
tags: [wasm, bytecode, verification, deployment, install, upload, cli-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [unreachable-code-reached, wasm-memory-exhausted]
---

# CLI Error: Contract WASM Module Bytecode Verification Failed

## Symptoms

- Contract installation via `stellar contract install` or `soroban contract deploy` fails during the simulation or upload phase.
- CLI output displays: `error: contract wasm verification failed: invalid import or unsupported opcode`.
- Simulation RPC returns: `HostError(Error(WasmVm, InvalidAction))` or `contract bytecode failed validation against VM protocol limits`.

## Root Causes

1. **Floating Point Operations (f32/f64):** Standard Rust mathematical libraries compiled without `#![no_std]` or using floating-point operations that non-deterministically violate Soroban VM determinism rules.
2. **Missing WASM Target Optimization:** The WASM file was compiled for generic `wasm32-unknown-unknown` without running `stellar contract build` or `soroban-opt`, leaving unsupported external imports or standard library system call bindings.
3. **WASM Section Limit Exceeded:** The compiled bytecode imports host functions from non-existent modules or exceeds custom section table limits defined in the current Stellar Protocol version.

## Reproduction Steps

Attempt to deploy a non-Soroban compiled WASM or corrupted bytecode binary:

```bash
# Create a dummy malformed WASM header
echo -n -e '\x00\x61\x73\x6d\x01\x00\x00\x00\x00\x05\x01\x02\x03\x04\x05' > invalid_contract.wasm

# Attempt to install on testnet
soroban contract install \
  --wasm invalid_contract.wasm \
  --source default \
  --network testnet
```

Expected Output:
```text
error: failed to install contract wasm
  Caused by:
    0: host error: Error(WasmVm, InvalidAction)
    1: DiagnosticEvent: host error: WASM module bytecode verification failed (invalid section structure or illegal imports)
```

## Solutions

1. **Build with the Official Toolchain:** Always compile contracts with `stellar contract build` (or `cargo build --target wasm32-unknown-unknown --release` followed by `stellar contract optimize`).
2. **Ensure `#![no_std]` Compliance:** Avoid standard library dependencies that invoke OS syscalls (`std::fs`, `std::net`, `std::time`, or threading).
3. **Run WASM Inspection & Validation:** Use `traptrace decode` or `wasm-tools validate contract.wasm` prior to deployment to verify opcode determinism and section tables.

## References

- [Stellar Developers: Building and Optimizing Soroban Contracts](https://developers.stellar.org/docs/build/smart-contracts/getting-started/build)
- [Soroban VM Bytecode Specification and Opcode Constraints](https://developers.stellar.org/docs/learn/smart-contract-internals/execution-model)
