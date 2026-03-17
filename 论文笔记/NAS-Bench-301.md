---
title: "NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH"
method_name: "NAS-Bench-301"
authors: [Julien Siems, Lucas Zimmer, Arber Zela, Jovita Lukasik, Margret Keuper, Frank Hutter]
year: 2020
venue: arXiv
tags: [NAS, benchmark, surrogate-model, darts-search-space]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2008.09777
local_pdf: D:/PRO/essays/papers/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH.pdf
local_code: D:/PRO/essays/code_depots/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH
created: 2026-03-17
---

# 论文笔记：NAS-Bench-301

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH |
| arXiv | https://arxiv.org/abs/2008.09777 |
| 代码 | https://github.com/automl/nasbench301 |
| 本地 PDF | `D:/PRO/essays/papers/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH` |

## 一句话总结

> 这篇论文提出 [[Surrogate NAS Benchmark]]（NAS-Bench-301），用学习到的代理模型替代真实训练评估，在 DARTS 超大搜索空间（>10^18）上以秒级查询实现更现实且低成本的 NAS 基准。

## 核心贡献

1. 提出第一个覆盖 DARTS 级真实大空间（>10^18）的代理式 NAS 基准，而非仅能穷举小空间的表格基准（Sec. 1, Sec. 3）。
2. 在 NAS-Bench-101 上给出动机实验：代理模型可通过“跨架构平滑”降低单次 SGD 噪声影响，MAE 低于单次 lookup 的 tabular baseline（Sec. 2, Table 1）。
3. 构建并发布约 50k 架构评估数据，系统比较多种 surrogate（GIN / LGB / XGB 等），并分析泛化到未见优化器轨迹的能力（Sec. 3-4, Table 2-4）。
4. 证明 surrogate benchmark 能较好复现真实 benchmark 的优化器行为排序，同时把单次架构评估成本从 1-2 小时降到秒级（Sec. 5, Fig. 9-10）。

## 问题背景

### 要解决的问题

- 传统 NAS 评估成本高，很多方法只跑单次实验，统计显著性差。
- 现有 tabular benchmark 依赖“穷举所有架构”，导致搜索空间过小，与真实 NAS 场景差距大。

### 现有方法局限

- 小空间 benchmark 会高估局部搜索/随机搜索的竞争力。
- 单次训练噪声大时，tabular lookup 本质上是“按架构独立记忆”，无法利用相似架构之间的统计规律。

### 本文动机

- 既然架构性能预测已经是可学习问题，就可以用 surrogate 对大空间做近似评估，换取 realism + speed + repeatability。

## 方法详解

### 1) 数据集与搜索空间

- 搜索空间：DARTS cell-based space（normal/reduction 两个 cell，4 个中间节点，7 种算子）。
- 数据收集：10 类优化器轨迹 + 离散随机采样，共约 50k 架构。
- Table 2 给出的关键采样量：
  - RS 24047
  - DE 7275
  - RE 4639
  - TPE 6741
  - BANANAS 2243
  - COMBO 745
  - DARTS 2053
  - GDAS 234
  - RANDOM-WS 198
  - PC-DARTS 149

### 2) surrogate 候选与评估指标

- 候选模型：GIN、XGBoost、LightGBM、RF、SVR、BANANAS predictor 等（Sec. 4.1）。
- 评估指标：
  - R2（拟合误差）
  - [[Sparse Kendall Tau]]（近似忽略 0.1% 精度量化内的排序交换）

### 3) 核心结果（Table 3/4/5）

- Table 3（Test）：
  - GIN: R2=0.804, sKT=0.782
  - XGBoost: R2=0.886, sKT=0.820
  - LGB: R2=0.894, sKT=0.814
- 结论：树模型（XGB/LGB）在拟合上更强，GIN 在分布建模与后续 KL 指标上更稳。

- Table 4（Leave-One-Optimizer-Out）：
  - 左出 DARTS 时，LGB/XGB 的 R2 出现负值（-0.027 / -0.104），说明“未见轨迹外推”在某些分布上仍有挑战。
  - 但 sKT 在多数 left-out 设定仍保持较高，表明相对排序仍可用。

- Table 5（5 次重复评估上的噪声建模）：
  - GIN: MAE 1.64e-3，KL 3.2（最好）
  - LGB: MAE 1.44e-3，KL 63.1
  - XGB: MAE 1.46e-3，KL 113.9
  - 解释：LGB/XGB 点估计更准，但 GIN ensemble 的分布拟合更接近真实分布。

### 4) 作为 benchmark 的行为一致性

- Fig. 9/10 显示 surrogate 上的优化器轨迹与真实 benchmark 的排序趋势接近。
- 论文给出的真实 benchmark 单次运行成本约 >10^7 秒（约 115 天 GPU 时间），而 surrogate 可支持多次重复并给误差条。
- 随机搜索在该大空间不再是强 baseline，这与小空间 benchmark 的结论不同。

## 与代码实现的对照

- 官方代码仓：`automl/nasbench301`（已归档到本地）。
- README 提供了模型/数据下载与版本信息（v0.9/v1.0），并支持本地查询接口。
- 论文强调公平使用规范：把 surrogate 当黑盒 query，不直接“攻击 surrogate embedding”以免过拟合基准（Sec. 6）。

## 批判性思考

### 优点

1. 首次把 surrogate benchmark 推到真实 NAS 常用的超大搜索空间量级。
2. 同时讨论了点预测、排序、不确定性/分布拟合，不只是单指标比拼。
3. 给出了基准使用规范，降低“刷榜式过拟合 surrogate”风险。

### 局限

1. surrogate 质量仍依赖采样覆盖；优化器采样偏差会影响可泛化性。
2. 留一优化器实验里存在退化场景，说明对分布外轨迹仍不稳。
3. 主要在 DARTS 搜索空间与 CIFAR-10 设定展开，跨任务跨空间外推仍待验证。

### 可复现性评估

- [x] 代码开源
- [x] 数据/模型权重可下载（README 指向 figshare）
- [x] 指标和协议较完整
- [ ] 完整重跑成本仍高（真实 benchmark 部分）

## 关联概念

- [[Surrogate NAS Benchmark]]
- [[Surrogate Predictor]]
- [[Sparse Kendall Tau]]
- [[Kendall's Tau]]
- [[Neural Architecture Search]]
- [[One-shot NAS]]

