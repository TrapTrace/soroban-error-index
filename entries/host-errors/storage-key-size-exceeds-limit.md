---
id: storage-key-size-exceeds-limit
title: Host Error - Ledger Storage Key Size Exceeds Network Cap
category: host-error
error_code: HostError::StorageKeySizeLimit
verified: false
summary: Contract attempted to persist a storage entry whose key exceeds Soroban's maximum ledger key size limit (typically 64KB or protocol cap).
tags: [storage, limits, key-size, protocol-limits, scval]
soroban_version: "21.0.0"
severity: warning
related_entries: [contract-data-size-exceeds-limit, host-invalid-action]
---

# Host Error: Ledger Storage Key Size Exceeds Network Cap

## Symptoms

- Contract simulation fails during storage write with `HostError(Error(Storage, KeySizeLimitExceeded))` or `HostError(Error(Context, InvalidAction))`.
- Writing dynamic keys containing large byte buffers or concatenated strings causes transactions to abort immediately.
- RPC simulation returns zero execution progress past the storage write instruction.

## Root Causes

1. **Embedding Payloads Inside Storage Keys:** Using arbitrary user-supplied data (such as IPFS hashes, large string IDs, or public keys combined with descriptions) directly as a storage key instead of computing a fixed-size hash.
2. **Unbounded Key Structures:** Serializing complex structs or nested tuples into storage keys without enforcing fixed upper bounds.
3. **Protocol Key Size Quota Violation:** Exceeding Soroban's strict protocol limits on `ScVal` key serialization length.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Bytes, Env};

#[contract]
pub struct HugeKeyContract;

#[contractimpl]
impl HugeKeyContract {
    pub fn write_oversized_key(env: Env, large_key_data: Bytes, value: u32) {
        // Attempting to write a key larger than allowable ledger limits
        env.storage().persistent().set(&large_key_data, &value);
    }
}
```

Invoke with an oversized byte payload:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn write_oversized_key \
  -- --large_key_data <HEX_STRING_EXCEEDING_LIMIT> --value 42
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Storage, KeySizeLimitExceeded)",
  "events": [
    "DiagnosticEvent: host error: HostError::StorageKeySizeLimit (storage key bytes exceed limit)"
  ]
}
```

## Solutions

1. **Hash Dynamic Keys with SHA-256 / Keccak:** Hash variable-length keys using `env.crypto().sha256(&large_key_data)` to produce a deterministic 32-byte `BytesN<32>` key.
2. **Use Enums / Symbols for Fixed Keys:** Use short symbols (`symbol_short!("admin")`) or typed enums (`DataKey::Balance(Address)`) for predictable key sizes.
3. **Validate Key Lengths:** Enforce strict input validation in contract arguments before executing storage calls.

## References

- [Stellar Network Protocol Limits](https://developers.stellar.org/docs/learn/fundamentals/stellar-data-structures/operations-and-transactions)
- [Soroban Crypto Host Functions](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Crypto.html)
