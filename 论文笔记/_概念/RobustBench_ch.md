---
type: concept
language: zh-CN
source_concept_note: "[[RobustBench]]"
aliases: [鲁棒架构基准, DARTS鲁棒基准]
---

# RobustBench 中文条目

## 一句话直觉
RobustBench 是面向鲁棒 NAS 的架构基准，提前给出一批架构的对抗训练结果，方便代理方法做公平比较。

## 它为什么重要
如果每次都重新对抗训练所有候选，成本很高。RobustBench 通过“固定候选 + 预计算鲁棒指标”降低评估门槛。

## 一个小例子
[[TRNAS]] 会先看 R-Score 与 RobustBench 上鲁棒精度的对应关系，再判断代理是否有筛选价值。

## 更正式的定义
在 TRNAS 使用语境里，RobustBench（由 ZCPRob 论文引入）包含 223 个来自 DARTS 搜索空间、已完成对抗训练并记录鲁棒精度的架构。

## 核心要点
1. 它服务于鲁棒 NAS 评测，不是通用图像分类榜单。
2. 提供攻击下鲁棒精度，适合评估鲁棒代理排序能力。
3. 可减少重复训练，提升研究复现效率。

## 这篇论文里怎么用
- [[TRNAS]] 用 RobustBench 验证 R-Score 的排序区分能力，并与 CRoZe/ZCPRob 等基线比较。

## 代表工作
- [[ZCPRob]]: 在鲁棒 zero-cost proxy 评测中引入 RobustBench。
- [[TRNAS]]: 使用 RobustBench 做训练前鲁棒代理评测与搜索分析。

## 相关概念
- [[Adversarial Robustness]]
- [[DARTS]]
- [[Zero-Cost Proxy]]
- [[NAS-Rob-Bench-201]]

