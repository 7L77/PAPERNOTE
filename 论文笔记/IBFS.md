---
title: "Revisiting Neural Networks for Few-Shot Learning: A Zero-Cost NAS Perspective"
method_name: "IBFS"
authors: [Haidong Kang]
year: 2025
venue: ICML
tags: [NAS, few-shot-learning, training-free, information-bottleneck, zero-cost-proxy]
zotero_collection: ""
image_source: online
arxiv_html: https://proceedings.mlr.press/v267/kang25e.html
local_pdf: D:/PRO/essays/papers/Revisiting Neural Networks for Few-Shot Learning A Zero-Cost NAS Perspective.pdf
created: 2026-03-20
---

# 论文笔记：IBFS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Revisiting Neural Networks for Few-Shot Learning: A Zero-Cost NAS Perspective |
| 会议 | ICML 2025 (PMLR 267) |
| 主页 | https://proceedings.mlr.press/v267/kang25e.html |
| OpenReview | https://openreview.net/forum?id=fNixzmprun |
| 本地 PDF | `D:/PRO/essays/papers/Revisiting Neural Networks for Few-Shot Learning A Zero-Cost NAS Perspective.pdf` |
| 官方代码 | 论文/PMLR/OpenReview 未提供明确官方仓库（已检索） |

## 一句话总结
> IBFS 用 [[Information Bottleneck]] 驱动的 [[Zero-Cost Proxy]] 在初始化阶段直接估计架构表达性，把 [[Few-shot Learning]] 的架构搜索从“重训练”改成“近似零训练打分+快速适配”。

## 核心贡献
1. 给出一个面向 [[Model-Agnostic Meta-Learning]] 的一阶收敛视角（Theorem 4.1），将关注点从二阶项转向可高效评估的架构性质（Sec. 4, Eq. 3）。
2. 提出 IBFS：用 [[Information Bottleneck]] 推导出的熵型指标对未训练架构进行排序，避免传统 NAS 的大规模训练开销（Sec. 4.1, Eq. 4-10）。
3. 在 NAS-Bench-201、ImageNet-1k、mini/tiered-ImageNet few-shot 任务上同时实现较高精度和更低搜索成本（Tab. 1-4）。

## 问题背景
### 要解决的问题
- 传统 [[Neural Architecture Search]] 多针对固定任务；迁移到新 few-shot 任务时，要么从头搜、要么借用旧架构，成本或最优性都不理想。
- 适配式 meta-NAS（如 AutoMeta/MetaNAS）能跨任务，但搜索开销可达数十到数百 GPU-days。

### 现有方法局限
- 通用 zero-cost 指标（如 NASWOT）在 FSL 场景相关性不稳定，方差偏大。
- MAML 相关目标含二阶项，理论和计算都更复杂，不利于直接构造低成本架构评分。

### 本文动机
- 如果能从一阶角度解释收敛并构造与 FSL 相关性更强的 proxy，就有机会在“几乎不训练”的前提下完成架构筛选。

## 方法详解
### 1) 从 MAML 全局收敛到一阶近似（Sec. 4, Theorem 4.1）
- 作者给出收敛上界，核心结论是：在特定条件下，MAML 收敛可由一阶损失地形刻画。
- 含义：可以把“FSL 架构好坏”转化为“初始化附近可计算的表达性指标”。

### 2) IB 驱动的训练自由打分（Sec. 4.1）
- 用 [[Information Bottleneck]] 目标写成 `I(R;X) - βI(R;Y)` 形式（Eq. 5），再推导到可计算的熵项（Eq. 6-8）。
- 对每个候选架构 `F_i`，在未训练参数下输入 batch 数据，构造 [[Jacobian Matrix]]（Eq. 9），取谱信息并计算熵型 expressivity 分数（Eq. 10）。
- 直觉：分数越高，架构在收敛后更可能达到更高精度。

### 3) 搜索与适配流程（Sec. 5-6）
- 搜索阶段：在 NAS-Bench-201 / DARTS 空间内直接用 IBFS 分数排序，几秒到毫小时级完成候选筛选。
- 下游阶段：将搜索得到的 cell 架构用于 few-shot 训练（文中主要用 RFS 协议），验证在 mini/tiered-ImageNet 的 5-way 1-shot/5-shot 表现。

## 关键公式
### 公式 1：NAS 双层优化（Eq. 1）
\[
\min_{\alpha} L_{val}(W^*(\alpha), \alpha),\quad
W^*(\alpha)=\arg\min_W L_{train}(W,\alpha)
\]
含义：外层优化架构参数 `α`，内层优化网络权重 `W`。

