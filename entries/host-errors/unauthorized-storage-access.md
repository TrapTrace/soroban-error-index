---
id: unauthorized-storage-access
title: "Host Error - Unauthorized Contract Storage Footprint Access"
category: host-error
error_code: "HostError::StorageAccessUnauthorized"
verified: false
summary: "Contract execution attempted to access storage ledger keys outside its allocated ledger footprint or across contract security boundaries."
tags: [host-error, storage, footprint, security, permissions]
soroban_version: "21.0.0"
severity: critical
related_entries: [storage-ledger-entry-not-found, storage-key-missing]
---

## Symptoms
- Transactions fail during on-chain execution with `StorageAccessUnauthorized` or `FootprintMismatch`.
- Simulation succeeds on local mock environment but fails when submitted to live network RPC.
- Multi-contract transaction envelopes reject execution before state mutations take effect.

## Root Causes
1. **Cross-Contract Storage Boundary Violation:** Attempting to directly inspect or mutate another contract instance's private storage keys without going through its exported public methods.
2. **Missing Ledger Footprint in Transaction Envelope:** The transaction envelope omitted read-only or read-write footprint keys required by nested sub-invocations.
3. **Dynamic Key Resolution Drift:** The contract dynamically computed a storage key at runtime that was not present in the pre-flight simulated footprint.

## Reproduction Steps
```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

#[contract]
pub struct UnauthorizedStorageContract;

#[contractimpl]
impl UnauthorizedStorageContract {
    pub fn access_foreign_storage(env: Env) {
        let key = symbol_short!("FOREIGN");
        let _val: u32 = env.storage().instance().get(&key).unwrap();
    }
}
```

## Solutions
1. **Access Foreign State via Public Methods:** Always query foreign contract data through its exported getter interface:
   ```rust
   let target_client = TargetContractClient::new(&env, &target_address);
   let value = target_client.get_value();
   ```
2. **Pre-flight Footprint Synchronization:** Always generate transaction footprints via `simulateTransaction` and attach the exact returned footprint to the signed transaction envelope.
3. **Inspect Contract Ledger Entries:** Use `traptrace storage --contract <id>` or the Web Studio Storage Auditor to verify valid storage ownership.

## References
- [Stellar RPC simulateTransaction Footprint Specs](https://developers.stellar.org/docs/data/rpc/api-reference/methods/simulateTransaction)
- [Soroban Storage Isolation Architecture](https://developers.stellar.org/docs/learn/smart-contract-internals/state-archival)
