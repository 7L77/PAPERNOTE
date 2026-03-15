---
type: concept
language: zh-CN
source_concept_note: "[[Lipschitz Constant]]"
aliases: [利普希茨常数, Lipschitz Constant]
---

# Lipschitz Constant 中文条目

## 一句话直觉
Lipschitz Constant 描述“输入改一点，输出最多会被放大多少”的最坏情况灵敏度。

## 它为什么重要
在对抗鲁棒中，若模型对输入扰动的放大上界更小，通常更不容易被小扰动攻击成功。

## 一个小例子
若有界 `|f(x+delta)-f(x)| <= 2||delta||`，则同样大小的扰动最多把输出改动放大 2 倍。

## 更正式的定义
若存在 `L>=0` 使得任意 `x1,x2` 都满足
`||f(x1)-f(x2)|| <= L ||x1-x2||`，则 `f` 是 Lipschitz 连续，最小这样的 `L` 即 Lipschitz 常数。

## 数学形式（如有必要）
\[
\|f(x_1)-f(x_2)\| \le L\|x_1-x_2\|
\]
其中 `L` 表示最坏情况下的放大倍数。

## 核心要点
1. `L` 越小，函数最坏敏感性越低。
2. 网络整体 `L` 往往由层/算子上界组合得到。
3. 严格精确的 `L` 难算，工程上通常做近似。

## 这篇论文里怎么用
- [[RACL]]: 对网络 Lipschitz 上界施加概率置信约束，驱动架构搜索偏向更鲁棒候选。

## 代表工作
- Parseval 等谱约束工作把 Lipschitz 控制用于鲁棒训练。

## 相关概念
- [[Spectral Norm]]
- [[Adversarial Robustness]]
- [[Differentiable Architecture Search]]
