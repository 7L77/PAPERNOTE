---
title: "REP_ch"
type: method
language: zh-CN
source_method_note: "[[REP]]"
source_paper: "REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search"
source_note: "[[REP]]"
authors: [Yuqi Feng, Yanan Sun, Gary G. Yen, Kay Chen Tan]
year: 2025
venue: IEEE TKDE
tags: [nas-method, zh, robust-nas, differentiable-nas, plugin, adversarial-robustness]
created: 2026-03-14
updated: 2026-03-14
---

# REP 中文条目

## 一句话总结
> REP 是一个可插拔的鲁棒 NAS 方法：先从“架构-鲁棒性轨迹”中采样鲁棒基元，再通过距离正则提高鲁棒基元的选择概率，从而提升鲁棒性并尽量保留自然精度。

## 来源
- 论文: [REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search](https://doi.org/10.1109/TKDE.2025.3543503)
- HTML: Not reported in the paper
- 代码: https://github.com/fyqsama/REP
- 英文方法笔记: [[REP]]
- 论文笔记: [[REP]]

## 适用场景
- 问题类型: 面向可微 NAS 的对抗鲁棒架构搜索。
- 前提假设: 搜索空间可表示为 `(edge, op)` 基元，且可在搜索中评估对抗鲁棒性。
- 数据形态: CNN 图像分类与 GNN 节点分类。
- 规模与约束: 适合需要 supernet 高效搜索、无法逐个完整训练候选架构的场景。
- 适用原因: 不替换原始 NAS 主干，只在搜索外围增加“采样 + 正则”模块。

## 不适用或高风险场景
- 搜索过程中无法稳定获得鲁棒性评估信号。
- 搜索空间不是基元化表达，难构造鲁棒基元指示矩阵。
- 你优先追求结构多样性而非 cell-based 体系内改进。

## 输入、输出与目标
- 输入: 搜索空间 `S`、搜索策略 `P`、架构序列 `A`、鲁棒性评分 `R`、权重系数 `lambda`。
- 输出: 同时兼顾鲁棒性与自然精度的最终架构。
- 优化目标: 在最小化验证损失的同时，最小化到鲁棒基元矩阵的距离。
- 核心假设: 相邻架构的微小基元差异更能解释鲁棒性变化。

## 方法拆解

### 阶段 1: 架构池构建与鲁棒评估
- 运行基础可微 NAS，逐 epoch 记录候选架构。
- 对唯一架构执行对抗评估，得到 `(A, R)`。
- Source: Sec. III-B, Algorithm 1 (lines 3-13), Sec. IV-C

### 阶段 2: 鲁棒基元采样
- 扫描相邻架构对。
- 若 `Ri < Ri+1`，把 `Ai+1 \ Ai` 加入 `B1`；否则把 `Ai \ Ai+1` 加入 `B2`。
- 取 `B = B1 ∩ B2` 作为鲁棒基元集合。
- Source: Sec. III-C, Algorithm 2, Fig. 2, Fig. 3

### 阶段 3: 概率增强搜索
- 用鲁棒基元构造二值矩阵 `alpha_R`。
- 在目标中加入 `||alpha - alpha_R||^2`，提升鲁棒基元被选概率。
- 仍保持双层优化框架，不改变可微 NAS 主流程。
- Source: Sec. III-D, Eq. (3)-(6)

## 伪代码
```text
Algorithm: REP
Input: 搜索空间 S, 可微 NAS 策略 P, 搜索轮数 N, 攻击评估器 Attack(.), 系数 lambda
Output: 鲁棒架构 A*

1. 初始化 A=[] 和 R=[]。
   Source: Sec. III-B, Algorithm 1
2. 对 i=1..N:
   2.1 执行一轮基础可微 NAS，得到架构 Ai。
       Source: Sec. III-B, Algorithm 1
   2.2 若 Ai 已存在于 A，复用历史鲁棒性得分。
       Source: Sec. III-B
   2.3 否则计算 Ri=Attack(Ai)，并记录到 (A,R)。
       Source: Sec. III-B (lines 7-11)
3. 逐对扫描 (Ai, Ai+1):
   3.1 若 Ri < Ri+1，将 Ai+1 \ Ai 加入 B1。
       Source: Sec. III-C, Algorithm 2
   3.2 否则将 Ai \ Ai+1 加入 B2。
       Source: Sec. III-C, Algorithm 2
4. 取 B = B1 ∩ B2 作为鲁棒基元。
   Source: Sec. III-C, Algorithm 2
5. 由 B 构造 alpha_R（二值指示矩阵）。
   Source: Eq. (3)
6. 优化:
      min_alpha L_val(w*(alpha), alpha) + lambda * ||alpha - alpha_R||^2
      s.t. w*(alpha) = argmin_w L_train(w, alpha)
   Source: Eq. (4)-(6)
7. 由优化后的 alpha 离散化得到最终架构 A*。
   Source: Eq. (2), Sec. III-D
```

## 训练流程
1. 基础 supernet 搜索（与原始可微 NAS 一致）。
2. 在搜索期间评估候选架构鲁棒性并构建架构池。
3. 采样鲁棒基元集合。
4. 加入距离正则执行概率增强搜索。
5. 对最终架构执行标准训练/对抗训练并报告指标。

Sources:
- Sec. III-B, III-C, III-D
- Sec. IV-C

## 推理流程
1. 固定搜索得到的最终架构。
2. 加载对应权重。
3. 在 clean 与对抗样本上评估（CNN: FGSM/PGD/APGD/C&W；GNN: 随机/DICE/节点嵌入攻击）。

Sources:
- Sec. IV-C, Sec. V-A, V-B
- Source: Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给闭式。
- 空间复杂度: 论文未给闭式。
- 实际开销:
  - CNN 搜索约 `0.7 GPU days`。
  - 分解为原始搜索 `~0.5`、鲁棒评估 `~0.18`、概率增强搜索 `~0.07`。
  - GNN 搜索约 `0.0015 GPU days`。
- 扩展性说明: 额外开销主要来自候选架构鲁棒评估。

## 实现备注
- 本地代码: `D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search`
- `CNN/darts/train_search.py`: 记录 genotype，并在搜索期执行 FGSM/PGD 验证鲁棒性。
- `CNN/darts/sample.py`: 根据架构序列与鲁棒分数构造 `B1/B2` 并求交。
- `CNN/darts/architect.py`: 注入鲁棒基元指示矩阵并加入欧氏距离正则（默认 0.01）。
- `GNN/architect.py`: 以 `NA_primitives` 为模板执行同类距离正则。
- 实务注意: 若攻击设置改变，通常需要重新采样并更新鲁棒基元模板。

## 与相关方法关系
- 对比 [[AdvRush]] 一类方法: REP 在“过程与结果”层面都提供更强基元级解释。
- 对比 [[DARTS]] / [[PDARTS]] / [[PCDARTS]]: 保持主干不变，主要增强鲁棒性。
- 主要优势: 插件化、可迁移、可解释。
- 主要代价: 需要搜索期对抗评估，且效果与攻击器选择相关。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6, Fig. 7
- 关键表: Table I, II, III, IV, V, VI, VII, VIII, IX, X
- 关键公式: Eq. (3), Eq. (4), Eq. (5), Eq. (6), 以及 DARTS Eq. (2)
- 关键算法: Algorithm 1, Algorithm 2

## 参考链接
- DOI: https://doi.org/10.1109/TKDE.2025.3543503
- 代码: https://github.com/fyqsama/REP
- 本地实现: D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search
