---
title: "DeepFedNAS"
type: method
source_paper: "Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training"
source_note: "[[DeepFedNAS]]"
authors: [Bostan Khan, Masoud Daneshtalab]
year: 2026
venue: arXiv
tags: [nas-method, federated-nas, predictor-free-search, hardware-aware]
created: 2026-03-23
updated: 2026-03-23
---

# DeepFedNAS

## One-line Summary

> DeepFedNAS replaces random federated supernet sampling with Pareto-guided curriculum training, then performs deployment-time subnet search by directly optimizing a structural fitness proxy instead of training an expensive accuracy predictor.

## Source

- Paper: [Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training](https://arxiv.org/abs/2601.15127)
- HTML: https://arxiv.org/html/2601.15127v2
- Code: https://github.com/bostankhan6/DeepFedNAS
- Paper note: [[DeepFedNAS]]
- Local code: `D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training`

## Applicable Scenarios

- Problem type: Federated NAS where one supernet must support many client/device targets.
- Assumptions: Structural fitness can become a reliable proxy for subnet accuracy after guided supernet training.
- Data regime: Federated non-IID image classification (CIFAR-10/100, CINIC-10 in paper).
- Scale / constraints: Multi-client training with communication constraints and deployment-side MAC/Params/Latency limits.
- Why it fits: It minimizes post-training search overhead while keeping hardware-aware flexibility.

## Not a Good Fit When

- You need transformer-only or non-CNN search spaces that have not been adapted to this framework.
- You cannot afford any offline cache-generation phase before federated training.
- Your supernet cannot preserve strong fitness-accuracy rank correlation after training.

## Inputs, Outputs, and Objective

- Inputs: Supernet search space \(S\), federated client datasets \(\{D_k\}\), architecture genome \(A=(d,e,w)\), resource constraints.
- Outputs: Trained supernet \(W^\*\), and deployment subnet \(A^\*_{deploy}\) under hardware budgets.
- Objective: Improve supernet conditioning and search efficiency by maximizing unified fitness while respecting resource constraints.
- Core assumptions: A high-quality Pareto path curriculum leads to better shared weights, making \(F(A)\) predictive for deployment search.

## Method Breakdown

### Stage 1: Offline Pareto Cache Generation

- Build a multi-objective fitness \(F(A)\) with entropy, effectiveness, depth penalty, and channel monotonicity terms.
- Solve multiple constrained GA searches over MAC budgets to construct a Pareto path cache.
- Source: Sec. III-C, Sec. III-D, Eq. (5)-(10), Fig. 2.

### Stage 2: Federated Pareto Optimal Supernet Training

- Replace random sandwich sampling with cache-guided assignment:
  - boundary clients train smallest/largest cached subnets,
  - other clients sample from cache.
- Aggregate sparse updates with overlap-aware MaxNet masking.
- Source: Sec. III-E, Alg. 1, Eq. (2), Eq. (11).

### Stage 3: Predictor-Free Deployment Search

- Search subnets by directly maximizing \(F(A)\), replacing predictor-data generation and predictor training.
- Validate with reported fitness-accuracy correlation.
- Source: Sec. III-F, Eq. (12), Fig. 6, Table V.

### Stage 4: Hardware-aware Extension

- Add hard constraints for params and optional latency budget.
- Optionally use a lightweight LPM as soft latency penalty term.
- Source: Sec. III-G, Eq. (13)-(17).

## Pseudocode

```text
Algorithm: DeepFedNAS
Input: Search space S, federated clients K, rounds T, budget set B={B1...BN}, constraints C_hw
Output: Trained supernet W*, deployment subnet A*_deploy

1. For each budget Bi in B, run GA to solve:
   A*i = argmax_A F(A) s.t. MACs(A) <= Bi
   and form cache C = {A*1...A*N}
   Source: Sec. III-D, Eq. (10)

2. For each federated round t:
   2.1 Select participating clients Kt
       Source: Alg. 1
   2.2 Assign client subnet Ak via cache-guided rule:
       - least-trained boundary clients get A_min/A_max
       - others sample from C
       Source: Eq. (11), Alg. 1
   2.3 Clients train local subnet weights and upload updates
       Source: Alg. 1
   2.4 Server performs overlap-aware aggregation on shared parameters
       Source: Eq. (2), Alg. 1

3. After training, perform deployment search:
   A*_deploy = argmax_A F_deploy(A)
   subject to MAC/Params/Latency constraints
   Source: Sec. III-F/G, Eq. (12), Eq. (16)-(17)
```

## Training Pipeline

1. Define supernet config (`configs/supernets/4-stage-supernet-deepfednas.json`).
2. Generate cache (`scripts/cache_generation/run_subnet_cache_generation.sh`).
3. Train with `--subnet_dist_type TS_optimal_path` and cache path in `experiments/02_deepfednas/*.sh`.
4. Server sampler (`src/deepfednas/Server/base_server_model.py`) enforces boundary-plus-cache sampling.
5. Aggregation uses overlap-aware masking in federated supernet updates.

Sources:

- Sec. III-B to III-E, Alg. 1.
- Code: `scripts/cache_generation/run_subnet_cache_generation.sh`, `experiments/02_deepfednas/cifar10.sh`, `src/deepfednas/Server/base_server_model.py`.

## Inference Pipeline

1. Set deployment target constraints (MACs mandatory, params/latency optional).
2. Run GA search with fitness maximizer (`scripts/evaluation/find_subnet_for_macs.py`).
3. Optionally load LPM and add latency hard/soft constraints.
4. Return best architecture config and deploy subnet.

Sources:

- Sec. III-F/G, Eq. (12)-(17).
- Code: `scripts/evaluation/find_subnet_for_macs.py`, `src/deepfednas/nas/deepfednas_fitness_maximizer.py`.

## Complexity and Efficiency

- Time complexity: Dominated by federated supernet training + GA searches; post-training search is no longer dominated by predictor-data generation.
- Space complexity: Supernet parameters + cached architecture set + optional LPM.
- Runtime characteristics (reported):
  - cache generation: ~20 min for 60 subnets,
  - per-target search: ~20 sec,
  - total post-training pipeline: ~20.33 min vs baseline ~20.65 h.
- Scaling notes: Works better when frequent redeployment across budget targets is needed.

## Implementation Notes

- Fitness implementation is in `src/deepfednas/nas/deepfednas_fitness_maximizer.py`.
- Cache-guided sampler is in `src/deepfednas/Server/base_server_model.py` (`TS_optimal_path`).
- Deployment GA entry is `scripts/evaluation/find_subnet_for_macs.py`.
- Hyperparameter presets for training are in `experiments/02_deepfednas/*.sh`.
- Practical nuance from code:
  - cache is sorted by MACs and boundary subnets are taken from first/last rows;
  - middle clients sample randomly from cache (not deterministic traversal);
  - fitness combines entropy-related score, effectiveness, depth/channel penalties, plus optional latency term.

## Comparison to Related Methods

- Compared with [[SuperFedNAS]]: keeps supernet paradigm but replaces unguided random sampling with Pareto-guided curriculum.
- Compared with predictor-based post-search pipelines: removes expensive subnet-accuracy dataset generation for surrogate training.
- Main advantage: substantially lower deployment-search overhead with strong empirical accuracy.
- Main tradeoff: relies on calibrated fitness design and strong rank correlation after training.

## Evidence and Traceability

- Key figure(s): Fig. 1 (pipeline), Fig. 2 (cache quality), Fig. 3/4 (accuracy-efficiency tradeoff), Fig. 6 (fitness-accuracy correlation).
- Key table(s): Table II/III/IV (accuracy and robustness), Table V (search cost), Table VI (fitness ablation).
- Key equation(s): Eq. (2), Eq. (5)-(12), Eq. (16)-(17).
- Key algorithm(s): Algorithm 1 (federated Pareto-guided training).

## References

- arXiv: https://arxiv.org/abs/2601.15127
- HTML: https://arxiv.org/html/2601.15127v2
- Code: https://github.com/bostankhan6/DeepFedNAS
- Local implementation: D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training
