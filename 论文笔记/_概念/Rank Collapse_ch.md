---
type: concept
language: zh-CN
source_concept_note: "[[Rank Collapse]]"
aliases: [秩坍塌, Rank Collapse]
---

# Rank Collapse 中文条目

## 一句话直觉
Rank Collapse 指的是层数加深后，表示矩阵越来越“挤”到少数方向上，信息多样性下降，极端时接近 rank-1。

## 它为什么重要
表示秩下降通常意味着模型表达能力变弱；在 NAS 中，这种现象反过来可以作为低成本评估信号。

## 一个小例子
4 个 token 原本方向各异，经过很多层后几乎都指向同一方向。虽然数值不完全相同，但可区分信息已经被压扁。

## 更正式的定义
对表示矩阵 `X`，若随深度增加其秩或有效秩持续下降（趋向 1），即可称为 rank collapse。

## 数学形式（如有必要）
常见度量思路是看 `X` 到最近 rank-1 矩阵的距离：
\[
\min_{u,v} \|X - uv^\top\|
\]
距离越小，说明坍塌越强。

## 核心要点
1. 本质是深层表示退化，不是单纯数值噪声。
2. 规范化/残差可缓解，但不一定能完全消除。
3. 可转化为训练免费代理中的有效特征。

## 这篇论文里怎么用
- [[TF-MAS]]: 基于 SSD 堆叠也会出现 rank-collapse 的观点，构建了 Mamba2 的训练免费代理。

## 代表工作
- [[TF-MAS]]: 把 rank-collapse 视角引入 Mamba2 架构搜索。

## 相关概念
- [[Effective Rank]]
- [[State Space Duality (SSD)]]
- [[Training-free NAS]]

