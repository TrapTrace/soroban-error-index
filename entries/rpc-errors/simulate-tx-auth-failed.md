---
id: simulate-tx-auth-failed
title: RPC Error - Simulate Transaction Authorization Verification Failed
category: rpc-error
error_code: RPC::SimulateAuthFailed
verified: true
summary: Simulation node failed to verify invocation authorization payload or signature footprint.
tags: [rpc, simulateTransaction, auth, signature, rpc-error]
soroban_version: "21.0.0"
---

# RPC Error: Simulate Transaction Authorization Verification Failed

## Symptoms

- RPC returns error JSON `{"code": -32600, "message": "Simulation failed: Auth error"}`.
- Invocation client output: `Failed to construct Soroban auth tree`.

## Root Causes

1. **Invalid Signature/Key:** Signer key does not match required `require_auth` address.
2. **Missing Footprint Scope:** Auth payload missing child sub-invocations.

## Reproduction Steps

1. Submit a `simulateTransaction` request with an unsigned or improperly authorized transaction envelope XDR:

```bash
curl -s -X POST https://soroban-testnet.stellar.org \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "simulateTransaction",
    "params": {
      "transaction": "<UNSIGNED_TRANSACTION_XDR>"
    }
  }'
```

2. Expected JSON-RPC Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "error": "HostError: Error(Auth, InvalidAction)",
    "latestLedger": 4018522
  }
}
```

3. Rust / SDK Reproduction:

```rust
// Invoking contract method enforcing require_auth with keypair B instead of Keypair A
pub fn transfer(env: Env, from: Address, to: Address, amount: i128) {
    from.require_auth(); // Fails simulation if 'from' signature is missing or mismatched
}
```

## Solutions

1. **Sign with Correct Key:** Ensure signature matches target address payload.
2. **Re-simulate Auth Tree:** Use JS SDK `assembleTransaction` to compute full auth requirements automatically.

## References

- [Soroban Auth Framework Overview](https://developers.stellar.org/docs/build/smart-contracts/authorization)

