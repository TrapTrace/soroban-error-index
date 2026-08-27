---
id: crypto-curve25519-invalid-scalar
title: "Host Error - Curve25519 / Ed25519 Invalid Scalar or Point"
category: host-error
error_code: "HostError::CryptoScalarInvalid"
verified: true
summary: "Host cryptographic verification failed due to non-canonical point encoding, invalid scalar length, or scalar out of subgroup range."
tags: [host-error, crypto, curve25519, ed25519, verification]
soroban_version: "21.0.0"
severity: critical
related_entries: [crypto-verification-failed, auth-invalid-signature]
---

## Symptoms
- Invocations involving custom cryptographic verification panic with `HostError::CryptoScalarInvalid` or `CryptoError`.
- Zero-knowledge proof (ZKP) or multi-party computation (MPC) threshold signatures fail verification.
- Diagnostic events output `crypto_ed25519_verify` or `curve25519_scalar_mul` trap codes.

## Root Causes
1. **Non-Canonical Point Encoding:** The passed public key or compressed Montgomery/Edwards point has highest-bit corruption or violates canonical 32-byte representation.
2. **Scalar Out of Prime Order:** Scalar integer value is greater than or equal to the prime curve group order $L = 2^{252} + 27742317777372353535851937790883648493$.
3. **Invalid Byte Array Length:** Passing a 64-byte raw signature into a function expecting a 32-byte public key slice or vice versa.

## Reproduction Steps
```rust
use soroban_sdk::{contract, contractimpl, BytesN, Env};

#[contract]
pub struct CryptoScalarContract;

#[contractimpl]
impl CryptoScalarContract {
    pub fn verify_scalar(env: Env, invalid_key: BytesN<32>, msg: BytesN<32>, sig: BytesN<64>) {
        env.crypto().ed25519_verify(&invalid_key, &msg.into(), &sig);
    }
}
```

## Solutions
1. **Canonicalize Public Keys Before Hashing:** Ensure client-side cryptographic libraries serialize keys using strict canonical Little-Endian representation:
   ```typescript
   import { Keypair } from '@stellar/stellar-sdk';
   const canonicalBytes = keypair.rawPublicKey();
   ```
2. **Validate Scalar Subgroup Range:** Check scalar values with modulo arithmetic against the group order $L$ before passing to host operations.
3. **Use Soroban SDK Native Crypto Helpers:** Prefer `env.crypto().ed25519_verify()` over custom WASM-compiled cryptography libraries.

## References
- [RFC 8032: Edwards-Curve Digital Signature Algorithm (EdDSA)](https://datatracker.ietf.org/doc/html/rfc8032)
- [Soroban Host Cryptography API](https://docs.rs/soroban-sdk/latest/soroban_sdk/struct.Crypto.html)
