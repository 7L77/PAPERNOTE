---
title: "UP-NAS: Unified Proxy for Neural Architecture Search"
method_name: "UP-NAS"
authors: [Yi-Cheng Huang, Wei-Hua Li, Chih-Han Tsou, Jun-Cheng Chen, Chu-Song Chen]
year: 2024
venue: "CVPR Workshops"
tags: [nas, training-free-nas, zero-cost-proxy, predictor-based-nas, gradient-ascent]
zotero_collection: ""
image_source: online
arxiv_html: ""
project_page: "https://github.com/AI-Application-and-Integration-Lab/UP-NAS"
local_pdf: D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search
created: 2026-03-20
---

# Paper Note: UP-NAS

## Meta
| Item | Content |
|---|---|
| Paper | UP-NAS: Unified Proxy for Neural Architecture Search |
| Venue | CVPR Workshops 2024 |
| Authors | Yi-Cheng Huang, Wei-Hua Li, Chih-Han Tsou, Jun-Cheng Chen, Chu-Song Chen |
| Code link in paper | https://github.com/AI-Application-and-Integration-Lab/UP-NAS |
| Local PDF | `D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf` |
| Local code | `D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search` |
| Archived code status | Local repo points to the official GitHub remote, but archived commit `2601145` still only contains `README.md` and `LICENSE`; implementation is not public yet. |

## One-line Summary
> UP-NAS learns a [[Unified Proxy]] over multiple [[Zero-Cost Proxy]] signals, predicts those signals from a continuous [[Architecture Embedding]], and then performs gradient ascent in latent space to search architectures quickly.

