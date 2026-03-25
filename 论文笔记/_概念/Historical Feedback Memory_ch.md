---
type: concept
language: zh-CN
source_concept_note: "[[Historical Feedback Memory]]"
aliases: [历史反馈记忆, Bounded Feedback History]
---

# Historical Feedback Memory 中文条目

## 一句话直觉
Historical Feedback Memory 就是“最近几轮改了什么、为什么改、结果怎样”的小账本，用来指导下一轮迭代。

## 它为什么重要
迭代式 LLM 优化很容易重复踩坑。把最近失败与成功结构化保存，可以在不拉长上下文的前提下持续改进。

## 一个小例子
如果最近两轮都因为输出维度错误失败，下一轮提示会优先要求保持分类头维度正确，而不是继续激进改结构。

## 更正式的定义
它是一个固定长度的历史缓冲区，每一轮只保留最近 `K` 条改进记录，并将旧记录丢弃。

## 数学形式（如有必要）
\[
H_t^{(K)}=\{(s_{t-K},a_{t-K}), \ldots, (s_{t-1},a_{t-1})\}
\]
其中 `s_i` 为建议，`a_i` 为应用建议后的结果。

## 核心要点
1. 保持提示长度稳定，避免上下文爆炸。
2. 让失败信息也成为可学习信号。
3. 在资源受限场景下比无界历史更可控。

## 这篇论文里怎么用
- [[Iterative LLM-Based NAS with Feedback Memory]]: 设定 `K=5` 的滑动窗口，作为每轮改进建议的主要上下文。

## 代表工作
- [[Iterative LLM-Based NAS with Feedback Memory]]: 将历史窗口作为代码级 NAS 闭环的核心机制。

## 相关概念
- [[Diagnostic Triple]]
- [[LLM-guided Search]]
- [[Neural Architecture Search]]
