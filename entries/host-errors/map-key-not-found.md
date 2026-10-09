---
id: map-key-not-found
title: Host Error - Soroban SDK Map Key Lookup Miss Panic
category: host-error
error_code: HostError::MapKeyNotFound
verified: false
summary: Contract execution panicked because a key lookup on a Soroban SDK Map failed to find the key and was followed by an explicit unwrap.
tags: [host-error, map, collection, key-not-found, panic, unwrap]
soroban_version: "21.0.0"
severity: critical
related_entries: [vec-index-out-of-bounds, option-unwrap-none, storage-ledger-entry-not-found]
---

# Host Error: Soroban SDK Map Key Lookup Miss Panic

## Symptoms

- Contract simulation reverts with `HostError(Error(Context, InvalidAction))` or `HostError(Error(Object, MissingKey))`.
- Diagnostic events contain: `called Option::unwrap() on a None value` during Map retrieval.
- User profile lookups, allowance lookups, or account registry lookups fail for unregistered users.

## Root Causes

1. **Unsafe `map.get(key).unwrap()`:** Assuming all possible queried keys exist in the Map collection.
2. **Missing Key Initialization:** Reading an account balance or settings map before an account has been initialized.
3. **Key Equality Mismatch:** Querying a Map with a subtly mismatched key type (e.g., mismatched Symbol casing or different address formatting).

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Address, Env, Map};

#[contract]
pub struct MapKeyContract;

#[contractimpl]
impl MapKeyContract {
    pub fn get_balance(_env: Env, accounts: Map<Address, i128>, user: Address) -> i128 {
        // Panics if user is not present in accounts map
        accounts.get(user).unwrap()
    }
}
```

Invoke with an unregistered address:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn get_balance \
  -- --accounts "{}" --user "GBXYZ..."
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Context, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::MapKeyNotFound (unwrapping absent map key)"
  ]
}
```

## Solutions

1. **Use `get()` with `unwrap_or` or Default:**
   ```rust
   let balance = accounts.get(user).unwrap_or(0);
   ```
2. **Return `Result<T, CustomError>`:**
   ```rust
   let balance = accounts.get(user).ok_or(CustomError::UserNotFound)?;
   ```
3. **Check `contains_key()` First:** Check `if !accounts.contains_key(user)` before processing dependent logic.

## References

- [Soroban SDK Map Documentation](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Map.html)
- [Soroban Error Handling Best Practices](https://developers.stellar.org/docs/learn/smart-contract-internals/errors)
