---
type: concept
language: zh-CN
aliases: [Text Gradient_ch]
---

# Textual Gradient

## Intuition

当系统某部分不可微时，可以不传数值梯度，而是让 LLM 用文字说明“该怎么改”。这种自然语言形式的更新信号就是 textual gradient。

## Why It Matters

agent 系统里的 prompt、tool 调用和图结构很难直接做反向传播；textual gradient 给了一个实用替代方案。

## Tiny Example

如果某个 debate operator 很不稳定，textual gradient 可能建议“降低 temperature”或“在投票前加入更严格的 critique prompt”。

## Definition

Textual gradient 是基于任务反馈生成的自然语言更新建议，用来指导 prompt、temperature 或 operator 结构的修改。

## Math Form (if needed)

MaAS 把 operator 侧更新写为 `dL/dO = T_P union T_T union T_N`，分别对应 prompt、temperature 和节点结构更新。

## Key Points

1. 它是“文字形式的优化信号”，不是普通数值梯度。
2. 它适合处理 agent 系统中不可微的组件。
3. 它与路由分布上的数值梯度形成互补。

## How This Paper Uses It

- [[MaAS]]: 用 textual gradient 更新 prompt、温度和 operator 节点结构。

## Representative Papers

- [[MaAS]]: 把 textual gradient 系统性接入 workflow search。

## Related Concepts

- [[Agentic Supernet]]
- [[Agentic Operator]]
- [[Early Exit]]

