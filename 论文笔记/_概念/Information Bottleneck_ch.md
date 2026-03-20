---
type: concept
language: zh-CN
source_concept_note: "[[Information Bottleneck]]"
aliases: [信息瓶颈, Information Bottleneck]
---

# Information Bottleneck 中文条目

## 一句话直觉
信息瓶颈的核心是“只保留对任务有用的信息，把无关细节压缩掉”。

## 它为什么重要
它给了我们一个统一框架来平衡“表达能力”和“冗余信息”，非常适合解释表示学习与 proxy 设计。

## 一个小例子
做猫狗分类时，耳朵形状和纹理是有效信息，背景中的随机噪声应被压缩。

## 更正式的定义
在 `X -> R -> Y` 中，目标是让 `R` 同时满足：尽量少记住 `X`（小 `I(R;X)`）且尽量保留预测 `Y` 的信息（大 `I(R;Y)`）。

## 数学形式（如有必要）
常见目标：`L_IB = I(R;X) - beta * I(R;Y)`，其中 `beta` 控制压缩强度。

## 核心要点
1. IB 是“压缩-预测能力”的权衡。
2. `beta` 越大，压缩倾向通常越强。
3. 实践中常用熵或散度近似互信息。

## 这篇论文里怎么用
- [[IBFS]]: 用 IB 目标推导出熵驱动的训练自由架构评分。

## 代表工作
- Tishby et al. (2000): IB 原始理论。
- [[IBFS]]: 将 IB 引入 few-shot NAS 的 zero-cost 排序。

## 相关概念
- [[Entropy]]
- [[KL Divergence]]
- [[Zero-Cost Proxy]]
