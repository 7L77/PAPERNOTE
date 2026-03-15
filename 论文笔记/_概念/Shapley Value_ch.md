---
type: concept
language: zh-CN
source_concept_note: "[[Shapley Value]]"
aliases: [夏普利值, 合作博弈归因]
---

# Shapley Value 中文条目

## 一句话直觉

Shapley Value 关心的是：在所有可能的“加入顺序”里，一个组件平均能带来多少边际收益。

## 它为什么重要

当组件之间存在协同或相互依赖时，简单做“去掉某个组件”的单次消融会失真；Shapley Value 能更公平地分配贡献。

## 一个小例子

三个 primitive 一起才有明显鲁棒增益，单个看都不突出。Shapley Value 会在所有加入顺序下统计边际增益并取平均，避免把“组合效应”错误归给某一个 primitive。

## 更正式的定义

对参与者集合 `N` 中的成员 `i`，若联盟收益函数为 `v(S)`，则：

\[
\phi_i(v)=\sum_{S \subseteq N\setminus\{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!}\big(v(S\cup\{i\})-v(S)\big)
\]

即：`i` 在所有排列上的期望边际贡献。

## 核心要点

1. 能处理组件交互与协同效应。
2. 满足经典公平性公理（效率、对称、虚拟参与者、可加性）。
3. 精确计算代价高，工程上常用采样估计近似。

## 这篇论文里怎么用

- [[LRNAS]] 把每个 search primitive 当作参与者，把“自然精度 + 对抗鲁棒性”的变化作为联盟收益（Sec. III-C, Eq. 3-8）。
- 通过排列采样得到无偏估计，用于更新架构参数并指导搜索。

## 代表工作

- L. S. Shapley, "A Value for n-Person Games," 1953.
- H. Xiao et al., "Shapley-NAS: Discovering Efficient and Robust Architectures via Shapley Value Guidance," 2022.

## 相关概念

- [[Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Adversarial Robustness]]
