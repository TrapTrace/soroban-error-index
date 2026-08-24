---
id: invalid-scval-tag
title: Host Error - Invalid ScVal Tag Discriminator (Malformed Val Handle)
category: host-error
error_code: HostError::InvalidScValTag
verified: true
summary: Host environment rejected a value representation because the 64-bit tagged Val or ScVal discriminator byte is corrupted, unrecognized, or invalid.
tags: [host-error, scval, val, tagged-pointer, val-tag, malformed]
soroban_version: "21.0.0"
severity: critical
related_entries: [scval-type-conversion-error, host-invalid-action]
---

# Host Error: Invalid ScVal Tag Discriminator (Malformed Val Handle)

## Symptoms

- Host aborts execution with `HostError(Error(Value, InvalidTag))` or `HostError(Error(Context, InvalidAction))`.
- Diagnostic events indicate an invalid tag bitmask encountered during host object dereferencing.
- Occurs when passing manually constructed raw byte payloads or corrupted XDR to host functions.

## Root Causes

1. **Manual Bit-Manipulation on `Val`:** Constructing raw 64-bit integer values and casting them directly into Soroban `Val` without following the host's bit tagging scheme (tag bits in the lower 8 bits).
2. **Malformed XDR Envelopes:** Binary deserialization of corrupted or truncated transaction envelopes where the `ScValType` enum discriminator is out of bounds.
3. **Cross-Protocol Version Incompatibility:** Passing a newer `ScVal` variant to a contract compiled against an older protocol version.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Env, Val};

#[contract]
pub struct BadTagContract;

#[contractimpl]
impl BadTagContract {
    pub fn trigger_bad_tag(_env: Env, raw_num: u64) -> Val {
        // Unsafe fabrication of a tagged pointer with an illegal tag mask
        unsafe { Val::from_payload(raw_num | 0xFF) }
    }
}
```

Invoke on testnet:
```bash
soroban contract invoke \
  --id <CONTRACT_ID> \
  --network testnet \
  --fn trigger_bad_tag \
  -- --raw_num 12345
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Value, InvalidTag)",
  "events": [
    "DiagnosticEvent: host error: HostError::InvalidScValTag (malformed val tag encountered)"
  ]
}
```

## Solutions

1. **Use Safe Soroban SDK Types:** Avoid `Val::from_payload` or raw unsafe pointers; rely on high-level SDK primitives (`Symbol`, `Address`, `Bytes`, `Map`, `Vec`).
2. **Verify XDR Payloads:** Validate transaction envelope XDR with `traptrace decode <xdr>` before broadcasting.
3. **Keep SDKs Synchronized:** Ensure contracts and client libraries are built against matching Soroban SDK versions.

## References

- [Soroban Host Val & Object Architecture](https://github.com/stellar/rs-soroban-env/blob/main/soroban-env-common/src/val.rs)
- [Stellar Developers: Data Types & SCVal](https://developers.stellar.org/docs/learn/smart-contract-internals/types)
