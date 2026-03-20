---
title: "Group Fisher Pruning"
type: method
source_paper: "Group Fisher Pruning for Practical Network Compression"
source_note: "[[Group Fisher Pruning]]"
authors: [Liyang Liu, Shilong Zhang, Zhanghui Kuang, Aojun Zhou, Jing-Hao Xue, Xinjiang Wang, Yimin Chen, Wenming Yang, Qingmin Liao, Wayne Zhang]
year: 2021
venue: ICML
tags: [nas-method, pruning, model-compression, structured-pruning]
created: 2026-03-20
updated: 2026-03-20
---

# Group Fisher Pruning

## One-line Summary

> Group Fisher Pruning is a structured channel pruning method that uses Fisher-based mask importance, autograd-derived layer grouping, and memory-normalized greedy pruning to compress CNNs with coupled channels in residual, grouped, depth-wise, and FPN-style structures.

## Source

- Paper: [Group Fisher Pruning for Practical Network Compression](https://proceedings.mlr.press/v139/liu21ab.html)
- HTML: Not provided by the paper source used in this note
- arXiv: https://arxiv.org/abs/2108.00708
- Code: https://github.com/jshilong/FisherPruning
- Paper note: [[Group Fisher Pruning]]

## Applicable Scenarios

- Problem type: Structured channel pruning for CNN inference acceleration.
- Assumptions: The model is already trained close to convergence, and channel-wise structural pruning is a valid compression operation.
- Data regime: Supervised image classification and object detection.
- Scale / constraints: CNN backbones and detectors with residual branches, grouped/depth-wise conv, and FPN-like multi-branch heads.
- Why it fits: It explicitly models cross-layer channel coupling, so the pruned structure remains deployable and yields real speedup instead of only theoretical FLOPs reduction.

## Not a Good Fit When

- The target model is not naturally channel-prunable, such as architectures dominated by attention blocks without a straightforward channel coupling interpretation.
- You need one-shot pruning without iterative prune-finetune cycles.
- The deployment target is not GPU-like and memory reduction is not a reliable latency proxy.

## Inputs, Outputs, and Objective

- Inputs: A converged dense model `W^0`, training data, prune interval `d`, and a target compute budget.
- Outputs: A pruned model `W` plus binary input masks `m` for channels or channel groups.
- Objective: Iteratively remove the channel/group with the smallest loss impact per unit compute reduction.
- Core assumptions: Local Taylor/Fisher approximation is meaningful near convergence, and coupled channels should share masks to preserve valid structure.

## Method Breakdown

### Stage 1: Masked Channel Parameterization

- Attach a binary input mask to each Conv/FC layer and multiply it with the layer input feature.
- Pruning a channel is implemented by setting the corresponding mask entry to zero.
- Source: Sec. 3, Sec. 3.1, Eq. (1)

### Stage 2: Single-Channel Fisher Importance

- Approximate the loss increase from deleting channel `i` via second-order Taylor expansion.
- Replace the Hessian diagonal with a Fisher approximation so that importance becomes proportional to the squared sample-wise gradient of the mask.
- Source: Sec. 3.1, Eq. (1), Eq. (2), Eq. (3)

### Stage 3: Layer Grouping for Coupled Channels

- Traverse the computation graph with DFS to find each Conv/FC layer's nearest Conv parents.
- Group layers whose parents overlap, and merge grouped/depth-wise cases where input and output channels are structurally tied.
- Make all channels in the same coupling group share one mask.
- Source: Sec. 3.2, Fig. 3, Fig. 4, Algorithm 1

### Stage 4: Group Importance and Greedy Pruning

- Sum gradients across all channels that share the same mask and square the result to obtain group importance.
- Normalize importance by memory reduction rather than FLOPs reduction.
- Every `d` iterations, prune the channel/group with minimum normalized importance, then continue training and re-accumulating scores.
- Source: Sec. 3.2, Eq. (4), Sec. 3.3, Fig. 6, Algorithm 2

### Stage 5: Deployment and Fine-tuning

- After reaching the target budget, physically remove zero-masked channels and fine-tune the compact model.
- Source: Sec. 3, Algorithm 2; code evidence in `deploy_pruning()`

## Pseudocode

```text
Algorithm: Group Fisher Pruning
Input: Converged dense model W^0, training data D, prune interval d, target budget
Output: Pruned model W, shared channel masks m

1. Attach binary input masks to all Conv/FC layers, initialized to 1.
   Source: Sec. 3, Sec. 3.1
2. Build the computation graph and run DFS to find nearest parent convolutions.
   Source: Fig. 4, Algorithm 1
3. Form layer groups for channels that are structurally coupled, and assign a shared mask to each group.
   Source: Sec. 3.2, Fig. 3, Algorithm 1
4. During training, accumulate sample-wise mask gradients and estimate Fisher importance for each layer/group.
   Source: Eq. (2), Eq. (3), Eq. (4)
5. Compute normalized pruning scores using importance divided by memory reduction.
   Source: Sec. 3.3, Fig. 6
6. Every d iterations, prune the channel/group with the smallest normalized score.
   Source: Algorithm 2
7. Repeat accumulation and pruning until the desired FLOPs budget is reached.
   Source: Algorithm 2
8. Materialize the compact network by slicing tensors according to the masks, then fine-tune.
   Source: Inference from source; code evidence in deploy_pruning()
```

## Training Pipeline

1. Start from a pre-trained dense model.
2. Insert mask buffers and register forward/backward hooks for Conv modules.
3. Run standard training iterations while collecting mask-gradient statistics.
4. Accumulate Fisher scores over a fixed interval.
5. Prune one channel/group greedily.
6. Reset accumulators and continue training until the target compute budget is met.
7. Fine-tune the compact architecture.

Sources:

- Algorithm 2
- Sec. 3.1, Sec. 3.2, Sec. 3.3
- Code: `FisherPruningHook.before_run`, `after_train_iter`, `group_fishers`, `channel_prune`

## Inference Pipeline

1. Take the pruned checkpoint with learned masks.
2. Convert mask-defined sparsity into actual smaller Conv/BN tensors.
3. Run the compact model normally without the pruning-time masking overhead.

Sources:

- Sec. 3
- Code: `after_build_model`, `deploy_pruning()`

## Complexity and Efficiency

- Time complexity: Not reported as a closed-form expression in the paper.
- Space complexity: Not reported as a closed-form expression in the paper.
- Runtime characteristics: The method adds pruning-time hook overhead and repeated prune-finetune cycles, but aims to reduce deployment-time wall-clock latency.
- Scaling notes: Its practical advantage grows when the architecture contains more coupled structures, because naive per-layer pruning fails to unlock those speedups.

## Implementation Notes

- Architecture: The public code wraps pruning as an MMCV hook named `FisherPruningHook`.
- Hyperparameters: The paper prunes every `d=25` iterations for classification and `d=10` for detection.
- Constraints / masking: Each Conv gets `in_mask` and `out_mask`; grouped layers share `in_mask` entries when they are structurally coupled.
- Optimization tricks: The method interleaves pruning and continued optimization instead of pruning everything in one shot.
- Practical gotchas:
  - The public repo requires `pytorch==1.3.0` because its grouping logic depends on old autograd internals.
  - The code uses `delta='acts'` as the memory-like normalization proxy.
  - The released repo is detection-centric; classification code mentioned in the paper/README is not fully released.
  - `set_group_masks()` contains `# TODO: support two stage model`, so the public implementation coverage is narrower than the paper narrative.

## Comparison to Related Methods

- Compared with [[Channel Pruning]] methods like CP / ThiNet: Group Fisher Pruning is global rather than layer-wise, and it does not rely on manual sensitivity analysis.
- Compared with heuristic coupling methods like IE / C-SGD: it derives shared-mask importance from the chain rule instead of heuristically combining scores.
- Main advantage: It turns structured coupling into a first-class object and optimizes for real GPU-friendly efficiency.
- Main tradeoff: It is more engineering-heavy and depends on iterative training plus graph introspection.

## Evidence and Traceability

- Key figure(s): Fig. 3, Fig. 4, Fig. 5, Fig. 6
- Key table(s): Table 1, Table 2, Table 3, Table 5, Table 6
- Key equation(s): Eq. (1), Eq. (2), Eq. (3), Eq. (4)
- Key algorithm(s): Algorithm 1, Algorithm 2

## References

- PMLR: https://proceedings.mlr.press/v139/liu21ab.html
- arXiv: https://arxiv.org/abs/2108.00708
- Code: https://github.com/jshilong/FisherPruning
- Local implementation: D:/PRO/essays/code_depots/Group Fisher Pruning for Practical Network Compression
