---
title: "RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection"
method_name: "RBFleX-NAS"
authors: [Tomomasa Yamasaki, Zhehui Wang, Tao Luo, Niangjun Chen, Bo Wang]
year: 2025
venue: TNNLS
tags: [nas, training-free-nas, zero-cost-proxy, rbf-kernel, activation-search]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2503.22733v3
local_pdf: D:/PRO/essays/papers/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection.pdf
local_code: D:/PRO/essays/code_depots/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection
created: 2026-03-16
---

# 论文笔记: RBFleX-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection |
| arXiv | https://arxiv.org/abs/2503.22733 |
| HTML | https://arxiv.org/html/2503.22733v3 |
| 官方代码 | https://github.com/Edge-AI-Acceleration-Lab/RBFleX-NAS |
| 本地 PDF | `D:/PRO/essays/papers/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection` |

## 一句话总结

> RBFleX-NAS 用 [[Radial Basis Function Kernel]] 同时建模激活输出与最后一层输入特征图的跨样本相似性，并用 [[Hyperparameter Detection Algorithm]] 自动找核参数，在多个 NAS 基准上提升了训练前排序质量与搜索到的 top-1 架构精度。

## 核心贡献

1. 提出 RBFleX-NAS：不再只看 ReLU 二值模式，而是同时建模激活输出矩阵 `X` 和最后层输入矩阵 `Y` 的相似性（Sec. III-A, Eq. (1)-(7)）。
2. 提出 HDA：从候选网络的样本统计中自动估计 `gamma_k` 与 `gamma_q`，避免昂贵网格搜索（Sec. III-B, Eq. (8)-(16)）。
3. 在 NAS-Bench-201 / NATS-Bench-SSS / NDS / TransNAS-Bench-101 上给出更高或更稳的 Pearson/Kendall 相关性，且 layer-based 基线中优势明显（Sec. IV-F, Table I-II, Fig. 12-14）。
4. 引入 NAFBee 激活函数设计空间，展示该方法可用于 activation search（Sec. IV-H, Table IV-V）。

## 问题背景

### 要解决的问题

训练型 NAS 成本高。训练前代理（zero-cost proxy）虽然快，但常见 layer-based 方法在低精度架构区间分辨力不足，且对非 ReLU 激活的搜索能力弱。

### 现有方法局限

- NASWOT/DAS 强依赖 ReLU 输出统计，对“低精度架构之间”的排序区分不够（Fig. 1(a), Fig. 13-14）。
- 只看激活层不足以刻画网络最终可分性，最后层输入特征图信息没有被充分利用（Sec. III-A）。

### 本文动机

将“激活输出差异 + 最后层输入特征图差异”联合建模，使用 RBF 核做更细粒度相似性评估，再用数据驱动的超参检测提高核函数敏感性。

## 方法详解

### 1) 特征采集

- 对每个输入样本，收集所有激活层输出并展平拼接得到向量 `x_i`。
- 收集最后层输入特征图并展平得到向量 `y_i`。
- 得到 `X in R^{N x Lk}`、`Y in R^{N x Lq}`（Sec. III-A, Fig. 4-5）。

### 2) 列归一化

- 对 `X` 和 `Y` 做列归一化（column-wise normalization）：
  - 论文指出 element-wise / row-wise 会削弱行间相关性，因此采用 column-wise（Eq. (1)）。

### 3) 双 RBF 相似矩阵

- 用 `gamma_k` 构建 `K`（基于 `X`），用 `gamma_q` 构建 `Q`（基于 `Y`）：
  - `K_ij = exp(-gamma_k ||x_i - x_j||^2)`（Eq. (2)）
  - `Q_ij = exp(-gamma_q ||y_i - y_j||^2)`（Eq. (3)）

### 4) 评分函数

- 原始形式：`score = log |K ⊗ Q|`（Eq. (6)）。
- 化简：`score = N * (log|K| + log|Q|)`（Eq. (7)）。
- 直觉：高质量架构应能让不同输入样本在这两类表示上都保持足够可分，从而形成更有信息量的核矩阵行列式。

### 5) HDA（超参数检测）

- 对任意两向量 `v_i, v_j`，用均值差与方差构造候选：
  - `D_ij = (m_i - m_j)^2`（Eq. (10)）
  - `G_ij = D_ij / (2*(s_i^2 + s_j^2))`（Eq. (13)）
- 分别在 `G_k` 与 `G_q` 取满足 `D_ij != 0` 的最小值：
  - `gamma_k = min G_k(i,j)`（Eq. (15)）
  - `gamma_q = min G_q(i,j)`（Eq. (16)）
- 论文用统计检验显示 HDA 显著优于“取最大值”与“随机 gamma”策略（Sec. IV-E, Fig. 11）。

## 关键公式

### Eq. (1): 列归一化
\[
\tilde{v}_{ij}=\frac{v_{ij}-\min(v_{:j})}{\max(v_{:j})-\min(v_{:j})}
\]
含义：按列缩放，保留样本间关系。

