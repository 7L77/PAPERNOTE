---
type: concept
aliases: [Gabor Wavelet, Gabor Kernel]
---

# Gabor Filter

## Intuition
A Gabor filter is a localized sinusoidal pattern modulated by a Gaussian envelope, useful for orientation- and frequency-selective feature extraction.

## Why It Matters
It can capture robust edge/texture patterns and is often used as a handcrafted inductive bias in vision models.

## Tiny Example
A 3x3 Gabor-like filter tuned to horizontal orientation responds strongly to horizontal edges but weakly to vertical edges.

## Definition
A 2D Gabor filter can be written as a Gaussian envelope times a cosine wave in rotated coordinates, parameterized by orientation, wavelength, phase, and aspect ratio.

## Math Form (if needed)
Typical symbols include `sigma`, `gamma`, `lambda`, `psi`, `theta` controlling scale, aspect ratio, wavelength, phase, and rotation.

## Key Points
1. Orientation-selective and frequency-aware.
2. Acts as a structured feature extractor.
3. Can be fixed or learned in neural pipelines.

## How This Paper Uses It
- [[ABanditNAS]]: Adds 3x3 Gabor filter as one candidate operation in robust NAS search space.

## Representative Papers
- Dennis Gabor, communication theory papers (1946).
- Robust Gabor Networks and related adversarial-robust feature work.

## Related Concepts
- [[Denoising Block]]
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]

