---
type: concept
language: zh-CN
source_concept_note: "[[Certified Robustness Lower Bound]]"
aliases: [认证鲁棒性下界, Certified Lower Bound]
---

# Certified Robustness Lower Bound 中文条目

## 一句话直觉

它不是“被攻击几次没坏”的经验结果，而是“在给定扰动半径内最坏情况也至少有多安全”的可证明下界。

## 它为什么重要

仅靠 PGD/FGSM 等攻击测试可能漏掉更强攻击；认证下界提供了更硬的鲁棒性保证。

## 一个小例子

如果某样本真实类与次优类的 logit 间隔，经过认证后最坏情况下仍有 0.02（大于 0），那么在该半径内该样本可被证明不会被翻转分类。

## 更正式的定义

在约束集合（如 `||delta||_p <= epsilon`）下，对分类 margin 的最小值给出可证明下界。下界若大于 0，则该样本在此威胁模型下“可认证鲁棒”。

## 数学形式（如有必要）

设 `m(x, delta)` 是扰动后真实类与最强竞争类的 margin，则认证方法给出：

\[
\underline{m}(x) \le \min_{\|\delta\|_p \le \epsilon} m(x,\delta)
\]

若 \(\underline{m}(x) > 0\)，说明样本在半径 `epsilon` 内具有认证鲁棒性。

## 核心要点

1. 认证下界是“保证”，不是“抽样攻击成绩”。
2. 下界越紧通常越好，但计算成本也更高。
3. 结论依赖威胁模型（范数类型、扰动半径等）。

## 这篇论文里怎么用

- [[DSRNA]]: 把 block 级线性界组合成整网 certified lower bound，并作为可微架构鲁棒性指标参与 NAS 优化。

## 代表工作

- [[CNN-Cert]]: 通过线性界传播为 CNN 给出鲁棒性认证下界。

## 相关概念

- [[Adversarial Robustness]]
- [[Jacobian Norm Bound]]
