---
title: "TRNAS: A Training-Free Robust Neural Architecture Search"
method_name: "TRNAS"
authors: [Shudong Yang, Xiaoxing Wang, Jiawei Ding, Yanyi Zhang, En Wang]
year: 2025
venue: ICCV
tags: [NAS, robust-nas, training-free-nas, zero-cost-proxy, adversarial-robustness]
zotero_collection: ""
image_source: online
arxiv_html: "https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html"
local_pdf: "D:/PRO/essays/papers/TRNAS A Training-Free Robust Neural Architecture Search Supplementary Material.pdf"
created: 2026-03-15
---

# 论文笔记：TRNAS

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | TRNAS: A Training-Free Robust Neural Architecture Search |
| 正文 | https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html |
| Supplement | D:/PRO/essays/papers/Yang_TRNAS_A_Training-Free_ICCV_2025_supplemental.pdf |
| Code | 未找到官方仓库（截至 2026-03-15） |
| 本地 PDF | `D:/PRO/essays/papers/TRNAS A Training-Free Robust Neural Architecture Search Supplementary Material.pdf` |

## 一句话总结

> TRNAS 通过训练前鲁棒性代理 [[R-Score]] + 多目标选择策略，在 [[Differentiable Architecture Search]] 风格搜索空间中高效筛出鲁棒架构，并在多种攻击下达到 SOTA 级鲁棒 NAS 表现。

## 核心贡献

1. 提出训练前鲁棒代理 `R-Score`，融合线性激活能力与特征一致性，对架构鲁棒性能进行无训练估计（正文 Sec. 3.1, Eq. (2)-(7)）。
2. 提出轻量多目标选择策略（MOS），缓解单目标进化搜索早熟与收敛不稳（正文 Sec. 3.2）。
3. 在 [[RobustBench]] 与 [[NAS-Rob-Bench-201]] 上均取得较强结果，且搜索成本低（正文 Table 2/3/4；补充 Table 1/2/3/4）。

## 问题背景

### 要解决的问题

鲁棒 NAS 依赖对候选架构做对抗训练评估，计算成本高，导致搜索效率低。

### 现有方法局限

- 标准 NAS 代理大多面向 clean accuracy，对鲁棒性排序不稳定。
- 部分鲁棒代理在 RobustBench 上出现大量重复分数，难以区分性能接近但鲁棒性不同的架构（补充 Sec. 3.6, Fig. 1）。
- 权重共享类鲁棒 NAS 代价高，迭代效率受限（正文 Sec. 1; 补充 Sec. 3.3）。

### 本文动机

作者希望用训练前可计算分数直接筛掉不鲁棒架构，再将进化搜索聚焦到高潜力区域，降低鲁棒 NAS 的整体开销。

## 方法详解

### 1) R-Score（训练前鲁棒性代理）

- 线性激活能力项（LAM）用于衡量局部扰动敏感性（正文 Sec. 3.1, Eq. (2)-(4)）。
- 特征一致性项（FRM）用于衡量跨样本全局稳定性（正文 Sec. 3.1, Eq. (5)-(6)）。
- 二者加权得到 `R-Score`（正文 Sec. 3.1, Eq. (7)）：

$$
R = \beta \cdot \text{LAM} + (1-\beta)\cdot \text{FRM}
$$

### 2) 多目标选择策略（MOS）

- 搜索过程同时考虑鲁棒指标、参数与 FLOPs，减少单目标偏置（正文 Sec. 3.2）。
- 根据聚类数量 `e` 构建 Pareto 候选并保留多样性（正文 Fig. 3；补充 Sec. 3.2 参数设置给出 `e=20`）。

### 3) 训练前搜索 + 训练后验证

- 搜索时用 `R-Score` 对候选架构打分并驱动进化更新。
- 得到最优架构后再做标准对抗训练，最终用 FGSM/PGD/AutoAttack 验证（正文 Sec. 4；补充 Sec. 3.2）。

## 关键图表与结果

### 正文关键结果

- Table 2（CIFAR-10）：TRNAS 在 clean 与多攻击下优于或持平多种鲁棒 NAS 基线。
- Table 3（CIFAR-100）：TRNAS 在鲁棒精度上保持优势。
- Table 4（Tiny-ImageNet）：TRNAS clean `54.7`、FGSM `42.5`、PGD20 `18.5`，综合表现领先。

### 补充关键结果

- Table 1（NAS-Rob-Bench-201）：TRNAS 达到 `79.6/69.7/69.2/53.5/48.1`（Clean/FGSM3/PGD3/FGSM8/PGD8），与 benchmark 最优持平。
- Table 2（效率）：TRNAS 每个有效评估 `2.42s`，有效率 `100%`，显著优于 ZCPRob 的单次耗时（补充 Sec. 3.3）。
- Table 4（20 次统计）：TRNAS 平均 Params `3.39±0.28`、FLOPs `549.84±38.91`，同时取得更优鲁棒指标，标准差较小。

## 实验设置与实现细节

- 搜索空间：DARTS cell-based（补充 Sec. 3.2）。
- 搜索更新：20 次进化，父代/子代规模各 50，累计评估约 1000（补充 Sec. 3.2）。
- 训练阶段：7-step PGD 对抗训练；CIFAR 120 epoch；Tiny-ImageNet 90 epoch（补充 Sec. 3.2）。
- 评估攻击：FGSM、PGD（20/100 steps）、AutoAttack，扰动预算 `8/255`（补充 Sec. 3.2）。
- 硬件：单卡 RTX 4090，PyTorch 2.0（补充 Sec. 3.2）。

## 批判性思考

### 优点

1. 训练前代理目标明确，且与鲁棒评估直接耦合。
2. 搜索效率较高，在多个数据集上表现稳定。
3. 提供了重复实验统计，显示方法方差较小。

### 局限

1. 理论解释目前是“简洁解释”，缺少更严格泛化界或误差界分析（补充 Sec. 3.6）。
2. 论文与补充未给出可核验的官方代码链接，复现门槛偏高。
3. 结果主要集中于 DARTS 风格空间，跨更大/异构空间的稳健性还需验证。

### 可复现性评估

- [x] 论文与补充材料可获取
- [ ] 官方代码已公开并可运行
- [x] 关键训练/评估超参数已给出
- [x] 攻击设置与硬件环境有描述

## 关联概念

- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[Differentiable Architecture Search]]
- [[R-Score]]
- [[RobustBench]]
- [[NAS-Rob-Bench-201]]
