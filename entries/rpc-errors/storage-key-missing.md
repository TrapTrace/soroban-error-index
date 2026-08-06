---
id: storage-key-missing
title: RPC Error - Requested Ledger Storage Key Missing
category: rpc-error
error_code: RPC::StorageKeyNotFound
verified: true
summary: RPC getLedgerEntries endpoint returned empty result for requested XDR storage key.
tags: [rpc, storage, key, getLedgerEntries, rpc-error]
soroban_version: "21.0.0"
---

# RPC Error: Requested Ledger Storage Key Missing

## Symptoms

- `getLedgerEntries` response returns `entries: []`.
- SDK throws `NotFoundError` when fetching contract data instance.

## Root Causes

1. **Uninitialized Storage:** Storage key was never written to on-chain.
2. **Archived Key:** Key expired and was moved to archived ledger state.

## Reproduction Steps

Query contract instance storage key for an address before initialization.

## Solutions

1. **Initialize State:** Execute contract setup/init function first.
2. **Check Archival Status:** Query state archival RPC endpoint to verify if restoration is required.

## References

- [Stellar RPC API Specification: getLedgerEntries](https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgerEntries)