### 公式 2：FSL 任务目标（Eq. 2）
\[
\min_{A, W^t}\sum_t L\big(D_t^{test}, G(D_t^{train}, \theta; A)\big)
\]
含义：在多任务上最小化 query loss，`G` 表示 support 集上的快速参数更新。

### 公式 3：IB 目标（Eq. 5）
\[
\mathcal{L}[p(r|x)] = I(R;X) - \beta I(R;Y)
\]
含义：在保留与目标相关信息的同时压缩无关信息。

### 公式 4：熵驱动的架构表达性分数（Eq. 9-10）
\[
J = \left(\frac{\partial f(x_1)}{\partial w},\ldots,\frac{\partial f(x_B)}{\partial w}\right)^\top,
\quad
S(F_i) \propto -\sum_k p(\lambda_k)\log p(\lambda_k)
\]
含义：基于 Jacobian 谱分布的熵来近似衡量未训练架构表达性。

## 关键图表与结论
### Figure 3 / Figure 4
- Fig. 3：作者比较 Entropy、KL、NASWOT 与真实精度关系，强调 Entropy 相关性更稳、方差更小。
- Fig. 4：随着训练 epoch 变化，熵与精度的 Kendall Tau 基本稳定，支持“初始化可评估”的主张。

### Table 1（NAS-Bench-201）
- IBFS 搜索时间约 3.82s。
- 测试精度约：CIFAR-10 94.37、CIFAR-100 73.09、ImageNet16-120 46.33。
- 文中报告其与真实排名的一致性（Kendall Tau）明显优于 NASWOT（0.752 vs 0.422）。

### Table 2（ImageNet-1k）
- IBFS 在 DARTS 空间报告 Top-1 76.7、Top-5 93.5。
- 搜索成本约 0.0042 GPU-days，低于多种训练式与训练自由基线。

### Table 3（Few-shot）
- mini-ImageNet 5-way：1-shot 64.55 ± 0.02，5-shot 81.52 ± 0.08。
- tiered-ImageNet 5-way：1-shot 72.56 ± 0.02，5-shot 86.73 ± 0.08。
- 相比 MetaNTK-NAS 等方法，搜索时长进一步下降到 0.1h 量级。

### Table 4（Transformer 设计）
- 在 AutoFormer 基准上，IBFS 报告 Top-1 76.5，搜索成本 0.03。
- 说明方法不局限于 CNN cell 搜索。

## 实验设置速记
- 搜索空间：NAS-Bench-201、DARTS、AutoFormer。
- Few-shot 数据：[[mini-ImageNet]]、[[tiered-ImageNet]]（5-way 1/5-shot）。
- 训练设置（下游）：SGD，momentum=0.9，wd=5e-4；miniImageNet 120 epoch，tieredImageNet 80 epoch。
- 硬件：RTX 2080Ti 为主，部分 A100 80G。

## 批判性思考
### 优点
1. 把 FSL-NAS 的核心瓶颈（搜索成本）压缩到非常低，并给出可操作的 proxy 设计。
2. 理论、proxy 构造、跨数据集实验形成了比较完整的链条。
3. 结果覆盖 CNN + Transformer 两类搜索场景，泛化叙事较完整。

### 局限
1. Theorem 4.1 依赖若干强假设（平滑性/强凸等），与实际深网设置仍有理论距离。
2. 主要实验集中在图像分类/FSL，跨模态或大规模预训练场景尚未验证。
3. 未公开明确官方代码，复现门槛和可验证性受影响。

### 对你当前 NAS/ZCP 方向的启发
1. 可把“谱分布熵”作为新的 proxy 维度，和现有 [[Zero-Cost Proxy]] 做融合打分。
2. 在低预算场景可先做“训练自由粗筛 + 少量训练精筛”的两阶段流程。
3. 可进一步检验熵型 proxy 在鲁棒 NAS 或 LLM NAS 搜索空间中的稳定性。

## 关联概念
- [[Few-shot Learning]]
- [[Model-Agnostic Meta-Learning]]
- [[Reptile]]
- [[Information Bottleneck]]
- [[Zero-Cost Proxy]]
- [[Jacobian Matrix]]
- [[Entropy]]
- [[KL Divergence]]
- [[Kendall's Tau]]
- [[Neural Tangent Kernel]]
- [[NAS-Bench-201]]
- [[mini-ImageNet]]
- [[tiered-ImageNet]]

## 速查卡片
> [!summary] IBFS
> - 核心问题: few-shot 新任务下，传统 NAS 搜索代价过高
> - 核心方法: 一阶收敛视角 + IB 熵型 zero-cost proxy
> - 关键收益: 在 FSL 与 ImageNet1k 上实现高精度/低搜索成本
> - 当前风险: 理论假设偏强、官方代码未公开
