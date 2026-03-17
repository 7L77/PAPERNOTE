---
title: "RZ-NAS"
type: method
source_paper: "RZ-NAS: Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy"
source_note: "[[RZ-NAS]]"
authors: [Zipeng Ji, Guanghui Zhu, Chunfeng Yuan, Yihua Huang]
year: 2025
venue: ICML (PMLR 267)
tags: [nas-method, llm-guided-search, zero-cost-proxy, evolutionary-search, reflection]
created: 2026-03-17
updated: 2026-03-17
---

# RZ-NAS

## One-line Summary
> RZ-NAS uses an LLM as a mutation policy inside evolutionary NAS and scores candidates with zero-cost proxies, while adding reflective feedback to improve next-step mutation quality.

## Source
- Paper: [RZ-NAS: Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy](D:/PRO/essays/papers/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy.pdf)
- HTML: Not reported in paper (ICML proceedings paper)
- Code: https://github.com/PasaLab/RZ-NAS
- Paper note: [[RZ-NAS]]

## Applicable Scenarios
- Problem type: Neural architecture search under limited compute budget.
- Assumptions: Zero-cost proxy ranking is informative enough to guide search.
- Data regime: Image classification benchmarks (CIFAR-10/100, ImageNet-16-120; and ImageNet macro search) plus COCO detection transfer.
- Scale / constraints: Works on both micro cell-based and macro MobileNet-like spaces.
- Why it fits: It replaces expensive candidate training in search loop with cheap proxy scoring and LLM-guided mutation.

## Not a Good Fit When
- You need deterministic search behavior with minimal external service variance.
- Your search space cannot be safely constrained by text+code prompt rules.
- Proxy-target correlation is weak for your domain, making zero-cost guidance unreliable.

## Inputs, Outputs, and Objective
- Inputs: task `T`, dataset `D`, search space `S`, model family `M`, proxy type, iteration/population budgets.
- Outputs: architecture with highest proxy score in population.
- Objective: maximize proxy objective over architecture space.
- Core assumptions: Higher proxy score is a useful surrogate for final performance; reflection text can improve mutation policy over iterations.

## Method Breakdown

### Stage 1: Population Initialization and Candidate Selection
- Start from initial architecture and maintain population `P`.
- Select one candidate each iteration (random selection in reported setup).
- Source: Sec. 3.2; Algorithm 1 lines 1-4; Sec. 4.2.2.

### Stage 2: LLM-guided Mutation with Structured Prompt
- Build prompt with search-space description, network construction code/text, proxy code/text, and in-context example.
- Ask LLM to produce mutated architecture in JSON format.
- Source: Sec. 3.2-3.3; Fig. 2.

### Stage 3: Validation and Zero-Cost Evaluation
- Check architecture validity and budget constraints.
- Compute proxy score by executable code (not by LLM).
- Source: Sec. 3.2; Algorithm 1 lines 5-8; Fig. 1.

### Stage 4: Reflection and Population Update
- Use architecture before/after mutation, score, and exceptions to produce reflection hints.
- Insert candidate, prune worst-score member when pool exceeds size.
- Source: Sec. 3.2; Algorithm 1 lines 9-16; Appendix A.2.

## Pseudocode
```text
Algorithm: RZ-NAS
Input: Search space S, dataset D, proxy zc, budget B, iterations T, population size N, init architecture F0
Output: Best architecture F*

1. Initialize P = {F0}. Source: Alg. 1 line 1
2. For t = 1..T, randomly pick Ft from P. Source: Alg. 1 lines 2-3
3. Generate mutated architecture F't via LLM prompt with text+code context. Source: Sec. 3.2-3.3, Fig. 2
4. Validate F't under architecture and budget constraints. Source: Alg. 1 lines 5-7
5. Compute z = zc(F't) by proxy code, append F't into P. Source: Alg. 1 lines 7-8; Sec. 3.2
6. If |P| > N, remove architecture with smallest proxy score. Source: Alg. 1 lines 9-10
7. Build reflection from (Ft, F't, z, exception) for next mutations. Source: Alg. 1 line 15; Sec. 3.2; Appendix A.2
8. Return highest-score architecture in P. Source: Alg. 1 line 17
```

## Training Pipeline
1. Search phase:
   run iterative mutation+proxy loop for each proxy/search-space setting.
2. Architecture pick:
   keep best proxy-score candidate.
3. Final evaluation:
   train/evaluate selected architecture under benchmark-specific settings.

Sources:
- Sec. 4 (Experiment settings and performance evaluation)

## Inference Pipeline
1. Instantiate the searched architecture in downstream task model.
2. Run standard task inference/evaluation (classification or detection heads).
3. Compare accuracy/mAP under same FLOPs budget.

Sources:
- Sec. 4.1.3, Sec. 4.3, Fig. 4, Table 5.

## Complexity and Efficiency
- Time complexity: Not provided in closed-form.
- Space complexity: Not provided in closed-form.
- Runtime characteristics: Reported low search cost (e.g., 0.03 GPU days on CIFAR-10 in Table 1; per-proxy API cost about $75 in Sec. 4).
- Scaling notes: Demonstrated on micro and macro spaces with similar loop structure.

## Implementation Notes
- Local code path: `D:/PRO/essays/code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy`.
- Entry script: `evolution_search.py` with selectable proxy (`--zero_shot_score`) and search-space module (`--search_space`).
- Prompt file: `prompt/template.txt` includes role, operation descriptions, network constraints, proxy code, and in-context example.
- Code-level caveat 1: `generate_by_llm(structure_str)` does not currently inject `structure_str` into prompt content.
- Code-level caveat 2: prompt template terminates with an unfinished assistant JSON block, implying completion-style continuation.
- Code-level caveat 3: default iteration/population in code differ from paper's reported settings.
- Paper-code mismatch note: reflective design is strong in paper text, but external reflection module boundaries are less explicit in current code.

## Comparison to Related Methods
- Compared with [[GENIUS]]: RZ-NAS emphasizes text+code prompt grounding and reflection-guided mutation loop.
- Compared with [[EvoPrompting]]: broader search-space support and lower reported search cost on listed benchmarks.
- Main advantage: better proxy-guided search quality without full candidate training.
- Main tradeoff: dependence on LLM behavior and prompt/system implementation details.

## Evidence and Traceability
- Key figure(s): Fig. 1 (pipeline), Fig. 2 (prompt design), Fig. 3 (ablation), Fig. 4 (detection transfer).
- Key table(s): Table 1-7; Appendix Table 9-10.
- Key equation(s): Eq. (1) objective; Appendix Eq. (2)-(7) proxy formulas.
- Key algorithm(s): Algorithm 1.

## References
- arXiv: Not reported in extracted paper text
- HTML: Not reported in extracted paper text
- Code: https://github.com/PasaLab/RZ-NAS
- Local implementation: D:/PRO/essays/code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy
