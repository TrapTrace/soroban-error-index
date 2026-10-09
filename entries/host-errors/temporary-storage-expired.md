---
id: temporary-storage-expired
title: Host Error - Temporary Ledger Storage Entry Expired (TTL Evicted)
category: host-error
error_code: HostError::TemporaryStorageExpired
verified: false
summary: Contract attempted to read or write a temporary storage key whose time-to-live (TTL) passed without being bumped, resulting in permanent eviction.
tags: [storage, ttl, temporary-storage, eviction, cap-0046, rent]
soroban_version: "21.0.0"
severity: critical
related_entries: [entry-archived-ttl-expired, storage-ledger-entry-not-found]
---

# Host Error: Temporary Ledger Storage Entry Expired (TTL Evicted)

## Symptoms

- Contract simulation fails with `HostError(Error(Storage, DeadEntry))` or `Error(Storage, MissingValue)`.
- Temporary state keys (nonces, short-lived signatures, session authorizations) cannot be read after a ledger threshold.
- Unlike Persistent storage entries, calling `extend_ttl` or restoration transactions fails because temporary entries are permanently deleted upon TTL expiration.

## Root Causes

1. **Failure to Bump Temporary TTL:** Temporary storage entries (`env.storage().temporary()`) were created with a short initial TTL (e.g., 16 ledgers) and never renewed using `env.storage().temporary().extend_ttl(...)`.
2. **Permanent Deletion Model:** Soroban state archival (CAP-0046) treats temporary entries as ephemeral; once expired, they cannot be restored via `RestoreFootprintOp`.
3. **Misclassifying Persistent State as Temporary:** Storing critical protocol state (user balances, pool reserves) in temporary storage rather than persistent or instance storage.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

const TEMP_KEY: Symbol = symbol_short!("session");

#[contract]
pub struct TempStorageContract;

#[contractimpl]
impl TempStorageContract {
    pub fn init_session(env: Env, user_id: u32) {
        // Stored in temporary storage without TTL extension
        env.storage().temporary().set(&TEMP_KEY, &user_id);
    }

    pub fn get_session(env: Env) -> u32 {
        // Fails with Storage DeadEntry if called after temporary TTL expires
        env.storage().temporary().get(&TEMP_KEY).unwrap()
    }
}
```

Invoke `get_session` after the temporary TTL passes:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn get_session
```

Expected RPC Simulation Error:
```json
{
  "error": "HostError: Error(Storage, MissingValue)",
  "events": [
    "DiagnosticEvent: host error: HostError::TemporaryStorageExpired (key evicted from state)"
  ]
}
```

## Solutions

1. **Extend Temporary TTL on Read/Write:** Call `env.storage().temporary().extend_ttl(&TEMP_KEY, threshold, extend_to)` whenever accessing active sessions.
2. **Use Persistent Storage for State:** Use `env.storage().persistent()` for ledger data that may need to be restored if archived.
3. **Use Instance Storage for Shared Protocol State:** Store contract admin and configuration data in `env.storage().instance()`.

## References

- [Stellar Docs: State Archival & Storage Types](https://developers.stellar.org/docs/learn/smart-contract-internals/state-archival)
- [CAP-0046: Soroban State Archival](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046.md)
