---
type: concept
aliases: ["Architecture Search Benchmark", "NAS Dataset"]
---

# NAS Benchmark

## Intuition

A NAS benchmark is a search space with precomputed architecture results, so we can test search algorithms without rerunning full training for every experiment.

## Why It Matters

Benchmarks make NAS research reproducible. They let us compare search methods fairly and isolate the search algorithm from the enormous noise and cost of retraining everything from scratch.

## Tiny Example

NASBench-201 stores the performance of all architectures in its search space on several datasets. A researcher can query those results directly instead of training every candidate manually.

## Definition

A NAS benchmark is a structured repository of candidate architectures and their measured or estimated task/hardware outcomes, designed for standardized evaluation of NAS methods.

## Key Points

1. Benchmarks reduce cost and improve reproducibility.
2. Their usefulness depends on how realistic the search space and metrics are.
3. A benchmark can bias conclusions if it overrepresents one architecture family.

## How This Paper Uses It

- [[Zero-shot NAS Survey]]: evaluates proxies on NASBench-101, NASBench-201, NATS-Bench, TransNAS-Bench-101, and hardware-aware benchmarks.

## Representative Papers

- [[Zero-shot NAS Survey]]: discusses both standard and hardware-aware NAS benchmarks.
- [[NAS-Bench-201]]: one of the most widely used tabular NAS benchmarks.

## Related Concepts

- [[Hardware-aware NAS]]
- [[Hardware Performance Model]]

