---
id: wasm-memory-exhausted
title: Host Error - WASM VM Memory Page Allocation Exhausted
category: host-error
error_code: HostError::MemoryExhausted
verified: true
summary: Contract execution halted because total WASM linear memory pages allocated at runtime exceeded the Soroban VM memory cap.
tags: [wasm, memory, linear-memory, pages, out-of-memory, host-error]
soroban_version: "21.0.0"
severity: critical
related_entries: [budget-exceeded, unreachable-code-reached]
---

# Host Error: WASM VM Memory Page Allocation Exhausted

## Symptoms

- Transaction simulation or invocation terminates with `HostError(Error(Budget, Exceeded))` or `HostError::MemoryExhausted`.
- CLI output indicates out-of-memory (OOM) or memory page allocation failure (`grow_memory` returned -1).
- Execution halts when constructing large vectors, allocating deep recursive stack frames, or decompressing large data in WASM.

## Root Causes

1. **Large Transient Heap Allocations:** Instantiating massive Rust `std::vec::Vec` or `String` buffers inside contract WASM heap rather than host-managed collections.
2. **Deep Recursive Call Stacks:** Unbounded recursion consuming WASM shadow stack and memory pages.
3. **In-Memory Sorting of Large Datasets:** Buffering thousands of objects in memory for sorting or aggregation instead of processing via batched iterations.
4. **Memory Leaks in Custom Allocators:** Failure to free or reuse memory across high-iteration processing loops inside WASM.

## Reproduction Steps

```rust
use soroban_sdk::{contract, contractimpl, Env};

#[contract]
pub struct MemoryExhaustedContract;

#[contractimpl]
impl MemoryExhaustedContract {
    pub fn allocate_huge_memory(_env: Env) {
        // Attempt to allocate a 100MB transient buffer in WASM heap
        let mut huge_vec: Vec<u8> = Vec::with_capacity(100 * 1024 * 1024);
        huge_vec.resize(100 * 1024 * 1024, 0xEE);
    }
}
```

Invoke the contract via CLI on testnet:
```bash
soroban contract invoke --id <CONTRACT_ID> --source-account <ACCOUNT> --network testnet --fn allocate_huge_memory
```

Expected RPC Simulation Output:
```json
{
  "error": "HostError: Error(Budget, Exceeded)",
  "events": [
    "DiagnosticEvent: host error: HostError::MemoryExhausted (memory page limit reached)"
  ]
}
```

## Solutions

1. **Use Host Collections:** Replace `std::vec::Vec` and `std::collections::BTreeMap` with Soroban SDK host-managed types (`soroban_sdk::Vec`, `soroban_sdk::Map`), which reside in host memory and do not consume WASM linear heap.
2. **Stream and Batch Processing:** Process records sequentially in stream-style chunks rather than buffering the complete dataset in memory.
3. **Avoid Unbounded Recursion:** Convert recursive algorithms to iterative state loops with bounded iteration caps.
4. **Pre-Flight Memory Profiling:** Run `traptrace simulate <xdr>` to inspect the `mem_bytes` consumption gauge before on-chain submission.

## References

- [Stellar Developers: Soroban Memory and Metering Limits](https://developers.stellar.org/docs/learn/fundamentals/fees-and-metering)
- [WebAssembly Linear Memory Specification](https://webassembly.github.io/spec/core/syntax/modules.html#memories)
