---
title: "VDAT"
type: method
source_paper: "Vulnerable Data-Aware Adversarial Training"
source_note: "[[VDAT]]"
authors: [Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: NeurIPS
tags: [nas-method, adversarial-training, data-filtering, robust-nas]
created: 2026-03-20
updated: 2026-03-20
---

# VDAT

## One-line Summary
> VDAT estimates per-sample vulnerability by margin shifts under attack, then probabilistically routes vulnerable samples to adversarial training for a better robustness-cost tradeoff.

## Source
- Paper: Vulnerable Data-Aware Adversarial Training
- PDF (local): `D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf`
- Code: https://github.com/fyqsama/VD-AT (currently inaccessible, 404 at archive time)
- Paper note: [[VDAT]]

## Applicable Scenarios
- Problem type: Robust model training where adversarial robustness is required but full PGD-AT cost is too high.
- Assumptions: Sample vulnerability can be approximated by margin gap between clean and attacked samples.
- Data regime: Supervised image classification with iterative adversarial training.
- Scale / constraints: Medium to large datasets where reducing adversarial subset size gives meaningful speedup.
- Why it fits: Keeps adversarial updates focused on high-risk samples instead of uniformly perturbing all samples.

## Not a Good Fit When
- You require deterministic, fixed data pipelines without stochastic filtering.
- The vulnerability estimate is unreliable (e.g., severe label noise or unstable logits early in training).
- The downstream task has no clear notion of class-logit margin.

## Inputs, Outputs, and Objective
- Inputs: Dataset \(X=\{(x_i,y_i)\}\), model \(f_\theta\), attack operator for pre-filter perturbation, interval \(T\), temperature \(\tau\).
- Outputs: Trained robust model parameters \(\theta^*\).
- Objective: Improve robustness and natural accuracy while reducing training cost via sample-wise adversarial allocation.
- Core assumptions: Vulnerable samples should receive stronger adversarial supervision than non-vulnerable samples.

## Method Breakdown
### Stage 1: Generate attack references
- Create adversarial variants \(x_i'\) for vulnerability estimation.
- Source: Sec. 4, Fig. 3.

### Stage 2: Compute vulnerability scores
- Use margin difference between clean and adversarial samples.
- Replace hard margin with soft margin for targeted-attack-aware estimation.
- Source: Sec. 4.1, Eq. (2)-(5).

### Stage 3: Convert vulnerability to routing probability
- Normalize vulnerabilities into \(P_\theta(x_i)\in[0,1]\).
- Source: Sec. 4.2, Eq. (6).

### Stage 4: Sample-wise filtering and mixed-loss training
- Route each sample to adversarial or natural branch by Bernoulli gate.
- Optimize \(L_{\text{nat}}+L_{\text{adv}}\).
- Source: Sec. 4.2, Eq. (7)-(8), Alg. 1.

### Stage 5: Periodic refresh
- Recompute vulnerabilities and routing every \(T\) epochs.
- Source: Alg. 1 (line 2-5), Sec. 4.2.

## Pseudocode
```text
Algorithm: VDAT
Input: dataset X={(x_i,y_i)}, model f_theta, epochs N, interval T, temperature tau
Output: trained model theta*

1. for epoch = 0..N:
   Source: Alg. 1
2.   if epoch mod T == 0:
       for each sample x_i:
         generate x_i' via attack used for vulnerability estimation
         Source: Fig. 3, Sec. 4
3.       compute soft margins S_theta^y(x_i), S_theta^y(x_i')
         V_theta(x_i) = -|S_theta^y(x_i)-S_theta^y(x_i')|
         Source: Eq. (3)-(5)
4.       normalize vulnerabilities to probability P_theta(x_i)
         Source: Eq. (6)
5.       sample r~Uniform(0,1):
         if r <= P_theta(x_i), place x_i into X_adv; else into X_nat
         Source: Eq. (7)
6.   compute L_train = L_nat(X_nat,theta) + L_adv(X_adv,theta)
     update theta
     Source: Eq. (8), Alg. 1
7. return theta*
```

## Training Pipeline
1. Set attack for vulnerability estimation (default FGSM in paper settings).
2. At refresh steps, compute vulnerability and split \(X_{\text{adv}}\), \(X_{\text{nat}}\).
3. Train with mixed natural/adversarial loss each epoch.
4. Evaluate robustness with FGSM/PGD/C&W/AA benchmarks.

Sources:
- Sec. 5.1, Eq. (6)-(8), Alg. 1, Tab. 1-3.

## Inference Pipeline
1. Use the final trained model directly for standard forward inference.
2. For robustness evaluation, run attack suites (PGD, C&W, AA) without filtering logic.

Sources:
- Sec. 5.1-5.2.

## Complexity and Efficiency
- Time complexity: \(O(nk)\) for vulnerability calculation + filtering per refresh cycle.
- Space complexity: Linear in batch/data buffers, plus adversarial sample cache when implemented.
- Runtime characteristics: Reduced wall-clock by adversarially training only a subset of samples.
- Scaling notes: Gains persist from CIFAR to ImageNet-1K in reported experiments.

## Implementation Notes
- Key hyperparameters: \(\tau=5\), refresh interval \(T=10\) (default in experiments).
- Filtering-interval tradeoff: smaller \(T\) usually improves robustness but increases cost.
- Perturbation choice for vulnerability estimation: FGSM is default for cost-effectiveness.
- Framework flexibility: paper validates integration into TRADES and AWP.
- Code status: official link listed by authors is currently not downloadable (404), so this note is paper-derived.

## Comparison to Related Methods
- Compared with batch-wise filtering FAT (e.g., DFEAT/AdvGradMatch): VDAT operates at sample granularity.
- Compared with pure fast example-generation FAT: VDAT explicitly optimizes sample allocation.
- Main advantage: Better accuracy-cost tradeoff by targeted adversarial supervision.
- Main tradeoff: Adds periodic vulnerability estimation and stochastic routing.

## Evidence and Traceability
- Key figure(s): Fig. 1 (motivation), Fig. 2 (ImageNet tradeoff), Fig. 3 (pipeline), Fig. 4-5 (visualization).
- Key table(s): Tab. 1-4 (main), Tab. 5-10 (hyperparameter and ablation).
- Key equation(s): Eq. (1)-(8).
- Key algorithm(s): Alg. 1 (VDAT), Alg. 2 (robust NAS integration in appendix).

## References
- Local PDF: `D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf`
- Code: https://github.com/fyqsama/VD-AT
- Local implementation: Not archived (repository inaccessible at note time)

