---
id: unreachable-code-reached
title: Host Error - WASM Unreachable Code Reached (Panic)
category: host-error
error_code: HostError::WasmUnreachable
verified: true
summary: WASM virtual machine hit an explicit panic instruction or out-of-bounds index execution.
tags: [wasm, panic, unreachable, bounds, host-error]
soroban_version: "21.0.0"
---

# Host Error: WASM Unreachable Code Reached (Panic)

## Symptoms

- Call fails with `HostError(Error(WasmVm, Unexpected))`.
- Terminal log reports `VM trapped: unreachable code executed`.
- Contract panics abruptly during call.

## Root Causes

1. **Unwrap on None/Err:** Calling `.unwrap()` or `.expect()` on an Option/Result that returned `None` or `Err`.
2. **Out of Bounds Indexing:** Accessing vector or array elements at invalid indexes (`vec[index]`).
3. **Integer Division by Zero:** Performing `a / b` when `b == 0`.

## Reproduction Steps

```rust
pub fn divide(env: Env, a: u64, b: u64) -> u64 {
    // Triggers unreachable code panic when b == 0
    a / b
}
```

## Solutions

1. **Use Checked Operations & Match:** Avoid `.unwrap()`. Return `Result<T, ContractError>` instead.
2. **Safe Math & Boundary Checks:** Validate inputs before indexing or performing division.

```rust
pub fn safe_divide(env: Env, a: u64, b: u64) -> Result<u64, Error> {
    if b == 0 {
        return Err(Error::from_contract_error(1));
    }
    Ok(a / b)
}
```

## References

- [Soroban Error Handling Best Practices](https://developers.stellar.org/docs/build/smart-contracts/getting-started/errors)
