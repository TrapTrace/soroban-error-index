---
id: sub-invocation-user-error
title: Host Error - User-Defined Contract Error in Cross-Contract Sub-Invocation
category: host-error
error_code: HostError::ContractUserError
verified: true
summary: Cross-contract execution reverted because the callee contract returned an explicit user-defined contract error enum discriminant.
tags: [cross-contract, sub-invocation, custom-error, contracterror, bubbling, host-error]
soroban_version: "21.0.0"
severity: warning
related_entries: [sub-invocation-failed, unreachable-code-reached]
---

# Host Error: User-Defined Contract Error in Cross-Contract Sub-Invocation

## Symptoms

- Transaction simulation or invocation terminates with `HostError(Error(Contract, 1))` (or other integer error code).
- Top-level contract aborts even though its own logic has not panicked.
- Diagnostic events list shows callee contract emitting error discriminant before aborting execution context.

## Root Causes

1. **Callee Business Logic Assertion:** The target child contract hit a business logic validation failure (e.g. `InsufficientBalance`, `UnauthorizedCaller`) and returned a custom `#[contracterror]` variant.
2. **Unhandled `Result<T, E>` in Caller:** The invoking contract called a child contract method that returns `Result` but immediately used `.unwrap()` or the `?` operator without catching or mapping domain errors.
3. **Invalid Invariant in Child Contract:** Callee state was corrupted or uninitialized, leading the callee to return an error variant.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contracterror, contractimpl, Address, Env};

#[contracterror]
#[derive(Copy, Clone, Debug, Eq, PartialEq, PartialOrd, Ord)]
#[repr(u32)]
pub enum VaultError {
    VaultLocked = 1,
    InsufficientFunds = 2,
}

#[contract]
pub struct VaultContract;

#[contractimpl]
impl VaultContract {
    pub fn withdraw(_env: Env, _amount: i128) -> Result<(), VaultError> {
        // Explicitly return a user-defined contract error
        Err(VaultError::VaultLocked)
    }
}
```

Invoke caller contract that invokes `VaultContract::withdraw`:
```bash
soroban contract invoke --id <CALLER_CONTRACT_ID> --network testnet --fn call_vault
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Contract, 1)",
  "events": [
    "DiagnosticEvent: contract call failed: Error(Contract, 1)"
  ]
}
```

## Solutions

1. **Catch and Handle Errors in Caller:** Avoid unconditional `.unwrap()`; use pattern matching or `match callee_client.try_withdraw(&amount)` to handle child error variants gracefully.
2. **Inspect Error Code Enum:** Look up the callee contract's `#[contracterror]` definition to map the integer discriminant (e.g. `1` $\rightarrow$ `VaultLocked`).
3. **Trace Invocations with CLI:** Run `traptrace inspect <tx_hash>` or `traptrace simulate <xdr>` to view the full cross-contract call tree and pinpoint which child contract emitted the error code.

## References

- [Stellar Developers: Soroban Custom Errors and ContractError](https://developers.stellar.org/docs/learn/smart-contract-internals/errors)
- [Soroban Rust SDK ContractError Attribute](https://docs.rs/soroban-sdk/latest/soroban_sdk/attr.contracterror.html)
