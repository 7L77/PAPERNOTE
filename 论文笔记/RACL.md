---
title: "Adversarially Robust Neural Architectures"
method_name: "RACL"
authors: [Minjing Dong, Yanxi Li, Yunhe Wang, Chang Xu]
year: 2025
venue: TPAMI
tags: [NAS, robust-nas, differentiable-nas, adversarial-robustness, lipschitz]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: "D:/PRO/essays/papers/Adversarially robust neural architectures.pdf"
created: 2026-03-15
---

# 论文笔记：RACL

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Adversarially Robust Neural Architectures |
| DOI | https://doi.org/10.1109/TPAMI.2025.3542350 |
| 发表 | IEEE TPAMI, Vol.47 No.5, May 2025 |
| 方法名 | RACL (Robust Architecture Search with Confidence Learning) |
| 本地 PDF | `D:/PRO/essays/papers/Adversarially robust neural architectures.pdf` |
| 代码 | 论文正文未提供官方仓库链接（截至 2026-03-15 未定位到官方代码） |
| 方法笔记 | [[NAS方法/RACL]] |

## 一句话总结

> RACL 把 [[Adversarial Robustness]] 与 [[Lipschitz Constant]] 约束显式接到 [[Differentiable Architecture Search]] 中，并用 [[Confidence Learning]] + [[Log-normal Distribution]] 对架构参数建模，在不改搜索空间的前提下稳定找到更鲁棒的 cell。

## 核心贡献

1. 给出“架构参数 -> 网络 Lipschitz 上界 -> 对抗鲁棒性”的可优化链路（Sec. III-A/B, Eq. (2)-(10)）。
2. 提出把架构参数 `alpha`/`beta` 视为分布而不是点估计，采用对数正态采样，显式建模“参数置信度”（Sec. III-C, Eq. (11)-(12)）。
3. 用概率约束 `Pr(lambda_F <= lambda_F_bar) >= eta` 形成凸化的置信约束，并通过 [[Alternating Direction Method of Multipliers]] 求解（Eq. (13)-(19)）。
4. 在 CIFAR-10/100、Tiny-ImageNet、ImageNet 及 [[NAS-Bench-201]] 上，白盒/迁移黑盒均优于多种 NAS 与 robust NAS 基线（Sec. IV）。

## 问题背景

### 要解决的问题

现有对抗鲁棒方法主要优化权重 `W`，但架构 `A` 本身对鲁棒性有显著影响；直接做 robust NAS 又很贵，尤其对抗训练内层 max 开销大。

### 现有方法局限

- 普通 DARTS/PC-DARTS 只做可微架构搜索，不显式约束鲁棒相关量。
- robust NAS 很多仍依赖昂贵 adversarial training 或经验代理。
- 架构参数通常“同置信度 argmax 采样”，搜索-离散化 gap 大，稳定性差。

### 本文动机

把 Lipschitz 约束直接作用到架构参数分布上，让搜索阶段就偏向低 Lipschitz、且高置信的连接/算子组合，降低后续对抗训练负担。

## 方法详解

### 1) 从鲁棒目标到 Lipschitz 约束

- 对抗样本攻击目标（Eq. (1)）：在扰动预算内最大化分类损失。
- 损失差上界（Eq. (2)(3)）：`|F(x+delta)-F(x)| <= lambda_F ||delta||`，说明更小 `lambda_F` 往往更鲁棒。
- robust architecture 形式（Eq. (4)）：在优化 `W,A` 同时约束 `lambda_F` 的上下界。

### 2) 在可微 NAS 中展开到 cell/edge

- 使用 DARTS 风格 mixed operation（Eq. (5)），由 `alpha`（算子权重）和 `beta`（输入边权）控制。
- 推到网络级 Lipschitz 上界（Eq. (7)(9)(10)）：
  - 每个 edge 的常数由算子 Lipschitz 加权和给出。
  - 每个 cell 的常数由入边项累加。
  - 整网上界为各 cell 项乘积。
- 算子 Lipschitz 估计：pool/skip/zero 有解析值，卷积类用 [[Spectral Norm]]（文中用 power iteration 近似）。

### 3) 置信采样：把架构参数改成对数正态随机变量

- 令 `alpha ~ LN(mu_alpha, Sigma_alpha)`, `beta ~ LN(mu_beta, Sigma_beta)`。
- 选择对数正态的原因：采样值恒正，和 Lipschitz 正值约束一致。
- 利用“对数正态的乘积仍为对数正态、和可近似为对数正态”的性质，把 edge/node/network 的 Lipschitz 上界都写成可处理分布（Eq. (11)(12) 及后续推导）。

### 4) 置信约束与优化

