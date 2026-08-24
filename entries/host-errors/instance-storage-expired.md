---
id: instance-storage-expired
title: Host Error - Contract Instance and Executable Storage Archived
category: host-error
error_code: HostError::InstanceStorageExpired
verified: true
summary: Contract invocation failed because the contract instance or executable WASM bytecode exceeded its maximum live TTL and was archived by the network.
tags: [storage, instance-storage, archival, ttl, cap-0046, restore-footprint]
soroban_version: "21.0.0"
severity: critical
related_entries: [entry-archived-ttl-expired, temporary-storage-expired]
---

# Host Error: Contract Instance and Executable Storage Archived

## Symptoms

- Contract invocations revert during simulation with `HostError(Error(Storage, InstanceArchived))` or `Error(Storage, DeadEntry)`.
- Transaction footprint indicates `ContractData` or `ContractCode` ledger keys are archived.
- Contract execution cannot proceed until a `RestoreFootprintOp` transaction is submitted and confirmed on-chain.

## Root Causes

1. **Infrequent Contract Invocation:** Contracts that remain idle without invocations or explicit TTL bumps eventually hit their `live_until_ledger` threshold.
2. **Missing Instance TTL Bump:** Failing to execute `env.storage().instance().extend_ttl(...)` in contract initialization or execution entrypoints.
3. **Unrestored Footprint:** Attempting to invoke an archived contract without preceding the call with a footprint restoration operation.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, symbol_short, Env, Symbol};

const STATE_KEY: Symbol = symbol_short!("admin");

#[contract]
pub struct IdleContract;

#[contractimpl]
impl IdleContract {
    pub fn init(env: Env) {
        // Initializes instance storage without setting an extended TTL
        env.storage().instance().set(&STATE_KEY, &123u32);
    }

    pub fn execute(env: Env) -> u32 {
        env.storage().instance().get(&STATE_KEY).unwrap()
    }
}
```

Invoke `execute` against an archived contract instance on testnet:
```bash
soroban contract invoke \
  --id <ARCHIVED_CONTRACT_ID> \
  --network testnet \
  --fn execute
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Storage, InstanceArchived)",
  "events": [
    "DiagnosticEvent: contract instance entry archived; submit restore footprint before invocation"
  ]
}
```

## Solutions

1. **Restore Footprint via CLI/SDK:** Submit a restoration transaction (`soroban contract restore --id <CONTRACT_ID> --network testnet`) to revive the contract instance.
2. **Implement Proactive TTL Bumping:** Call `env.storage().instance().extend_ttl(50_000, 100_000)` inside popular contract methods to ensure the instance never archives during regular use.
3. **Automated Rent Monitor:** Integrate TrapTrace Storage TTL Auditor (`traptrace storage --contract <ID>`) into operational monitoring workflows.

## References

- [Stellar Docs: Restoring Archived Contracts](https://developers.stellar.org/docs/learn/smart-contract-internals/state-archival#restoring-archived-data)
- [Soroban Storage TTL Management Guide](https://developers.stellar.org/docs/data/rpc/api-reference/simulateTransaction)
