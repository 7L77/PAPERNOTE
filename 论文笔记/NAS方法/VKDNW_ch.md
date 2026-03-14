---
title: "VKDNW_ch"
type: method
language: zh-CN
source_method_note: "[[VKDNW]]"
source_paper: "Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights"
source_note: "[[VKDNW]]"
authors: [Ondrej Tybl, Lukas Neumann]
year: 2025
venue: arXiv
tags: [nas-method, zh, training-free-nas, fisher-information, ranking-proxy]
created: 2026-03-14
updated: 2026-03-14
---

# VKDNW 中文条目

## 一句话总结

> VKDNW 在网络初始化阶段用经验 FIM 特征值谱熵来做零训练排序，再配合规模项与 nDCG 评测，更强调“把好架构排到前面”的能力。

## 来源

- 论文: [Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights](https://arxiv.org/abs/2502.04975)
- HTML: https://arxiv.org/html/2502.04975v1
- 代码: https://github.com/ondratybl/VKDNW
- 英文方法笔记: [[VKDNW]]
- 论文笔记: [[VKDNW]]

## 适用场景

- 问题类型: 图像分类场景下的 training-free NAS 架构排序。
- 前提假设: 初始化阶段的参数估计几何信息与最终性能排序相关。
- 数据形态: 可仅用随机输入（无标签）计算核心分数。
- 规模与约束: 当无法对每个候选都完整训练时最有价值。
- 适用原因: 该方法优先优化“头部候选识别”，符合 NAS 实际工作流。

## 不适用或高风险场景

- 需要直接预测绝对精度，而非仅排序。
- 搜索空间结构导致“少量层采样 FIM”代表性不足。
- 候选数量极大且梯度计算预算仍然紧张。

## 输入、输出与目标

- 输入: 架构 `f`、初始化参数 `theta_init`、随机 mini-batch、可选其他零成本特征。
- 输出: `VKDNW(f)`、`VKDNWsingle(f)`，以及可选 `VKDNWagg`。
- 优化目标: 让高精度架构在排名前列（top-P）。
- 核心假设: 初始化时经验 FIM 谱可反映训练可估计性与架构优劣次序。

## 方法拆解

### 阶段 1: 构造经验 FIM

- 用模型预测分布而非真实标签构造经验 FIM。
- 通过稳定分解和参数采样保证可计算性与数值稳定性。
- Source: Sec. II-B, Eq. (8), Eq. (9), Eq. (10)

### 阶段 2: 计算 VKDNW 谱熵

- 从谱中取代表性分位特征值，归一化后计算熵分数。
- 去除极端特征值以提高稳定性。
- Source: Sec. II-C, Eq. (11)

### 阶段 3: 构建单分数排序

- 将规模代理与 VKDNW 相加：`VKDNWsingle = N_layers + VKDNW`。
- 可理解为“先按规模分组，再按谱熵精排”。
- Source: Sec. III(a), Eq. (12)

### 阶段 4: 可选聚合排序

- 使用 log-product 聚合 V/J/E/T/F 多种 ranking。
- 也可用随机森林做 model-driven 聚合。
- Source: Sec. V-A, Eq. (15), Table I, Table III

### 阶段 5: 面向 NAS 的评测

- 使用 KT、SPR 及 nDCG@P 评估，nDCG 更关注头部识别。
- Source: Sec. III, Eq. (13), Eq. (14), Fig. 2

## 伪代码

```text
Algorithm: VKDNW-based Training-free Ranking
Input: Candidate architecture set F, random batch size B, top cutoff P
Output: Ranked architectures (single or aggregated)

1. For each architecture f in F, initialize weights theta_init.
   Source: Sec. II-C
2. Compute empirical FIM approximation with stable factorization:
   F_hat(theta) = (1/N) * sum_n A_n^T A_n, using sampled parameters.
   Source: Sec. II-B, Eq. (8)-(10)
3. Compute VKDNW(f) as entropy over normalized decile eigenvalues.
   Source: Sec. II-C, Eq. (11)
4. Compute VKDNWsingle(f) = N_layers(f) + VKDNW(f).
   Source: Sec. III(a), Eq. (12)
5. Optionally aggregate with Jacov/Expressivity/Trainability/FLOPs:
   rank_agg(f) = log(prod_j rank_j(f)).
   Source: Sec. V-A, Eq. (15)
6. Use ranking for search and evaluate with KT/SPR/nDCG@P.
   Source: Sec. III, Eq. (13)-(14)
```

## 训练流程

1. 生成随机输入（或基线需要时使用真实输入）。
2. 初始化候选架构并计算代理分数。
3. 构建排名并驱动搜索（保留 top 候选）。
4. 仅对最终 shortlist 做完整训练与验证。

Sources:

- Sec. V-A, Sec. V-B, Table II, supplementary Sec. VIII-IX.

## 推理流程

1. 给定新候选架构，初始化参数。
2. 计算经验 FIM 与 VKDNW 分数。
3. 在候选池中转成相对排序。
4. 选出 top 架构进入后续高成本训练。

Sources:

- Sec. II-B, Sec. II-C, Sec. III(a), Sec. V.

## 复杂度与效率

- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: MobileNetV2 搜索报告为 ZS 0.4 GPU days；最终模型完整训练仍需高成本（8xA100 上约 7 天）。
- 扩展性说明: 通过层/参数采样控制 FIM 计算开销。

## 实现备注

- 经验 FIM 采用稳定分解，避免直接在超大矩阵上做不稳定特征分解。
- 实验显示随机输入与真实输入效果接近，默认 batch size 64。
- 典型采样策略：前 128 层每层采样少量权重。
- 聚合组件：V、J、E、T、F（VKDNWsingle/Jacov/Expressivity/Trainability/FLOPs）。
- model-driven 聚合可在 1024 架构上训练随机森林。
- 本地代码状态：2026-03-14 连接 GitHub 超时，未完成归档。

## 与相关方法关系

- 对比 [[Zero-Cost Proxy]]：增加了基于 Fisher 谱的统计动机信号。
- 对比 [[AZ-NAS]]：在 nDCG（头部检索）上更有优势，同时保持 KT/SPR 竞争力。
- 主要优势: 更强的 top 架构识别能力。
- 主要代价: 仍需梯度相关计算，且聚合版本依赖更多特征。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4
- 关键表: Table I, Table II, Table III, Table V, Table VII, Table VIII
- 关键公式: Eq. (8)-(12), Eq. (14), Eq. (15)
- 关键算法: Sec. V-B 与补充 Sec. VIII 的搜索流程描述

## 参考链接

- arXiv: https://arxiv.org/abs/2502.04975
- HTML: https://arxiv.org/html/2502.04975v1
- 代码: https://github.com/ondratybl/VKDNW
- 本地实现: Not archived (GitHub connectivity timeout on 2026-03-14)
