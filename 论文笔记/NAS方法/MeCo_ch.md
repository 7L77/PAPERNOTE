---
title: "MeCo_ch"
type: method
language: zh-CN
source_method_note: "[[MeCo]]"
source_paper: "MeCo: Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation"
source_note: "[[MeCo]]"
authors: [Tangyu Jiang, Haodi Wang, Rongfang Bie]
year: 2023
venue: NeurIPS
tags: [nas-method, zh, nas, training-free, zero-cost-proxy]
created: 2026-03-14
updated: 2026-03-15
---

# MeCo 中文条目

## 一句话总结
> MeCo 在每层特征图上计算 Pearson 相关矩阵最小特征值并跨层求和，用“一条随机样本 + 一次前向”完成 zero-shot NAS 排序。

## 来源
- 英文方法笔记: [[MeCo]]
- 主文 PDF: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Paper-Conference.pdf
- 补充材料: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Supplemental-Conference.pdf
- OpenReview: https://openreview.net/forum?id=KFm2lZiI7n
- 代码: https://github.com/HamsterMimi/MeCo

## 适用场景
- 问题类型: 训练前架构排序、低成本 NAS 候选筛选。
- 约束条件: 候选很多、预算很小、希望避免反向传播型 proxy。
- 原因: MeCo 只需前向计算，易嵌入 Zero-Cost-PT 这类搜索流程。

## 不适用或高风险场景
- 搜索空间中通道数变化非常大，导致原始 MeCo 出现负相关。
- 小样本统计导致相关矩阵数值不稳定（特征值波动大）。
- 任务域偏移显著，proxy 与最终精度相关性不足。

## 输入、输出、目标
- 输入: 架构 `A`、随机输入 `X`、层特征 `f^i(X; θ)`。
- 输出: `MeCo` 或 `MeCoopt` 分数。
- 目标: 提高 proxy 排序与真实性能排序的一致性（Spearman 相关更高）。

## 方法分解
### 阶段 1: 特征图相关统计
- 对随机输入做一次前向。
- 在每层特征图上计算 Pearson 相关矩阵。
- Source: Def. 3 / Eq. (12)

### 阶段 2: 原始 MeCo 分数
- 按层取最小特征值并求和:
  `MeCo = sum_i lambda_min(P(f^i(X; θ)))`。
- Source: Eq. (12)

### 阶段 3: MeCoopt 修正
- 固定每层采样通道数 `n`，得到采样相关矩阵 `P'_i`。
- 按 `c(i)/n` 做缩放聚合:
  `MeCoopt = sum_i (c(i)/n) * lambda_min(P'_i)`。
- Source: Eq. (13), Sec. 5.1

### 阶段 4: 接入 NAS 搜索
- 在候选构建阶段和验证阶段使用 MeCo 评分。
- Source: Supplementary App. C Algorithm 1

## 伪代码
```text
Algorithm: MeCo-based zero-shot NAS
Input: A0, O, E, N, K
Output: Abest

1. 构造候选架构 Ai:
   1.1 用 MeCo 对操作/边进行选择
       Source: Supplementary App. C Algorithm 1 (Stage 1)
2. 在候选集上做最终排序:
   Abest = argmax_i MeCo(Ai)
   Source: Supplementary App. C Algorithm 1 (Stage 2)
3. 可选: 用 MeCoopt 替代 MeCo
   Source: Eq. (13), Inference from source
```

## 关键结果（主文）
- Table 1: NATS-Bench-TSS 上 `0.894/0.883/0.845`（三数据集）表现领先。
- Table 1: NATS-Bench-SSS 上原始 MeCo 出现负相关，触发 MeCoopt 动机。
- Table 2: NAS-Bench-301 上 MeCo/MeCoopt 达到最优组表现。
- Table 4: DARTS-CNN + Zero-Cost-PT 中，MeCo 搜索结果具备较好精度/成本比。

## 实现要点（代码对照）
- 随机输入: `torch.randn(size=(1, 3, 64, 64))`
- 采集方式: forward hook 收集中间层输出。
- 统计过程: `torch.corrcoef` + 清理 NaN/Inf + `torch.linalg.eig` 取最小特征值。
- 接入参数: `--proj_crit meco`
- 关键路径:
  - `correlation/foresight/pruners/measures/meco.py`
  - `nasbench201/networks_proposal.py`

## 本地路径
- 主文 PDF: `D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation.pdf`
- 补充 PDF: `D:/PRO/essays/papers/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation Supplementary Material.pdf`
- 代码: `D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation`
