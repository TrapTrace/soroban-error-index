---
id: crypto-verification-failed
title: Host Error - Cryptographic Signature or Curve Verification Failed
category: host-error
error_code: HostError::CryptoError
verified: true
summary: Smart contract execution panicked during host cryptographic primitives verification (such as env.crypto().ed25519_verify) due to an invalid signature, corrupted public key, or payload mismatch.
tags: [crypto, ed25519, secp256k1, signature, verification, curve, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [auth-invalid-signature, host-invalid-action]
---

# Host Error: Cryptographic Signature or Curve Verification Failed

## Symptoms

- Contract execution or simulation aborts with `HostError(Error(Crypto, InvalidInput))` or `HostError::CryptoError`.
- Host diagnostic event logs report: `crypto function verification failure` or `ed25519 verification failed`.
- Zero-knowledge proof, multi-sig verification, or off-chain message attestation methods fail with immediate execution revert.

## Root Causes

1. **Tampered Signature Payload:** The message byte slice passed into `env.crypto().ed25519_verify(&public_key, &message, &signature)` or `secp256k1_verify` does not match the exact bytes hashed during signing.
2. **Invalid Public Key or Signature Length:** Passing a public key or signature byte buffer whose length deviates from curve standards (e.g. 32 bytes for Ed25519 public keys, 64 bytes for Ed25519 signatures, 65 bytes for uncompressed Secp256k1).
3. **Mismatched Signature Encoding:** Providing DER-encoded or hex-encoded signatures when the Soroban cryptographic host function expects raw binary bytes (`BytesN<64>`).

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, crypto::Crypto, Bytes, BytesN, Env};

#[contract]
pub struct CryptoVerifierContract;

#[contractimpl]
impl CryptoVerifierContract {
    pub fn verify_signature(
        env: Env,
        public_key: BytesN<32>,
        message: Bytes,
        invalid_signature: BytesN<64>,
    ) {
        // Attempting to verify with an intentional dummy signature
        env.crypto().ed25519_verify(&public_key, &message, &invalid_signature);
    }
}
```

Invoke with a zeroed signature buffer on testnet:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn verify_signature \
  -- --public_key 0000000000000000000000000000000000000000000000000000000000000000 \
     --message 68656c6c6f \
     --invalid_signature 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Crypto, InvalidInput)",
  "events": [
    "DiagnosticEvent: host error: HostError::CryptoError (ed25519_verify signature verification failed)"
  ]
}
```

## Solutions

1. **Verify Exact Message Hashing:** Ensure message payloads are canonicalized before hashing (e.g. SHA-256 / Keccak-256) and match the exact signing domain parameters.
2. **Validate Fixed-Size Byte Arrays:** Enforce `BytesN<32>` and `BytesN<64>` type constraints in function arguments so malformed buffers fail before reaching the host cryptographic primitives.
3. **Use Soroban Custom Account Contract Interfaces:** For account authentication, prefer implementing the standard `CustomAccountInterface` with `__check_auth` rather than manual ad-hoc crypto verification inside contract business logic.

## References

- [Soroban SDK Crypto Module Docs](https://docs.rs/soroban-sdk/latest/soroban_sdk/crypto/struct.Crypto.html)
- [Stellar Smart Contract Auth & Cryptography Standards](https://developers.stellar.org/docs/learn/smart-contract-internals/authorization)
