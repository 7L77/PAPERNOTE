---
type: concept
language: zh-CN
source_concept_note: "[[Zero-Shot Learning]]"
aliases: [零样本学习, ZSL]
---

# Zero-Shot Learning 中文条目

## 一句话直觉
Zero-Shot Learning（ZSL）是在训练时完全没见过某些类别样本的前提下，仍能在测试时识别这些“未见类”。

## 它为什么重要
现实任务里不可能给每个类别都收集大量标注数据，ZSL 通过语义信息迁移能力，降低新类别落地成本。

## 一个小例子
训练集中只有马、斑马，没有“霍加狓（okapi）”。如果模型知道 okapi 的语义属性（有条纹、食草、蹄类），就能把测试图像匹配到这个未见类别。

## 更正式的定义
设 seen 类集合 `Y_s` 与 unseen 类集合 `Y_u` 互斥。训练仅使用 `Y_s` 的样本，测试时只在 `Y_u` 中做分类，语义空间是两者的桥梁。

## 核心要点
1. 训练阶段不能看见 unseen 类图像。
2. 必须有跨类共享的语义表示（属性、文本嵌入等）。
3. 生成式 ZSL 常先合成 unseen 特征，再训练普通分类器。

## 这篇论文里怎么用
- [[ZeroNAS]]: 通过搜索 GAN 架构提升 unseen 特征质量，从而提升 ZSL 识别精度。

## 代表工作
- [[ZeroNAS]]: 把可微 NAS 与 GAN 特征生成结合到 ZSL。

## 相关概念
- [[Generalized Zero-Shot Learning]]
- [[Generative Adversarial Network]]
- [[Neural Architecture Search]]

