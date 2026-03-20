---
type: concept
language: zh-CN
source_concept_note: "[[Few-shot Learning]]"
aliases: [少样本学习, Few-shot Learning]
---

# Few-shot Learning 中文条目

## 一句话直觉
Few-shot Learning 研究的是：每个类别只有极少标注样本时，模型如何仍然学会新任务。

## 它为什么重要
现实中标注常常昂贵，很多任务无法提供大规模标签。

## 一个小例子
5-way 1-shot：5 个类别、每类 1 张标注图，模型需要在此基础上完成分类。

## 更正式的定义
FSL 通常采用 episode 评测：在 support 集快速适配，在 query 集评估泛化能力。

## 数学形式（如有必要）
每个 episode 包含 `D_support` 与 `D_query`，模型在 support 更新后于 query 计算准确率。

## 核心要点
1. 核心不是拟合训练集，而是小样本泛化。
2. 元学习与度量学习是两类主流路线。
3. 常见基准包括 mini-ImageNet 与 tiered-ImageNet。

## 这篇论文里怎么用
- [[IBFS]]: 直接以 few-shot 任务作为 NAS 目标，报告 5-way 1/5-shot 结果。

## 代表工作
- Finn et al. (2017): MAML。
- [[IBFS]]: 面向 few-shot 的训练自由架构搜索。

## 相关概念
- [[Model-Agnostic Meta-Learning]]
- [[mini-ImageNet]]
- [[tiered-ImageNet]]
