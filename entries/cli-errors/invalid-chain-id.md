---
id: invalid-chain-id
title: CLI Error - Network Passphrase or Chain ID Mismatch
category: cli-error
error_code: CLI::InvalidChainId
verified: true
summary: Transaction simulation or submission rejected because the transaction network passphrase hash does not match the target Stellar node network ID.
tags: [network, chain-id, passphrase, testnet, mainnet, futurenet, cli-error]
soroban_version: "21.0.0"
severity: warning
related_entries: [simulate-tx-auth-failed, auth-invalid-signature]
---

# CLI Error: Network Passphrase or Chain ID Mismatch

## Symptoms

- Transaction simulation or broadcast fails with error `Invalid network passphrase` or `Transaction signature verification failed for target network`.
- Stellar RPC returns simulation error: `HostError: Error(Context, InvalidAction)` with transaction signature mismatch.
- CLI displays error: `error: the transaction was signed for a different network passphrase than the connected node`.

## Root Causes

1. **Passphrase Mismatch:** The transaction envelope was constructed and signed with one network passphrase (e.g. `Public Global Stellar Network ; September 2015`) but submitted to a different node RPC (e.g. `https://soroban-testnet.stellar.org` expecting `Test SDF Network ; September 2015`).
2. **CLI Network Configuration Drift:** The `--network` flag was omitted or pointed to a customized local standalone network while `--rpc-url` was directed at Public Testnet.
3. **Multi-Environment Signature Pipelines:** Pre-signed envelopes generated in staging or offline hardware keys were broadcast to testnet without updating the target network hash.

## Reproduction Steps

Sign a transaction with the Mainnet passphrase and submit it to the Testnet RPC:

```bash
soroban contract invoke \
  --id CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC \
  --network-passphrase "Public Global Stellar Network ; September 2015" \
  --rpc-url https://soroban-testnet.stellar.org \
  --fn hello
```

Expected Output:
```json
{
  "error": "Transaction signature verification failed: passphrase hash does not match node network ID (expected 'Test SDF Network ; September 2015')"
}
```

## Solutions

1. **Explicitly Specify Network in CLI:** Use the pre-configured `--network testnet` or `--network mainnet` flag rather than hardcoding raw passphrase strings.
2. **Verify Environment Configurations:** Ensure `STELLAR_NETWORK_PASSPHRASE` matches the RPC endpoint defined in `STELLAR_RPC_URL`.
3. **Use TrapTrace Network Manager:** Use `traptrace inspect <tx_hash> --network testnet` or `traptrace rpc` to verify the node's official passphrase before signing.

## References

- [Stellar Network Passphrases Reference](https://developers.stellar.org/docs/learn/fundamentals/networks)
- [Soroban CLI Network Management](https://developers.stellar.org/docs/tools/developer-tools/cli/stellar-cli)
