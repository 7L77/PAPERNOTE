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
updated: 2026-03-14
---

# MeCo 中文条目

## 一句话总结
> MeCo 用一次随机样本前向传播得到各层特征图相关矩阵，并把最小特征值按层求和作为 zero-shot NAS 排序分数。

## 来源
- 英文方法笔记: [[MeCo]]
- 论文: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Paper-Conference.pdf
- 补充材料: https://proceedings.neurips.cc/paper_files/paper/2023/file/95a50c26d63cf9f3dcf67784f40eb6fd-Supplemental-Conference.pdf
- OpenReview: https://openreview.net/forum?id=KFm2lZiI7n
- 代码: https://github.com/HamsterMimi/MeCo

## 适用场景
- 问题类型: 训练前架构排序、低成本 NAS 候选筛选。
- 关键假设: 特征图相关结构与最终可训练性/性能排序有关。
- 资源约束: 适合大候选池、极低预算。

## 不适用场景
- 相关矩阵估计在当前任务下波动过大。
- 模型结构不易稳定提取中间层特征。
- 域偏移明显导致 proxy 与真实性能相关性失效。

## 输入、输出、目标
- 输入: 架构 `A`、随机输入 `X`、层特征 `F_l(X)`。
- 输出: `S_MeCo` 或 `S_MeCoopt` 分数。
- 目标: 提升 proxy 排序与最终训练后精度排序的一致性。

## 方法分解
### 阶段 1: 构造相关矩阵
- 对随机输入做一次前向。
- 对每层特征图展平，计算 `P(F_l(X))`。
- Source: Def. 3 / Eq. (12)

### 阶段 2: 计算 MeCo 分数
- 取每层相关矩阵最小特征值 `lambda_min`。
- 跨层求和得到 `S_MeCo`。
- Source: Eq. (12)

### 阶段 3: MeCoopt 修正
- 加入最大特征值加权项:
  `S_MeCoopt = S_MeCo + sum_l xi_l * lambda_max(P(F_l(X)))`。
- Source: Eq. (16)

### 阶段 4: 接入 NAS 搜索
- 用 MeCo 分数做架构提议和候选验证。
- Source: Supplementary App. C Algorithm 1

## 伪代码
```text
Algorithm: MeCo-based zero-shot NAS
Input: A0, O, E, N, K
Output: Abest

1. 生成候选架构 Ai:
   1.1 用 MeCo 对操作/边进行选择与裁剪
       Source: Supplementary App. C Algorithm 1 (Stage 1)
2. 在候选集上做最终 MeCo 排序:
   Abest = argmax_i MeCo(Ai)
   Source: Supplementary App. C Algorithm 1 (Stage 2)
3. 可选: 用 MeCoopt 代替 MeCo
   Source: Eq. (16), Inference from source
```

## 实现要点
- `meco.py` 中使用 `torch.randn(1,3,64,64)` 作为随机输入。
- 通过 forward hook 采集中间层输出。
- `torch.corrcoef` 计算相关矩阵，NaN/Inf 置零，再 `torch.linalg.eig` 取最小特征值。
- 搜索脚本通过 `--proj_crit meco` 接入。

## 证据与可追溯性
- Def. 3 / Eq. (12): MeCo 核心定义。
- Eq. (16): MeCoopt 修正。
- Supplementary App. C Algorithm 1: 搜索流程。
- 代码路径:
  - `correlation/foresight/pruners/measures/meco.py`
  - `nasbench201/networks_proposal.py`

## 本地实现路径
- `D:/PRO/essays/code_depots/MeCo Zero-Shot NAS with One Data and Single Forward Pass via Minimum Eigenvalue of Correlation`
