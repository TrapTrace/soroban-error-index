---
id: scval-type-conversion-error
title: SDK Error - ScVal to Native Rust Type Conversion Failed
category: sdk-error
error_code: SDK::ScValConversionFailed
verified: false
summary: Soroban SDK or client library failed to convert a serialized ScVal or Val handle into the expected native Rust type (e.g. integer width mismatch or invalid symbol).
tags: [sdk, scval, type-conversion, val, conversion, deserialization]
soroban_version: "21.0.0"
severity: warning
related_entries: [value-conversion-failed, invalid-scval-tag]
---

# SDK Error: ScVal to Native Rust Type Conversion Failed

## Symptoms

- Contract invocations panic with `ConversionError` when deserializing function arguments or returned values.
- Client SDKs (JS/TS, Python) fail with `Invalid ScVal discriminator` or `Cannot convert ScVal to BigInt`.
- Contract tests fail with `TryFromVal failed for target type`.

## Root Causes

1. **Integer Size Mismatches:** Passing an `i32` or `u32` into a function argument typed as `i128` or `u64` without explicit type coercion.
2. **Invalid Symbol Character Encoding:** Constructing `Symbol` or `symbol_short!` with characters outside the allowed alphanumeric + underscore set or exceeding length limits.
3. **Mismatched Struct Shape:** Contract ABI expected a tuple/struct with specific field keys, but the client passed a generic vector or mismatched map.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

#[contract]
pub struct ConversionContract;

#[contractimpl]
impl ConversionContract {
    pub fn process_amount(_env: Env, amount: i128) -> i128 {
        amount
    }
}
```

Invoke with mismatched argument type via CLI:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn process_amount \
  -- --amount "not-a-number"
```

Expected Output:
```text
error: failed to convert argument 'amount' to i128: Invalid ScVal payload
```

## Solutions

1. **Use Explicit ScVal Type Constructors:** Construct arguments explicitly in SDKs (`nativeToScVal(100n, { type: 'i128' })`).
2. **Use `TryFromVal` for Safe Conversion:** In Rust contracts, convert dynamic values using `.try_into_val(&env)` and handle conversion errors explicitly.
3. **Inspect Contract ABI:** Use `traptrace abi <contract_id>` or the Web Studio WASM ABI tab to verify exact function signature types before calling.

## References

- [Soroban Types & Conversions](https://developers.stellar.org/docs/learn/smart-contract-internals/types)
- [Stellar SDK ScVal Serialization](https://stellar.github.io/js-stellar-sdk/)
