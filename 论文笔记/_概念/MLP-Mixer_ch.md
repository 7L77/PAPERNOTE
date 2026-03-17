---
type: concept
language: zh-CN
source_concept_note: "[[MLP-Mixer]]"
aliases: [MLP-Mixer, Mixer 架构]
---

# MLP-Mixer 中文条目

## 一句话直觉
MLP-Mixer 用 MLP 在“token 维”和“通道维”交替混合信息，不依赖注意力机制。

## 它为什么重要
它提供了结构简洁的全局交互建模方式，适合把节点统计向量做跨段融合。

## 一个小例子
将节点特征分段后，先做“段间混合”，再做“通道混合”，即可捕获跨节点依赖。

## 更正式的定义
MLP-Mixer 由 token-mixing 和 channel-mixing 两类 MLP 子层组成，通常配合 LayerNorm 与残差连接。

## 数学形式（如有必要）
一个标准 block 包含：
1) 在转置后的输入上做 token mixing；
2) 在原布局上做 channel mixing；
并在各子层后加入残差。

## 核心要点
1. 无注意力但可建模全局交互。
2. 不限于图像 patch，可迁移到结构化向量输入。
3. 对归一化与隐藏维配置较敏感。

## 这篇论文里怎么用
- [[ParZC]]: 用 mixer 处理节点级 ZC 向量，并与 Bayesian 层组合提升排序能力。

## 代表工作
- [[ParZC]]: 在 NAS 排序器中改造并应用 mixer 架构。

## 相关概念
- [[Bayesian Neural Network]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
