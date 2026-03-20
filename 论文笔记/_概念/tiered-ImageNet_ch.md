---
type: concept
language: zh-CN
source_concept_note: "[[tiered-ImageNet]]"
aliases: [tieredImageNet, tiered-ImageNet]
---

# tiered-ImageNet 中文条目

## 一句话直觉
tiered-ImageNet 是一个规模更大、语义层级更复杂的 few-shot 基准。

## 它为什么重要
相较 mini-ImageNet，它更能检验模型在跨类别层级上的泛化能力。

## 一个小例子
训练类与测试类属于不同细粒度类别族，模型必须在更强分布偏移下完成 few-shot 识别。

## 更正式的定义
tiered-ImageNet 使用 ImageNet 的层级信息做类别划分，通常比 mini-ImageNet 更大、更难。

## 数学形式（如有必要）
指标同样是大量 N-way K-shot episode 的平均准确率。

## 核心要点
1. 是更“硬核”的 few-shot 评测集。
2. 常与 mini-ImageNet 共同报告，验证泛化稳定性。
3. 能更好区分方法在跨域泛化上的差异。

## 这篇论文里怎么用
- [[IBFS]]: 在 tiered-ImageNet 上报告 5-way 1-shot/5-shot 结果并对比搜索成本。

## 代表工作
- Ren et al. (2018): tiered-ImageNet 基准。
- [[IBFS]]: 用于 few-shot 搜索效果验证。

## 相关概念
- [[Few-shot Learning]]
- [[mini-ImageNet]]
