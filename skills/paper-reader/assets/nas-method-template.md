---
title: "{MethodName}"
type: method
source_paper: "{PaperTitle}"
source_note: "[[{PaperNoteName}]]"
authors: [{Authors}]
year: {Year}
venue: {Venue}
tags: [nas-method, {tag1}, {tag2}]
created: {Date}
updated: {Date}
---

<!-- Canonical house style: mirror D:/Project/paper/论文笔记/NAS方法/DeCoST.md -->

# {MethodName}

## One-line Summary

> {One sentence that states the problem, the core idea, and the main structural choice.}

## Source

- Paper: [{PaperTitle}]({ArxivUrl})
- HTML: {ArxivHtmlUrl}
- Code: {CodeUrl}
- Paper note: [[{PaperNoteName}]]

## Applicable Scenarios

- Problem type: {What optimization / prediction / planning problem this method targets}
- Assumptions: {Key assumptions needed by the method}
- Data regime: {Offline / online / synthetic / supervised / RL / mixed}
- Scale / constraints: {Typical node count, sequence length, memory/runtime constraints}
- Why it fits: {Short rationale tied to the method structure, not a generic compliment}

## Not a Good Fit When

- {Scenario 1}
- {Scenario 2}
- {Scenario 3}

## Inputs, Outputs, and Objective

- Inputs: {Structured inputs}
- Outputs: {Structured outputs}
- Objective: {Optimization or learning objective}
- Core assumptions: {Assumptions that must hold for the method to work as described}

## Method Breakdown

### Stage 1: {StageName}

- {What happens in this stage}
- Source: {Sec/Fig/Alg/Eq citations}

### Stage 2: {StageName}

- {What happens in this stage}
- Source: {Sec/Fig/Alg/Eq citations}

## Pseudocode

```text
Algorithm: {MethodName}
Input: {Inputs}
Output: {Outputs}

1. {Step 1}
   Source: {Sec/Fig/Alg/Eq}
2. {Step 2}
   Source: {Sec/Fig/Alg/Eq}
3. {Step 3}
   Source: {Sec/Fig/Alg/Eq}
4. {If a step is inferred rather than explicitly stated, mark it}
   Source: Inference from source
```

<!-- Keep the pseudocode aligned with the stage breakdown above. Use the paper's actual modules, state variables, and optimization steps when available. -->

## Training Pipeline

1. {Data generation / preprocessing}
2. {Model forward pass}
3. {Losses / supervision}
4. {Optimization details}

Sources:

- {Sec/Fig/Alg/Eq citations}

## Inference Pipeline

1. {Inference step 1}
2. {Inference step 2}
3. {Post-processing / optimization step}

Sources:

- {Sec/Fig/Alg/Eq citations}

## Complexity and Efficiency

- Time complexity: {If given}
- Space complexity: {If given}
- Runtime characteristics: {Reported wall-clock behavior / bottlenecks}
- Scaling notes: {How performance changes with problem size}

## Implementation Notes

- Architecture: {Encoder/decoder/backbone/modules}
- Hyperparameters: {Only the important ones}
- Constraints / masking: {Important feasibility logic}
- Optimization tricks: {Curriculum, reward shaping, loss balancing, search refinement, etc.}
- Failure modes / gotchas: {Practical issues}

## Comparison to Related Methods

- Compared with [[{Baseline1}]]: {Key difference}
- Compared with [[{Baseline2}]]: {Key difference}
- Main advantage: {Why this method matters}
- Main tradeoff: {What it gives up}

## Evidence and Traceability

- Key figure(s): {Figure references}
- Key table(s): {Table references}
- Key equation(s): {Equation references}
- Key algorithm(s): {Algorithm references}

## References

- arXiv: {ArxivUrl}
- HTML: {ArxivHtmlUrl}
- Code: {CodeUrl}
- Local implementation: {LocalCodePath or "Not archived"}
