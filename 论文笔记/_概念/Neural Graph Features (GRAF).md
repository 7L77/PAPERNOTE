---
type: concept
aliases: [GRAF, Neural Graph Features]
---

# Neural Graph Features (GRAF)

## Intuition
GRAF describes an architecture as a graph and extracts topology statistics (for example path-length constraints), instead of relying only on gradient-based proxy scores.

## Why It Matters
Pure zero-cost proxies can miss structural signals. Graph features add complementary information about connectivity patterns, which can improve architecture prediction.

## Tiny Example
Two cells may have similar `jacov` scores but very different path structures. GRAF can separate them using features such as minimum valid path length or allowed operations on paths.

## Definition
Neural Graph Features are handcrafted, topology-oriented descriptors computed from neural architecture graphs, used as additional features for architecture performance prediction.

## Key Points
1. Captures architecture topology explicitly.
2. Usually complements, rather than replaces, standard zero-cost proxies.
3. Can improve prediction when baseline proxy features are insufficient.

## How This Paper Uses It
- [[ZCP-Eval]]: Appends 191 GRAF dimensions to proxy vectors and reports improvements on many robustness-dataset settings (Table 6/7).

## Representative Papers
- Kadlecova et al. (2024): Introduces GRAF in NAS context.
- [[ZCP-Eval]]: Evaluates GRAF + ZCP fusion for robust prediction.

## Related Concepts
- [[Zero-Cost Proxy]]
- [[NAS-Bench-201]]
- [[Cell-based Search Space]]
