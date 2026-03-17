---
title: "Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning"
method_name: "Task Adaptation RL-NAS Transfer"
authors: [Amber Cassimon, Siegfried Mercelis, Kevin Mets]
year: 2024
venue: arXiv
tags: [nas, reinforcement-learning, transfer-learning, transnasbench-101]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2412.01420v2
local_pdf: D:/PRO/essays/papers/Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning.pdf
created: 2026-03-17
---

# Paper Note: Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning

## Meta
| Item | Content |
|---|---|
| arXiv | https://arxiv.org/abs/2412.01420 |
| HTML | https://arxiv.org/html/2412.01420v2 |
| Local PDF | `D:/PRO/essays/papers/Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning.pdf` |
| Original PDF | `D:/PRO/essays/papers/2412.01420v2.pdf` |
| Official code | Not linked in paper (not archived) |
| Benchmark data | https://github.com/yawen-d/TransNASBench |

## One-line Summary
> The paper shows that pretraining a reinforcement learning NAS agent on one task and transferring it to another task usually improves final quality and reduces training time versus training from scratch.

## Core Contributions
1. Evaluates cross-task transfer for an iterative RL-based NAS agent (built on Cassimon et al., 2024) over four heterogeneous TransNAS-Bench-101 tasks.
2. Defines and compares three transfer regimes: zero-shot transfer, fine-tuning (`1e6` target steps), and re-training (`1e7` target steps).
3. Introduces task-specific reward shaping for semantic segmentation with gamma transform `R'(s,a)=R(s,a)^gamma`, tuned at `gamma=0.478`.
4. Reports statistically supported gains in most source-target pairs for both final performance and time-to-reference-performance.

## Problem Context
- Target problem: make [[Neural Architecture Search]] agents reusable across tasks instead of retraining from scratch each time.
- Why this matters: baseline RL-NAS training can require dozens to hundreds of GPU-hours.
- Benchmark scope: four tasks from [[TransNAS-Bench-101]] with low cross-task correlation (object classification, room layout, autoencoding, semantic segmentation).

## Method
### Transfer protocol
1. Train source-task agent for `1e7` timesteps.
2. Transfer parameters to target task.
3. Evaluate under three regimes:
- Zero-shot: no target training.
- Fine-tuning: +`1e6` target timesteps.
- Re-training: +`1e7` target timesteps.

### Reward shaping
- For semantic segmentation only, the authors use:
  `R'(s,a)=R(s,a)^gamma` with `gamma=0.478`.
- Motivation: spread low-end mIoU rewards to improve policy learning signal.

### RL setup highlights
- Algorithm family: distributed value-based RL with [[Ape-X]]-style training.
- Uses double Q-learning, dueling heads, 3-step bootstrapping + partial episode bootstrapping.
- Optimizer: Adam, LR `5e-5`, gradient clipping `L2=40`.
- Replay: [[Prioritized Experience Replay]], capacity `25k`, alpha `0.6`, beta `0.4`.

## Key Results
1. In re-training and fine-tuning regimes, transferred agents usually outperform scratch-trained agents on target tasks.
2. Zero-shot transfer is consistently weakest, but still shows non-trivial transfer signal.
3. Even limited target training (`1e6` steps) can produce clear gains over zero-shot.
4. Time-to-match-scratch performance is often reduced significantly for transferred agents, with strongest effects on room-layout and autoencoder targets.
5. Benefit magnitude is source-target dependent; not all task pairs are equally helpful.

## Critical View
### Strengths
1. Clean experimental matrix across source-target pairs and three transfer regimes.
2. Practical message: transfer can cut RL-NAS warm-up cost.
3. Includes statistical reporting (mean/std/95% CI) rather than only point estimates.

### Limitations
1. Only one RL algorithm (Ape-X family) is tested.
2. All tasks are computer vision; cross-domain transfer is untested.
3. Shared search space assumption may break in broader multi-domain NAS settings.
4. No official method repository link is provided in the paper text.

## Useful Takeaways For Our Work
1. If we keep the same search space, cross-task pretraining is likely a strong default for RL-NAS bootstrapping.
2. Reward shaping can be task-specific and still compatible with transfer.
3. For fast adaptation, a practical schedule is source pretrain `1e7` + target fine-tune `1e6` before deciding whether full retraining is needed.

## Related Concepts
- [[Transfer Learning]]
- [[Ape-X]]
- [[Prioritized Experience Replay]]
- [[Kendall's Tau]]

