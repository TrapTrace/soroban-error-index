---
id: value-conversion-failed
title: SDK Error - ScVal to Native JavaScript/Rust Value Conversion Failed
category: sdk-error
error_code: SDK::ScValConversionError
verified: true
summary: Soroban SDK failed to deserialize raw XDR ScVal into target programming language primitive or struct.
tags: [sdk, scval, xdr, conversion, sdk-error]
soroban_version: "21.0.0"
---

# SDK Error: ScVal to Native Value Conversion Failed

## Symptoms

- SDK throws `TypeError: Cannot convert ScVal to native type`.
- Panic in Rust client: `called Result::unwrap() on an Err value: ConversionError`.

## Root Causes

1. **Type Mismatch:** Attempting to decode `ScVal::Symbol` as `ScVal::I128` or `ScVal::Address`.
2. **Schema Drift:** SDK client bindings out of sync with contract Wasm interface schema.

## Reproduction Steps

Pass a string argument in JS SDK to a contract function parameter expecting `i128`.

## Solutions

1. **Use Type-Safe Binding Generator:** Generate client bindings using `soroban contract bindings typescript`.
2. **Explicit Conversion Helpers:** Use `scValToNative()` and `nativeToScVal()` helpers with proper type casting.

## References

- [Stellar Soroban JS SDK Documentation](https://stellar.github.io/js-soroban-client/)
