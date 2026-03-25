---
type: concept
aliases: ["FedNAS", "Federated NAS"]
---

# Federated Neural Architecture Search

## Intuition

Federated Neural Architecture Search (FedNAS) means we do architecture search directly in federated learning, instead of first deciding an architecture centrally and then federating only training.

## Why It Matters

Client devices are heterogeneous in data and hardware. A single manually chosen architecture is often suboptimal, while FedNAS can discover architectures that better match federated constraints.

## Tiny Example

In a mobile keyboard scenario, low-end phones may require a much smaller subnet than high-end phones. FedNAS can search a supernet so each device gets a fitting architecture.

## Definition

FedNAS studies how to optimize neural architectures under federated settings where data is decentralized, communication is limited, and client heterogeneity is significant.

## Key Points

1. It couples architecture design with federated optimization rather than treating architecture as fixed.
2. It must handle both statistical heterogeneity (non-IID data) and system heterogeneity (device budgets).
3. Supernet and weight sharing are commonly used to reduce search cost.

## How This Paper Uses It

- [[DeepFedNAS]]: builds a Pareto-guided supernet training curriculum and predictor-free deployment search in a federated NAS framework.

## Representative Papers

- [[DeepFedNAS]]: predictor-free and hardware-aware federated NAS with Pareto-guided training.
- [[SuperFedNAS]]: decouples federated supernet training and post-training subnet search.

## Related Concepts

- [[Neural Architecture Search]]
- [[Super-network]]
- [[Hardware-aware NAS]]

