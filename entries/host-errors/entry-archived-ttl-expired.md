---
id: entry-archived-ttl-expired
title: Host Error - Storage Entry Archived or TTL Expired
category: host-error
error_code: HostError::EntryArchived
verified: true
summary: Attempted access to a persistent or instance storage entry whose Time-To-Live (TTL) has expired and been archived.
tags: [storage, ttl, archive, state-archival, host-error]
soroban_version: "21.0.0"
---

# Host Error: Storage Entry Archived or TTL Expired

## Symptoms

- Call fails with error string `Error(Storage, ExceededStateArchival)`.
- Transaction simulation rejects access to persistent key with message `ContractData entry archived`.
- Previously functioning contract suddenly fails when accessing user balance or state.

## Root Causes

1. **State Archival:** State entry was not bumped prior to reaching minimum TTL threshold (CAP-0046).
2. **Missing Restored Access:** Accessing archived state without issuing a `RestoreFootprint` transaction.

## Reproduction Steps

1. Deploy a contract with persistent storage entries.
2. Allow ledger sequence to advance past the entry's expiration ledger sequence.
3. Call a read/write function touching the expired storage key.

```rust
pub fn read_user_data(env: Env, user: Address) -> UserData {
    // Fails if TTL has reached zero
    env.storage().persistent().get(&user).unwrap()
}
```

## Solutions

1. **Bump TTL in Contract Logic:** Use `env.storage().persistent().extend_ttl(&key, threshold, extend_to)` to proactively renew storage lifespan.
2. **Issue Restore Transaction:** Submit a `RestoreFootprint` operation via Soroban CLI or SDK before invoking the contract.

```bash
soroban contract restore --id <CONTRACT_ID> --key <STORAGE_KEY>
```

## References

- [CAP-0046: Soroban State Archival](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046.md)
- [Stellar Documentation: State Archival Lifecycle](https://developers.stellar.org/docs/learn/fundamentals/state-archival)
