---
id: contract-not-found
title: Host Error - Contract Code or Instance Not Found
category: host-error
error_code: HostError::ContractNotFound
verified: true
summary: Host environment failed to locate WASM executable bytecode or instance storage for given contract ID.
tags: [contract-id, wasm, missing, deploy, host-error]
soroban_version: "21.0.0"
---

# Host Error: Contract Code or Instance Not Found

## Symptoms

- Call fails with `Error(Storage, MissingValue)` or `ContractNotFound`.
- Soroban CLI outputs `Error: Contract instance C... does not exist`.

## Root Causes

1. **Incorrect Contract Address:** Typo in contract address hash.
2. **Network Mismatch:** Calling Testnet contract ID against Mainnet RPC.
3. **Uninstalled WASM:** WASM code hash not uploaded prior to instance creation.

## Reproduction Steps

```bash
soroban contract invoke --id CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA --fn hello
```

## Solutions

1. **Verify Target Contract ID:** Re-check deployment output logs for exact address.
2. **Confirm Network Target:** Ensure `--network testnet` / `--network mainnet` matches deployment target.

## References

- [Stellar Soroban Contract Deployment Guide](https://developers.stellar.org/docs/build/smart-contracts/deploying)
