---
title: "Neural Architecture Dilation for Adversarial Robustness"
method_name: "NADAR"
authors: [Yanxi Li, Zhaohui Yang, Yunhe Wang, Chang Xu]
year: 2021
venue: NeurIPS
tags: [robust-nas, adversarial-robustness, architecture-dilation, neurips]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=55FrYwhCN6
local_pdf: D:/PRO/essays/papers/Neural Architecture Dilation for Adversarial Robustness.pdf
local_code: "Not archived (official code URL unavailable as of 2026-03-15)"
created: 2026-03-15
---

# 论文笔记: NADAR

## 元信息
| Item | Value |
|---|---|
| Paper | Neural Architecture Dilation for Adversarial Robustness |
| Venue | NeurIPS 2021 |
| Link | https://openreview.net/forum?id=55FrYwhCN6 |
| Local PDF | `D:/PRO/essays/papers/Neural Architecture Dilation for Adversarial Robustness.pdf` |
| Local code | Not archived (official URL unavailable) |

## 一句话总结
> NADAR keeps a strong clean-accuracy backbone fixed and learns a lightweight dilation branch under standard-loss and FLOPs constraints, so robust accuracy increases with limited clean-accuracy drop.

## 核心贡献
1. 提出神经架构“扩张”范式：不从零搜索整网，而是对已有 backbone 逐块挂接 NAS cell 形成 hybrid network（Sec. 3.1, Fig. 1, Eq. 2）。
2. 引入标准性能约束，显式限制 hybrid 标准损失不高于 backbone，减少鲁棒性提升时的精度损失（Sec. 3.2, Eq. 7, Eq. 13-14）。
3. 引入可微 FLOPs 约束，在鲁棒目标下同时优化计算成本（Sec. 3.3, Eq. 10-12）。
4. 用 [[Alternating Direction Method of Multipliers]] 分别处理架构参数与权重参数的约束优化（Sec. 3.4, Eq. 15-22）。

## 问题背景
- 研究对象：[[Adversarial Robustness]] 与标准准确率之间的 trade-off。
- 已有路线：
1. 训练层面（PGD/TRADES/FAT/FreeAT）能提升鲁棒性但常损失自然精度。
2. 结构层面（[[Robust Neural Architecture Search]]，如 [[RACL]] / [[RobNet]]）往往需要重搜索或牺牲较多标准精度。
- 本文思路：固定一个标准性能足够好的 backbone，仅学习“增量结构”去补鲁棒性。

## 方法详解

### 1. Hybrid network (Backbone + Dilation)
- 将 backbone 按分辨率划分为 `L` 个 block，每个 block 对应一个 dilation cell。
- 每层输出做逐元素相加：
`z_hyb^(l) = f_b^(l)(z_hyb^(l-1)) + f_d^(l)(z_hyb^(l-1), z_hyb^(l-2))`
- 整体分类器基于最终 `z_hyb^(L)`（Eq. 2）。

### 2. 目标函数与约束
- 对抗训练目标（min-max）见 Eq. 1。
- 架构层优化：最小化验证集对抗损失（Eq. 3-4）。
- 标准性能约束：
`L_std(f_hyb) - L_std(f_bck) <= 0`（Eq. 7, Eq. 13-14）。

### 3. FLOPs-aware differentiable search
- dilation cell 在 NASNet-like search space 中搜索（Sec. 3.1）。
- 用 [[Differentiable Architecture Search]] 风格的 softmax 混合操作与 edge normalization（Eq. 8-9）。
- 基于操作概率求期望 FLOPs（Eq. 10），并将 FLOPs 项加入目标（Eq. 11-12）。
- 训练代价控制：使用 partial channel connections（来自 PC-DARTS 思路）。

### 4. 约束优化（ADMM）
- 上层（架构参数）与下层（网络权重）都写成增广拉格朗日形式。
- 交替更新 `(alpha_d, lambda_1)` 与 `(omega_d, lambda_2)`（Eq. 17-18, Eq. 21-22）。

## 理论分析要点
- Theorem 1：hybrid 的标准误差上界由 backbone 标准误差与 `hb`/`hd` 的符号不一致项共同决定，解释了为什么要加标准约束（Sec. 4, Eq. 26 附近）。
- Theorem 3：在固定 backbone 的情况下，引入 dilation 分支可改善对抗误差上界中的关键项，支持“扩张提鲁棒”的可行性（Sec. 4, Eq. 31 附近）。

## 关键实验结果

### CIFAR-10（Table 1）
- `NADAR-B`: Natural `86.23`, PGD-20 `53.43`, AA `50.44`（AA 来自 Table 4）。
- 对比 WRN34-10 + PGD-7：Natural `87.25`, PGD-20 `45.84`。
- 在仅约 `1.02` 个点自然精度下降下，PGD-20 提升约 `+7.59`（Table 6 也给出同结论）。

### CIFAR-100（Table 2）
- `NADAR-B`: Natural `62.56`, PGD-20 `28.40`。
- 高于 RACL (`27.80`) 与 FreeAT-8 (`25.88`) 的对抗精度。

### Tiny-ImageNet（Table 3）
- ResNet-50 backbone 上，NADAR 在 PGD-4 / FreeAT-4 / FastAT 三种训练下都提高鲁棒精度。
- 代价是训练 GPU days 上升约 `1.8x ~ 2.4x`（文中描述）。

### AutoAttack 与黑盒攻击（Table 4-5）
- `NADAR-B` 在 APGD-CE/APGD-T-DLR/FAB-T/Square/AA 指标上均优于 PGD-7、FastAT、FreeAT-8。
- 黑盒场景中，对不同 source network 产生的扰动也更稳健。

## Ablation（Table 7）
- “separate objectives + standard constraint” 组合达到最好平衡：
1. Natural `85.97 +/- 0.26`
2. PGD-20 `53.18 +/- 0.25`
- 去掉标准约束时，对抗提升显著变弱。

## 实现与复现备注
- 本地归档 PDF：已完成。
- 官方代码：OpenReview 提供 URL `https://github.com/liyanxi12/NADAR`，当前不可访问（repository not found），故未能完成代码归档。
- 可复现关键点：
1. backbone 先训练到较高标准精度；
2. dilation 搜索时使用 FreeAT 降成本；
3. 保留标准约束与 FLOPs 约束，否则 trade-off 变差。

## 关联笔记
- [[RACL]]
- [[RobNet]]
- [[Adversarial Robustness]]
- [[PGD Attack]]
- [[FGSM]]
- [[Alternating Direction Method of Multipliers]]
- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]
- [[Neural Architecture Dilation]]
