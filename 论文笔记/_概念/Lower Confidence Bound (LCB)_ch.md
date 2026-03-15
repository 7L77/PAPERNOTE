---
type: concept
language: zh-CN
source_concept_note: "[[Lower Confidence Bound (LCB)]]"
aliases: [下置信界, LCB]
---

# Lower Confidence Bound (LCB) 中文条目

## 一句话直觉
LCB 是“保守分数”：历史均值 - 不确定性项，不确定性越大，LCB 越低。

## 它为什么重要
在“先公平试、再淘汰”的流程里，LCB 能避免因为早期样本不足而误杀潜在好操作。

## 一个小例子
某操作当前均值一般但样本很少，LCB 会比较低，从而被再次采样验证，而不是立即被剪枝。

## 更正式的定义
常见形式：
\[
\hat{r}_k - \sqrt{\frac{2\log N}{n_k}}
\]
其中符号含义与 UCB 一致。

## 数学形式（如有必要）
LCB 与 UCB 互补：UCB 偏乐观选择，LCB 可用于保守评估或公平采样控制。

## 核心要点
1. 强调“下界”而不是“上界”。
2. 适合做谨慎决策前的补采样。
3. 常与 UCB 组合使用。

## 这篇论文里怎么用
- [[ABanditNAS]]: 先用 `softmax(-LCB)` 采样操作，再用 UCB 执行淘汰。

## 代表工作
- 置信界 bandit 系列方法。
- ABanditNAS（2020）中的 anti-bandit 采样设计。

## 相关概念
- [[Multi-Armed Bandit]]
- [[Upper Confidence Bound (UCB)]]
- [[ABanditNAS]]

