---
id: host-invalid-action
title: Host Error - Invalid Action or Host Invariant Violation
category: host-error
error_code: HostError::InvalidAction
verified: true
summary: Contract execution failed because a host function was called with invalid domain arguments or violated host state invariants.
tags: [host-error, invalid-action, host-functions, validation, crypto]
soroban_version: "21.0.0"
severity: critical
related_entries: [sub-invocation-failed, unreachable-code-reached]
---

# Host Error: Invalid Action or Host Invariant Violation

## Symptoms

- Transaction simulation returns `HostError(Error(Context, InvalidAction))` or `HostError::InvalidAction`.
- Diagnostic events log indicates failure inside host functions such as `crypto`, `events`, or `prng`.
- Contract aborts immediately during cryptographic verification, event publishing, or invalid handle conversion.

## Root Causes

1. **Malformed Cryptographic Inputs:** Passing invalid public key byte lengths or improperly encoded signatures to host functions like `env.crypto().ed25519_verify()`.
2. **Excessive Event Topics:** Calling `env.events().publish(...)` with more than 4 topic elements, violating the Soroban topic limit invariant.
3. **Invalid Context / State Mutation:** Attempting a reentrant call or mutating host storage during read-only execution contexts.
4. **Invalid RawVal Handle Conversion:** Attempting to cast or dereference an invalid or uninitialized host `Val` handle.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, vec, BytesN, Env, Symbol};

#[contract]
pub struct InvalidActionContract;

#[contractimpl]
impl InvalidActionContract {
    pub fn trigger_invalid_event(env: Env) {
        // Violates topic length limit (max 4 topics allowed in Soroban)
        let topics = (
            Symbol::new(&env, "topic1"),
            Symbol::new(&env, "topic2"),
            Symbol::new(&env, "topic3"),
            Symbol::new(&env, "topic4"),
            Symbol::new(&env, "topic5"), // Invalid 5th topic
        );
        env.events().publish(topics, 100u32);
    }
}
```

Invoke the contract via CLI on testnet:
```bash
soroban contract invoke --id <CONTRACT_ID> --source-account <ACCOUNT> --network testnet --fn trigger_invalid_event
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Context, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::InvalidAction"
  ]
}
```

## Solutions

1. **Verify Cryptographic Key and Signature Lengths:** Ensure public keys are exact 32-byte slices (`BytesN<32>`) and signatures are exact 64-byte slices (`BytesN<64>`) before calling verification host methods.
2. **Limit Event Topics:** Ensure all event topic tuples contain between 1 and 4 elements maximum.
3. **Validate Raw Val Handles:** Use SDK wrapper types (`Address`, `Bytes`, `Vec`, `Map`) rather than raw `Val` / `RawVal` representations to prevent uninitialized handle errors.
4. **Inspect Diagnostic Events:** Run `traptrace inspect <tx_hash>` or check `diagnosticEvents` in the RPC response to pinpoint the exact host function call that triggered `InvalidAction`.

## References

- [Soroban Host Environment Error Codes (rs-soroban-env)](https://github.com/stellar/rs-soroban-env)
- [Stellar Developers: Smart Contract Events & Topics](https://developers.stellar.org/docs/learn/smart-contract-internals/events)
