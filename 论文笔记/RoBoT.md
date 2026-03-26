---
title: "RoBoT：鲁棒且增强的免训练神经架构搜索"
method_name: "RoBoT"
authors: [Zhenfeng He, Yao Shu, Zhongxiang Dai, Bryan Kian Hsiang Low]
year: 2024
venue: ICLR
tags: [nas, training-free-nas, bayesian-optimization, zero-cost-proxy, benchmark]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2403.07591v1
local_pdf: D:/PRO/essays/papers/Robustifying and Boosting Training-Free Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search
created: 2026-03-17
---

# 论文笔记：RoBoT

## TL;DR
> RoBoT 通过 BO 优化的线性加权融合多个免训练指标，得到更鲁棒的估计器；随后将剩余预算用于对高排名架构的贪心开发，以缩小代理评分与真实性能之间的估计差距。

## 元信息
| 条目 | 内容 |
|---|---|
| 论文 | Robustifying and Boosting Training-Free Neural Architecture Search |
| 会议 | ICLR 2024 |
| OpenReview | https://openreview.net/forum?id=qPloNoDJZn |
| arXiv | https://arxiv.org/abs/2403.07591 |
| Code | https://github.com/hzf1174/RoBoT |
| 本地 PDF | `D:/PRO/essays/papers/Robustifying and Boosting Training-Free Neural Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search` |

## 问题设定
- 目标：在固定搜索预算下，让免训练 NAS 在多任务场景中更稳定，并提升最终选中架构的质量。
- RQ1：能否将跨任务不稳定的单一免训练指标变得更鲁棒？
- RQ2：在得到鲁棒指标后，如何量化并利用代理评分与真实性能之间的估计差距？

## 核心贡献
1. 提出免训练指标的加权集成，并用 BO 为当前任务优化权重向量。
2. 基于 Precision@T 量化估计差距，并在高排名候选上进行贪心开发，提升最终架构选择质量。
3. 基于部分监测（Partial Monitoring）给出理论分析，在较温和假设下对期望排序性能提供界。
4. 在 NAS-Bench-201、TransNAS-Bench-101（micro/macro）和 DARTS 搜索空间上取得较强实证结果。

## 方法

### 1) 通过加权组合构建鲁棒指标（Sec. 4.1）
鲁棒指标定义为：

$$
M(A; w) = \sum_{i=1}^{M} w_i M_i(A)
$$

目标权重为：

$$
w^* = \arg\max_w f(A(w)), \quad A(w)=\arg\max_{A \in \mathcal{A}} M(A;w)
$$

来源：Sec. 4.1, Eq. (1)。

### 2) 用 BO 探索权重优化（Sec. 4.2, Alg. 1）
- BO 迭代提出权重向量。
- 对每个权重向量，RoBoT 选择其评分最高的架构；若该架构此前未被查询，则获取其目标性能反馈。
- 查询到的最优权重对应鲁棒估计器 \(M(\cdot; \tilde{w}^*)\)。

### 3) Precision@T 与开发阶段（Sec. 4.3, Alg. 2）
Precision@T 定义为：

$$
\rho_T(M,f)=\frac{|\{A\;|\;R_M(A)\le T \land R_f(A)\le T\}|}{T}
$$

随后将剩余预算用于在鲁棒指标排序后的前 \(T-T_0\) 个架构中进行贪心搜索。

来源：Sec. 4.3, Eq. (2), Eq. (3), Alg. 2。

### 4) 理论分析（Sec. 5）
- 论文将 Algorithm 1 映射到 [[Partial Monitoring]] 框架。
- 在类似全局可观测性条件和 BO 策略假设下，作者推导了 RoBoT 所选架构的期望排序上界。
- 关键结论见 Theorem 2（Eq. 5）。

## 关键结果

### NAS-Bench-201（Table 2）
- RoBoT: 94.36 / 73.51 / 46.34 (C10/C100/IN-16), search cost 3051 GPU-sec.
- 在与大量训练式方法相当或更低的成本下，优于或持平于表中最佳免训练/混合基线。

### TransNAS-Bench-101（Table 3）
- 在预算 100 下，RoBoT 在多数 micro 与 macro 任务上达到第一梯队或最优验证排名。
- 示例（micro）：Scene 2、Object 1、Jigsaw 17、Segment 4、Normal 8（越小越好）。

### DARTS 搜索空间上的 ImageNet 迁移（Table 4）
- RoBoT reports 24.1% top-1 error / 7.3% top-5 error, 0.6 GPU days search cost.
- 与 TE-NAS、HNAS、NASI-ADA 及多种经典 NAS 基线相比具有竞争力。

## 与归档代码的一致性核对

已核对仓库：
`D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search`

观察到的一致点：
1. `search_nb201.py` 与 `search_tnb101.py` 都实现了指标组合和 min-max 归一化。
2. BO 在 \([-1,1]\) 范围内搜索指标权重，跟踪最优已查询架构-性能对，并记录不重复查询的架构（对应 `T0` 行为）。
3. 开发阶段会在优化权重下扫描高排名架构，用完剩余预算。

值得注意的实现细节：
1. 脚本直接使用 BO 的 `ucb` 采集函数；论文理论部分提到 IDS 条件，因此实际代码路径可视为更简化的 BO 实例化。
2. 在 benchmark 脚本中，目标反馈来自表格化验证性能；在 DARTS 空间中，脚本会训练采样架构以获得验证信号。

## 优点
1. 清晰分离了鲁棒化（指标集成）与增强（预算约束下的开发）两个阶段。
2. 实用性强：可复用现有免训练指标与基准数据表。
3. 同时提供了实证收益与明确的理论框架。

## 局限性
1. 依赖候选池质量与目标查询预算。
2. 理论依赖若干假设（如可观测性相关条件），在真实搜索空间中不一定始终成立。
3. 权重优化仍引入 BO 额外开销，并对超参数较敏感。

## 相关概念
- [[Training-free NAS]]
- [[Bayesian Optimization]]
- [[Precision@T]]
- [[Partial Monitoring]]
- [[Information Directed Sampling]]
- [[NAS-Bench-201]]
- [[TransNAS-Bench-101]]
- [[Differentiable Architecture Search]]
