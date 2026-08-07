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

1. Send a JSON-RPC `getLedgerEntries` request for an uninitialized or non-existent contract data storage key:

```bash
curl -s -X POST https://soroban-testnet.stellar.org \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getLedgerEntries",
    "params": {
      "keys": [
        "AAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAAEdGVzdAAAAAA="
      ]
    }
  }'
```

2. Expected JSON-RPC Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "entries": [],
    "latestLedger": 4018522
  }
}
```

3. TypeScript / JS SDK Reproduction:

```typescript
import { Server } from "@stellar/stellar-sdk/rpc";

const server = new Server("https://soroban-testnet.stellar.org");
const result = await server.getContractData(contractId, key);
// Result returns null or empty entries when key is absent from state
```

## Solutions

1. **Initialize State:** Execute contract setup/init function first.
2. **Check Archival Status:** Query state archival RPC endpoint to verify if restoration is required.

## References

- [Stellar RPC API Specification: getLedgerEntries](https://developers.stellar.org/docs/data/rpc/api-reference/methods/getLedgerEntries)

