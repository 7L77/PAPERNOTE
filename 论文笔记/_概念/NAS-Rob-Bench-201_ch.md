---
type: concept
language: zh-CN
source_concept_note: "[[NAS-Rob-Bench-201]]"
aliases: [鲁棒NAS-Bench-201, NAS-Rob-Bench201]
---

# NAS-Rob-Bench-201 中文条目

## 一句话直觉
NAS-Rob-Bench-201 是一个“鲁棒版 NAS 基准”，把固定搜索空间内大量架构的对抗训练结果预先算好，便于快速比较搜索算法。

## 它为什么重要
鲁棒 NAS 最贵的是反复对抗训练。这个基准能把成本前置，让不同方法在同一预算下公平比较。

## 一个小例子
在 [[TRNAS]] 的补充实验里，作者把各类 NAS 方法都迁移到该基准并统一设为 1000 次评估，从而直接比较精度和效率。

## 更正式的定义
NAS-Rob-Bench-201 包含 15,625 个已完成对抗训练的架构，并提供 clean 与多攻击设置下的鲁棒指标。

## 核心要点
1. 对其定义的搜索空间具有较完整覆盖。
2. 适合做预算受控的鲁棒 NAS 比较。
3. 随机种子会引入轻微最优结果波动，解读时应关注统计稳定性。

## 这篇论文里怎么用
- [[TRNAS]] 在该基准上对比标准 NAS 与鲁棒 NAS 基线，展示了更高效率和较强鲁棒表现。

## 代表工作
- Robust NAS under adversarial training 的 benchmark 论文（ICLR 2024）构建该基准。
- [[TRNAS]] 在其上做效率与性能验证。

## 相关概念
- [[RobustBench]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]

