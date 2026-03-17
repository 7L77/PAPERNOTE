---
type: concept
language: zh-CN
source_concept_note: "[[Cross-Attention]]"
aliases: [交叉注意力, Cross-Attention]
---

# Cross-Attention 中文条目

## 一句话直觉
Cross-Attention 让一组特征去“询问”另一组特征，从而实现条件化的信息融合。

## 它为什么重要
PO-NAS 需要把“架构信息”和“指标信息”关联起来，交叉注意力正好可以学到“这个架构更该信哪些指标”。

## 一个小例子
把架构 embedding 当作 Query，把指标 embedding 当作 Key/Value，输出就是“按当前架构定制过的指标表示”。

## 更正式的定义
Cross-Attention 在 \(Q\) 与 \((K,V)\) 之间计算注意力权重，再对 \(V\) 做加权汇聚，得到与 Query 条件相关的表示。

## 数学形式（如有必要）
\[
\mathrm{Attn}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V
\]

其中 \(Q\) 是查询，\(K,V\) 是另一来源的键和值，\(d\) 是缩放维度。

## 核心要点
1. 适合跨来源特征融合。
2. 多头机制能学习多种对应关系。
3. 比简单拼接更能表达复杂依赖。

## 这篇论文里怎么用
- [[PO-NAS]]: 用 multi-head cross-attention 生成“每个架构独立”的指标权重。

## 代表工作
- [[Attention Is All You Need]]: 注意力机制基础。
- [[PO-NAS]]: 在 NAS 代理模型中落地交叉注意力融合。

## 相关概念
- [[Graph Attention Network]]
- [[Surrogate Predictor]]
- [[Zero-Cost Proxy]]
