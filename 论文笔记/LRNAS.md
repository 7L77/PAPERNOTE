---
title: "LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture"
method_name: "LRNAS"
authors: [Yuqi Feng, Zeqiong Lv, Hongyang Chen, Shangce Gao, Fengping An, Yanan Sun]
year: 2025
venue: IEEE TNNLS
tags: [nas, adversarial-robustness, differentiable-nas, lightweight-model]
zotero_collection: ""
image_source: online
arxiv_html: https://doi.org/10.1109/TNNLS.2024.3382724
local_pdf: D:/PRO/essays/papers/LRNAS Differentiable Searching for Adversarially Robust Lightweight Neural Architecture.pdf
created: 2026-03-15
---

# 论文笔记：LRNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture |
| 期刊 | IEEE Transactions on Neural Networks and Learning Systems |
| DOI | 10.1109/TNNLS.2024.3382724 |
| 本地 PDF | `D:/PRO/essays/papers/LRNAS Differentiable Searching for Adversarially Robust Lightweight Neural Architecture.pdf` |
| 官方代码 | 未在论文正文与公开检索中发现明确官方仓库（截至 2026-03-15） |

## 一句话总结
> LRNAS 在 [[Differentiable Architecture Search]] 框架里，用 [[Shapley Value]] 评估 search primitive 对自然精度与对抗鲁棒性的联合贡献，再用贪心策略在参数预算内组装架构，得到更轻量且鲁棒的网络。

## 核心贡献
1. 提出基于 Shapley value 的 primitive 价值评估，把自然精度增益与鲁棒性增益同时纳入搜索目标（Sec. III-C, Eq. 3-8）。
2. 提出受模型大小阈值约束的贪心架构选择策略，在预算内尽可能保留高价值 primitive（Sec. III-D, Alg. 2）。
3. 在 CIFAR-10/100、SVHN、Tiny-ImageNet-200、ImageNet 上验证了“轻量 + 鲁棒 + 精度”三者兼顾的效果（Sec. V）。

## 问题背景
### 要解决的问题
- 对抗鲁棒性通常需要更高模型容量与更高训练成本。
- 现有“鲁棒+轻量”方案多依赖手工架构或压缩流程，架构本身未必最优。

### 现有方法的主要局限
- 一些方法会把“贡献有限”的组件也带入最终结构，导致冗余参数。
- 鲁棒 NAS 的搜索成本常偏高，且不同方法在轻量约束下稳定性不足。

### 本文动机
- 需要一个可解释、可微、可控参数预算的搜索机制，直接在搜索阶段平衡自然精度与鲁棒性。

## 方法详解
### 搜索空间与记号（Sec. III-A）
- 采用 DARTS 风格 [[Cell-based Search Space]]，每条边有候选操作集合 `O`。
- 架构参数 `alpha` 决定每条边最终保留的操作：

$$
o^{(i,j)} = \arg\max_{o \in O} \alpha_o^{(i,j)}
$$

（Eq. 2）

### Shapley 价值评估（Sec. III-C）
核心思想：把每个 search primitive 当作“合作博弈参与者”，按其在所有排列中的边际贡献定义价值。

$$
V_{o(i,j)}=\frac{1}{N!}\sum_{p \in P(O \times E)} \big[\Delta A_{o(i,j)}(p)+\Delta R_{o(i,j)}(p)\big]
$$

（Eq. 3）

- 其中 `Delta A` 与 `Delta R` 分别是移除该 primitive 后自然精度与鲁棒性变化（Eq. 4-7）。
- 为降低 `N!` 复杂度，使用随机采样排列的无偏估计：

$$
\hat{V}_{o(i,j)}=\frac{1}{n}\sum_{t=1}^{n}\big[\Delta A_{o(i,j)}(p_t)+\Delta R_{o(i,j)}(p_t)\big]
$$

（Eq. 8, Theorem 1 证明其无偏）。

- 价值与架构参数更新：

$$
V_i=(1-\mu)V_{i-1}+\mu\frac{\hat{V}(\omega_i,\alpha_{i-1})}{\|\hat{V}(\omega_i,\alpha_{i-1})\|}
$$

