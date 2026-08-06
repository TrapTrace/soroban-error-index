---
id: tx-failed-bad-seq
title: CLI Error - Transaction Failed Bad Sequence Number
category: cli-error
error_code: txBAD_SEQ
verified: true
summary: Transaction submission rejected because account sequence number did not match network sequence counter.
tags: [sequence, nonce, transaction, txBAD_SEQ, cli-error]
soroban_version: "21.0.0"
---

# CLI Error: Transaction Failed Bad Sequence Number

## Symptoms

- Transaction rejected with status `txBAD_SEQ`.
- CLI output: `Transaction submission failed: ResultCode txBAD_SEQ`.

## Root Causes

1. **Concurrent Submissions:** Multiple transactions submitted simultaneously using the same source account.
2. **Out of Sync Sequence Cache:** CLI local sequence counter out of sync with RPC node state.

## Reproduction Steps

Submit two transactions rapidly from separate terminal instances using identical `--source` keypair.

## Solutions

1. **Retry Transaction:** Re-run command to refresh sequence number automatically from RPC.
2. **Use Channels:** For high-throughput automated scripts, use separate channel accounts for transaction signing.

## References

- [Stellar Horizon & RPC Transaction Flow](https://developers.stellar.org/docs/learn/fundamentals/transactions/operations)
