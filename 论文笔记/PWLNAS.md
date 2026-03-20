---
title: "Loss Functions for Predictor-based Neural Architecture Search"
method_name: "PWLNAS"
authors: [Han Ji, Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICCV
tags: [NAS, predictor-based, loss-function, ranking-learning, weighted-loss]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2506.05869v1
local_pdf: D:/PRO/essays/papers/Loss Functions for Predictor-based Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/Loss Functions for Predictor-based Neural Architecture Search
created: 2026-03-20
---

# 论文笔记：PWLNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Loss Functions for Predictor-based Neural Architecture Search |
| 会议 | ICCV 2025 |
| arXiv | https://arxiv.org/abs/2506.05869 |
| HTML | https://arxiv.org/html/2506.05869v1 |
| 官方代码 | https://github.com/jihan4431/PWLNAS |
| 本地 PDF | `D:/PRO/essays/papers/Loss Functions for Predictor-based Neural Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Loss Functions for Predictor-based Neural Architecture Search` |

## 一句话总结
> 这篇论文系统比较 predictor-based NAS 中 8 种损失函数，并提出阶段切换的 [[Piecewise Loss Function]]（PWLNAS），在多个搜索空间上稳定优于单一损失。

## 核心贡献
1. 首次在 predictor-based NAS 中统一比较回归、排序、加权三大类损失（主文 Sec. 3-4）。
2. 给出 13 个任务、5 个搜索空间上的大规模实验，并同时报告全局排序与 top-ranking 能力（主文 Sec. 4）。
3. 提出 PWLNAS：前期用回归/排序损失 warm-up，后期切到加权损失强化 top 架构识别（Sec. 4.3）。
4. 实验表明同一 predictor 在不同数据量、不同搜索空间、不同骨干下，最佳损失类型并不固定（Sec. 4-5）。

## 问题背景
### 要解决的问题
- 在 [[Surrogate Predictor]] 框架里，loss 会决定 predictor 学到“绝对精度”还是“排序关系”还是“头部架构偏好”。
- 过去大多数工作只用 MSE 或单一排序损失，缺少系统性比较与可迁移结论。

### 现有方法局限
- 只看全局相关性（如 [[Kendall's Tau]]）可能掩盖 top 架构筛选能力。
- 固定单一 loss 难以适应“训练样本从少到多”的动态搜索过程。

### 本文动机
- 把损失函数当作 NAS 搜索质量的核心杠杆，研究“何时该用哪类 loss”，并尝试阶段组合策略。

## 方法详解
### 1) 损失函数分组（8 个）
- 回归类：MSE。
- Pairwise 排序类：[[Pairwise Ranking Loss]]（HR, LR, MSE+SR）。
- Listwise 排序类：[[Listwise Ranking Loss]]（[[ListMLE]]）。
- 加权类：EW、[[MAPE Loss]]、[[WARP Loss]]。

### 2) 评测指标
- 全局排序：[[Kendall's Tau]]。
- 头部质量：[[Precision@T]]、[[N@K]]。
- 设计重点：NAS 的目标是找到最优架构，因此头部指标优先级更高。

### 3) PWLNAS（Piecewise Loss）
- 思路：固定单一损失改为按阶段切换损失。
- 早期（训练样本少）：用回归/排序损失让 predictor 先学稳定排序结构。
- 后期（训练样本增多）：切到加权损失，强化对高性能架构的区分。
- 论文给出的典型组合：
  - NAS-Bench-201 / DARTS: HR -> MAPE
  - NAS-Bench-101: ListMLE -> WARP
  - TransNAS-Bench-101 Micro: Jigsaw 用 MSE -> EW，其他任务用 HR -> WARP

## 关键公式
> 公式记号与标准化版本来自主文和补充材料（Suppl. A.1-A.7）。

### 公式 1：MSE（回归）
\[
\mathcal{L}_{MSE}=\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
\]
含义：直接拟合架构绝对性能。

### 公式 2：Pairwise 排序（以 LR/HR 为代表）
\[
\mathcal{L}_{LR}=\frac{1}{|\mathcal{N}|}\sum_{(i,j)\in\mathcal{N}}\log\!\left(1+\exp(-s_{ij}(\hat{y}_i-\hat{y}_j))\right)
\]
\[
\mathcal{L}_{HR}=\frac{1}{|\mathcal{N}|}\sum_{(i,j)\in\mathcal{N}}\max\left(0,m-s_{ij}(\hat{y}_i-\hat{y}_j)\right)
\]
含义：惩罚“相对顺序”错误的样本对。

### 公式 3：ListMLE（listwise）
\[
\mathcal{L}_{ListMLE}=-\sum_{i=1}^{n}\log\frac{\exp(\hat{y}_{\pi(i)})}{\sum_{k=i}^{n}\exp(\hat{y}_{\pi(k)})}
\]
含义：直接优化整张排序列表的一致性，而不只看样本对。

### 公式 4：加权损失（EW / MAPE / WARP）
\[
\mathcal{L}_{EW}=\frac{1}{n}\sum_i \exp(y_i-1)(y_i-\hat{y}_i)^2
\]
\[
\mathcal{L}_{MAPE}=\frac{1}{n}\sum_i\left|\frac{(1-\hat{y}_i)-b}{(1-y_i)-b}-1\right|
\]
\[
\mathcal{L}_{WARP}=\sum_i\sum_{j\in\mathcal{N}_i}L(rank_i)\cdot \max(0,1-\hat{y}_i+\hat{y}_j)
\]
含义：对高性能样本赋予更强优化权重，强调 top-ranking。

### 公式 5：PWLNAS 分段策略（概念式）
\[
\mathcal{L}_{PW}(t)=
\begin{cases}
\mathcal{L}_{warm}, & t \le t_{warm} \\
\mathcal{L}_{focus}, & t > t_{warm}
\end{cases}
\]
含义：按搜索阶段切换 loss，而不是全程固定。

## 关键图表与结论
### Figure 2/3（主文）
- 不同损失在 `Precision@0.5 / N@10 / Kendall's Tau` 上表现差异显著。
- 结论不是“某个 loss 永远最好”，而是“loss 与数据量、搜索空间、predictor 结构强耦合”。

### Table 1（不同 predictor 骨干）
- AP(MLP) 下 ListMLE 最稳；PINAT(Transformer) 下 WARP 的 top-ranking 更强。
- 说明“loss 选择”与“predictor 容量/泛化能力”共同决定最终效果。

### Table 2（NAS-Bench-201 搜索）
- PWLNAS(PW) 达到 CIFAR-10 `5.63`，与 Global Best 持平；其余数据集也优于多种基线。

### Table 3（NAS-Bench-101）
- PW 达到 `5.80`，优于 MSE/HR/ListMLE/WARP 的单独使用结果。

### Table 4（TransNAS-Bench-101 Micro）
- PW 在 Cls.O / Cls.S / Auto / Jigsaw 四任务均优于同表对比方法。

### Table 5（DARTS）
- PWLNAS(PW) 以 `2.47%` test error 超过 DCLP (`2.48%`) 等方法。

## 实验设置速记
- 搜索空间：[[NAS-Bench-101]], [[NAS-Bench-201]], [[TransNAS-Bench-101]], [[NAS-Bench-Graph]], DARTS。
- 指标：[[Kendall's Tau]]、[[Precision@T]]、[[N@K]]。
- predictor-based NAS 评测中，查询预算常用 50/100/150 架构级别（依任务而定）。
- DARTS 场景下，查询到的架构训练 50 epoch 作为 predictor 监督信号。

## 批判性思考
### 优点
1. 不是只提新 loss，而是给出跨设置的可执行经验，工程指导价值高。
2. 把“全局排序”和“头部识别”分开评估，贴合 NAS 实际使用目标。
3. PWLNAS 简单直接，几乎可无缝嵌入现有 predictor-guided 搜索流程。

### 局限
1. PW 阈值和切换策略仍依赖人工经验，自动化程度不足。
2. 主文强调结论跨搜索空间并不恒定，方法迁移仍需重新校准。
3. 官方仓库当前主要公开 predictor/loss 相关组件，完整搜索脚本尚未完全放出（README 明示）。

### 对你当前方向的启发（ZCP / 鲁棒 NAS）
1. 在低样本早期可先用 pairwise/listwise 训练 predictor，后期再切 weighted loss。
2. 若目标是“尽快找到 top 架构”，优先看 `Precision@T/N@K` 而不是只看 Kendall。
3. 可以把 PW 扩展成连续权重调度，而不是硬切换阈值。

## 关联概念
- [[Neural Architecture Search]]
- [[Surrogate Predictor]]
- [[Pairwise Ranking Loss]]
- [[Listwise Ranking Loss]]
- [[ListMLE]]
- [[WARP Loss]]
- [[MAPE Loss]]
- [[Piecewise Loss Function]]
- [[Kendall's Tau]]
- [[Precision@T]]
- [[N@K]]
- [[NAS-Bench-101]]
- [[NAS-Bench-201]]
- [[TransNAS-Bench-101]]
- [[NAS-Bench-Graph]]

## 速查卡片
> [!summary] PWLNAS
> - 核心问题: predictor-based NAS 的 loss 该如何选、何时切换
> - 核心方法: 回归/排序/加权损失系统评测 + 分段损失 PWLNAS
> - 关键结论: 低样本偏排序，高样本偏加权，组合优于单一
> - 代表组合: NB201 与 DARTS 上 HR -> MAPE
