---
title: "MCTS-Learned Hierarchy"
type: method
source_paper: "Neural Architecture Search by Learning a Hierarchical Search Space"
source_note: "[[MCTS-Learned Hierarchy]]"
authors: [Anonymous authors]
year: 2025
venue: ICLR (under review)
tags: [nas-method, nas, mcts, search-space-design]
created: 2026-03-20
updated: 2026-03-20
---

# MCTS-Learned Hierarchy

## One-line Summary
> The method learns a hierarchy over architectures from output-space similarity, then runs tree-structured Boltzmann+UCT sampling to make MCTS in one-shot NAS more sample-efficient.

## Source
- Paper: Neural Architecture Search by Learning a Hierarchical Search Space (local PDF)
- HTML: Not provided in the source PDF
- Code: Not found in paper (anonymous ICLR submission)
- Paper note: [[MCTS-Learned Hierarchy]]

## Applicable Scenarios
- Problem type: Weight-sharing NAS with architecture sampling over large discrete spaces.
- Assumptions: Output-vector similarity from a partially trained supernet reflects semantic closeness between architectures.
- Data regime: Supervised image classification with train/validation split for reward estimation.
- Scale / constraints: Works best when pairwise distance construction is affordable (paper suggests around `<10k` candidates).
- Why it fits: Reorders early tree decisions to improve branch discriminability and reduce wasted exploration.

## Not a Good Fit When
- Search space is extremely large and `O(N^2)` distance/clustering is prohibitive.
- You cannot afford even short warm-up pretraining for supernet outputs.
- You require full code-level reproducibility from official implementation immediately.

## Inputs, Outputs, and Objective
- Inputs: Search space `S`, supernet `f`, train mini-batches `X_t`, validation mini-batches `X_v`.
- Outputs: Best architecture sampled from learned tree with `lambda=0` (no exploration at final selection).
- Objective: Improve architecture quality/ranking under limited compute by better conditional sampling.
- Core assumptions: Early tree branch quality controls downstream visit statistics and reward estimation quality.

## Method Breakdown
### Stage 1: Uniform pretraining for representation
- Train the supernet with uniform architecture sampling for `e_pt` epochs.
- Source: Algorithm 1 (pre-training block), Sec.4.

### Stage 2: Build learned hierarchy
- Run each architecture on validation batch, collect output vectors, compute pairwise distance matrix.
- Build binary tree using hierarchical agglomerative clustering.
- Source: Sec.4 Tree design, Algorithm 1 (build the search tree).

### Stage 3: Tree-based training with Boltzmann + UCT
- Sample root-to-leaf path using Boltzmann node sampling.
- Update supernet on training batch, evaluate validation accuracy, then backpropagate reward leaf-to-root.
- Source: Eq.(2), Eq.(3), Eq.(4), Algorithm 1.

### Stage 4: Final architecture extraction
- Sample candidate architectures from the learned tree with `lambda=0`, rank by validation performance.
- Source: Sec.4 Search and training; Sec.5 setup text.

## Pseudocode
```text
Algorithm: MCTS-Learned Hierarchy NAS
Input: Search space S, supernet f, training batches Xt, validation batches Xv
Output: Selected architecture a*

1. Pretrain supernet with uniform sampling over S for e_pt epochs.
   Source: Algorithm 1 (pre-training)
2. For each architecture ai in S, collect output oi=f_ai(Xv, w_p); build distance matrix D.
   Source: Sec.4 Tree design, Algorithm 1
3. Build binary hierarchy T via agglomerative clustering on D.
   Source: Sec.4 Tree design, Algorithm 1
4. During MCTS training, sample child nodes with Boltzmann probability p(ai).
   Source: Eq.(2)
5. Update node reward by R(ai)=C(ai)+lambda*sqrt(log(|parent|)/|ai|), and
   C(ai)=beta*C(ai)+(1-beta)*Acc(f_a(Xv,w)).
   Source: Eq.(3), Eq.(4)
6. After training, sample architectures with lambda=0 and pick the best by validation accuracy.
   Source: Sec.4 Search and training; Inference from source
```

## Training Pipeline
1. Uniform-sampling pretraining (`e_pt`).
2. Output-vector extraction on validation mini-batch for all candidate architectures.
3. Distance matrix + hierarchical clustering to form tree.
4. MCTS warm-up and main training with Boltzmann+UCT updates.

Sources:
- Sec.4, Eq.(2-4), Algorithm 1, Appendix B.1.

## Inference Pipeline
1. Disable exploration (`lambda=0`) in trained tree.
2. Sample `k` candidate architectures from the tree.
3. Evaluate/rank on validation set and select the best architecture.

Sources:
- Sec.4 Search and training; Algorithm 1 output description.

## Complexity and Efficiency
- Time complexity: `O(N)` inference for output extraction + `O(N^2)` for distance/clustering.
- Space complexity: Pairwise matrix storage is `O(N^2)`.
- Runtime characteristics: Best in relatively small-to-mid search spaces; still effective on constrained ImageNet budget search.
- Scaling notes: Paper reports practical fit around `<10k` candidates unless additional pruning/budgeting is used.

## Implementation Notes
- Sampling: Boltzmann on siblings with annealed temperature `T`.
- Reward: UCT-style exploration term + EMA-smoothed validation accuracy.
- Hyperparameters (reported): `beta=0.95`, `lambda=0.5`; with warm-up split roughly `40/25/35` for uniform/warm-up/MCTS in CIFAR10 experiments.
- Pretraining/search schedules differ by benchmark (Pooling, NAS-Bench-Macro, ImageNet).
- Code status: no official repo link in the source PDF.

## Comparison to Related Methods
- Compared with default-tree MCTS: improves branch quality by learning hierarchy from outputs, not fixed layer order.
- Compared with `MCTS + Reg.` (Su et al., 2021a): avoids explicit regularization while matching or improving results.
- Compared with flat Boltzmann/independent sampling: better architecture ranking due to conditional tree factorization.
- Main advantage: better sample efficiency from higher-quality early branching.
- Main tradeoff: extra pretraining + `O(N^2)` tree construction overhead.

## Evidence and Traceability
- Key figure(s): Fig.1 (factorization view), Fig.2 (tree structure), Fig.3 (branching quality).
- Key table(s): Table 1/2/3/4/5, Table 7 (appendix reward ablation).
- Key equation(s): Eq.(2), Eq.(3), Eq.(4).
- Key algorithm(s): Algorithm 1 (appendix).

## References
- arXiv: Not provided in source PDF
- HTML: Not provided in source PDF
- Code: Not found (anonymous submission)
- Local implementation: Not archived
