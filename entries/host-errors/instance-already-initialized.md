---
id: instance-already-initialized
title: "Host Error - Smart Contract Instance Already Initialized"
category: host-error
error_code: "HostError::ContractAlreadyInitialized"
verified: false
summary: "Attempting to invoke contract initialization logic on an already initialized contract instance."
tags: [host-error, initialization, constructor, security, state]
soroban_version: "21.0.0"
severity: critical
related_entries: [host-invalid-action, sub-invocation-user-error]
---

## Symptoms
- Contract deployment and initialization scripts fail with `ContractAlreadyInitialized` or custom init error enum.
- Re-invoking constructor-style methods like `init()`, `initialize()`, or `set_admin()` reverts on-chain.
- Transaction simulation fails during contract onboarding flows.

## Root Causes
1. **Re-initialization Guard Triggered:** The contract implementation uses a boolean flag in instance storage (`IS_INIT`) or constructor pattern, and a second invocation was attempted after initial deployment.
2. **Factory Contract Race Condition:** A factory contract deployed the instance and called `initialize` in the same transaction, followed by an external caller attempting initialization again.
3. **Missing Idempotency Handling:** The deployment pipeline did not check if the contract was already initialized before calling setup methods.

## Reproduction Steps
```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

const IS_INIT: Symbol = symbol_short!("IS_INIT");

#[contract]
pub struct InitializedContract;

#[contractimpl]
impl InitializedContract {
    pub fn initialize(env: Env) -> Result<(), ()> {
        if env.storage().instance().has(&IS_INIT) {
            return Err(()); // Already initialized
        }
        env.storage().instance().set(&IS_INIT, &true);
        Ok(())
    }
}
```

## Solutions
1. **Check Initialization State First:** Use `.has(&IS_INIT)` before attempting initialization calls:
   ```rust
   if !client.is_initialized() {
       client.initialize(&admin);
   }
   ```
2. **Use Protocol 21 Native `__constructor`:** Utilize native Soroban constructors that can only execute once during initial instance deployment.
3. **Atomic Factory Deployment:** Deploy and initialize instances in a single atomic transaction envelope.

## References
- [Soroban Smart Contract Initialization Patterns](https://developers.stellar.org/docs/learn/smart-contract-internals)
- [Stellar CAP-0046: Lifecycle Management](https://stellar.org)
