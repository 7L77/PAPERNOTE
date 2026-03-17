---
title: "ParZC: Parametric Zero-Cost Proxies for Efficient NAS"
method_name: "ParZC"
authors: [Peijie Dong, Lujun Li, Zhenheng Tang, Xiang Liu, Zimian Wei, Qiang Wang, Xiaowen Chu]
year: 2025
venue: AAAI
tags: [NAS, zero-cost-proxy, training-free, predictor-based]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2402.02105
local_pdf: D:/PRO/essays/papers/ParZC Parametric Zero-Cost Proxies for Efficient NAS.pdf
created: 2026-03-17
---

# 论文笔记：ParZC

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | ParZC: Parametric Zero-Cost Proxies for Efficient NAS |
| 会议 | AAAI 2025 |
| arXiv | https://arxiv.org/abs/2402.02105 |
| 本地 PDF | `D:/PRO/essays/papers/ParZC Parametric Zero-Cost Proxies for Efficient NAS.pdf` |
| 官方代码 | 未在论文/arXiv页面公开明确官方仓库（已检索） |

## 一句话总结
> ParZC 把 [[Zero-Cost Proxy]] 从“节点同权求和”升级为“可学习的节点建模+可微排序优化”，在低样本 NAS 排序中显著提升 [[Kendall's Tau]] 与 [[Spearman's Rank Correlation]]。

## 核心贡献
1. 提出 **Parametric Zero-Cost Proxies (ParZC)**，将节点级 ZC 统计变成可学习特征，而不是直接求和（Sec. 3）。
2. 提出 **MABN**（Mixer Architecture with [[Bayesian Neural Network]]），显式建模节点统计不确定性（Sec. 3.2）。
3. 提出 **DiffKendall**（可微 Kendall Tau 近似）直接优化排序一致性（Sec. 3.3）。
4. 额外给出训练自由版本 **ParZC†**（非负正弦加权），无需训练即可增强已有 proxy（Sec. 3.4）。

## 问题背景
### 要解决的问题
- 现有 ZC proxy 默认“节点贡献同质”，但作者实证显示不同节点对性能预测贡献差异很大（Fig. 2）。
- 自动组合/搜索 proxy 的方法（如 EZNAS/HNAS）通常需要较多架构-精度样本，成本高。

### 现有方法局限
- 节点同权导致信息利用粗糙，排序上限受限。
- 在低样本场景，训练型 predictor 稳定性不足。

### 本文动机
- 用可学习参数化方式吸收节点异质性，并通过可微排序损失直接对齐“排名正确性”。

## 方法详解
### 1) 节点级 ZC 编码（Node-wise ZC Encoding）
- 对每个节点的 proxy 统计做 min-max 缩放，缓解尺度差异和方差不稳定（Sec. 3.1）。
- 输入可来自权重/激活/梯度/Hessian 等节点统计（Fig. 5）。

### 2) MABN：Mixer + Bayesian Network
- 使用类似 [[MLP-Mixer]] 的分段混合结构建模“跨节点/跨段交互”（Sec. 3.2）。
- 在 mixer 前后插入 Bayesian 层，通过概率反传估计不确定性。
- 直观理解：不仅学“哪个节点重要”，还学“重要性估计有多不确定”。

### 3) DiffKendall 排序优化
- 将 Kendall Tau 的符号函数替换为平滑可导形式，便于梯度优化（Sec. 3.3）。
- 目标直接对齐排序一致性，而非只拟合点估计误差。

### 4) ParZC† 非负加权（训练自由）
- 从 ParZC 学到的分布规律出发，设计正弦非负权重，给已有 proxy 做节点重加权（Sec. 3.4, Eq. 1）。
- 特点是无需额外训练，适合快速增强现有 ZC 指标。

## 关键公式
### 公式 1：节点统计归一化（Sec. 3.1）
\[
\varsigma(z_k(\mathcal{N}^{(m)})) = \frac{z_k(\mathcal{N}^{(m)})-\min(z_k(\mathcal{N}^{(m)}))}{\max(z_k(\mathcal{N}^{(m)}))-\min(z_k(\mathcal{N}^{(m)}))}
\]
含义：把每个架构的节点 proxy 拉到统一尺度，减少条件数问题。

