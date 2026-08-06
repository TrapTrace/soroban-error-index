---
id: sub-invocation-failed
title: Host Error - Cross-Contract Sub-Invocation Failed
category: host-error
error_code: HostError::ContextFailed
verified: true
summary: Cross-contract call to child contract returned an unhandled error or panic.
tags: [cross-contract, invocation, call, sub-call, host-error]
soroban_version: "21.0.0"
---

# Host Error: Cross-Contract Sub-Invocation Failed

## Symptoms

- Parent contract invocation aborts with `Error(Context, Failed)`.
- RPC log indicates sub-invocation call stack unwound.

## Root Causes

1. **Child Contract Trapped:** Target child contract raised a host error or panic.
2. **Mismatch Interface / Symbol:** Calling non-existent function name or passing wrong argument types across contract boundary.

## Reproduction Steps

```rust
let client = TargetContractClient::new(&env, &target_address);
// Fails if target_address is invalid or function panics
client.execute_action(&param);
```

## Solutions

1. **Verify Target Address:** Check target contract existence on-chain.
2. **Propagate or Handle Error:** Wrap sub-invocations carefully and inspect child contract logs.

## References

- [Soroban Cross-Contract Calls Specification](https://developers.stellar.org/docs/build/smart-contracts/invoking-contracts)
