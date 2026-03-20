---
title: "Fisher Pruning for Gaze Prediction"
type: method
source_paper: "Faster Gaze Prediction With Dense Networks and Fisher Pruning"
source_note: "[[Faster gaze prediction with dense networks and Fisher pruning]]"
authors: [Lucas Theis, Iryna Korshunova, Alykhan Tejani, Ferenc Huszar]
year: 2018
venue: arXiv
tags: [nas-method, pruning, saliency, distillation, efficient-inference]
created: 2026-03-20
updated: 2026-03-20
---

# Fisher Pruning for Gaze Prediction

## One-line Summary
> The method compresses DeepGaze-style saliency models by distilling a strong teacher into smaller backbones and then greedily pruning feature maps with an empirical-Fisher loss estimate regularized by FLOPs.

## Source
- Paper: [Faster Gaze Prediction With Dense Networks and Fisher Pruning](https://arxiv.org/abs/1801.05787)
- HTML: https://arxiv.org/html/1801.05787
- Code: Not officially released in the paper / author page (checked 2026-03-20)
- Paper note: [[Faster gaze prediction with dense networks and Fisher pruning]]

## Applicable Scenarios
- Problem type: Static-image saliency / gaze prediction with deployment-time latency constraints.
- Assumptions: A large teacher already performs well; feature-map sensitivity estimated from gradients is informative for pruning.
- Data regime: Supervised fixation data plus teacher-generated saliency maps for distillation.
- Scale / constraints: CNN backbones where channel pruning changes real runtime on CPU.
- Why it fits: The method directly trades task loss against computational cost instead of pruning with a task-agnostic magnitude heuristic.

## Not a Good Fit When
- You need a training-free architecture ranking method before any teacher/student training.
- The model architecture is not channel-structured, so removing feature maps does not translate into actual runtime gains.
- Your task has no stable teacher model or no reliable probability-style supervision.

## Inputs, Outputs, and Objective
- Inputs: Image `I`, fixation labels `z`, teacher saliency maps, pretrained backbone features, current feature-map activations.
- Outputs: A pruned saliency model such as FastGaze or DenseGaze and a pixelwise fixation probability map.
- Objective: Minimize saliency cross-entropy while reducing FLOPs through greedy feature-map removal.
- Core assumptions: Local second-order loss change can be approximated by an empirical Fisher diagonal; reduced FLOPs correlate with faster inference.

## Method Breakdown

### Stage 1: Build efficient saliency students
- Replace DeepGaze II's heavy VGG-19 multi-layer feature stack with smaller backbones such as VGG-11 or DenseNet-121.
- Move readout before upsampling and use separable Gaussian blur to reduce compute.
- Source: Sec. 2, Eq. (1).

### Stage 2: Distill teacher knowledge into the students
- Train DeepGaze II teacher models and ensemble them to produce saliency maps on SALICON.
- Train students with a weighted combination of real fixation cross-entropy and teacher-map cross-entropy.
- Source: Sec. 2.4.

### Stage 3: Score feature maps with Fisher pruning
- Introduce a binary mask on each feature map and estimate the loss increase from removing a map via squared gradients.
- Use the empirical Fisher approximation to avoid an explicit Hessian computation.
- Source: Sec. 2.1, Eq. (2)-(9), Supplementary Sec. S1/S2.

### Stage 4: Prune under a compute-aware objective
- Compute FLOPs per layer and combine predicted loss increase with compute decrease in a Lagrangian objective.
- Greedily remove the feature map with the best joint loss-cost tradeoff, then continue training and repeat.
- Source: Sec. 2.2, Eq. (10)-(13).

### Stage 5: Tune or auto-tune the tradeoff weight
- Either sample a fixed `beta` or rank features by the threshold value `beta_i = -DeltaL_i / DeltaC_i`.
- Auto-tuning works reasonably for light pruning but is weaker under aggressive pruning.
- Source: Sec. 2.3, Eq. (14)-(16), Sec. 3.1.

## Pseudocode

```text
Algorithm: Fisher Pruning for Gaze Prediction
Input: Image dataset with fixations, teacher saliency model, candidate student backbone, tradeoff beta
Output: Pruned saliency network

1. Train or reuse a strong DeepGaze-style teacher and generate teacher saliency maps on extra data.
   Source: Sec. 2.4
2. Train a smaller student saliency model with fixation CE + teacher-map CE.
   Source: Sec. 2.4
3. Insert a binary mask mk on each feature map and collect gradients over several training steps.
   Source: Sec. 2.1, Eq. (8)-(9)
4. Estimate per-feature pruning loss Delta_k = (1 / 2N) sum_n g_nk^2.
   Source: Sec. 2.1, Eq. (7), Eq. (9)
5. Compute compute change DeltaC_k from the current architecture FLOPs.
   Source: Sec. 2.2, Eq. (10)-(11)
6. Select the feature map minimizing DeltaL_k + beta * DeltaC_k and prune it.
   Source: Sec. 2.2, Eq. (12)-(13)
7. Continue optimization, refresh pruning signals and compute costs, and repeat until the target budget is reached.
   Source: Sec. 2.4, Fig. 1
8. Optionally rank maps by beta_k = -DeltaL_k / DeltaC_k when using the hyperparameter-free variant.
   Source: Sec. 2.3, Eq. (15), Inference from source
```

## Training Pipeline
1. Pretrain / train the DeepGaze II teacher with SALICON and MIT1003.
2. Ensemble 10 teacher models to produce distilled supervision on SALICON.
3. Train FastGaze or DenseGaze with fixation loss weight `0.1` and teacher-map loss weight `0.9`.
4. After convergence, alternate between accumulating pruning signals for 10 steps and pruning one feature map.
5. During pruning, continue optimization with SGD, learning rate `0.0025`, momentum `0.9`.

Sources:
- Sec. 2.4.

## Inference Pipeline
1. Extract image features with the pruned FastGaze or DenseGaze backbone.
2. Apply the readout network, then upsample, blur, and add the center-bias prior.
3. Apply softmax to obtain a fixation probability distribution over pixels.

Sources:
- Sec. 2, Eq. (1), Fig. 4.

## Complexity and Efficiency
- Time complexity: Not given analytically for the whole pruning loop.
- Space complexity: Not reported in the paper.
- Runtime characteristics: CPU single-image latency is the primary target.
- Scaling notes: Reported FLOPs drop from `240.6 GFLOP` for DeepGaze II to `10.7` for FastGaze and `12.8` for DenseGaze on MIT300 reporting.
- Practical outcome: About `10x` speedup for similar AUC on CAT2000; heavily pruned models can exceed `39x` to `75x` speedup depending on the metric comparison.

## Implementation Notes
- The pruning signal is channel-level, not individual-weight sparsification, because real speedups depend on dense tensor shapes.
- Cost estimates must be updated after each pruning step; otherwise neighboring-layer interactions make early cost estimates stale.
- The method relies on probability-style saliency supervision, so the gradient is taken with respect to log-probability outputs.
- Strong distillation is essential here because fixation datasets alone are too small to safely fine-tune the whole backbone.
- Official code was not released, so the exact teacher ensemble and pruning schedule must be reconstructed from the paper.

## Comparison to Related Methods
- Compared with [[DeepGaze II]]: This method keeps the saliency output structure but compresses the backbone and prunes channels aggressively.
- Compared with Molchanov-style pruning: Similar gradient-based spirit, but with a cleaner Fisher-based derivation and stronger compute-aware regularization.
- Main advantage: The pruning decision is tied to both task loss sensitivity and actual FLOPs.
- Main tradeoff: It is a post-training compression workflow, not a direct architecture search method from scratch.

## Evidence and Traceability
- Key figure(s): Fig. 1-4.
- Key table(s): Table 1 and Table 2.
- Key equation(s): Eq. (1), Eq. (7)-(16).
- Key algorithm(s): No formal algorithm block; pruning loop reconstructed from Sec. 2.1-2.4 and Fig. 1.

## References
- arXiv: https://arxiv.org/abs/1801.05787
- HTML: https://arxiv.org/html/1801.05787
- Code: Not officially released (checked 2026-03-20)
- Local implementation: Not archived

