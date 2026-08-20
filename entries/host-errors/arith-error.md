---
id: arith-error
title: Host Error - Integer Arithmetic Overflow, Underflow, or Division by Zero
category: host-error
error_code: HostError::ArithDomain
verified: true
summary: Contract execution panicked due to an arithmetic domain error such as integer overflow, underflow, or division by zero in WASM.
tags: [arithmetic, overflow, underflow, divide-by-zero, math, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [unreachable-code-reached, host-invalid-action]
---

# Host Error: Integer Arithmetic Overflow, Underflow, or Division by Zero

## Symptoms

- Contract simulation or execution aborts immediately with `HostError(Error(Context, InvalidAction))` or `HostError::ArithDomain`.
- Diagnostic events indicate an unreachable panic (`attempt to add with overflow` or `attempt to divide by zero`).
- Token transfers, reward calculation math, or liquidity pool calculations fail during extreme value inputs.

## Root Causes

1. **Unchecked Integer Math:** Performing raw Rust operators (`+`, `-`, `*`, `/`) in release or debug mode where arithmetic overflows trigger a WASM trap.
2. **Division by Zero:** Executing `/` or `%` on a variable denominator that evaluated to `0` without guard checks.
3. **Lossy Casting:** Casting large integer types (`i128` to `u64` or `i64`) where values exceed destination type boundaries.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Env};

#[contract]
pub struct ArithErrorContract;

#[contractimpl]
impl ArithErrorContract {
    pub fn calculate_overflow(_env: Env, base: u128) -> u128 {
        // Raw arithmetic addition triggers overflow panic on u128::MAX
        base + 1
    }

    pub fn calculate_divide_zero(_env: Env, val: u64, divisor: u64) -> u64 {
        // Triggers division by zero if divisor is 0
        val / divisor
    }
}
```

Invoke the contract via CLI with `u128::MAX` on testnet:
```bash
soroban contract invoke --id <CONTRACT_ID> --network testnet --fn calculate_overflow -- --base 340282366920938463463374607431768211455
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Context, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::ArithDomain (arithmetic overflow panic)"
  ]
}
```

## Solutions

1. **Use Checked Arithmetic:** Replace raw operators with checked arithmetic methods (`checked_add`, `checked_sub`, `checked_mul`, `checked_div`) and handle `None` gracefully.
2. **Use Saturating Arithmetic:** Use `saturating_add` or `saturating_sub` where clamping values to type limits is acceptable.
3. **Explicit Zero Checks:** Validate divisors before executing division or modulo operations (`if divisor == 0 { return Err(Error::ZeroDivisor); }`).

## References

- [Stellar Developers: Soroban Safe Math Practices](https://developers.stellar.org/docs/learn/smart-contract-internals/errors)
- [Rust Standard Library Checked Arithmetic](https://doc.rust-lang.org/std/primitive.u128.html#method.checked_add)
