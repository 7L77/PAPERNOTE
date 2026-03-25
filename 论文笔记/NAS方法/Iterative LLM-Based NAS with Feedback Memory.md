---
title: "Iterative LLM-Based NAS with Feedback Memory"
type: method
source_paper: "Resource-Efficient Iterative LLM-Based NAS with Feedback Memory"
source_note: "[[Iterative LLM-Based NAS with Feedback Memory]]"
authors: [Xiaojie Gu, Dmitry Ignatov, Radu Timofte]
year: 2026
venue: arXiv
tags: [nas-method, llm-nas, iterative-search, feedback-memory]
created: 2026-03-23
updated: 2026-03-23
---

# Iterative LLM-Based NAS with Feedback Memory

## One-line Summary
> The method turns LLM-based architecture generation into a closed-loop NAS process with bounded historical memory and explicit failure-aware feedback.

## Source
- Paper: [Resource-Efficient Iterative LLM-Based NAS with Feedback Memory](https://arxiv.org/abs/2603.12091)
- HTML: https://arxiv.org/html/2603.12091v1
- Code: https://anonymous.4open.science/r/Iterative-LLM-Based-NAS-with-Feedback-Memory-E7D6/README.md
- Paper note: [[Iterative LLM-Based NAS with Feedback Memory]]

## Applicable Scenarios
- Problem type: Low-budget architecture search for image classification.
- Assumptions: Early-epoch accuracy can provide useful ranking signal.
- Data regime: Supervised image datasets (CIFAR-10/100, ImageNette in paper).
- Scale / constraints: Single consumer GPU, no LLM fine-tuning.
- Why it fits: It reuses failure logs and bounded history instead of brute-force random re-generation.

## Not a Good Fit When
- You need SOTA fully converged architecture quality without additional full-training verification.
- The code-generation model has very low pass rate on your target domain.
- Your task requires strict architecture constraints that are hard to enforce via text prompting.

## Inputs, Outputs, and Objective
- Inputs: Dataset spec, current best architecture code, current iteration result, recent improvement history.
- Outputs: New candidate architecture code and updated best architecture.
- Objective: Maximize one-epoch proxy accuracy over iterations.
- Core assumptions: Bounded recent history is enough for useful iterative decision making.

## Method Breakdown
### Stage 1: Candidate generation
- Generate `Net(nn.Module)` code with prompt conditioning on best code and previous suggestions.
- Source: Sec. 3.1, Sec. 3.2, Alg. 1.

### Stage 2: Validation and proxy evaluation
- Run quick structural validation, then one-epoch training and Top-1 test accuracy evaluation.
- Source: Sec. 3.3, Sec. 4.1.

### Stage 3: Feedback refinement
- Prompt Improver analyzes current result + bounded history and emits structured suggestions.
- Source: Sec. 3.4, Eq. (1)-(3).

### Stage 4: History update and loop
- Save `(problem, suggestion, outcome)` and keep last `K=5` entries.
- Source: Sec. 3.4, Eq. (1), Alg. 1.

## Pseudocode
```text
Algorithm: Iterative LLM-Based NAS with Feedback Memory
Input: LLM L, max iterations T, history window K=5, dataset D
Output: Best architecture A*

1. Initialize A* = None, a* = 0, H = empty, s0 = None
   Source: Alg. 1
2. For t = 1..T:
   2.1 Generate candidate At using Code Generator with (A*, st-1, current code/result)
       Source: Sec. 3.1/3.2, Alg. 1
   2.2 Quick-validate At (instantiation + forward shape check)
       Source: Sec. 3.3
   2.3 If valid, train At for one epoch and get proxy accuracy at; else record error
       Source: Sec. 3.3, Sec. 4.1
   2.4 If at > a*, set A*=At, a*=at
       Source: Alg. 1
   2.5 Prompt Improver generates st from (A*, At, at/error, H)
       Source: Sec. 3.4
   2.6 Append diagnostic triple (problem, suggestion, outcome) and truncate H to last K
       Source: Eq. (1), Eq. (3)
3. Return A*
   Source: Alg. 1
```

## Training Pipeline
1. Load dataset and augmentation (CIFAR random crop + flip, etc.).
2. Instantiate generated model and run one-epoch training.
3. Optimize with SGD (`lr=0.01`, `momentum=0.9`, `weight_decay=5e-4`) + cosine scheduler.
4. Evaluate Top-1 accuracy as proxy score.

Sources:
- Sec. 3.3, Sec. 4.1, Table 2.

## Inference Pipeline
1. For each iteration, LLM generates architecture code from prompt context.
2. Evaluator returns proxy score or structured error.
3. Prompt Improver updates next-iteration guidance.
4. Keep best-so-far architecture for final output.

Sources:
- Sec. 3.1-3.4, Alg. 1.

## Complexity and Efficiency
- Time complexity: `O(T * C_eval)` where `C_eval` is one-epoch train+eval cost.
- Space complexity: dominated by loaded LLM + candidate model training footprint.
- Runtime characteristics: reported ~18 GPU hours for 2000 iterations on RTX 4090.
- Scaling notes: higher image resolution can sharply reduce generation/evaluation success rate.

## Implementation Notes
- Pipeline orchestrator: `pipeline.py`.
- Generation settings: `temperature=0.7`, `top_p=0.9`, `max_new_tokens=2048` (`llm_client.py`).
- History storage: `improvement_history` with configurable `history_size` (default 5).
- Validation details: forward pass check and output class check in `evaluator.py`.
- Training worker isolation: subprocess in `train_script.py` with 30-minute timeout.
- Reproducibility: fixed seed 43 + deterministic CUDA flags in pipeline and train script.

## Comparison to Related Methods
- Compared with [[LLMO]]: this method works in open executable code space rather than fixed discrete cells.
- Compared with [[EvoPrompting]]: no LLM fine-tuning requirement in the reported pipeline.
- Compared with [[OPRO]]: explicitly models failure outcomes via diagnostic triples.
- Main advantage: failure-aware iterative refinement under limited compute budget.
- Main tradeoff: proxy objective may not fully match converged final accuracy.

## Evidence and Traceability
- Key figure(s): Fig. 1 (pipeline), Fig. 2 (trajectory), Fig. 3 (ablation).
- Key table(s): Table 1 (positioning), Table 2 (main quantitative comparison).
- Key equation(s): Eq. (1) history window, Eq. (2) Markov assumption, Eq. (3) diagnostic triple.
- Key algorithm(s): Algorithm 1 in Sec. 3.4.

## References
- arXiv: https://arxiv.org/abs/2603.12091
- HTML: https://arxiv.org/html/2603.12091v1
- Code: https://anonymous.4open.science/r/Iterative-LLM-Based-NAS-with-Feedback-Memory-E7D6/README.md
- Local implementation: D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory
