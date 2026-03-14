---
title: "LLMENAS"
type: method
source_paper: "LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance"
source_note: "[[LLMENAS]]"
authors: [Xu Zhai, Xiaoyan Sun, Huan Zhao, Shengcai Liu, Rongrong Ji]
year: 2025
venue: arXiv
tags: [nco-method, nas, llm, evolutionary-search]
created: 2026-03-13
updated: 2026-03-13
---

# LLMENAS

## One-line Summary
> LLMENAS replaces handcrafted evolutionary crossover/mutation with LLM-guided operators and couples them with one-shot + surrogate evaluation to search stronger architectures at lower cost.

## Source
- Paper: [LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance](https://arxiv.org/abs/2501.13154)
- HTML: https://arxiv.org/html/2501.13154v2
- Code: https://github.com/LLMENAS/LLMENAS
- Paper note: [[LLMENAS]]

## Applicable Scenarios
- Problem type: Image-classification NAS with cell-based search spaces.
- Assumptions: Architecture tokens/graphs can be serialized for prompt-guided editing.
- Data regime: Supervised image classification (CIFAR-10, ImageNet-16-120 in paper).
- Scale / constraints: Suitable when search budget is constrained and full training for every candidate is too expensive.
- Why it fits: LLM-guided operators improve exploration quality while surrogate + one-shot cut evaluation cost.

## Not a Good Fit When
- You cannot call an external/frozen LLM during search.
- Search space is not naturally expressible as editable architecture tokens.
- Deterministic reproducibility is mandatory but prompt-driven generation variance is unacceptable.

## Inputs, Outputs, and Objective
- Inputs: Population of candidate architectures, crossover/mutation rates, history statistics `H=[f_best,f_avg,f_min]`.
- Outputs: Best discovered architecture genotype/cell.
- Objective: Maximize architecture accuracy under bounded search cost.
- Core assumptions: LLM edits are semantically useful and evaluation proxy correlates with final performance.

## Method Breakdown

### Stage 1: Population Initialization
- Build initial architecture population in a cell-based NAS search space.
- Source: Sec. 4.1, Eq. (1)

### Stage 2: LLM-guided Crossover
- Generate offspring by prompting LLM to combine parents under architecture constraints.
- Source: Sec. 4.2, Eq. (3), Fig. 2

### Stage 3: LLM-guided Mutation
- Apply mutation prompt conditioned on mutation rate and history performance summary.
- Source: Sec. 4.2, Eq. (4), Eq. (5)

### Stage 4: Fast Evaluation
- Use one-shot/supernet and surrogate predictor to score candidates cheaply.
- Source: Sec. 4.3, Sec. 4.4, Eq. (6)

### Stage 5: Selection and Iteration
- Keep high-quality candidates, update population, and repeat until budget ends.
- Source: Sec. 4.5, Algorithm 1

## Pseudocode
```text
Algorithm: LLMENAS
Input: Initial population P, crossover rate p_c, mutation rate p_m, max generations G_max
Output: Best architecture P*

1. Initialize population P in the NAS search space.
   Source: Sec. 4.1, Eq. (1)
2. For generation g = 1..G_max:
   2.1 Select parent architectures P^A, P^B.
       Source: Sec. 4.2
   2.2 Generate crossover child G^C = LLM_Crossover(P^A, P^B, p_c).
       Source: Eq. (3), Fig. 2
   2.3 Build history context H=[f_best,f_avg,f_min] and mutate:
       G^M = LLM_Mutation(G^C, p_m, H).
       Source: Eq. (4), Eq. (5)
   2.4 Evaluate candidate quickly with one-shot/surrogate score s=g_phi(E(P)).
       Source: Sec. 4.3-4.4, Eq. (6)
   2.5 Select next population by predicted/validated fitness.
       Source: Sec. 4.5, Algorithm 1
3. Return best architecture by target accuracy.
   Source: Eq. (7)
```

## Training Pipeline
1. Search stage: run iterative LLM-guided evolution + fast evaluation.
2. Derive final genotype from best candidate.
3. Retrain/evaluate discovered architecture in the target setting.
4. Report standard and robustness metrics.

Sources:
- Sec. 4, Sec. 5, Tab. 1/2/4/5

## Inference Pipeline
1. Use the selected final architecture (fixed genotype).
2. Run standard model inference on target images.
3. For robustness tests, apply PGD attack protocol before scoring.

Sources:
- Sec. 5.1-5.2, Tab. 4

## Complexity and Efficiency
- Time complexity: Not given as closed-form.
- Space complexity: Not given as closed-form.
- Runtime characteristics: Search reported at ~340 samples and 0.6 GPU days.
- Scaling notes: Compared with direct-search baselines, sample count and search cost are substantially reduced.

## Implementation Notes
- Architecture modules in code: `model_search.py`, `operations.py`, `genotypes.py`.
- Evaluation scripts: `train.py`, `test.py`.
- Important hyperparameters from public code: `epochs=600`, `init_channels=36`, `layers=20`, SGD + cosine LR.
- Practical gotcha: current public repo is mainly evaluation pipeline; full LLM-driven search implementation is not fully released yet (explicitly stated in README).
- Paper/code gap: method-level LLM operator details are paper-derived; code mainly validates the final architecture.

## Comparison to Related Methods
- Compared with [[Evolutionary Neural Architecture Search]]: replaces handcrafted crossover/mutation with LLM-guided operators.
- Compared with [[One-shot NAS]]: still leverages one-shot efficiency but adds LLM semantic prior for better candidate generation.
- Main advantage: better quality-cost tradeoff in search.
- Main tradeoff: dependency on LLM access and prompt quality.

## Evidence and Traceability
- Key figure(s): Fig. 1, Fig. 2, Fig. 4
- Key table(s): Tab. 1, Tab. 2, Tab. 4, Tab. 5
- Key equation(s): Eq. (1)-(7)
- Key algorithm(s): Algorithm 1 (search loop in Sec. 4.5)

## References
- arXiv: https://arxiv.org/abs/2501.13154
- HTML: https://arxiv.org/html/2501.13154v2
- Code: https://github.com/LLMENAS/LLMENAS
- Local implementation: D:/PRO/essays/code_depots/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance

