---
id: vec-index-out-of-bounds
title: Host Error - Soroban SDK Vec Index Out of Bounds Panic
category: host-error
error_code: HostError::VecIndexOutOfBounds
verified: true
summary: Contract execution panicked because an indexing operation on a Soroban SDK Vec accessed an index greater than or equal to the vector length.
tags: [host-error, vec, collection, index-out-of-bounds, panic, bounds-check]
soroban_version: "21.0.0"
severity: critical
related_entries: [map-key-not-found, option-unwrap-none, unreachable-code-reached]
---

# Host Error: Soroban SDK Vec Index Out of Bounds Panic

## Symptoms

- Contract simulation reverts abruptly with `HostError(Error(Context, InvalidAction))` or `HostError(Error(Object, IndexOutOfBounds))`.
- Diagnostic events contain a panic message: `index out of bounds: the len is X but the index is Y`.
- Multi-recipient payouts or batch array iterations crash mid-execution.

## Root Causes

1. **Unchecked Direct Indexing:** Calling `vec.get(index).unwrap()` or `vec.get_unchecked(index)` where `index >= vec.len()`.
2. **Off-by-One Loop Iteration:** Using `<=` instead of `<` in numeric iteration loops over vector lengths.
3. **Empty Collection Assumptions:** Assuming a contract state vector or user input list has at least one element without guarding `if vec.is_empty()`.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, vec, Env, Vec};

#[contract]
pub struct VecBoundsContract;

#[contractimpl]
impl VecBoundsContract {
    pub fn get_element(env: Env, index: u32) -> u32 {
        let items: Vec<u32> = vec![&env, 10, 20, 30];
        // Panics if index >= 3
        items.get(index).unwrap()
    }
}
```

Invoke with index `5` on testnet:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn get_element \
  -- --index 5
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Object, IndexOutOfBounds)",
  "events": [
    "DiagnosticEvent: host error: HostError::VecIndexOutOfBounds (index 5 >= len 3)"
  ]
}
```

## Solutions

1. **Use `get()` and Match/Handle `None`:** Instead of unwrapping, handle `None` gracefully:
   ```rust
   match items.get(index) {
       Some(val) => Ok(val),
       None => Err(Error::ItemNotFound),
   }
   ```
2. **Validate Input Index:** Check `if index >= items.len() { return Err(Error::OutOfBounds); }`.
3. **Use Iterators:** Iterate elements directly with `for item in items.iter()` to eliminate manual indexing errors.

## References

- [Soroban SDK Vec Documentation](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Vec.html)
- [Rust Array and Vector Bounds Checking](https://doc.rust-lang.org/book/ch08-01-vectors.html)
