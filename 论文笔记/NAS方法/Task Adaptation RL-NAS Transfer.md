---
title: "Task Adaptation RL-NAS Transfer"
type: method
source_paper: "Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning"
source_note: "[[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]"
authors: [Amber Cassimon, Siegfried Mercelis, Kevin Mets]
year: 2024
venue: arXiv
tags: [nas-method, reinforcement-learning, transfer-learning, transnasbench-101]
created: 2026-03-17
updated: 2026-03-17
---

# Task Adaptation RL-NAS Transfer

## One-line Summary
> Pretrain an iterative RL-NAS agent on one task, transfer weights to a new task, and adapt with limited or full target-task training to improve efficiency and final quality.

## Source
- Paper: [Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning](https://arxiv.org/abs/2412.01420)
- HTML: https://arxiv.org/html/2412.01420v2
- Code: Not linked in paper
- Paper note: [[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]

## Applicable Scenarios
- Problem type: cross-task adaptation of RL-based architecture search policies.
- Assumptions: source and target tasks share a compatible search space and environment interface.
- Data regime: benchmark-driven RL interaction (offline benchmark evaluator + online policy updates).
- Scale/constraints: expensive from-scratch RL-NAS training where transfer can reduce warm-up cost.
- Why it fits: reuses policy/value initialization so target optimization starts from better priors.

## Not a Good Fit When
- Source and target tasks use incompatible search spaces.
- Reward ranges are highly mismatched without proper normalization/shaping.
- A high-quality source policy is unavailable.

## Inputs, Outputs, and Objective
- Inputs: source task `Ts`, target task `Tt`, pretrained RL-NAS agent parameters `theta_s`.
- Outputs: adapted target-task agent `theta_t` and searched architectures for `Tt`.
- Objective: maximize target-task NAS performance while reducing adaptation time.
- Core assumptions: transferable architecture-edit behavior exists across tasks.

## Method Breakdown
### Stage 1: Task subset design
- Select diverse tasks with relatively low ranking correlation using Kendall's tau matrix from TransNAS-Bench-101.
- Source: Sec. 3.1, Fig. 1.

### Stage 2: Source-task pretraining
- Train one RL-NAS agent per source task for `1e7` timesteps.
- Source: Sec. 4 (experiment protocol).

### Stage 3: Target-task transfer regime
- Initialize target agent with source weights and run one of:
  - zero-shot (no extra training),
  - fine-tuning (`+1e6` target steps),
  - re-training (`+1e7` target steps).
- Source: Sec. 4, Figs. 5-7.

### Stage 4: Task-specific reward shaping
- For semantic segmentation only, apply `R'(s,a)=R(s,a)^gamma` with `gamma=0.478`.
- Source: Sec. 3.2, Figs. 2-4.

## Pseudocode
```text
Algorithm: Task Adaptation RL-NAS Transfer
Input: task set T, source task Ts, target task Tt, RL-NAS agent A
Output: adapted target-task agent At and its searched architectures

1. Pretrain As on Ts for 1e7 timesteps.
   Source: Sec. 4
2. Initialize At <- As parameters.
   Source: Sec. 3 (transfer setup)
3. If Tt == segmentsemantic, use gamma-shaped reward:
      R'(s,a) = R(s,a)^gamma, gamma = 0.478
   Source: Sec. 3.2, Figs. 2-4
4. Run one regime:
   4.1 Zero-shot: evaluate directly on Tt.
       Source: Sec. 4
   4.2 Fine-tune: train At on Tt for 1e6 timesteps, then evaluate.
       Source: Sec. 4
   4.3 Re-train: train At on Tt for 1e7 timesteps, then evaluate.
       Source: Sec. 4
5. Compare with scratch-trained baseline on Tt using mean/std/95% CI.
   Source: Sec. 4.1-4.3, Figs. 5-13
```

## Training Pipeline
1. Build TransNAS-Bench-101 task-specific environments.
2. Train source agents with Ape-X style distributed replay-based Q-learning.
3. Transfer weights to target tasks and continue optimization per regime.
4. Evaluate using test metrics (validation metrics used during training).

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4.

## Inference Pipeline
1. Use the adapted RL agent to navigate architecture-neighborhood edits.
2. Rank/choose candidate architectures via learned policy/value outputs.
3. Output the selected architecture set for target-task evaluation.

Sources:
- Source: Inference from source (paper describes training/evaluation protocol but not standalone deployment algorithm block).

## Complexity and Efficiency
- Time complexity: dominated by RL interaction steps (`1e7` source + `1e6` or `1e7` target steps).
- Space complexity: replay buffer + model parameters.
- Runtime characteristics: still expensive, but transfer reduces time-to-reference performance in many pairs.
- Scaling notes: convergence speed appears weakly tied to search-space size in the reported comparisons.

## Implementation Notes
- RL details: double Q-learning, dueling heads, 3-step bootstrap + PEB.
- Optimizer: Adam (`lr=5e-5`), gradient clipping `L2=40`.
- Target network update period: 8192 steps.
- Replay buffer: prioritized replay, capacity `25k`, `alpha=0.6`, `beta=0.4`.
- Input processing: architecture graph padding + one-hot operations + transformer encoder.
- No official code link is provided for this paper in-text.

## Comparison to Related Methods
- Compared with training-from-scratch RL-NAS:
  transfer often gives better final performance and faster adaptation.
- Compared with zero-shot-only transfer:
  even short fine-tuning (`1e6`) yields major gains.
- Main advantage: practical cost reduction for new tasks without redesigning the search agent.
- Main tradeoff: gains depend on source-target pairing and shared search-space assumptions.

## Evidence and Traceability
- Key figure(s): Fig. 1 (task correlation), Fig. 2-4 (reward shaping), Fig. 5-7 (regime outcomes), Fig. 10-13 (time-to-reference).
- Key table(s): no dedicated numbered tables; figure matrices carry quantitative outcomes.
- Key equation(s): `R'(s,a)=R(s,a)^gamma` in Sec. 3.2.
- Key algorithm(s): transfer protocol in Sec. 4 (regime definitions).

## References
- arXiv: https://arxiv.org/abs/2412.01420
- HTML: https://arxiv.org/html/2412.01420v2
- Code: Not linked in paper
- Local implementation: Not archived

