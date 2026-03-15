---
type: concept
language: zh-CN
source_concept_note: "[[Alternating Direction Method of Multipliers]]"
aliases: [交替方向乘子法, ADMM]
---

# Alternating Direction Method of Multipliers 中文条目

## 一句话直觉
ADMM 把一个难的约束优化问题拆成几个更容易的子问题，交替优化，并通过对偶变量把它们“拧”回同一个约束上。

## 它为什么重要
当目标项和约束项单独都好优化、但联合优化很难时，ADMM 往往比直接硬解更稳。

## 一个小例子
你既要最小化分类损失，又要满足某个概率约束。ADMM 可先更新主变量，再更新对偶变量来惩罚约束违背。

## 更正式的定义
ADMM 常用于
`min f(x)+g(z)` s.t. `Ax+Bz=c`，
通过增广拉格朗日并交替更新 primal/dual 变量求解。

## 数学形式（如有必要）
典型三步：
1. 更新 `x`
2. 更新 `z`
3. 更新对偶变量 `u <- u + (Ax+Bz-c)`

## 核心要点
1. 能把耦合约束问题拆开处理。
2. 在大规模约束优化中实用性强。
3. 惩罚系数设置会显著影响收敛与解质量。

## 这篇论文里怎么用
- [[RACL]]: 用 ADMM 风格更新来处理置信 Lipschitz 约束下的架构分布参数优化。

## 代表工作
- Boyd 等 ADMM 综述是经典参考。

## 相关概念
- [[Confidence Learning]]
- [[Lipschitz Constant]]
- [[Differentiable Architecture Search]]
