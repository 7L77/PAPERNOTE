---
title: "Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights"
method_name: "VKDNW"
authors: [Ondrej Tybl, Lukas Neumann]
year: 2025
venue: arXiv
tags: [NAS, training-free-nas, zero-cost-proxy, fisher-information]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2502.04975v1
local_pdf: D:/PRO/essays/papers/Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights.pdf
created: 2026-03-14
---

# 论文笔记：VKDNW

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights |
| arXiv | https://arxiv.org/abs/2502.04975 |
| Code | https://github.com/ondratybl/VKDNW |
| 本地 PDF | `D:/PRO/essays/papers/Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights.pdf` |
| 本地代码 | 未完成归档（2026-03-14 连接 GitHub 443 超时） |

## 一句话总结

> 本文提出基于 [[Fisher Information Matrix]] 的零训练 NAS 代理分数 VKDNW，用参数估计不确定性的“谱熵”来排序架构，并提出 [[Normalized Discounted Cumulative Gain]] 更贴近 NAS 目标的评测方式。

## 核心贡献

1. 提出可在大模型上稳定估计经验 FIM 谱的实现方案（Sec. II-B, Eq. (8)-(10)）。
2. 提出训练前可计算的代理分数 `VKDNW`，并证明其与模型大小信息相对正交（Sec. II-C, Fig. 3/4, Table IV）。
3. 提出 TF-NAS 评测指标 `nDCG`，强调“是否能把好模型排到前面”，补足 KT/SPR 的不足（Sec. III, Eq. (14), Fig. 2）。

## 问题背景

### 要解决的问题

传统 NAS 需要对海量候选架构训练后再评估，成本极高。TF-NAS 希望用 cheap proxy 替代完整训练。

### 现有方法局限

- 单一 proxy 常受模型规模偏置影响，可能只是“偏爱大模型”。
- 常用评测（Kendall tau、Spearman rho）对“头部架构识别”不敏感。

### 本文动机

作者从 [[Cramer-Rao Bound]] 出发，把“权重可估计性/不确定性结构”转成可计算统计量，并把 NAS 的评价重点放回“top 架构检索能力”。

## 方法详解

### 1) Fisher 信息建模

- 把分类网络训练视为最大似然估计，定义 FIM（Eq. (2)）。
- 用 Cramer-Rao 下界解释：FIM 谱反映参数估计难度与方向不平衡性（Sec. II-A, Eq. (3) 及后续讨论）。

### 2) 经验 FIM 的可计算实现

- 经验 FIM 定义见 Eq. (8)。
- 采用分解形式避免数值不稳定，得到 `F_hat = (1/N) sum A_n^T A_n`（Eq. (9)-(10)）。
- 只采样少量代表参数（每层少量权重）降低维度并提升稳定性。
- 使用模型预测分布而非真实标签构造经验 FIM，因此可用随机输入（Sec. II-B）。

### 3) VKDNW 分数

- 从 FIM 谱取 decile（去掉极小/极大边界特征值），归一化后做熵：Eq. (11)。
- 直觉：谱越均衡，说明不同参数方向的不确定性更均匀，训练可估计性更好。

### 4) 用于排序的 size-aware 形式

- 单分数排序：`VKDNWsingle(f) = N_layers(f) + VKDNW(f)`（Eq. (12)）。
- 作用：先按规模粗分组，再在组内用 VKDNW 精排。

### 5) 评测指标与聚合

- 新指标 `nDCG_P`（Eq. (14)）更关注 top-P 的检索质量。
- 非线性聚合：`rank_agg = log(prod_j rank_j)`（Eq. (15)），聚合 V/J/E/T/F 五类分数（Sec. V-A）。
- 还给出 model-driven 聚合（随机森林等）作为补充。

## 关键公式

### Eq. (2): Fisher Information Matrix

$$
F(\theta)=\mathbb{E}[\nabla_\theta \sigma_\theta(c|x)\,\nabla_\theta \sigma_\theta(c|x)^T]
$$