## Core Contributions
1. Proposes a unified score `UP(A)=sum_i lambda_i f_i(A)` that combines 13 zero-cost proxies, with weights searched on a small benchmark subset using [[Tree-structured Parzen Estimator]] and [[Kendall's Tau]].
2. Introduces a Multi-Proxy Estimator (MPE): a pretrained architecture encoder plus a two-hidden-layer MLP that predicts the full proxy vector from architecture embeddings instead of recomputing all proxies at search time.
3. Uses gradient ascent directly in continuous architecture latent space, then decodes the optimized point back into a discrete architecture.
4. Shows competitive results on NAS-Bench-201 and strong DARTS/ImageNet search performance, including `23.5%` top-1 error on ImageNet with about `5 sec` search cost in the DARTS space.

## Problem Context
### Target problem
- Improve [[Training-free NAS]] when a single proxy is unreliable and repeatedly evaluating many proxies during search is still costly.

### Prior limitation
- Different zero-cost proxies work well on different tasks or search spaces, so single-proxy NAS is biased and unstable.
- Multi-proxy methods exist, but many either stay in discrete search loops or do not provide a smooth latent-space optimization path.
- Direct predictor-based NAS often needs true accuracy supervision, which is more expensive than proxy supervision.

### Why UP-NAS
- It amortizes proxy computation through a learned predictor.
- It consolidates proxy strengths through a single weighted score.
- It turns discrete architecture search into a smooth latent optimization problem via [[Variational Graph Autoencoder]]-style architecture encoding.

## Method Details
### 1) Unified Proxy objective
The paper defines a weighted sum over `M` proxies:

$$
UP(A)=\sum_{i=1}^{M}\lambda_i f^i_{zc}(A)
$$

- Source: Eq. (1), Sec. 3.1.
- `f^i_{zc}(A)` is the `i`-th zero-cost proxy score for architecture `A`.
- `lambda_i` is a learned combination weight.
- The paper searches these weights on NAS-Bench-201-CIFAR-10 and then reuses them across other spaces and datasets.

### 2) Architecture autoencoder and latent representation
- Architectures are cell DAGs encoded by an upper-triangular adjacency matrix `A` and one-hot operation matrix `X`.
- The encoder follows the `arch2vec` setup built on a [[Variational Graph Autoencoder]] with [[Graph Isomorphism Network]] encoders.
- The decoder reconstructs adjacency and operation matrices from latent node embeddings.

The autoencoder is trained by maximizing a variational lower bound:

$$
\mathcal{L}
=
\mathbb{E}_{q(Z|\mu,\sigma^2)}[\log p(\hat X,\hat A|Z)]
-D_{KL}(q(Z|\mu,\sigma^2)\|p(Z))
$$

- Source: Eq. (2), Sec. 3.2.
- Practical role: this makes each discrete architecture mappable to a continuous [[Architecture Embedding]] that can be optimized by gradients.

### 3) Multi-Proxy Estimator (MPE)
MPE takes an architecture embedding and predicts all proxy scores at once.

- Structure: pretrained architecture encoder + two-hidden-layer MLP.
- Each hidden layer uses linear + batch norm + ReLU.
- Training target: regress the full proxy vector, not final accuracy.

The MPE loss is mean-squared error over the proxy vector:

$$
\mathcal{L}_{MPE}(W)=\|s\|^2,
\quad
s=f_{MPE}(A;W)-[f^1_{zc}(A),\dots,f^M_{zc}(A)]
$$

- Source: Eq. (3)-(4), Sec. 3.3.
- Key implication: UP-NAS avoids re-running all proxies during each search step once MPE is trained.

### 4) Gradient-ascent search in latent space
After fixing the MPE weights `W` and proxy weights `lambda`, the paper optimizes latent vector `Z` with:

$$
F(Z)=\sum_{i=1}^{M}\lambda_i f_{MLP}(Z;W)_i
$$

and updates

$$
Z^{t+1}=Z^t+\eta \nabla_Z F(Z)
$$

- Source: Eq. (5)-(6), Sec. 3.4.
- Search procedure:
  1. sample an architecture from the search space,
  2. encode it to latent space,
  3. do gradient ascent through frozen MPE,
  4. decode the optimized latent back to a discrete architecture.

### 5) Proxy set and weight settings
The paper uses 13 proxies:

- `snip`, `flops`, `params`, `l2-norm`, `grasp`, `gradnorm`, `synflow`, `jacov`, `EPENAS`, `Zen`, `fisher`, `plain`, `Nwot`.

It reports four weighting modes:

1. `UPsum`: equal weight on all 13 proxies.
2. `UPsum-`: equal weight, but excludes `grasp` because it is much slower.
3. `UPweighted`: real-valued weights learned by TPE.
4. `UPselected`: binarized version of learned weights.

Important table-level takeaways from Table 1:

- Positive high weights in `UPweighted` go to `jacov (1.000)`, `synflow (0.840)`, `flops (0.609)`, `grasp (0.441)`, `Zen (0.416)`.
- Negative weights go to `params (-0.587)`, `fisher (-0.342)`, `snip (-0.164)`, `l2 norm (-0.100)`.
- `UPselected` keeps only `flops`, `synflow`, `jacov`, and `Nwot`.
- `grasp` costs about `10 sec` per DARTS architecture, while the other 12 proxies are about `1 sec` each, which motivates learning MPE.

## Important Figures
### Figure 1
- High-level picture of MPE + Unified Proxy.
- Message: proxy fusion is not just averaging scores; it is mediated by a learned estimator operating on architecture representations.

### Figure 2
- End-to-end UP-NAS pipeline.
- Training phase: architecture encoder + MLP predicts proxy vector.
- Search phase: frozen predictor guides latent-space gradient ascent.

### Figure 3
- Architecture autoencoder.
- Important because the whole method depends on discrete architectures being decoded from optimized latent vectors.

### Figure 4 / Figure 5
- DARTS cells found by `UPselected` and `UPweighted`.
- `UPselected` yields the stronger ImageNet result (`23.5%` error), while `UPweighted` gives a slightly smaller model but worse accuracy (`24.5%` error).

## Key Experimental Evidence
### Table 2: Rank correlation on NAS-Bench-201-CIFAR-10
- Best original single proxy is `Nwot` with Kendall's tau `0.574`.
- Predicted proxy scores from MPE are usually close to original proxy correlations, showing that MPE does not destroy ranking signal.
- Unified scores are stronger:
  - `UPsum`: `0.58` original, `0.50` predicted
  - `UPweighted`: `0.71` original, `0.66` predicted
  - `UPselected`: `0.68` original, `0.59` predicted

### Table 3 / Table 4: NAS-Bench-201 search
- All UP variants return the same searched architecture in NAS-Bench-201.
- Test accuracy:
  - CIFAR-10: `94.18`
  - CIFAR-100: `71.59`
  - ImageNet-16-120: `47.16`
- Upper bound of the benchmark:
  - CIFAR-10: `94.37`
  - CIFAR-100: `73.51`
  - ImageNet-16-120: `47.31`

### Table 5: DARTS space searched on CIFAR-10, evaluated on ImageNet
- `UPselected`: `23.5%` top-1 error, `6.5M` params, about `5 sec` search cost.
- `UPweighted`: `24.5%` top-1 error, `5.7M` params, about `5 sec` search cost.
- This beats listed training-free baselines such as TE-NAS (`24.5%`) and Zero-Cost-PT (`24.4%`), and is competitive with or better than several non-training-free methods.

### Table 6: Search-method ablation on DARTS/CIFAR-10
- `Gradient Ascentweighted`: `2.44%` CIFAR-10 error.
- `Evolutionaryweighted`: `2.75%`.
- `Randomweighted`: `2.88%`.

### Table 7: MLP ablation
- One, two, and three hidden layers are compared.
- Two hidden layers give the best validation accuracy and become the default MPE choice in the paper.

## Implementation Details Worth Reproducing
1. Search spaces:
   - NAS-Bench-201 latent dimension: `128`
   - DARTS latent dimension: `352`
2. NAS-Bench-201 MPE training:
   - uses `50%` of architectures,
   - Adam,
   - batch size `16`,
   - `70` epochs.
3. DARTS MPE training:
   - uses `10,000` sampled architectures,
   - Adam,
   - batch size `64`,
   - `50` epochs.
4. MPE training on both NAS-Bench-201 and DARTS reportedly takes less than `2 minutes`.
5. Search starts from a random architecture, encodes it, and runs Adam-based latent optimization until the decoded architecture becomes invalid.

Note:
- The PDF text extraction in a few places garbles exponent formatting for learning rates, so if exact learning-rate exponents matter for reimplementation, the original PDF should be checked visually.
- The archived official repo currently does not expose code, so these details are paper-derived rather than code-verified.

## Critical View
### Strengths
1. Cleanly separates expensive proxy computation from fast search-time optimization.
2. Uses a practical latent-space search strategy rather than enumerating or mutating architectures blindly.
3. Gives an interpretable proxy-combination view: which proxies help, which hurt, and how much.

### Limitations
1. Proxy weights are learned on NAS-Bench-201-CIFAR-10 and then transferred; the paper argues this generalizes, but that transfer assumption is still strong.
2. The unified score is a linear combination, so higher-order interactions among proxies are not modeled.
3. MPE predicts proxies, not final accuracy, so the method inherits whatever mismatch exists between proxy quality and real performance.
4. Official implementation is still unavailable in the archived repository, which weakens reproducibility.

### Follow-up Ideas
1. Replace the fixed global weight vector with input-conditional proxy fusion.
2. Study whether weight transfer still holds outside CNN cell-based spaces, especially for transformer NAS.
3. Compare against later proxy-fusion methods like [[PO-NAS]] to separate the value of proxy fusion from the value of latent gradient search.

## Related Concepts
- [[Unified Proxy]]
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Architecture Embedding]]
- [[Variational Graph Autoencoder]]
- [[Graph Isomorphism Network]]
- [[Tree-structured Parzen Estimator]]
- [[Kendall's Tau]]
- [[NAS-Bench-201]]