- 关键概率约束（Eq. (13)）：`Pr(lambda_F <= lambda_F_bar) >= eta`。
- 通过 CDF 形式重写（Eq. (14)(15)）得到 `mu` 与 `sigma` 的显式关系。
- 最终目标（Eq. (16)）：交叉熵 + 梯度范数下界项 + 概率约束。
- 用 ADMM 变成 min-max（Eq. (17)-(19)）交替更新 `mu/sigma` 与对偶变量。

## 关键公式（提炼版）

### 公式 1：鲁棒性与 Lipschitz 上界

$$
|F(x+\delta)-F(x)| \le \lambda_F \|\delta\|
$$

含义：攻击半径固定时，`lambda_F` 越小，最坏扰动导致的损失漂移越小。

### 公式 2：DARTS mixed operation（节点更新）

$$
I^{(j)} = \sum_{i<j} \beta^{(i,j)} \sum_{o\in\mathcal O} \alpha_o^{(i,j)}\, o(I^{(i)})
$$

含义：RACL 沿用可微 NAS 超网表示，但后续不把 `alpha/beta` 当作确定值。

### 公式 3：网络 Lipschitz 上界（结构化展开）

$$
\lambda_F \lesssim C\prod_k\prod_j\sum_{i<j}\beta^{(i,j)}\sum_o\alpha_o^{(i,j)}\lambda_o
$$

含义：上界直接由架构参数驱动，因此可以“从架构端”优化鲁棒性。

### 公式 4：置信概率约束

$$
\Pr(\lambda_F\le \bar\lambda_F)\ge \eta
$$

含义：不仅要小上界，还要求“以至少 eta 的置信度”满足该上界。

## 关键图表与实验结论

### Figure 1-2

- Fig.1：RACL 总览（log-normal 采样 + Lipschitz 分布近似 + CDF 约束）。
- Fig.2：与传统可微 NAS 对比，强调“参数值 + 置信度”联合决策。

### Table I-III（带 AT）

- CIFAR-10：
  - FGSM `62.55%`，比 PC-DARTS `+1.47%`。
  - PGD100 `55.32%`，比 PC-DARTS `+2.96%`。
  - MIM `60.00%`，比 RobNet-free `+7.05%`。
- CIFAR-100：AutoAttack `25.55%`，比 DARTS `+1.25%`。
- Tiny-ImageNet：CW `42.99%`，比 NASNet `+1.06%`。
- ImageNet：PGD100 `31.24%`，比 DARTS `+1.27%`。

### Table IV-V（不带 AT / NAS-Bench-201）

- 无对抗训练也更鲁棒：CIFAR-10 AutoAttack `40.48%`，比 PC-DARTS `+7.61%`。
- NAS-Bench-201：
  - CIFAR-10 AutoAttack `27.88%`，比 GDAS `+6.13%`。
  - CIFAR-100 PGD100 `14.07%`，比 GDAS `+2.22%`。

### Table VI-VIII（迁移黑盒）

- 在 transfer-based closed-box 设置下，RACL 作为 target 的鲁棒精度整体最优。
- 作为 source 时也常产生更强迁移攻击，说明其决策边界与其他架构差异更明显。

### Table IX-X（稳定性与消融）

- 多次重训下，RACL 平均鲁棒精度更高且方差更小（如 AutoAttack `50.14%`, PGD20 `55.50%`）。
- 去掉置信学习或去掉梯度范数下界项都会掉鲁棒精度。
- `eta` 通过交叉验证取 `0.9` 最优。

## 训练/搜索设置（复现抓手）

- 搜索空间：8 ops（sep conv/dilated sep conv/pool/skip/zero）。
- 超网：8 cells（6 normal + 2 reduction），每个 cell 6 nodes。
- 搜索：50 epochs，batch 128，SGD 更新权重 + Adam 更新架构分布参数。
- 搜索成本：约 `0.5 GPU-day`。
- 重训（AT）：20-cell 网络，100 epochs，SGD，梯度裁剪 5。

## 批判性思考

### 优点

1. 把“架构鲁棒性”从经验现象提升到可优化约束，理论链条完整。
2. 通过分布化架构参数缓解了可微 NAS 的采样不稳定问题。
3. 实验覆盖白盒、黑盒迁移、多数据集与 NAS-Bench，证据较充分。

### 局限

1. 理论中对“和的对数正态近似”依赖近似质量，误差界未细化。
2. 仍需完整 search + retrain 流程；相比 training-free robust NAS 仍偏重。
3. 官方代码未在论文中给出，工程复现门槛高。

## 关联概念

- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Lipschitz Constant]]
- [[Spectral Norm]]
- [[Log-normal Distribution]]
- [[Confidence Learning]]
- [[Alternating Direction Method of Multipliers]]
- [[NAS-Bench-201]]
