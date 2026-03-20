---
title: "APD"
type: method
source_paper: "Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models"
source_note: "[[APD]]"
authors: [Haidong Kang, Lihong Lin, Hanling Wang]
year: 2025
venue: NeurIPS
tags: [nas-method, training-free-nas, zero-cost-proxy, llm, actor-critic]
created: 2026-03-16
updated: 2026-03-20
---

# APD

## One-line Summary

> APD uses an LLM to generate zero-cost proxies and an actor-critic scheduler to choose initialization/mutation/crossover prompt strategies, turning proxy design into a learnable evolutionary process.

## Source

- Paper: [Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models](https://openreview.net/forum?id=JJEiQmE5yA)
- PDF: https://openreview.net/pdf/4de84ad7c65b21c88fbadfd0dda141113b8c3017.pdf
- NeurIPS page: https://nips.cc/virtual/2025/poster/120003
- Code: https://github.com/yohbii/APD
- Paper note: [[APD]]

## Applicable Scenarios

- Problem type: Training-free ranking of neural architectures via automatically discovered zero-cost proxies.
- Assumptions: A benchmark subset with ground-truth performance is available for correlation-based fitness.
- Data regime: Image classification and related vision tasks across multiple NAS search spaces.
- Scale / constraints: Useful when full candidate retraining is too expensive and ranking quality is the main objective.
- Why it fits: It jointly optimizes proxy content and evolution strategy, not only proxy formulas.

## Not a Good Fit When

- You cannot safely execute generated code in a sandboxed environment.
- You have no reliable ground-truth subset for fitness feedback.
- Strong determinism is required and LLM variance cannot be tolerated.

## Inputs, Outputs, and Objective

- Inputs: Prompt set `Π`, current population `P_t`, context window `C_t`, benchmark architectures with known performance.
- Outputs: Evolved proxy population and best proxy `f*`.
- Objective: Maximize ranking correlation between proxy scores and true architecture performance.
- Core assumptions: Better prompt operations can be learned from reward signals, and generated proxy code captures transferable ranking heuristics.

## Method Breakdown

### Stage 1: Context-aware Proxy Generation

- At each step, APD selects an operation (`init`, `mut`, `cross`) and calls LLM with prompt plus context proxies.
- Each proxy is represented as `(T, C)`: natural-language thought + executable code.
- Source: Sec. 3.1, Eq. (2), Eq. (3), Fig. 4.

### Stage 2: Fitness Evaluation

- Evaluate proxy by correlation with ground-truth architecture performance, penalized by runtime cost.
- Source: Sec. 3.1, Eq. (4).

### Stage 3: Actor-Critic Scheduling

- Actor picks next operation based on history state; critic provides value baseline.
- Reward is the mean fitness of generated candidates.
- Source: Sec. 3.1, Eq. (5).

### Stage 4: Population Update

- Merge old/new candidates, keep top population size, repeat for `T_max` generations.
- Source: Sec. 3.2, Algorithm 1.

## Pseudocode

```text
Algorithm: APD
Input: LLM L, prompt operations Π={init,mut,cross}, benchmark B, population size N, budget T_max
Output: Best proxy f*

1. Initialize population P0 from initialization prompt.
   Source: Sec. 3.2 Step 0, Algorithm 1
2. For generation t = 1..T_max:
   2.1 Build state s_t from strategy/reward history.
       Source: Sec. 3.1 (state description)
   2.2 Sample action a_t=(op, C_t) from actor policy πθ(a|s_t).
       Source: Sec. 3.1, Eq. (5)
   2.3 Generate candidates P'_t = L(op, C_t) via prompt-conditioned LLM call.
       Source: Sec. 3.1 Eq. (2)(3), Sec. 3.2 Step 1
   2.4 Evaluate each candidate fitness ϕ with correlation (and cost term).
       Source: Sec. 3.1 Eq. (4), Sec. 3.2 Step 2
   2.5 Compute reward r_t = E[ϕ(P'_t)], update actor/critic.
       Source: Sec. 3.1 Eq. (5), Sec. 3.2 Step 3
   2.6 Select next population P_{t+1} from P_t ∪ P'_t.
       Source: Sec. 3.2 Step 4, Algorithm 1
3. Return proxy with highest fitness.
   Source: Algorithm 1
```

## Training Pipeline

1. Build benchmark-specific prompt templates (`init/mut/cross`) and operation constraints.
2. Run evolutionary loop with actor-critic scheduler.
3. Evaluate candidate proxies over sampled architecture subsets.
4. Keep top proxies and iterate across generations.

Sources:

- Sec. 3.1, Sec. 3.2, Algorithm 1, Appendix B/C.

## Inference Pipeline

1. Fix the discovered proxy function.
2. For a new architecture, run single forward-style proxy computation at initialization.
3. Use proxy scores to rank candidates, then retrain only selected top architectures.

Sources:

- Sec. 2, Sec. 4.2-4.5.

## Complexity and Efficiency

- Time complexity: Not provided as closed-form.
- Space complexity: Not provided as closed-form.
- Runtime characteristics: Paper reports APD reaches Spearman > 0.80 within ~30 generations in ~1 GPU hour on RTX4090.
- Scaling notes: Cost grows with number of generations, population size, and per-proxy evaluation overhead.

## Implementation Notes

- Main loop implementation: `main.py` (`get_new_pop`, env evaluation, A2C update, top-k replacement).
- Proxy extraction format: `src/utils.py` parses markdown blocks with description + Python code.
- Execution model: `src/env.py` runs generated code via `exec`; failures default to score `0`.
- Prompt operations: action index `0/1/2` maps to initialization/mutation/crossover.
- Reported default hyperparameters in paper: episodes=10, steps=100, history=5, gamma=0.9, hidden=256, batch=16, repeats=5 (Table 8).
- Paper/code divergence:
  - Paper defines `ϕ = ρ - β cost`; current env path mainly consumes a scalar score returned by evaluator.
  - Paper says invalid proxy gets `-∞`; code falls back to `0`.
  - `ValueNet` in current code uses `softmax` over a single value output, which collapses critic expressiveness.
  - Repository currently lacks some files imported by `env.py` (`evaluate_nas201`, `evaluate_nas101`, `evaluate_trans101`) and prompt resources.

## Comparison to Related Methods

- Compared with [[Zero-Cost Proxy]] handcrafting: APD automates proxy discovery instead of manual design.
- Compared with [[AZ-NAS]] / [[SWAP-NAS]]-style fixed proxies: APD searches for benchmark-adaptive proxy code.
- Main advantage: adaptive and extensible proxy generation with empirical gains across diverse search spaces.
- Main tradeoff: dependence on LLM APIs, code-execution safety, and fitness supervision subset.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5.
- Key table(s): Table 1, Table 2, Table 3, Table 4, Table 5, Table 6, Table 7, Table 8.
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5).
- Key algorithm(s): Algorithm 1.

## References

- OpenReview: https://openreview.net/forum?id=JJEiQmE5yA
- PDF: https://openreview.net/pdf/4de84ad7c65b21c88fbadfd0dda141113b8c3017.pdf
- NeurIPS page: https://nips.cc/virtual/2025/poster/120003
- Code: https://github.com/yohbii/APD
- Local implementation: D:/PRO/essays/code_depots/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models
