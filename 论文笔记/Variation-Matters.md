---
title: "Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation"
method_name: "Variation-Matters"
authors: [Pavel Rumiantsev, Mark Coates]
year: 2025
venue: arXiv
tags: [NAS, zero-shot-nas, training-free-nas, stochastic-ordering, evolutionary-search]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2502.19657v1
local_pdf: D:/PRO/essays/papers/Variation Matters from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation.pdf
created: 2026-03-16
---

# 论文笔记：Variation-Matters

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation |
| arXiv | https://arxiv.org/abs/2502.19657 |
| HTML | https://arxiv.org/html/2502.19657v1 |
| 代码 | Paper 中未给出官方仓库；arXiv 页面未标注代码链接（截至 2026-03-16） |
| 本地 PDF | `D:/PRO/essays/papers/Variation Matters from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation.pdf` |

## 一句话总结
> 这篇工作把 [[Training-free NAS]] 中“多次评估只做平均”的思路，升级为“把打分当随机变量并做统计比较”，用 [[Mann-Whitney U Test]] 近似检验 [[Stochastic Dominance]]，在随机搜索和进化搜索上都更稳定地选到更好结构。

## 核心贡献
1. 提出排名函数波动分析框架：定义跨搜索空间的变异度指标 `Var_SS(r, B, V)`（Sec. 4.1, Eq. 1）。
2. 用统计比较替代均值比较：把每个架构的多次打分看作样本，用单侧 Mann-Whitney U-test 做 `Stat-MAX / Stat-TOPK`（Sec. 4.2, Alg. 1）。
3. 在 NAS-Bench-101/201 与 TransNAS-Bench-101 上验证：随机搜索和进化搜索大多数设定提升（Sec. 5.2, 5.3, Table 1-3）。

## 问题背景
### 要解决的问题
- 零训练 NAS 的排名函数（如 NTK、ReLU 距离、Eigenvalue score 等）受随机 batch、随机初始化影响较大。
- 传统做法是多次评估后取平均，但平均会丢掉“分布信息”（比如尾部风险、重叠程度）。

### 现有做法的局限
- 仅比较均值 `E[X] > E[Y]` 无法区分“均值接近但分布风险不同”的候选架构。
- 在进化搜索里，重复评估与重访架构会放大随机性，导致早期决策反复被推翻（Appendix F, Table 7）。

### 本文动机
- 既然一次 ranking 输出本质是随机样本，搜索过程应比较“分布谁更优”，而不只是“均值谁更大”。

## 方法详解
### 1) 排名函数波动度量（Sec. 4.1）
作者定义：

\[
\mathrm{Var}_{SS}(r,B,V)=\frac{1}{N_{SS}}\sum_{i=1}^{N_{SS}} \mathrm{CV}(M_i(B,V)),
\quad
M_i(B,V)=\{r(\mathrm{arch}_i,d_v)\}_{v=1}^{V}
\]

其中：
- `B`：batch size；
- `V`：每个架构评估次数；
- `CV(X)=Var(X)/Mean(X)`，对应 [[Coefficient of Variation]]。

该指标用于判断某 ranking function 在某搜索空间上的稳定性。

### 2) 统计比较替代平均比较（Sec. 4.2）
对两架构 A、B，不再比较 `mean(score_A)` 与 `mean(score_B)`，而是比较它们的随机样本是否满足随机占优：

\[
P(X>k)\ge P(Y>k),\ \forall k,\ \text{且对某些 }k\text{严格大于}
\]

实现上用单侧 Mann-Whitney U-test：
- `Stat-MAX`：逐个比较并维护“当前统计最优”；
- `Stat-TOPK`：重复调用 `Stat-MAX` 选出前 K。

### 3) 与搜索算法耦合（Sec. 4.2, Appendix B）
- Random Search：对每个 sampled 架构做 `V=10` 次评估，用统计比较排序。
- REA / FreeREA / Greedy Evolution：父代选择与最终选择都可替换成统计比较；缓存每个架构的多次评估样本以避免重复波动放大。

## 关键图表与结论
### Figure 1（波动性对比）
- 不同 ranking function 的 CV 相差很大。
- Eigenvalue score 与 ReLU distance 整体更稳；部分 NTK 类指标波动更大。

### Figure 3 / Figure 4（相关性）
- 架构准确率与 CV 常呈负相关（但非总是）。
- CV 与平均分在某些指标上高度相关，解释了“直接把 CV 加进评分”不稳定。

### Table 1（随机搜索）
- 统计比较相对平均比较在“几乎所有设定”提升，文中报告平均提升约 `+0.49`（Sec. 5.2）。

### Table 2 / 3（进化搜索）
- 在多数搜索空间与 ranking function 上，统计比较持续优于平均比较；
- FreeREA 通常最佳，且统计比较后优势更明显（Sec. 5.3）。

### Table 7（缓存实验）
- 缓存比 on-the-fly 重算更稳、更好，说明“搜索决策一致性”是性能关键因素之一（Appendix F）。

## 实验设置（可复现要点）
- 典型设置：`B=64`, `V=10`。
- 统计阈值：`p < 0.05`；阈值消融显示较优范围约 `0.025 ~ 0.075`（Appendix E, Fig. 5）。
- 搜索空间：NAS-Bench-101/201、TransNAS-Bench-101（含多个任务）。

## 批判性思考
### 优点
1. 思路通用：不依赖具体 proxy，可直接包裹在已有搜索流程外。
2. 额外开销低：复用已有多次评估，仅更换比较器。
3. 工程启发强：明确指出缓存机制不仅省算力，还提升稳定性。

### 局限
1. 对数据无关指标（SynFlow/LogSynFlow）优势不稳定，甚至可能不如平均（Sec. 5.3, Appendix C）。
2. 统计阈值仍是超参数，且不同空间可能有偏好（Appendix E）。
3. 未提供官方代码链接，落地需自行复刻细节（Alg. 1 + Appendix B）。

### 可改进方向
1. 直接做“分布级”搜索优化（作者在结论中也提出）。
2. 设计对初始化/批次更不敏感的 ranking function，与统计比较形成互补。
3. 做跨搜索空间自适应阈值或 Bayesian 比较器，减少手调。

## 关联概念
- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Coefficient of Variation]]
- [[Mann-Whitney U Test]]
- [[Stochastic Dominance]]
- [[Evolutionary Neural Architecture Search]]
- [[Neural Tangent Kernel]]
- [[Kendall's Tau]]
- [[NAS-Bench-201]]
- [[SWAP-NAS]]
- [[MeCo]]