含义：衡量参数扰动对预测分布的敏感性与信息量。

### Eq. (11): VKDNW 熵分数

$$
\text{VKDNW}(f)=-\sum_{k=1}^{9} \tilde{\lambda}_k\log \tilde{\lambda}_k,
\quad \tilde{\lambda}_k=\frac{\lambda_k}{\sum_{j=1}^9 \lambda_j}
$$

含义：用归一化特征值熵刻画“权重不确定性分布的均衡性”。

### Eq. (12): 单代理排序

$$
\text{VKDNW}_{single}(f)=\mathcal{N}(f)+\text{VKDNW}(f)
$$

其中 `N(f)` 是可训练层数代理。

### Eq. (14): nDCG

$$
\text{nDCG}_P=\frac{1}{Z}\sum_{j=1}^{P}\frac{2^{acc_{k_j}}-1}{\log_2(1+j)}
$$

含义：更重视高排名位置上的高精度架构。

## 关键图表

### Figure 1

- 在 ImageNet16-120 上，VKDNW 系列在 nDCG 上领先，且 KT/SPR 也保持竞争力。

### Figure 2

- 用 toy 例子说明：KT/SPR 可能认为某排序“相关性更高”，但 nDCG 能识别其 top 排名损坏。

### Figure 3 / Figure 4

- 展示 VKDNW 与模型规模（可训练层数或参数量）相关性更低，支持“正交信息”论点。

### Table I (NAS-Bench-201)

- `VKDNWsingle` 在 ImageNet16-120 上 `KT/SPR/nDCG = 0.622/0.814/0.608`。
- `VKDNWagg` 进一步提升到 `0.743/0.906/0.664`，优于 AZ-NAS 的 `0.673/0.859/0.534`。

### Table II (MobileNetV2 search)

- 在约 450M FLOPs 约束下，`VKDNWagg` 得到 `78.8` Top-1，优于 AZ-NAS 的 `78.6`，搜索成本同为 `0.4 GPU days`（最终训练仍昂贵）。

### Table V / VII / VIII

- 随机输入与真实输入表现接近；批量大小变化影响小。
- FIM 维度和层内采样策略有一定鲁棒区间（作者默认用 128 层采样与 batch size 64）。

## 实验设置与实现细节

- 搜索空间：NAS-Bench-201、MobileNetV2（Sec. V）。
- NAS-Bench-201 使用 9,445 个 unique 结构作为主报告（另给全 15,625 结果于补充）。
- 分数计算常用 64 张随机输入图像。
- model-driven 聚合在 1024 个架构上训练随机森林。
- MobileNetV2 实验在进化搜索中跑 100,000 次评估，保留 top 1024，再训练最终模型（480 epoch, SGD + cosine）。

## 与代码实现的对照

- 论文给出官方仓库：https://github.com/ondratybl/VKDNW。
- 本次尝试本地归档时，环境对 GitHub 连接超时（2026-03-14），因此未能完成代码级核查。
- 当前方法与实现细节解读以论文正文/补充文本为主。

## 批判性思考

### 优点

1. 理论动机明确：从 FIM 与统计估计理论推导 proxy，而非纯经验组合。
2. 评测视角改进到“top 架构检索”，更贴近 NAS 实际使用。
3. 在多个数据集和两个搜索空间上给出一致改进。

### 局限

1. proxy 中仍显式叠加了规模项 `N_layers`，在不同搜索空间的泛化边界仍需更多验证。
2. model-driven 聚合需要已知精度样本训练，降低了“完全零成本”属性。
3. 关键结论依赖补充材料中的细节（如采样稳定性），主文中不够展开。

### 可复现性评估

- [x] 论文公开
- [x] 官方代码链接公开
- [ ] 本地代码归档完成（本次因网络阻塞失败）
- [x] 公式与实验流程可追踪

## 关联概念

- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Fisher Information Matrix]]
- [[Cramer-Rao Bound]]
- [[Normalized Discounted Cumulative Gain]]
- [[NAS-Bench-201]]