$$
\alpha_i=\alpha_{i-1}+\eta\frac{V_i}{\|V_i\|}
$$

（Eq. 9-10）

### 贪心架构选择（Sec. III-D, Alg. 2）
1. 先在每条边上取 `alpha` 最大的 primitive 候选。
2. 按其 `alpha` 值全局降序排序。
3. 在模型大小阈值 `lambda` 约束下逐个加入，直到预算上限。

该策略目标是在预算内最大化“高价值 primitive”覆盖率。

### 复杂度（Sec. III-E）
- Shapley 估计部分：`O(n * |O| * |E|)`。
- 贪心选择部分：`O(|O| * |E|)`。
- 总体由前者主导：`O(n * |O| * |E|)`。

## 关键图表与实验结论
### 关键图
- Fig. 1：对抗攻击与样本示意。
- Fig. 2：与 SOTA 对比，LRNAS 架构冗余更少。
- Fig. 3：整体流程示意（warm-up + Shapley 更新 + greedy 选型）。
- Fig. 4：单个排列中 primitive 依次移除并计算边际贡献。
- Fig. 5：NAS-Bench-201 上不同方法的 `alpha` 热力图。
- Fig. 6：primitive 平均价值与自然/鲁棒指标相关性可视化。
- Fig. 7：warm-up 与 greedy 的消融可视化。

### 关键表
- Table I/II：CIFAR-10/100 与 SVHN 白盒攻击结果。
- Table III：迁移黑盒攻击结果。
- Table IV/V：迁移到 Tiny-ImageNet-200 / ImageNet 的结果。
- Table VI：对抗剪枝（HYDRA）前后对比。
- Table VII：NAS-Bench-201 上 Kendall's tau 相关性对比。
- Table VIII：不同参数阈值 `lambda` 下搜索效果。
- Table IX：warm-up 与 greedy 组件消融。

### 结果要点（来自 Sec. V）
1. CIFAR-10 上，LRNAS 参数量约 2.1M，白盒下整体鲁棒性领先；C&W 为 43.90%，仅略低于 DSRNA 0.04%。
2. CIFAR-100 上，LRNAS 参数量约 2.3M，在三种攻击下鲁棒性领先，同时保持较高自然精度。
3. SVHN 上参数量约 2.2M，FGSM/PGD/C&W 鲁棒性最佳，自然精度略低于少数对手。
4. 搜索成本约 0.4 GPU days，低于多数对比方法（仅少数方法更低）。
5. NAS-Bench-201 上，LRNAS 的相关性（Kendall's tau）报告为 0.07（Nat.）与 -0.02（Adv.），优于对比。
6. 阈值消融显示 `lambda=2.0M` 取得较优综合折中；greedy 对减参和鲁棒性提升作用明显，warm-up 主要提升自然精度。

## 与代码实现对照
- 官方论文未提供明确可访问的官方实现链接（本文档生成时未发现）。
- 因未找到官方代码，方法细节均来自论文正文（Sec. III-V）与算法/公式描述。

## 批判性思考
### 优点
1. 把“可解释贡献分解”引入鲁棒轻量 NAS，目标明确。
2. 通过无偏估计缓解 Shapley 计算量问题，工程上可落地。
3. 贪心选型直接把参数预算纳入最终结构构建流程。

### 局限
1. Shapley 估计仍需多次采样，计算成本仍高于最便宜的一些 NAS 基线。
2. 主要在 cell-based 搜索空间验证，搜索空间表达力仍受限。
3. 论文也承认“更大空间 + 更低优化成本”仍未同时解决（Sec. VI）。

### 我的使用建议
1. 如果你当前目标是“2M~3M 参数 + 对抗鲁棒”，LRNAS 的策略值得优先复用。
2. 如果极限追求搜索成本，可先降低 `n` 做粗搜，再二阶段精搜。
3. 对新任务迁移时，建议先复现实验里的 `lambda` 扫描流程再定预算。

## 关联概念
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]
- [[NAS-Bench-201]]
- [[Kendall's Tau]]
- [[Shapley Value]]
