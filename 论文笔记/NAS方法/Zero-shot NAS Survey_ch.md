---
title: "Zero-shot NAS Survey_ch"
type: method
language: zh-CN
source_method_note: "[[Zero-shot NAS Survey]]"
source_paper: "Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities"
source_note: "[[Zero-shot NAS Survey]]"
authors: [Guihong Li, Duc Hoang, Kartikeya Bhardwaj, Ming Lin, Zhangyang Wang, Radu Marculescu]
year: 2024
venue: IEEE TPAMI
tags: [nas-method, zh, survey, zero-shot-nas]
created: 2026-03-20
updated: 2026-03-20
---

# Zero-shot NAS Survey 中文条目

## 一句话总结

> 这不是一篇提出新搜索算法的论文，而是一篇把 zero-shot NAS 系统拆成“proxy 设计、benchmark、硬件建模、约束场景实验、future directions”的综述；它最重要的结论是：很多 proxy 在真实设置里并没有稳定超过 `#Params/#FLOPs`。

## 来源

- 论文: [Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities](https://arxiv.org/abs/2307.01998)
- HTML: https://arxiv.org/html/2307.01998v3
- 代码: https://github.com/SLDGroup/survey-zero-shot-nas
- 英文方法笔记: [[Zero-shot NAS Survey]]
- 论文笔记: [[Zero-shot NAS Survey]]

## 适用场景

- 问题类型: 为 zero-shot NAS 选择 proxy、做 proxy 对比，或设计硬件约束下的训练前排序策略。
- 前提假设: 候选架构可以在随机初始化时被快速打分，benchmark/API/硬件指标可获得。
- 数据形态: 以 benchmark 驱动的监督视觉任务为主，并结合 latency/energy 等硬件指标。
- 规模与约束: 适合在全量训练候选网络太贵时，先做廉价筛选与排序。
- 适用原因: 这篇综述给了一个很实用的判断框架，告诉你 proxy 什么时候值得信，什么时候应该直接回退到简单 baseline。

## 不适用或高风险场景

- 你需要一个可以直接产出最优架构的端到端搜索算法。
- 你需要覆盖 2024 年之后新 proxy、LLM4NAS、Mamba/大模型架构搜索的最新综述。
- 你的搜索空间和文中 benchmark 差异很大，又没有条件自己重测 proxy 排序质量。

## 输入、输出与目标

- 输入: 候选架构集合、proxy 家族、benchmark/任务集合，以及可选的硬件约束。
- 输出: proxy 分数、排序相关性分析、proxy 挑出的候选架构，以及对后续 proxy 设计的经验结论。
- 优化目标: 判断哪些 zero-shot proxy 能较好逼近最终精度排序，以及它们在硬件约束下是否仍然有用。
- 核心假设: 初始化阶段的统计量对最终训练后性能至少保留了部分有用信号。

## 方法拆解

### 阶段 1: 定义“好 proxy”应该测什么

- 作者提出，一个好的 proxy 应同时尽量反映表达能力、泛化能力和可训练性，而不是只看某一个角度。
- Source: Sec. 2.1, Table 2

### 阶段 2: 整理现有 proxy

- 把已有方法分成 gradient-based 和 gradient-free，并逐个解释理论动机。
- Source: Sec. 2.2, Sec. 2.3, Table 2

### 阶段 3: 选择 benchmark 与硬件模型

- 在 NASBench-101/201、NATS-Bench、TransNAS-Bench-101、ImageNet-1K CNN、ViT、硬件约束场景上统一评测。
- Source: Sec. 3, Fig. 5, Table 3

### 阶段 4: 做跨场景对比实验

- 比较 unconstrained、top-5% constrained、特定网络家族、大规模任务、ViT、Pareto 约束等设置下的 proxy 表现。
- Source: Sec. 4.1-4.4, Fig. 6-19, Table 4-6

### 阶段 5: 总结失败模式与未来方向

- 分析为什么 `#Params` 经常有效、它何时失效、现有 benchmark 有哪些缺口、未来为什么可能需要分家族定制 proxy。
- Source: Sec. 4.5, Sec. 5

## 伪代码

```text
Algorithm: Zero-shot NAS Survey Evaluation Framework
Input: 搜索空间 S, proxy 集合 P, benchmark/任务集合 B, 可选硬件约束 H
Output: 相关性分析, proxy 排名, 设计结论

1. 定义 proxy 质量标准：表达能力、泛化能力、可训练性。
   Source: Sec. 2.1
2. 将 proxy 分成 gradient-based 与 gradient-free 两类。
   Source: Sec. 2.2, Sec. 2.3, Table 2
3. 对每个 benchmark / 任务 / 硬件设置：
   3.1 在随机初始化下计算候选架构的 proxy 分数。
       Source: Sec. 4, Inference from source
   3.2 用 SPR / KT 比较 proxy 与最终精度的相关性，并单独看 top-performing 子集。
       Source: Sec. 4.1, Fig. 6-14
   3.3 在硬件约束下比较 proxy 找到的 Pareto 候选与真实前沿的距离。
       Source: Sec. 4.4, Fig. 18-19
4. 记录哪些场景下简单 baseline (#Params/#FLOPs) 更强，哪些场景下专门 proxy 更有优势。
   Source: Sec. 4.1-4.4
5. 总结 benchmark 缺口、理论缺口与未来 proxy 设计方向。
   Source: Sec. 4.5, Sec. 5
```

## 训练流程

1. 这不是传统意义上需要训练的新模型，而是评估初始化阶段 proxy 的有效性。
2. 选定 benchmark 或网络家族，枚举候选架构。
3. 在不完整训练这些候选的前提下计算 proxy 分数。
4. 将这些分数与最终训练后的真实性能或硬件约束下的 Pareto 前沿比较。

Sources:

- Sec. 3, Sec. 4, Table 4-6, Fig. 18-19

## 推理流程

1. 选定搜索空间与可选硬件预算。
2. 对初始化网络计算目标 proxy。
3. 用 proxy 对候选架构排序或筛选。
4. 对排名靠前的候选再做真实训练验证，尤其要重点检查高精度尾部区域。

Sources:

- Sec. 2, Sec. 4.1, Sec. 4.4

## 复杂度与效率

- 时间复杂度: 论文未给封闭形式。
- 空间复杂度: 论文未给封闭形式。
- 运行特征: zero-shot proxy-based NAS 比 one-shot NAS 便宜得多；Table 6 中最低可到 `0.03` GPU hours，而 one-shot baseline 为 `200` GPU hours。
- 扩展性说明: gradient-free proxy 因为没有 backward，通常比 gradient-based 更便宜，但更便宜不等于排序更准。

## 实现备注

- 代码结构: `main.py` 负责枚举 benchmark 架构并计算各类 proxy。
- 代理实现: `measures/grad_norm.py`、`snip.py`、`grasp.py`、`fisher.py`、`jacob_cov.py`、`synflow.py`。
- 额外逻辑: NTK、Logdet、Zen-score 的主流程在 `main.py` 与 `measures/__init__.py`。
- 外部依赖: NAS-Bench/NATS-Bench API、数据集、CUDA、`ptflops` 等。
- 代码与论文的关系: 官方仓库更像“评估工具箱 + 论文列表”，不是一键复现整篇 survey 全部实验图表的完整流水线。

## 与相关方法的关系

- 对比 [[One-shot NAS]]: zero-shot NAS 省掉 supernet 训练，便宜很多，但排序质量更弱、更不稳定。
- 对比 [[Multi-shot NAS]]: zero-shot NAS 代价更低，但依赖初始化统计量而不是真实训练后的候选精度。
- 主要优势: 帮你判断 proxy 在什么条件下真的有用，而不是只看论文 headline。
- 主要代价: 目前没有一个 proxy 能在搜索空间、任务、硬件约束之间都稳定通吃。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 5, Fig. 6-9, Fig. 17-19
- 关键表: Table 2, Table 3, Table 4-6
- 关键公式: Eq. (1)-(6), Eq. (10)-(20)
- 关键算法: 论文没有单一算法框，而是一个跨 Sec. 2-4 的比较分析框架

## 参考链接

- arXiv: https://arxiv.org/abs/2307.01998
- HTML: https://arxiv.org/html/2307.01998v3
- 代码: https://github.com/SLDGroup/survey-zero-shot-nas
- 本地实现: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities

