---
id: cross-contract-reentrancy-blocked
title: "Host Error - Cross-Contract Re-entrancy Blocked"
category: host-error
error_code: "HostError::ReentrancyBlocked"
verified: false
summary: "Soroban host VM detected mutual recursive invocation cycle across contract call frames without explicit reentrancy permissions."
tags: [host-error, reentrancy, cross-contract, security, recursion]
soroban_version: "21.0.0"
severity: critical
related_entries: [sub-invocation-failed, budget-exceeded]
---

## Symptoms
- Complex cross-contract calls fail with `HostError(Context, ReentrancyBlocked)` or WASM call stack abort.
- Flash loan or automated market maker (AMM) callbacks fail unexpectedly.
- Diagnostic events output circular contract invocation traces: `Contract A -> Contract B -> Contract A`.

## Root Causes
1. **Direct Circular Call Stack:** Contract A called Contract B, which attempted to call back into Contract A while execution frame A was still active.
2. **Reentrancy Guard Activation:** The target contract employs a reentrancy mutex (`storage().instance().set(&LOCKED, &true)`) and detected an interleaved invocation.
3. **Unchecked Callback Interfaces:** Implementing external hook/callback mechanisms without decoupling state mutations from external dispatch.

## Reproduction Steps
```rust
use soroban_sdk::{contract, contractimpl, Address, Env};

#[contract]
pub struct ReentrantContract;

#[contractimpl]
impl ReentrantContract {
    pub fn execute_callback(env: Env, target: Address) {
        let client = CallbackClient::new(&env, &target);
        client.on_callback(&env.current_contract_address());
    }
}
```

## Solutions
1. **Checks-Effects-Interactions Pattern:** Perform all internal balance and state updates *before* calling external contract interfaces:
   ```rust
   // 1. Checks
   assert!(balance >= amount);
   // 2. Effects (Internal State Mutation)
   env.storage().persistent().set(&user, &(balance - amount));
   // 3. Interactions (External Call)
   token_client.transfer(&user, &recipient, &amount);
   ```
2. **Asynchronous Architecture / Split Transactions:** Design multi-step workflows across separate ledger transactions rather than deep synchronous nested callbacks.
3. **Non-Reentrant Status Enums:** Guard state transitions with strict lifecycle status machines instead of nested synchronous queries.

## References
- [Soroban Cross-Contract Calls & Security](https://developers.stellar.org/docs/learn/smart-contract-internals/cross-contract)
- [SWC-107: Reentrancy Vulnerability Guidance](https://swcregistry.io/docs/SWC-107)
