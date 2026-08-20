---
id: contract-data-size-exceeds-limit
title: Host Error - Contract Data Size Exceeds Ledger Entry Limit
category: host-error
error_code: HostError::StorageValueExceedsLimit
verified: true
summary: Contract execution terminated because an attempted storage write or data structure serialization exceeded the maximum protocol ledger entry byte limit (64KB).
tags: [storage, size-limit, 64kb, contract-data, payload, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [budget-exceeded, storage-ledger-entry-not-found]
---

# Host Error: Contract Data Size Exceeds Ledger Entry Limit

## Symptoms

- Transaction simulation or invocation returns `HostError(Error(Storage, ExceededLimit))` or `HostError::StorageValueExceedsLimit`.
- Invocation fails when writing large collections (`Vec`, `Map`, or oversized `Bytes`) to instance or persistent storage.
- RPC error indicates `txINTERNAL_ERROR` or simulation footprint exceeds maximum allowable ledger entry byte quota.

## Root Causes

1. **Monolithic Storage Arrays:** Appending unbounded items to a single `Vec` or `Map` under one storage key until the serialized XDR exceeds the 64KB ledger entry limit.
2. **Oversized String / Blob Payloads:** Writing raw image data, JSON documents, or large byte buffers into a single storage slot instead of off-chain decentralized storage or split chunks.
3. **Bloated Instance Storage:** Storing heavy dynamic user data in `instance` storage rather than dedicated partitioned keys in `persistent` storage.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Bytes, Env, Symbol};

const LARGE_DATA: Symbol = symbol_short!("BIG_DATA");

#[contract]
pub struct SizeLimitContract;

#[contractimpl]
impl SizeLimitContract {
    pub fn store_oversized_payload(env: Env) {
        // Create a 70KB buffer exceeding the 64KB Soroban ledger entry limit
        let mut big_bytes = Bytes::new(&env);
        for _ in 0..70_000 {
            big_bytes.push_back(0x42);
        }
        env.storage().persistent().set(&LARGE_DATA, &big_bytes);
    }
}
```

Invoke the contract via CLI on testnet:
```bash
soroban contract invoke --id <CONTRACT_ID> --source-account <ACCOUNT> --network testnet --fn store_oversized_payload
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Storage, ExceededLimit)",
  "events": [
    "DiagnosticEvent: host error: HostError::StorageValueExceedsLimit"
  ]
}
```

## Solutions

1. **Partition State Across Keys:** Store individual items under distinct indexed keys (e.g. `DataKey::Item(u32)`) rather than a single monolithic `Vec`.
2. **Chunking Mechanism:** Split large payloads into 32KB chunks stored across deterministic sub-keys (`DataKey::Chunk(hash, index)`).
3. **Off-Chain Content Hashing:** Store only cryptographic hashes (e.g. IPFS / Arweave CID `BytesN<32>`) in contract storage and retain the raw data off-chain.
4. **Pre-Flight Metering:** Run `traptrace simulate <xdr>` to check simulated storage byte footprint before submitting transactions.

## References

- [Stellar Developers: Soroban Resource Limits and Fees](https://developers.stellar.org/docs/learn/fundamentals/fees-and-metering)
- [CAP-0046: Soroban State Archival and Storage Sizing](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046.md)
