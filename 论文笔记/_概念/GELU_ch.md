---
type: concept
language: zh-CN
source_concept_note: "[[GELU]]"
aliases: [Gaussian Error Linear Unit, GELU]
---

# GELU 中文条目

## 一句话直觉
GELU 是比 ReLU 更平滑的门控激活，对接近零的输入不会“硬切断”。

## 它为什么重要
平滑激活常带来更稳定的梯度传播，在鲁棒训练中也可能更稳。

## 一个小例子
接近 0 的输入在 GELU 下输出会连续变化，而不是像 ReLU 那样突变。

## 更正式的定义

$$
\text{GELU}(x)\approx 0.5x\left(1+\tanh\left[\sqrt{2/\pi}(x+0.044715x^3)\right]\right)
$$

## 核心要点
1. 属于平滑激活。
2. 在 Transformer/CNN 都有应用。
3. 常作为 ReLU 替代候选。

## 这篇论文里怎么用
- [[Robust Principles]]: 把 GELU 作为平滑激活对照，验证其鲁棒优势。

## 代表工作
- [[Robust Principles]]: 在激活函数鲁棒对比中包含 GELU。

## 相关概念
- [[SiLU (Sigmoid Linear Unit)]]
- [[Adversarial Robustness]]

