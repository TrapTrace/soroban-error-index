---
id: budget-exceeded
title: Host Error - CPU or Memory Execution Budget Exceeded
category: host-error
error_code: HostError::BudgetExceeded
verified: true
summary: Contract execution terminated because CPU instruction count or memory allocation exceeded specified envelope limits.
tags: [budget, cpu, memory, limits, host-error]
soroban_version: "21.0.0"
---

# Host Error: CPU or Memory Execution Budget Exceeded

## Symptoms

- Transaction simulation or invocation returns `HostError::BudgetExceeded`.
- CLI output displays `Error: HostError(Error(Budget, Exceeded))`.
- Contract fails during high-iteration loops, complex cryptographic verification, or large serialization operations.

## Root Causes

1. **Unbounded Loops:** Iterating over unbounded storage vectors or maps within a single contract call.
2. **Heavy Computation:** Performing cryptographic hashing, sorting, or heavy math operations inside WASM without leveraging built-in host functions.
3. **Large Memory Allocations:** Instantiating large vectors, buffers, or complex nested structures that exceed allocated byte limits.

## Reproduction Steps

```rust
// Contract code containing unbounded iteration
pub fn process_all_items(env: Env, items: Vec<u32>) {
    for item in items.iter() {
        // Heavy computation per item causing CPU budget failure
        let _result = heavy_hash_calculation(item);
    }
}
```

Invoke the contract with a vector of 10,000 items on testnet:
```bash
soroban contract invoke --id <CONTRACT_ID> --fn process_all_items -- --items '[...]'
```

## Solutions

1. **Chunking & Pagination:** Break processing into smaller batches across multiple transactions rather than processing in a single call.
2. **Optimize Host Functions:** Use Soroban host-provided primitives (`env.crypto().sha256()`) instead of pure WASM crypto implementations.
3. **Increase Budget (Test Harness Only):** In local unit tests, raise the budget with `env.budget().reset_unlimited()`.

## References

- [Stellar Developers: Soroban Resource Model](https://developers.stellar.org/docs/learn/fundamentals/fees-and-metering)
- [Soroban Host Environment Budget Specification](https://github.com/stellar/rs-soroban-env)
