---
id: option-unwrap-none
title: Host Error - Rust Option::unwrap() Called on None in Contract Code
category: host-error
error_code: HostError::OptionUnwrapNone
verified: true
summary: Contract execution panicked because Option::unwrap() or Result::unwrap() was invoked on a None or Err value inside the smart contract WASM bytecode.
tags: [host-error, unwrap, panic, option, rust, safe-rust]
soroban_version: "21.0.0"
severity: critical
related_entries: [vec-index-out-of-bounds, map-key-not-found, unreachable-code-reached]
---

# Host Error: Rust Option::unwrap() Called on None in Contract Code

## Symptoms

- Contract simulation halts immediately with `HostError(Error(Context, InvalidAction))` or `HostError(Error(WasmVm, UnreachableCodeReached))`.
- Diagnostic events contain: `panicked at 'called Option::unwrap() on a None value'`.
- Gas is consumed up to the point of panic and all state modifications are rolled back.

## Root Causes

1. **Direct `unwrap()` on Fallible Operations:** Using `.unwrap()` on storage reads, map lookups, vector element indexing, or math helpers.
2. **Missing Input / Environment Guards:** Assuming optional parameters or ambient contract configurations are always populated.
3. **Rust Standard Panic in WASM:** In `no_std` Soroban builds, any `panic!` invokes the WASM unreachable instruction, causing the host to trap.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

const OWNER_KEY: Symbol = symbol_short!("owner");

#[contract]
pub struct UnwrapContract;

#[contractimpl]
impl UnwrapContract {
    pub fn get_owner(env: Env) -> Symbol {
        // Panics if OWNER_KEY was not previously written to instance storage
        env.storage().instance().get(&OWNER_KEY).unwrap()
    }
}
```

Invoke `get_owner` prior to storage initialization:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn get_owner
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Context, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::OptionUnwrapNone (panicked at unwrap on None)"
  ]
}
```

## Solutions

1. **Use `?` Operator with Custom Error Enums:**
   ```rust
   #[contracterror]
   #[derive(Copy, Clone, Debug, Eq, PartialEq, PartialOrd, Ord)]
   #[repr(u32)]
   pub enum Error {
       NotInitialized = 1,
   }

   pub fn get_owner(env: Env) -> Result<Symbol, Error> {
       env.storage().instance().get(&OWNER_KEY).ok_or(Error::NotInitialized)
   }
   ```
2. **Use `unwrap_or()` or `unwrap_or_else()`:** Provide safe fallback defaults for non-critical reads.
3. **Use TrapTrace Linter:** Run `traptrace lint <file.rs>` to automatically detect unsafe `.unwrap()` patterns before compiling.

## References

- [Soroban Custom Errors Guide](https://developers.stellar.org/docs/learn/smart-contract-internals/errors#custom-errors)
- [Rust Error Handling Book](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html)