### Eq. (2)-(3): RBF 相似核
\[
K_{ij}=e^{-\gamma_k\|\tilde{x}_i-\tilde{x}_j\|^2},\quad
Q_{ij}=e^{-\gamma_q\|\tilde{y}_i-\tilde{y}_j\|^2}
\]
含义：分别从激活输出与最后层输入两路构建样本相似性。

### Eq. (6)-(7): 评分
\[
score=\log|K\otimes Q|=N(\log|K|+\log|Q|)
\]
含义：通过对数行列式聚合两路信息，避免直接操作大 Kronecker 矩阵。

### Eq. (13), (15), (16): HDA 核参数
\[
G_{ij}=\frac{D_{ij}}{2(s_i^2+s_j^2)},\quad
\gamma_k=\min G_k,\quad
\gamma_q=\min G_q
\]
含义：选择“能拉开样本差异且不过饱和”的核参数。

## 关键图表与实验结论

### Fig. 1 / Fig. 13 / Fig. 14

- 展示 NASWOT/DAS 在低精度区间混叠更明显，RBFleX-NAS 的 score-accuracy 关系更线性、更可分。

### Fig. 9

- 对初始化、batch size、image batch 三种扰动稳定，标准差远小于评分方差，说明排序一致性较强。

### Fig. 10 + Fig. 11

- RBF kernel + HDA 在 Pearson/Kendall 上优于 linear kernel / PSNR / SSIM。
- HDA 相比 max(G) 或随机 gamma，相关性更高且统计显著（P-value << 0.05）。

### Table I（NAS-Bench-201 / NATS-Bench-SSS）

- NAS-Bench-201 上，RBFleX 在 CIFAR-10 的 Pearson/Kendall 达到 `0.898 / 0.569`，明显高于 NASWOT `0.727 / 0.374`。
- NATS-Bench-SSS 上，RBFleX 在 CIFAR-100/ImageNet 的 Pearson 达 `0.855 / 0.869`，Kendall 达 `0.639 / 0.649`。

### Table II（TransNAS-Bench-101）

- 在 OC/SS 的 macro/micro 任务上，RBFleX 能达到较高相关性并找到更高精度或更高 mIoU 的架构。

### Table III + Fig. 15-17（搜索质量与成本）

- 在 sample size `S=1000` 时，RBFleX 在 NAS-Bench-201 / NATS-Bench-SSS 的 top-1 搜索精度整体领先训练前基线。
- DARTS 空间中，精度接近 ZiCo 但搜索速度更快（论文给出约 5.2x）。

### Table IV-V（NAFBee）

- VGG-19 / BERT 激活搜索中，RBFleX 能成功识别最佳激活配置，说明其可拓展到非 ReLU 设计空间。

## 与代码实现的对照（已归档仓库）

代码路径：`D:/PRO/essays/code_depots/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection`

1. 激活与最后层输入采集：
   - `register_forward_hook` 抓取 ReLU 输出拼到 `network.K`；
   - 最后模块的输入拼到 `network.Q`；
   - 见 `RBFleX_NAS-Bench-201.py` 与 `HDA.py` 的 `counting_forward_hook` / `counting_forward_hook_FC`。
2. 核矩阵与评分：
   - `Simularity_Mat` 实现 `exp(-gamma * dist2)`；
   - `torch.linalg.slogdet` 计算对数行列式；
   - `score = batch_size_NE * (K + Q)` 对应 Eq. (7) 化简。
3. HDA：
   - `HDA.py` 中按样本对计算 `M=(m1-m2)^2` 与 `s1,s2`；
   - 候选 gamma 计算 `M/(2*(s1+s2))`；
   - 最终取 `np.min` 作为 `GAMMA_K / GAMMA_Q`。

## 批判性思考

### 优点

1. 把“激活差异 + 最后层输入差异”联合建模，确实比纯 ReLU 二值统计更有判别力。
2. HDA 给出可解释且便宜的核参数策略，避免了人工调参。
3. 在多基准、多任务（分类/分割/NLP）上都做了验证，并包含搜索时间分析。

### 局限

1. 对 batch 构成与输入分布仍有依赖，跨域泛化边界有待进一步量化。
2. 仍需多次前向与特征拼接，超大模型和长序列时内存/IO 成本可能上升。
3. 文中主要在既有 benchmark 上报告，开放真实工业搜索空间的验证仍不充分。

### 复现性评估

- [x] 论文公开（arXiv/期刊信息可查）
- [x] 官方代码公开且已本地归档
- [x] 关键公式、实验设置、核心超参可追踪
- [ ] 一键复现实验脚本（跨全部基准）仍需额外工程整理

## 关联概念

- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Radial Basis Function Kernel]]
- [[Kronecker Product]]
- [[Hyperparameter Detection Algorithm]]
- [[Fisher Linear Discriminant]]
- [[NAS-Bench-201]]
- [[NATS-Bench-SSS]]
- [[TransNAS-Bench-101]]
- [[Activation Function Search]]
- [[Kendall's Tau]]

