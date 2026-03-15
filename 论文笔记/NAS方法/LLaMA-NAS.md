---
title: "LLaMA-NAS"
type: method
source_paper: "LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models"
source_note: "[[LLaMA-NAS]]"
authors: [Anthony Sarah, Sharath Nittur Sridhar, Maciej Szankin, Sairam Sundaresan]
year: 2024
venue: arXiv
tags: [nas-method, llm, peft, lora, multi-objective]
created: 2026-03-14
updated: 2026-03-14
---

# LLaMA-NAS

## One-line Summary
> LLaMA-NAS trains a mixed-rank adapter super-network once, then uses NSGA-II to search Pareto-optimal adapter subnetworks that balance task score and parameter count.

## Source
- Paper: [LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models](https://arxiv.org/abs/2405.18377)
- HTML: https://arxiv.org/html/2405.18377v1
- Project: https://llama-nas.github.io/
- Code link from project page: https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning
- Paper note: [[LLaMA-NAS]]

## Applicable Scenarios
- Problem type: Adapter architecture selection for LLM fine-tuning under resource constraints.
- Assumptions: A one-shot super-network can represent candidate rank configurations.
- Data regime: Supervised instruction/task fine-tuning for downstream NLP tasks.
- Scale / constraints: Works when full-model fine-tuning is too costly and adapter budget is limited.
- Why it fits: It explicitly optimizes the accuracy/size tradeoff via Pareto search instead of fixed-rank heuristics.

## Not a Good Fit When
- You require a single closed-form rule for adapter rank without running any search.
- You need strict guarantees outside the searched adapter space.
- Your deployment objective is not well represented by performance + adapter parameter count.

## Inputs, Outputs, and Objective
- Inputs: Base LLM, task data, rank search space per layer, search budget.
- Outputs: A Pareto set of adapter subnetworks and selected deployment configuration(s).
- Objective: Jointly maximize task metric and minimize adapter parameters.
- Core assumptions: Mixed-rank adapters and weight sharing preserve enough signal for reliable search.

## Method Breakdown

### Stage 1: Build and train mixed-rank super-network
- Insert mixed-rank adapter choices into each layer and train under one-shot sharing.
- The trained super-network serves as a reusable substrate for many candidate subnetworks.
- Source: Sec. 3.1.

### Stage 2: Search Pareto-efficient subnetworks
- Define two objectives: task performance and parameter count.
- Run NSGA-II over architecture choices to discover non-dominated candidates.
- Source: Sec. 3.2.

### Stage 3: Select and evaluate candidate architectures
- Export subnetworks from the Pareto set and evaluate on target tasks.
- Compare with heuristic rank settings and PEFT baselines.
- Source: Sec. 4, Table 2-5.

## Pseudocode
```text
Algorithm: LLaMA-NAS
Input: Base LLM M, task dataset D, adapter search space A, search budget B
Output: Pareto set P of adapter architectures and selected deployment model

1. Construct a mixed-rank adapter super-network S(M, A).
   Source: Sec. 3.1
2. Train S on D with one-shot weight sharing.
   Source: Sec. 3.1
3. Initialize a population of adapter architectures from A.
   Source: Sec. 3.2
4. For each generation, evaluate architecture fitness:
   - Objective 1: task metric
   - Objective 2: adapter parameter count
   Source: Sec. 3.2
5. Apply NSGA-II selection/crossover/mutation to update population.
   Source: Sec. 3.2
6. Return non-dominated architectures as Pareto set P and pick a budget-feasible point.
   Source: Sec. 4, Table 2-5
```

## Training Pipeline
1. Prepare task datasets (commonsense and math in the paper).
2. Train adapter super-network on top of base LLM (7B/13B and later additional models).
3. Run evolutionary multi-objective search on the trained super-network.
4. Evaluate selected subnetworks against LoRA/QLoRA/AdaLoRA/LoNAS baselines.

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4
- Table 2-5

## Inference Pipeline
1. Choose one architecture from the Pareto set under deployment budget.
2. Export corresponding adapter subnetwork.
3. Run task inference with the chosen base model + searched adapter.

Sources:
- Sec. 4
- Inference from source (serving stack details are not separately formalized)

## Complexity and Efficiency
- Time complexity: Not reported analytically.
- Space complexity: Not reported analytically.
- Runtime characteristics: One-shot training amortizes cost across many candidate adapter structures.
- Scaling notes: NSGA-II generally outperforms heuristic rank assignment on the reported tasks (Table 2), but tradeoffs remain task dependent.

## Implementation Notes
- Paper implementation idea is clear: mixed-rank adapter super-network + NSGA-II.
- Project page points to an IntelLabs umbrella repository.
- As checked on 2026-03-14, the archived repo does not expose a clearly named `LLaMA-NAS` subproject path.
- Practical implication: method note is primarily paper-derived; code link is preserved as the official project-page endpoint.

## Comparison to Related Methods
- Compared with [[Low-Rank Adapter]] (LoRA): LLaMA-NAS searches layer-wise rank configuration instead of fixed manual rank.
- Compared with [[Parameter-Efficient Fine-Tuning]] heuristics: it optimizes a Pareto frontier rather than a single hand-crafted budget point.
- Main advantage: Better quality/size tradeoff with explicit multi-objective control.
- Main tradeoff: Requires search procedure and budget; reproducibility depends on implementation availability.

## Evidence and Traceability
- Key figure(s): Fig. 1-3 (pipeline and search-space behavior).
- Key table(s): Table 2-5.
- Key equation(s): Multi-objective optimization formulation in method description.
- Key algorithm(s): NSGA-II-based architecture search (Sec. 3.2).

## References
- arXiv: https://arxiv.org/abs/2405.18377
- HTML: https://arxiv.org/html/2405.18377v1
- Project: https://llama-nas.github.io/
- Code: https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning
- Local implementation: D:/PRO/essays/code_depots/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models
