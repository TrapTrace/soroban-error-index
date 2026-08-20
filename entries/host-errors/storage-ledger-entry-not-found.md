---
id: storage-ledger-entry-not-found
title: Host Error - Storage Ledger Entry Not Found or Missing Value
category: host-error
error_code: HostError::StorageNotFound
verified: true
summary: Contract attempted to read a non-existent or uninitialized key from instance, persistent, or temporary storage without fallback handling.
tags: [storage, ledger-entry, missing-value, persistent, temporary, instance, host-error]
soroban_version: "21.0.0"
severity: warning
related_entries: [storage-key-missing, entry-archived-ttl-expired]
---

# Host Error: Storage Ledger Entry Not Found or Missing Value

## Symptoms

- Contract invocation halts with `HostError(Error(Storage, MissingValue))` or `HostError::StorageNotFound`.
- Diagnostic events indicate an unwrap on `None` following an `env.storage().instance().get(&key)` call.
- Simulation trace shows contract failed during state initialization or state transition reads.

## Root Causes

1. **Unchecked Storage Unwrap:** Calling `.get(&key).unwrap()` on a storage key that has not yet been set or initialized on-chain.
2. **Storage Key Type Mismatch:** Querying a key using a different type representation than the one used during write (e.g. `Symbol` vs `u32` or enum variant discriminant).
3. **Storage Tier Confusion:** Storing data in `temporary` storage that has expired at a ledger boundary, or confusing `instance` vs `persistent` storage locations.
4. **Deleted State Entries:** Attempting to retrieve a key that was explicitly removed via `env.storage().persistent().remove(&key)`.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

const COUNTER: Symbol = symbol_short!("COUNTER");

#[contract]
pub struct StorageMissingContract;

#[contractimpl]
impl StorageMissingContract {
    pub fn get_counter_unsafe(env: Env) -> u32 {
        // Direct unwrap without checking existence or providing a default
        env.storage().instance().get(&COUNTER).unwrap()
    }
}
```

Invoke the contract via CLI before any initialization:
```bash
soroban contract invoke --id <CONTRACT_ID> --source-account <ACCOUNT> --network testnet --fn get_counter_unsafe
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Storage, MissingValue)",
  "events": [
    "DiagnosticEvent: host error: HostError::StorageNotFound"
  ]
}
```

## Solutions

1. **Use `get_or` Pattern:** Always use `.get(&key).unwrap_or(default_value)` or `env.storage().instance().has(&key)` before accessing storage values.
2. **Safe Option Handling:** Return `Option<T>` from read-only contract methods instead of panicking on uninitialized values.
3. **Consistent Type Serialization:** Define a dedicated enum for storage keys (e.g. `#[contracttype] pub enum DataKey { Counter, Admin }`) to eliminate type mismatches across reads and writes.
4. **Inspect State with CLI:** Run `traptrace storage --contract <CONTRACT_ID>` to verify which storage keys exist on-chain and their TTL status.

## References

- [Stellar Developers: State Storage in Soroban](https://developers.stellar.org/docs/learn/smart-contract-internals/state-archival)
- [Soroban Rust SDK Storage Documentation](https://docs.rs/soroban-sdk/latest/soroban_sdk/storage/index.html)
