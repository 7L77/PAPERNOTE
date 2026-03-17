---
title: "RZ-NAS: Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy"
method_name: "RZ-NAS"
authors: [Zipeng Ji, Guanghui Zhu, Chunfeng Yuan, Yihua Huang]
year: 2025
venue: ICML (PMLR 267)
tags: [NAS, LLM-guided-search, zero-cost-proxy, evolutionary-search, reflection]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy.pdf
local_code: D:/PRO/essays/code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy
created: 2026-03-17
---

# Paper Note: RZ-NAS

## TL;DR
> RZ-NAS inserts [[LLM-guided Search]] and [[LLM Reflection]] into [[Evolutionary Neural Architecture Search]] while using [[Zero-Cost Proxy]] as fitness, yielding stronger accuracy-cost tradeoffs across micro/macro NAS spaces.

## Metadata
| Item | Value |
|---|---|
| Paper | RZ-NAS: Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy |
| Venue | ICML 2025 (PMLR 267) |
| Code | https://github.com/PasaLab/RZ-NAS |
| Local PDF | `D:/PRO/essays/papers/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy.pdf` |
| Local Code | `D:/PRO/essays/code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy` |

## Problem Setup
- Goal: improve LLM-to-NAS quality and efficiency beyond small search spaces and high-cost train-and-eval loops.
- Challenge 1: pure text prompting is unstable and hard to interpret.
- Challenge 2: prior LLM-to-NAS often supports only small spaces or weak performance on standard NAS benchmarks.
- Challenge 3: training each candidate is expensive; they replace this with [[Zero-Cost Proxy]] scoring.

## Core Contributions
1. Reflective Zero-Cost strategy: combine LLM-driven mutation with proxy-based scoring.
2. Prompt design with both textual and code-level architecture/search-space descriptions.
3. Reflection feedback loop that uses score and exception information to guide next mutations.
4. Broad evaluation on NAS-Bench-201, DARTS, MobileNet search space, and COCO detection.

## Method

### Objective
Paper formulates search as:

\[
a^* = \arg\max_{a \in \mathcal{A}} \mathcal{O}(a, T, S, D, M)
\]

- `a`: architecture candidate.
- `O`: selected zero-cost proxy objective.
- Source: Sec. 3.1, Eq. (1).

### Pipeline (Fig. 1 + Alg. 1)
1. Initialize population `P = {F0}`.
2. Randomly select one architecture from `P`.
3. Ask LLM to mutate architecture under search-space and construction constraints.
4. Validate architecture (syntax/constraints/FLOPs budget).
5. Compute proxy score with code (not by LLM).
6. Insert into population and prune lowest-score model when pool is full.
7. Feed mutation result + score + exception to reflection module for next-step guidance.

Source: Sec. 3.2, Alg. 1, Fig. 1, Fig. 2.

### Prompt Structure (Fig. 2)
- System prompt: role + search-space semantics + network construction constraints + proxy details.
- In-context example: mutation example + reasoning trace.
- User prompt: JSON input with `arch`, `type`, `score`.
- Reflection instructions are embedded in system prompt and iterative feedback.

Source: Sec. 3.3, Fig. 2.

## Key Results

### Table 1 (Capability/Cost Summary)
- Reported CIFAR-10 search efficiency: **0.03 GPU days** for RZ-NAS, lower than most listed LLM-to-NAS baselines.
- Supports both micro and macro spaces, and zero-cost NAS setting.

### Table 2 (NAS-Bench-201)
- RZ-NAS improves each base proxy variant (GraSP/GradNorm/Synflow/Zen-NAS/ZiCo) versus original proxy baselines.
- Strong entries include Ours(ZiCo):
  - CIFAR-10 test: **94.24 +- 0.12**
  - CIFAR-100 test: **73.30 +- 0.21**
  - ImageNet-16-120 test: **46.24 +- 0.23**

### Table 3 (Proxy-Accuracy Correlation)
- Correlation metrics ([[Kendall's Tau]], [[Spearman's Rank Correlation]]) consistently improve after RZ-NAS guidance.
- Example: ZiCo on CIFAR-100, SPR from **0.81** to **0.84**.

### Table 4 (DARTS Space)
- RZ-NAS improves all tested proxy families in CIFAR-10/100 error.
- Example: Synflow error drops from **5.9** to **4.3** (CIFAR-10).

### Table 5 (MobileNet Space on ImageNet)
- At ~450M FLOPs, Ours(ZiCo) reaches **21.0%** top-1 error (79.0% top-1 accuracy in text).
- Reported much lower search cost than classic multi-shot approaches.

### Ablations (Fig. 3, Table 6/7, Appendix A.4)
- Removing in-context examples, reflection, code description, or textual description hurts performance.
- Appendix reports exception rate increase:
  - without in-context: ~2% -> 7%
  - without reflection: ~2% -> 5%
- Random selection for mutation target remains competitive vs highest-score-only selection.

## Implementation Cross-check with Archived Code

Repository inspected: `.../code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy` (commit `8d6b55e`).

Observed alignment:
- Has `evolution_search.py`, prompt template, and multiple zero-cost proxy implementations.
- Uses GPT-4o label and proxy calculators (GradNorm/Synflow/Zen/NASWOT etc.).

Observed mismatches / risks:
1. `generate_by_llm(structure_str)` currently does not interpolate `structure_str` into prompt text.
2. `prompt/template.txt` ends with an unfinished assistant JSON block and appears to rely on continuation completion.
3. Search defaults in code (`evolution_max_iter=4.8e5`, `population_size=512`) differ from paper experiment settings (1500 iterations, pop 100/256).
4. Reflection as an explicit external module in paper is not cleanly separated in code; implementation appears mostly prompt-level.

Interpretation: repo captures core idea but may need adaptation before exact paper-number reproduction.

## Strengths
1. Practical bridge between LLM prior and cheap zero-cost fitness.
2. Works across micro and macro spaces and extends beyond classification (COCO detection setting).
3. Good ablation coverage on prompt ingredients and selection strategy.

## Limitations
1. LLM API dependence and prompting sensitivity remain intrinsic.
2. Reported cost assumes API usage; reproducibility depends on model/version and prompt/runtime environment.
3. Open-source code and paper protocol are close but not one-to-one.

## Related Concepts
- [[LLM-guided Search]]
- [[LLM Reflection]]
- [[In-context Learning]]
- [[Zero-Cost Proxy]]
- [[Evolutionary Neural Architecture Search]]
- [[Cell-based Search Space]]
- [[NAS-Bench-201]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
