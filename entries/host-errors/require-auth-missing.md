---
id: require-auth-missing
title: Host Error - Missing Required Invocation Authorization
category: host-error
error_code: HostError::AuthMissing
verified: true
summary: Contract execution halted because an operation required explicit authorization from an Address that was not provided in the invocation auth tree.
tags: [auth, require-auth, authorization, security, permissions, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [auth-invalid-signature, simulate-tx-auth-failed]
---

# Host Error: Missing Required Invocation Authorization

## Symptoms

- Transaction simulation or invocation terminates with `HostError(Error(Auth, InvalidAction))` or `HostError::AuthMissing`.
- RPC simulation returns `Auth error: HostError::AuthMissing (require_auth failed for address)`.
- Contract aborts during privileged administrative functions, token transfers, or state ownership modifications.

## Root Causes

1. **Unsigned Client Invocation:** Client submitted a transaction envelope that called a contract method enforcing `address.require_auth()` without appending the corresponding `SorobanAuthorizationEntry` to the transaction footprint.
2. **Sub-Invocation Authorization Gaps:** Contract invoked a child contract requiring caller authorization without wrapping the call in `require_auth_for_args(...)`.
3. **Mismatched Authorization Address:** Passing an address parameter `admin` to the method that does not match the actual transaction submitter or signed credentials.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Address, Env};

#[contract]
pub struct AdminOnlyContract;

#[contractimpl]
impl AdminOnlyContract {
    pub fn update_admin(env: Env, new_admin: Address) {
        let current_admin: Address = env.storage().instance().get(&1u32).unwrap();
        // Fails if current_admin has not signed the invocation
        current_admin.require_auth();
        env.storage().instance().set(&1u32, &new_admin);
    }
}
```

Invoke the contract via CLI without supplying the admin's signature:
```bash
soroban contract invoke --id <CONTRACT_ID> --source-account <RANDOM_ACCOUNT> --network testnet --fn update_admin -- --new_admin <NEW_ACCOUNT>
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Auth, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::AuthMissing"
  ]
}
```

## Solutions

1. **Include Auth Entries:** In client applications using JS/Python/Rust SDKs, simulate the transaction first to generate the required `auth` tree and sign each required entry.
2. **Authorizing Contract Calls:** If calling between contracts, use `Address::require_auth_for_args(&address, args)` to explicitly authorize arguments passed to nested contracts.
3. **Inspect Auth Trees with CLI:** Run `traptrace simulate <xdr>` to inspect required authorizers and verify whether all needed signatures are included.

## References

- [Stellar Developers: Soroban Authorization Architecture](https://developers.stellar.org/docs/learn/smart-contract-internals/authorization)
- [Soroban Rust SDK Address::require_auth](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Address.html#method.require_auth)
