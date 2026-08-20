---
id: auth-invalid-signature
title: Host Error - Contract Authorization Invalid Signature
category: host-error
error_code: HostError::AuthInvalidSignature
verified: true
summary: Transaction execution or simulation aborted because an authorization entry signature failed cryptographic verification against the required signer address or public key.
tags: [auth, signature, ed25519, secp256k1, verification, require-auth, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [simulate-tx-auth-failed, host-invalid-action]
---

# Host Error: Contract Authorization Invalid Signature

## Symptoms

- Transaction simulation or on-chain submission fails with `HostError(Error(Auth, InvalidAction))` or `HostError::AuthInvalidSignature`.
- RPC response returns `Simulation failed: Auth error: Signature verification failed`.
- Invocation involving custom accounts, multi-sig contracts, or delegated `require_auth` fails during signature checking.

## Root Causes

1. **Incorrect Signer Keypair:** Signing the invocation authorization payload with a secret key that does not correspond to the public key or `Address` declared in `require_auth`.
2. **Signature Hash Mismatch:** Signing a different authorization tree hash (e.g. payload created for a different network passphrase or nonce) than what the Soroban host validates.
3. **Invalid Signature Encoding:** Passing a malformed, non-canonical 64-byte Ed25519 or 65-byte Secp256k1 signature slice to custom account verification methods (`__check_auth`).
4. **Expired Authorization Nonce:** Reusing an old authorization payload whose sequence nonce has already been consumed on-chain.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Address, Env};

#[contract]
pub struct AuthTestContract;

#[contractimpl]
impl AuthTestContract {
    pub fn transfer_protected(env: Env, from: Address, to: Address, amount: i128) {
        // Enforces explicit cryptographic authorization
        from.require_auth();
        // State mutation logic...
    }
}
```

Invoke the contract via CLI with an unverified or mismatched signature envelope:
```bash
soroban contract invoke --id <CONTRACT_ID> --network testnet --fn transfer_protected -- --from <ACCOUNT_A> --to <ACCOUNT_B> --amount 100
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Auth, InvalidAction)",
  "events": [
    "DiagnosticEvent: host error: HostError::AuthInvalidSignature (failed to verify ed25519 signature for address)"
  ]
}
```

## Solutions

1. **Verify Signer Matches Address:** Ensure the transaction signer or simulated auth entry keypair matches the `Address` parameter passed to `require_auth()`.
2. **Simulate Auth Footprints First:** Run `traptrace simulate <xdr>` to generate the required Soroban authorization tree before signing.
3. **Verify Network Passphrase:** Ensure off-chain signers are hashing signatures with the correct network passphrase (`Test SDF Network ; September 2015` on Testnet, `Public Global Stellar Network ; September 2015` on Mainnet).
4. **Handle Custom Account Auth:** In smart contract accounts implementing `__check_auth`, ensure signature verification returns `Ok(())` only when valid and bubbles explicit errors.

## References

- [Stellar Developers: Smart Contract Authorization](https://developers.stellar.org/docs/learn/smart-contract-internals/authorization)
- [Soroban Rust SDK Address and Auth Documentation](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Address.html)
