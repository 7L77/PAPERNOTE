---
type: concept
language: zh-CN
aliases: [Early Stop Operator_ch]
---

# Early Exit

## Intuition

不是每个 query 都值得走完整个推理深度。Early exit 允许系统在“已经够用”时提前停止。

## Why It Matters

如果没有 early exit，所有 query 都要支付最深工作流的成本，这会在简单样本上浪费大量 token 和 API 调用。

## Tiny Example

像“2 + 2”这样的简单问题不该触发多轮 debate、tool 调用和 self-refine；有了 early exit，系统可以在浅层就停下来。

## Definition

Early exit 是一种路由决策或 operator：当当前 workflow 已足够解决 query 时，终止更深层的采样与执行。

## Math Form (if needed)

在 MaAS 中，只要 controller 采样到 `O_exit`，后续层就不再继续，workflow 深度因此能随 query 改变。

## Key Points

1. 它让计算从固定深度变成自适应深度。
2. 它是 MaAS 节省推理成本的关键原因之一。
3. 当 query 难度差异很大时，它尤其重要。

## How This Paper Uses It

- [[MaAS]]: 在 supernet 中加入显式 early-exit operator，让简单 query 可以浅层结束。

## Representative Papers

- [[MaAS]]: 把 early exit 作为成本感知动态路由的核心部件。

## Related Concepts

- [[Agentic Supernet]]
- [[Agentic Operator]]
- [[Textual Gradient]]
