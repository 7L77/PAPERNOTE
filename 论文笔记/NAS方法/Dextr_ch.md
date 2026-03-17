---
title: "Dextr_ch"
type: method
language: zh-CN
source_method_note: "[[Dextr]]"
source_paper: "Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature"
source_note: "[[Dextr]]"
authors: [Rohan Asthana, Joschua Conrad, Maurits Ortmanns, Vasileios Belagiannis]
year: 2025
venue: TMLR
tags: [nas-method, zh, zero-cost-proxy, training-free-nas, svd, curvature]
created: 2026-03-16
updated: 2026-03-16
---

# Dextr 中文条目

## 一句话总结
> Dextr 是一个无标签 zero-shot NAS 打分方法：用特征图逆条件数衡量收敛/泛化潜力，用输出外在曲率衡量表达性，再做调和式融合得到最终分数。

## 来源
- 论文: [Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature](https://openreview.net/forum?id=X0vPof5DVh)
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- 代码: https://github.com/rohanasthana/Dextr
- 英文方法笔记: [[Dextr]]
- 论文笔记: [[Dextr]]

## 适用场景
- 问题类型: 训练前架构排序与低成本 NAS 搜索。
- 前提假设: 可在初始化状态提取层特征；可通过轨迹输入估计输出曲率。
- 数据形态: 无标签输入即可计算（论文中强调可单样本）。
- 规模与约束: 候选多、无法逐个完整训练的场景。
- 适用原因: 同时覆盖“易训练性”与“表达能力”，减少单侧偏置。

## 不适用或高风险场景
- 目标是严格硬件时延最优而非精度相关排序。
- 高阶自动求导预算不足（曲率项开销明显）。
- 网络结构导致层特征 SVD 不稳定或不可比。

## 输入、输出与目标
- 输入: 初始化网络 \(f\)、无标签 batch \(x\)、轨迹参数 \(\theta\) 及曲线输入 \(g(\theta)\)。
- 输出: 每个架构的 Dextr 标量分数。
- 优化目标: 用低成本分数逼近最终性能排序。
- 核心假设: \(\sum_l 1/c_l(X_\phi)\) 越大代表 C/G 越好，\(\kappa(\theta)\) 越大代表表达性越强。

## 方法拆解

### 阶段 1: 特征图线性独立性项
- 前向得到各层特征图。
- 展平后做奇异值分解。
- 计算逆条件数信号 \(1/c_l(X_\phi)\)。
- Source: Sec. 3.3.1-3.3.3, Eq. (8), Appendix A.6

### 阶段 2: 外在曲率项
- 构造圆形轨迹输入 \(g(\theta)\)。
- 计算输出对 \(\theta\) 的一阶/二阶导，估计 \(\kappa(\theta)\)。
- Source: Sec. 3.2.2, Eq. (5), Eq. (8), Appendix A.6

### 阶段 3: 融合
- 对两项做 log 压缩后融合：
  \[
  \text{Dextr}=\frac{a\cdot b}{a+b},
  \quad
  a=\log\!\left(1+\sum_l\frac{1}{c_l(X_\phi)}\right),\;
  b=\log(1+\kappa(\theta))
  \]
- Source: Sec. 3.3.3, Eq. (8)

### 阶段 4: 搜索中使用
- 将 Dextr 作为候选排序准则，驱动 benchmark correlation 或 search pipeline。
- Source: Sec. 4.1-4.2, Table 1-3, Appendix A.7

## 伪代码
```text
Algorithm: Dextr Scoring
Input: 网络 f, 无标签输入 x, 轨迹参数 theta
Output: Dextr 分数 s

1. 在 x 上前向并记录各层特征 X_phi,l。
   Source: Appendix A.6
2. 对每层特征矩阵做 SVD。
   Source: Sec. 3.3.1-3.3.2
3. 计算 a = log(1 + sum_l 1/c_l(X_phi,l))。
   Source: Sec. 3.3.3, Eq. (8)
4. 生成 g(theta)，计算输出对 theta 的导数并估计 kappa(theta)。
   Source: Sec. 3.2.2, Eq. (5), Appendix A.6
5. 计算 b = log(1 + kappa(theta))。
   Source: Sec. 3.2.2, Sec. 3.3.3
6. 返回 s = a*b/(a+b)。
   Source: Sec. 3.3.3, Eq. (8)
```

## 训练流程
1. 不需要为每个候选进行完整训练。
2. 初始化候选架构。
3. 用无标签输入 + 曲率轨迹计算 Dextr。
4. 依据分数排序并搜索。
5. 仅对最终选中架构做完整训练评估。

Sources:
- Sec. 4.1-4.2, Appendix A.6-A.7.

## 推理流程
1. 给定新候选架构，初始化参数。
2. 运行 Dextr 打分。
3. 在候选池中进行排序比较。
4. 选出 top 架构进入下游训练/部署评估。

Sources:
- Sec. 4.1, Appendix A.6.

## 复杂度与效率
- 时间复杂度: 论文未给闭式。
- 空间复杂度: 论文未给闭式。
- 运行特征: DARTS 搜索中报告约 0.07 GPU days。
- 扩展性说明: 曲率项是主要额外开销。

## 实现备注
- 本地实现路径：
  - `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`
  - `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr_utils/no_free_lunch_architectures/length.py`
- 代码中的层项用 `min(s)/max(s)`（逆条件数）并跨层求和。
- 两侧都做 `log(1+·)` 后再融合。
- 曲率异常时会回退到仅 SVD 侧分数。

## 与相关方法关系
- 对比 [[MeCo]]: Dextr 增加了表达性曲率项。
- 对比 [[AZ-NAS]]: Dextr 是单代理融合，AZ-NAS 是多代理组装。
- 主要优势: 无标签、结构简单、解释路径清晰。
- 主要代价: 曲率计算贵，且在少数空间可能不稳（Appendix 的 NATS-Bench-SSS）。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2
- 关键表: Table 1, Table 2, Table 3, Table 4, Appendix Table 6-8
- 关键公式: Eq. (5), Eq. (7), Eq. (8), Appendix Eq. (22)
- 关键算法: Appendix A.6 的计算流程描述

## 参考链接
- arXiv: README 未给出明确 arXiv 链接（使用 OpenReview 版本）
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- 代码: https://github.com/rohanasthana/Dextr
- 本地实现: D:/PRO/essays/code_depots/Dextr

