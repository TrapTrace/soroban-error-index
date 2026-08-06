---
id: account-not-found
title: CLI Error - Identity Account Not Found on Network
category: cli-error
error_code: CLI::AccountNotFound
verified: true
summary: Soroban CLI configured source identity account is not funded or does not exist on the target network.
tags: [account, keypair, fund, friendbot, cli-error]
soroban_version: "21.0.0"
---

# CLI Error: Identity Account Not Found on Network

## Symptoms

- CLI displays `Error: Account G... not found on network`.
- Invocation or deployment fails during transaction signing.

## Root Causes

1. **Unfunded Account:** Newly generated keys must be funded with minimum native XLM balance.
2. **Incorrect Identity:** Using wrong keypair alias.

## Reproduction Steps

```bash
soroban keys generate alice
soroban contract deploy --wasm target/wasm32-unknown-unknown/release/contract.wasm --source alice
```

## Solutions

1. **Fund Account via Friendbot (Testnet):**
```bash
soroban keys fund alice --network testnet
```
2. **Transfer Native Balance (Mainnet):** Send XLM to public key before deployment.

## References

- [Soroban CLI Identity Management](https://developers.stellar.org/docs/tools/developer-tools/cli/keys)
