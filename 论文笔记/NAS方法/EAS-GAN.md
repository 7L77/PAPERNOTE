---
title: "EAS-GAN"
type: method
source_paper: "Evolutionary Architectural Search for Generative Adversarial Networks"
source_note: "[[EAS-GAN]]"
authors: [Qiuzhen Lin, Zhixiong Fang, Yi Chen, Kay Chen Tan, Yun Li]
year: 2022
venue: IEEE Transactions on Emerging Topics in Computational Intelligence
tags: [nas-method, gan, evolutionary-search, image-generation]
created: 2026-03-20
updated: 2026-03-20
---

# EAS-GAN

## One-line Summary

> EAS-GAN searches generator architectures for GANs by evolving differentiable supernets under a fixed discriminator, using multiple adversarial objectives as mutation operators and then retraining the best derived architecture from scratch.

## Source

- Paper: [Evolutionary Architectural Search for Generative Adversarial Networks](https://doi.org/10.1109/TETCI.2021.3137377)
- HTML: IEEE article page via DOI
- Code: No official repository found as of 2026-03-20
- Paper note: [[EAS-GAN]]

## Applicable Scenarios

- Problem type: Search a better generator architecture for unconditional image-generation GANs.
- Assumptions: A fixed discriminator family is acceptable, and generator quality can be compared through critic-based fitness plus external metrics such as [[Frechet Inception Distance]].
- Data regime: Unsupervised image generation on datasets such as CIFAR-10, STL-10, LSUN bedroom, with transfer tested qualitatively on CelebA.
- Scale / constraints: Practical for low- to medium-resolution image synthesis; the paper reports about 24 hours on one Tesla V100 for a `32x32` generator search.
- Why it fits: It combines weight-sharing NAS with E-GAN-style evolutionary mutation/selection, so it can search structure and optimize weights in the same run.

## Not a Good Fit When

- You need a jointly searched generator and discriminator rather than a fixed discriminator.
- You need a modern high-resolution GAN recipe with StyleGAN-like components and strong engineering support.
- You need a ready-to-run official codebase for reproduction.

## Inputs, Outputs, and Objective

- Inputs: Real images `x`, latent noise `z`, a cell-based generator search space, a fixed discriminator, and mutation objectives.
- Outputs: A discrete generator architecture, trained generator weights, and generated samples.
- Objective: Improve GAN sample quality and stability by evolving a generator supernet whose structure and weights co-adapt under adversarial training.
- Core assumptions: Different adversarial objectives expose different optimization behaviors, and evolutionary selection can keep the most promising generator variants.

## Method Breakdown

### Stage 1: Build a differentiable generator supernet

- Represent the generator as cells, where each cell is a DAG over candidate operations.
- Relax discrete operator choices into softmax-weighted architecture parameters `alpha`.
- Source: Sec. III-A, Fig. 2, Fig. 3.

### Stage 2: Update weights and architecture in bilevel style

- Alternate between updating network weights `omega` and architecture parameters `alpha`.
- Use a DARTS-like one-step approximation to avoid solving the full inner optimization exactly.
- Source: Sec. III-B, Eq. (4)-(6).

### Stage 3: Apply evolutionary mutation over supernets

- Treat each parent generator supernet as an individual.
- For each parent, apply multiple mutation objectives: minimax, least-squares, and hinge.
- After updating architecture and weights under each mutation, evaluate the offspring fitness.
- Source: Sec. III-C, Eq. (7)-(10), Algorithm 1.

### Stage 4: Select the fittest generators

- Rank offspring by a fitness that combines sample quality and a diversity-promoting term.
- Keep only the best `mu` supernets for the next generation.
- Source: Sec. III-C, Eq. (10), Algorithm 1.

### Stage 5: Derive a discrete architecture and retrain

- Extract the maximum-weight operator on each retained edge to form the final generator.
- Retrain the derived architecture from scratch with standard adversarial training.
- Source: Algorithm 2, Fig. 1.

## Pseudocode

```text
Algorithm: EAS-GAN
Input: Real-image dataset D, latent prior p(z), parent count mu, mutation count n_m
Output: Final discrete generator architecture G*

1. Build a generator supernet from DAG-based cells with candidate operators on each edge.
   Source: Sec. III-A, Fig. 2, Fig. 3
2. Initialize generator weights omega, architecture parameters alpha, and a fixed discriminator D.
   Source: Sec. III-B
3. Repeat for each training iteration:
   3.1 Update discriminator D for n_D steps using real images and samples from current parents.
       Source: Algorithm 1, lines 2-5
   3.2 For each parent supernet j and each mutation objective M_h:
       a. Sample noise z and update architecture parameters alpha_j under mutation M_h.
          Source: Algorithm 1, lines 8-9; Sec. III-B
       b. Update generator weights omega_j under the same mutation.
          Source: Algorithm 1, line 10
       c. Compute offspring fitness F_{j,h}.
          Source: Algorithm 1, line 11; Eq. (10)
   3.3 Select the top-mu supernets by descending fitness.
       Source: Algorithm 1, line 14
4. Extract the highest-weight operation on each selected edge to form a discrete generator architecture.
   Source: Algorithm 2, line 2
5. Retrain the derived generator from scratch with adversarial training against D.
   Source: Algorithm 2, lines 3-10
```

## Training Pipeline

1. Define the generator search space with DAG cells and operator candidates.
2. Initialize a population of generator supernets.
3. Update the discriminator using real images and samples from the current population.
4. For each parent, generate multiple offspring by switching mutation objectives and updating `alpha` and `omega`.
5. Score offspring with the quality-plus-diversity fitness and keep the best parents.
6. After evolution, discretize the best supernet.
7. Retrain the discretized generator in a conventional GAN loop.

Sources:

- Sec. III-A to III-C.
- Algorithm 1 and Algorithm 2.

## Inference Pipeline

1. Sample latent noise `z ~ p(z)`.
2. Feed `z` through the final retrained generator `G*`.
3. Output generated images for sampling, interpolation, or visual inspection.

Sources:

- Algorithm 2.
- Inference from source: the paper focuses on training and evaluation, not deployment APIs.

## Complexity and Efficiency

- Time complexity: Not reported in closed form.
- Space complexity: Not reported in closed form.
- Runtime characteristics: Searching one `32x32` generator architecture takes about 24 hours on one Nvidia Tesla V100 GPU.
- Scaling notes: The method is demonstrated on `32x32`, `48x48`, and `64x64` settings; the paper does not establish scalability to modern high-resolution GAN regimes.

## Implementation Notes

- Search-space upsampling candidates: transposed convolution `3x3`, nearest-neighbor interpolation, bilinear interpolation.
- Other operator candidates: `1x1`, `3x3`, `5x5`, dilated `3x3`, dilated `5x5`, skip-connect, zero.
- Activation choice: ReLU for convolution and transposed convolution operators.
- Discriminator: fixed DCGAN-style architecture with batch normalization.
- Search optimizer: Adam with `beta1=0.5`, `beta2=0.9`, `lr=0.004`.
- Evolution settings: `mu=1`, three mutation objectives, `gamma=0.01`.
- Evaluation protocol: 50000 generated samples for IS / FID computation.
- Final retraining: hinge loss with Adam `lr=0.0002`.
- Practical gotcha: because no official code was located, reproduction requires re-implementing the supernet, mutation loop, and fitness computation from the paper text.

## Comparison to Related Methods

- Compared with [[Generative Adversarial Network]] baselines such as WGAN-GP: EAS-GAN changes architecture search rather than only loss or regularization.
- Compared with E-GAN: EAS-GAN evolves both architecture parameters and weights instead of keeping a fixed generator architecture.
- Compared with AutoGAN / AGAN: EAS-GAN avoids an RL controller and instead uses a differentiable supernet plus evolutionary selection.
- Main advantage: It unifies supernet-based architecture search with mutation-based GAN stabilization in one training loop.
- Main tradeoff: The search space and evaluation setting are narrower than modern GAN practice, and the discriminator is not searched.

## Evidence and Traceability

- Key figure(s): Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 9, Fig. 10.
- Key table(s): Table I, Table II.
- Key equation(s): Eq. (1), Eq. (4)-(10).
- Key algorithm(s): Algorithm 1, Algorithm 2.

## References

- DOI: https://doi.org/10.1109/TETCI.2021.3137377
- HTML: IEEE article page via DOI
- Code: No official repository found as of 2026-03-20
- Local implementation: Not archived

