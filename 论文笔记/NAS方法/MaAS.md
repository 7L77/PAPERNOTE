---
title: "MaAS"
type: method
source_paper: "Multi-agent Architecture Search via Agentic Supernet"
source_note: "[[MaAS]]"
authors: [Guibin Zhang, Luyang Niu, Junfeng Fang, Kun Wang, Lei Bai, Xiang Wang]
year: 2025
venue: ICML
tags: [nas-method, llm-agent, agentic-search, supernet]
created: 2026-03-20
updated: 2026-03-20
---

# MaAS

## One-line Summary

> MaAS learns a query-conditioned distribution over multi-agent workflows instead of a single fixed workflow, then samples a cost-aware agent system per query from an agentic supernet.

## Source

- Paper: [Multi-agent Architecture Search via Agentic Supernet](https://arxiv.org/abs/2502.04180)
- HTML: https://arxiv.org/html/2502.04180v2
- Code: https://github.com/bingreeky/MaAS
- Paper note: [[MaAS]]

## Applicable Scenarios

- Problem type: automatic design of LLM-agent workflows for math reasoning, code generation, and tool-use tasks.
- Assumptions: the task can be decomposed into reusable agentic operators and evaluated by a scalar reward or accuracy signal.
- Data regime: benchmark-driven optimization with train/test splits; online API execution during training.
- Scale / constraints: useful when inference cost matters and query difficulty varies widely across samples.
- Why it fits: MaAS explicitly models both performance and token/API cost, and its controller can stop early on easy inputs.

## Not a Good Fit When

- You need a fully deterministic, fixed workflow for auditing or compliance.
- You cannot afford repeated online LLM executions during optimization.
- The task has no reliable automatic utility signal, making controller updates noisy.

## Inputs, Outputs, and Objective

- Inputs: query `q`, operator library `O`, supernet distribution parameters `pi`, and environment feedback from executed workflows.
- Outputs: a sampled workflow `G` for each query and, after training, an optimized agentic supernet.
- Objective: maximize task utility while penalizing cost, as formalized in Eq. (5) and Eq. (10).
- Core assumptions: operator descriptions can be embedded meaningfully, and query-conditioned routing can predict which operators are worth activating.

## Method Breakdown

### Stage 1: Define Operator Space and Supernet

- Treat each composite workflow primitive as an [[Agentic Operator]] with LLM calls, prompts, and tools.
- Organize operators into an `L`-layer [[Agentic Supernet]] that induces a distribution over possible workflows.
- Source: Sec. 3.1, Def. 3.1, Def. 3.2, Eq. (1)-(4)

### Stage 2: Query-Conditioned Sampling

- Encode the query and operator descriptions, then let the controller score operators layer by layer.
- Select operators until the cumulative probability mass crosses a threshold, allowing multiple operators per layer.
- Use [[Early Exit]] so shallow workflows can terminate early on simple queries.
- Source: Sec. 3.2, Eq. (6)-(9), Fig. 2

### Stage 3: Execute the Sampled Workflow

- Build a query-specific multi-agent system `G` from the selected operators.
- Execute `G` to produce an answer and collect utility/cost feedback from the environment.
- Source: Sec. 3.2-3.3, Alg. 1

### Stage 4: Update the Supernet Distribution

- Approximate the gradient of the distribution parameters with a Monte Carlo estimator over sampled workflows.
- Weight trajectories by both answer quality and cost so cheap high-performing workflows get promoted.
- Source: Sec. 3.3, Eq. (10)-(11)

### Stage 5: Update Operators via Textual Gradient

- Because prompts, tool usage, and operator structures are not differentiable, use [[Textual Gradient]] to generate prompt, temperature, and structure edits.
- In effect, MaAS evolves both routing probabilities and the operators themselves.
- Source: Sec. 3.3, Eq. (12), Fig. 3

## Pseudocode

```text
Algorithm: MaAS
Input: Query q, operator library O, L-layer supernet A = {pi, O}, controller Q_theta
Output: Query-specific workflow G and an optimized supernet after training

1. Define candidate operators and initialize the L-layer agentic supernet.
   Source: Def. 3.1, Def. 3.2, Eq. (1)-(4)
2. For each training query, score operators layer by layer using the controller.
   Source: Sec. 3.2, Eq. (6)-(7)
3. At each layer, activate operators until cumulative score exceeds the threshold.
   Source: Eq. (9)
4. If the early-exit operator is selected, stop sampling deeper layers.
   Source: Eq. (8)
5. Execute the sampled workflow G and obtain answer quality and cost feedback.
   Source: Eq. (6), Alg. 1
6. Update the distribution parameters pi with a cost-aware Monte Carlo gradient estimate.
   Source: Eq. (10)-(11)
7. Update prompts / temperatures / node structure with textual gradient feedback.
   Source: Eq. (12), Fig. 3
8. Reuse the optimized supernet at inference time to sample a workflow for each new query.
   Source: Alg. 1, Sec. 3.3
```

## Training Pipeline

1. Prepare benchmark-specific train split and an operator repository.
2. Embed operator descriptions and queries with a lightweight sentence encoder.
3. Sample a multi-layer workflow per query via the controller.
4. Execute the workflow on the benchmark environment and record score, cost, and log-probability.
5. Compute a utility such as `score - lambda * cost` and update the controller / distribution.
6. If enabled, use textual gradient to revise prompts or operator structure.

Sources:

- Sec. 3.2-3.3
- Alg. 1
- Code evidence: `examples/maas/optimize.py`, `maas/ext/maas/models/controller.py`, `maas/ext/maas/benchmark/benchmark.py`

## Inference Pipeline

1. Encode the incoming query.
2. Use the trained controller to select operators layer by layer.
3. Stop at max depth or when `EarlyStop` / early exit is selected.
4. Execute the resulting workflow graph and return the final answer.

Sources:

- Sec. 3.2
- Fig. 5, Fig. 6
- Code evidence: `maas/ext/maas/scripts/optimized/*/graph.py`

## Complexity and Efficiency

- Time complexity: Not reported in asymptotic form in the paper.
- Space complexity: Not reported in asymptotic form in the paper.
- Runtime characteristics: the main bottleneck is repeated online LLM execution during optimization.
- Scaling notes: deeper supernets and larger sample count `K` improve flexibility but increase optimization cost.
- Reported evidence: on MATH, MaAS reports `3.38$` training cost and `0.42$` inference cost, versus AFlow's `22.50$` and `1.66$`.

## Implementation Notes

- Architecture: the public repo uses a `MultiLayerController` with four selector layers and MiniLM sentence embeddings.
- Hyperparameters: the paper uses `L=4`, `K=4`, `thres=0.3`, and a cost penalty coefficient `lambda`.
- Constraints / masking: the public code forces the first layer to include `Generate` and prevents `EarlyStop` from being selected first.
- Optimization tricks: the repo uses a REINFORCE-style loss `-(logprobs * utilities).mean()` with `utilities = score - 3 * cost`.
- Failure modes / gotchas: public code does not expose the full paper operator space and benchmark suite; reproducibility is therefore partial.

## Comparison to Related Methods

- Compared with [[AFlow]]: AFlow searches for a single final workflow, while MaAS learns a query-conditioned workflow distribution.
- Compared with [[AgentSquare]]: AgentSquare automates agent design but MaAS explicitly focuses on per-query routing and cost-aware sampling.
- Main advantage: dynamic resource allocation across queries instead of static one-size-fits-all execution.
- Main tradeoff: more moving parts, heavier dependence on online LLM feedback, and a less straightforward reproduction path.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 5, Fig. 6, Fig. 7
- Key table(s): Tab. 1, Tab. 2, Tab. 3, Tab. 4
- Key equation(s): Eq. (1), Eq. (5), Eq. (8), Eq. (9), Eq. (10), Eq. (11), Eq. (12)
- Key algorithm(s): Alg. 1

## References

- arXiv: https://arxiv.org/abs/2502.04180
- HTML: https://arxiv.org/html/2502.04180v2
- Code: https://github.com/bingreeky/MaAS
- Local implementation: D:/PRO/essays/code_depots/Multi-agent Architecture Search via Agentic Supernet

