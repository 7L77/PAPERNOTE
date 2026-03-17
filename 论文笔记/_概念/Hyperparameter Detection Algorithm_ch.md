---
type: concept
language: zh-CN
source_concept_note: "[[Hyperparameter Detection Algorithm]]"
aliases: [HDA, 超参数检测算法]
---

# Hyperparameter Detection Algorithm 中文条目

## 一句话直觉
HDA 是一种“用数据统计自动选核参数”的方法，避免手工调 `gamma`。

## 它为什么重要
RBF 核对 `gamma` 很敏感，参数不合适会让相似度矩阵失去区分度。

## 一个小例子
两组样本均值差大且方差小，HDA 会倾向给出更能放大差异的候选 gamma。

## 更正式的定义
对向量对 `(v_i, v_j)`：
- `D_ij = (m_i - m_j)^2`
- `s_i^2, s_j^2` 为方差
- `G_ij = D_ij / (2(s_i^2 + s_j^2))`
在候选矩阵上选取最终 gamma。

## 核心要点
1. 同时考虑“均值分离度”和“类内离散度”。
2. 计算便宜，可在少量候选网络上估计。
3. 比随机或盲目网格更稳定。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 分别构造 `G_k` 与 `G_q`。
- 最终 `gamma_k`、`gamma_q` 取最小有效候选项。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[Radial Basis Function Kernel]]
- [[Fisher Linear Discriminant]]