### 公式 2：Bayesian 权重重参数化（Sec. 3.2）
\[
W_b = \mu + \log(1+e^{\rho}) \cdot \varepsilon,\quad \varepsilon \sim \mathcal{N}(0, I)
\]
含义：用可训练分布参数（\(\mu,\rho\)）表示权重不确定性。

### 公式 3：DiffKendall（Sec. 3.3）
\[
\tau_d = \frac{1}{\binom{L}{2}}\sum_{i\neq j}\sigma_\alpha(\Delta x_{ij})\,\sigma_\alpha(\Delta y_{ij})
\]
其中 \(\sigma_\alpha\) 是对符号函数的可导近似（sigmoid-based smoothing）。

## 关键图表与结论
### Figure 2（节点重要性）
- SynFlow/GradNorm/Fisher 的节点贡献高度不均，深层节点通常更关键。
- 直接支撑“节点同权假设不成立”。

### Figure 4 + Table 3（样本效率）
- 在 NB201 上，ParZC 在少样本区间（如 78 样本）已明显优于多类 predictor。
- 说明 ParZC 在低标注预算下更稳健。

### Table 1（跨搜索空间相关性）
- ParZC 在 NB101/NB201/NDS 多设置上总体优于传统 ZC proxy 与 ParZC† 变体。
- 典型值：NB201-CIFAR10 上 ParZC 达到 SP/KD = 90.4/70.6。

### Table 4（NB201 搜索结果）
- ParZC: CIFAR-10 94.36, CIFAR-100 73.49, ImageNet16-120 46.34。
- 搜索成本约 3000 GPU sec（约 50 GPU 分钟），效率与性能兼顾。

### Table 5（ViT 搜索空间）
- 在 AutoFormer 搜索空间（ImageNet-1k）取得 Top-1 75.5，0.05 GPU-days。
- 说明方法可迁移到 ViT，不局限 CNN 搜索空间。

### Table 7/8（消融）
- Mixer + Bayesian + NP 组合最优。
- 仅用 DiffKendall 作为损失即可取得最优 rank correlation（NB101 消融）。

## 实验设置速记
- 基准：[[NAS-Bench-101]]、[[NAS-Bench-201]]、NDS（DARTS/NASNet/ENAS），外加 ViT AutoFormer。
- 训练：Adam，lr=1e-4，wd=1e-3；batch(train/eval)=10/50。
- epoch：NB101=150，NB201=200，NDS=296。
- DiffKendall 平滑系数 \(\alpha=0.5\)。

## 批判性思考
### 优点
1. 问题定义准确，直接击中“节点同权”这一 ZC proxy 的结构性缺陷。
2. 排序目标与损失函数一致（DiffKendall），优化目标更贴近 NAS 实际使用方式。
3. 同时给出训练版与训练自由版，兼顾性能上限与落地成本。

### 局限
1. ParZC 仍依赖少量架构-性能样本，不是完全零监督。
2. 论文未公开明确官方代码链接，复现门槛高于“代码即论文”的工作。
3. 非负权重策略虽然有效，但解释性仍偏经验，缺少更强理论边界。

### 对你当前方向的启发（ZCP/鲁棒 NAS）
1. 可以把你现有 proxy 先做节点展开，再试 ParZC† 风格的非负重加权，成本最低。
2. 若有少量标注预算，优先尝试 DiffKendall 直训排序器，而不只做 MSE 回归。
3. 在鲁棒 NAS 场景可把“clean/robust 双目标排名”统一为可微排序目标。

## 关联概念
- [[Zero-Cost Proxy]]
- [[DiffKendall]]
- [[Bayesian Neural Network]]
- [[MLP-Mixer]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
- [[Neural Architecture Search]]
- [[NAS-Bench-101]]
- [[NAS-Bench-201]]

## 速查卡片
> [!summary] ParZC
> - 核心问题: ZC 节点同权导致排序信息损失
> - 核心方法: Node-wise 编码 + MABN + DiffKendall
> - 关键收益: 低样本下更高排序相关性，跨 NB101/NB201/NDS/ViT 有效
> - 成本特征: 训练约 50 GPU 分钟（NB201 报告）
