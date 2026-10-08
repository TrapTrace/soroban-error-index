---
id: tx-simulation-fee-insufficient
title: "RPC Error - Insufficient Inclusion / Resource Fee for Transaction Submission"
category: rpc-error
error_code: "RPC::InsufficientInclusionFee"
verified: false
summary: "Transaction envelope rejected by RPC node or Horizon because the specified base inclusion fee or resource fee is below current ledger surge requirements."
tags: [rpc-error, fees, inclusion-fee, gas, mempool]
soroban_version: "21.0.0"
severity: warning
related_entries: [budget-exceeded, tx-failed-bad-seq]
---

## Symptoms
- `sendTransaction` RPC requests fail immediately with `txINSUFFICIENT_FEE` or `RESOURCE_LIMIT_EXCEEDED`.
- Transactions stall in mempool during high network congestion or surge pricing.
- Automated bots and relayer transactions fail with fee rejection errors.

## Root Causes
1. **Fee Below Network Base Reserve:** Specifying a `base_fee` lower than 100 stroops per operation (the Stellar protocol minimum).
2. **Surge Pricing Spike:** During network traffic surges, the minimum inclusion fee escalates beyond the pre-set max fee in the transaction envelope.
3. **Outdated `minResourceFee`:** Constructing the transaction using simulation data from a prior ledger without refreshing fee estimates.

## Reproduction Steps
```bash
curl -X POST "https://soroban-testnet.stellar.org" \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "id": 1,
       "method": "sendTransaction",
       "params": {
         "transaction": "AAAAAgAAAADpGsHrCHdI94ecdQ+kCJAORLt2V2oLk6H+/7asPt1kfAAAAAX/oAftBAjljQELlFpDYo3t97YZ45Kf3Uq7ihnBVVVYzAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAg"
       }
     }'
```

## Solutions
1. **Dynamic Fee Estimation via `getFeeStats`:** Query the current network fee stats before envelope assembly:
   ```typescript
   const feeStats = await server.getFeeStats();
   const recommendedFee = feeStats.fee_charged.mode;
   ```
2. **Add Surge Buffer to `minResourceFee`:** Add a 15–20% buffer to the `minResourceFee` returned by `simulateTransaction`:
   ```typescript
   const bufferedFee = Math.ceil(simResult.minResourceFee * 1.20);
   ```
3. **Use TrapTrace Gas Profiler:** Use `traptrace profile <xdr>` or the Web Studio Gas Profiler to inspect required resource fees in advance.

## References
- [Stellar RPC Documentation: sendTransaction](https://developers.stellar.org/docs/data/rpc/api-reference/methods/sendTransaction)
- [Stellar Protocol 21 Surge Pricing & Fee Mechanics](https://developers.stellar.org/docs/learn/fundamentals/fees-metering)
