---
type: concept
language: zh-CN
source_concept_note: "[[mini-ImageNet]]"
aliases: [miniImageNet, mini-ImageNet]
---

# mini-ImageNet 中文条目

## 一句话直觉
mini-ImageNet 是从 ImageNet 抽取并标准化的小规模 few-shot 评测基准。

## 它为什么重要
它是少样本学习里最常用的公开基准之一，便于不同方法公平对比。

## 一个小例子
常见评测是 5-way 1-shot / 5-way 5-shot：每次 episode 从测试类采样少量支持样本再评估。

## 更正式的定义
mini-ImageNet 通常包含 100 类，经典划分是 64/16/20（train/val/test），图像分辨率常用 84x84。

## 数学形式（如有必要）
最终指标一般是大量 episode 的平均准确率与置信区间。

## 核心要点
1. FSL 论文的常用对比基线。
2. 协议细节（采样方式、backbone）会显著影响结果。
3. 适合检验“快速适配能力”。

## 这篇论文里怎么用
- [[IBFS]]: 在 mini-ImageNet 上报告 5-way 1-shot/5-shot 结果验证架构搜索效果。

## 代表工作
- Vinyals et al. (2016): 早期经典 few-shot 基准工作。
- [[IBFS]]: 作为核心 FSL 评测集之一。

## 相关概念
- [[Few-shot Learning]]
- [[tiered-ImageNet]]
