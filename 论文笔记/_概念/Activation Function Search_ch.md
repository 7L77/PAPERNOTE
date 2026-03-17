---
type: concept
language: zh-CN
source_concept_note: "[[Activation Function Search]]"
aliases: [激活函数搜索]
---

# Activation Function Search 中文条目

## 一句话直觉
激活函数搜索把“用哪种激活函数”当作可搜索变量，而不是固定成 ReLU。

## 它为什么重要
不同任务和骨干网络的最优非线性可能不同，固定激活会限制模型上限。

## 一个小例子
BERT 结构通常偏好 GELU，而某些 CNN 可能更适配 ReLU/LeakyReLU。

## 更正式的定义
在模型设计或 NAS 搜索空间中，把激活类型（ReLU、GELU、SiLU、ELU 等）加入候选集合，并通过评估选择更优配置。

## 核心要点
1. 拓展了 NAS 搜索空间。
2. 依赖 ReLU 假设的代理方法可能在此场景退化。
3. 好的训练前评分方法应兼容多激活类型。

## 这篇论文里怎么用
- [[RBFleX-NAS]] 构建 NAFBee（VGG-19 / BERT）来测试激活搜索能力。
- 实验显示其更容易识别最优激活配置。

## 代表工作
- [[RBFleX-NAS]]

## 相关概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]

