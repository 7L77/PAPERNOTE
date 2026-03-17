---
type: concept
aliases: [Pseudoinverse, MP Pseudoinverse]
---

# Moore-Penrose Pseudoinverse

## Intuition
When a matrix is not square or not invertible, we cannot use ordinary inverse. The Moore-Penrose pseudoinverse gives a principled "best possible inverse-like" operator for least-squares solutions.

## Why It Matters
Many model equations are overdetermined or underdetermined. Pseudoinverse is the standard tool to obtain minimum-norm or best-fit solutions.

## Tiny Example
If `U` is tall (`T > W`), equation `UW=X` usually has no exact solution. `U^+X` gives the `W` that best approximates `X` in least-squares sense.

## Definition
For matrix `U`, the Moore-Penrose pseudoinverse `U^+` is the unique matrix satisfying four Penrose conditions, and it generalizes matrix inverse to singular/non-square cases.

## Math Form (if needed)
Using SVD `U = V_1 \Sigma V_2^\top`, we define
\[
U^+ = V_2 \Sigma^+ V_1^\top
\]
where `\Sigma^+` inverts non-zero singular values.

## Key Points
1. Works for rectangular and singular matrices.
2. Produces minimum-norm solutions in underdetermined systems.
3. Produces least-squares solutions in overdetermined systems.

## How This Paper Uses It
- [[TF-MAS]]: computes `W_X/W_B/W_C` via pseudoinverse when `T<W` and as least-squares approximation when `T>W`.

## Representative Papers
- [[TF-MAS]]: applies pseudoinverse directly in proxy matrix estimation.

## Related Concepts
- [[Principal Component Analysis]]
- [[Rank Collapse]]
- [[Training-free NAS]]

