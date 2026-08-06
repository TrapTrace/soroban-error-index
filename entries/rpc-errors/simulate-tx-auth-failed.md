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

Pass a signature from keypair B to a function demanding `address_a.require_auth()`.

## Solutions

1. **Sign with Correct Key:** Ensure signature matches target address payload.
2. **Re-simulate Auth Tree:** Use JS SDK `assembleTransaction` to compute full auth requirements automatically.

## References

- [Soroban Auth Framework Overview](https://developers.stellar.org/docs/build/smart-contracts/authorization)
