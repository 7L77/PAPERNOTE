---
title: "REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search"
method_name: "REP"
authors: [Yuqi Feng, Yanan Sun, Gary G. Yen, Kay Chen Tan]
year: 2025
venue: IEEE TKDE
tags: [nas, differentiable-nas, robust-nas, adversarial-robustness, plugin]
zotero_collection: ""
image_source: online
arxiv_html: https://doi.org/10.1109/TKDE.2025.3543503
local_pdf: D:/PRO/essays/papers/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search
created: 2026-03-14
---

# 论文笔记：REP

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | REP: An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search |
| 期刊 | IEEE Transactions on Knowledge and Data Engineering (Vol.37 No.5, 2025) |
| DOI | 10.1109/TKDE.2025.3543503 |
| 代码 | https://github.com/fyqsama/REP |
| 本地 PDF | `D:/PRO/essays/papers/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/REP An Interpretable Robustness Enhanced Plugin for Differentiable Neural Architecture Search` |

## 一句话总结
> REP 把“鲁棒性提升”从黑盒正则化目标转为“鲁棒搜索基元”的可解释构建过程：先采样鲁棒基元，再用距离正则提升其被选概率，从而同时兼顾自然精度与对抗鲁棒性。

## 核心贡献
1. 提出 [[Robust Search Primitive]] 视角：用搜索空间中的基元解释“为什么架构更鲁棒”，而不只看黑盒优化结果。
2. 提出基于相邻架构差分的鲁棒基元采样策略：通过 `B1/B2` 交集筛选稳定贡献鲁棒性的基元。
3. 提出概率增强搜索策略：在可微 NAS 的架构参数优化中加入到鲁棒基元指示矩阵的距离项，提升鲁棒基元入选概率，同时保留其他基元以维持自然精度。

## 问题背景
### 论文要解决什么问题
- 现有可微 NAS 多以自然精度为目标，面对 FGSM/PGD/C&W/APGD 等攻击时鲁棒性不足。
- 既有 robust NAS 往往把鲁棒性指标直接当正则项，过程可解释性弱，难回答“哪些结构元素导致鲁棒性提升”。
    Mok et al. [9] take the perspective of the input loss landscape
    Dong et al. [10] start from the Lipschitz constant and the adversarial robustness of architectures, and then explore the relationship between both.
    Hosseini et al. [11] propose two adversarial robustness metrics based on the certificated lower bound and Jacobian regularization, and both metrics are enumerated and regularized to the objective functions of differentiable NAS to perform joint maximal optimization.
    Cheng et al. [12] design an adversarial noise estimator to generate adversarial examples under different attack strengths, and the adversarial losses of these examples are optimized together with the natural loss.
### 现有方法不足
- 只给“结果更鲁棒”，不给“结构层面可追溯因果”。

- 架构参数搜索可能过拟合验证集，后期自然精度下降（论文引用 DARTS 退化问题）。

### REP 的核心思路
- 在搜索过程中收集架构池与对应对抗鲁棒性评分。
- 通过相邻架构比较筛出鲁棒基元（而非直接依赖最终 `alpha` 大小）。
- 在后续搜索中对鲁棒基元做概率增强（距离正则），引导最终架构包含更多鲁棒基元。

## 方法详解
### 1) 搜索基元定义（Sec. III-A）
- 把可微 NAS 搜索空间重定义为基元集合：`(edge, op)`。
- 架构由多个基元组成，鲁棒基元定义为：在两个“鲁棒性上升/下降”的架构对比中，能一致指向鲁棒提升的基元。

### 2) 鲁棒基元采样（Sec. III-C, Algorithm 2）
- 使用相邻 epoch 的架构 `Ai, Ai+1` 与鲁棒性 `Ri, Ri+1`。
- 若 `Ri < Ri+1`，取 `Ai+1 - Ai` 加入 `B1`；反之取 `Ai - Ai+1` 加入 `B2`。
- 最终鲁棒基元集合 `B = B1 ∩ B2`。
- 作者通过 Fig.3 论证：相邻架构差异小但鲁棒性差异明显，适合定位关键基元；非相邻差异过大，不利于定位。

### 3) 概率增强搜索（Sec. III-D）
- 构造与 `alpha` 同维度二值矩阵 `alpha_R`：鲁棒基元位置为 1，其他为 0。
- 定义距离项 `D(alpha)=||alpha-alpha_R||^2`，并把它加入可微 NAS 的双层优化目标。
- 直观上：缩小 `alpha` 与 `alpha_R` 的距离，会提高鲁棒基元被选概率；同时仍通过验证损失约束自然精度。

## 关键公式（含解释）
### Eq. (3): 鲁棒基元指示矩阵
$$
\alpha^R_{m,n}=
\begin{cases}
1, & (e_m,o_n)\ \text{是鲁棒基元}\\
0, & \text{否则}
\end{cases}
$$
- 含义：把“已识别鲁棒基元”编码成结构先验。

### Eq. (4): 距离正则
$$
D(\alpha)=\|\alpha-\alpha^R\|_2^2
$$
- 含义：越小表示架构参数越偏向鲁棒基元。

### Eq. (5)-(6): 搜索目标
$$
\min_{\alpha}\ L_{val}(w^*(\alpha),\alpha)+\lambda D(\alpha)
$$
$$
\text{s.t.}\quad w^*(\alpha)=\arg\min_w L_{train}(w,\alpha)
$$
- `L_val` 保证验证性能（自然精度主导），`D(alpha)` 引导鲁棒基元选择，`\lambda` 做折中。

### DARTS 离散化（Eq. (2), 前置）
$$
o^{(i,j)}=\arg\max_{o\in O}\alpha_o^{(i,j)}
$$
- REP 不改变离散化方式，而是通过正则改变 `alpha` 分布。

## 关键图表解读
### Figure 1
- 给出 DARTS + REP 的整体流程：先常规搜索并评估鲁棒性，再采样鲁棒基元，最后概率增强搜索。

### Figure 2
- 用两组相邻架构示例展示 `B1/B2` 的构造与交集筛选逻辑。

### Figure 3
- 统计支持“相邻采样”的合理性：相邻架构差异基元少、但鲁棒性变化显著。

### Figure 4/5
- 在更强攻击设置下，REP 曲线整体更稳；含鲁棒基元的架构平均鲁棒性更高。

### Figure 6/7
- 架构池构建消融 + 基元可视化：鲁棒基元的确与鲁棒提升相关，且“只保留鲁棒基元”会损伤性能，支持“鲁棒+其他基元并存”的设计。

### Table I/II/III
- CNN 与 GNN 上总体性能对比：REP 在自然精度与多攻击鲁棒性上表现领先或均衡更优。
- 跨数据集迁移（CIFAR-10->CIFAR-100/ImageNet，Cora->CiteSeer/PubMed）仍保持优势，HRS 也领先。

### Table IV（明确数值）
- CNN 搜索总开销约 `0.7 GPU days`（原搜索约 `0.5`，鲁棒评估 `0.18`，概率增强搜索 `0.07`）。
- GNN 搜索约 `0.0015 GPU days`（鲁棒采样约 `0.0013`，其中鲁棒评估约 `0.0005`）。

## 与代码实现的对照
- 代码仓库：`https://github.com/fyqsama/REP`（本地已归档）。
- `CNN/darts/train_search.py`：在每个新 genotype 上执行 FGSM/PGD 鲁棒评估并记录架构池。
- `CNN/darts/sample.py`：根据架构序列与鲁棒性构造 `B1/B2` 并求交集，得到鲁棒基元。
- `CNN/darts/architect.py`：以二值矩阵形式注入鲁棒基元先验，使用欧式距离正则（默认系数 0.01）。
- `GNN/architect.py`：同样加入架构参数到鲁棒基元模板的距离损失（论文思想扩展到 GNN）。

## 批判性思考
### 优点
1. 可解释性比“纯鲁棒正则”更强，能定位到具体基元。
2. 插件化，能接到多种可微 NAS（DARTS/PDARTS/PCDARTS/SANE/SPOS）。
3. 跨 CNN/GNN、跨多攻击与迁移场景都给出实验支持。

### 局限
1. 仍依赖攻击器来采样鲁棒基元，攻击器偏好会影响基元分布。
2. 论文主战场仍是 cell-based 搜索，结构多样性有限。
3. 表格中未给出统一复杂度闭式表达，主要依赖经验开销统计。

### 可复现性
- [x] 开源代码可用
- [x] 关键流程（采样 + 概率增强）在代码中可定位
- [ ] 表格完整数值复现仍需完整数据与训练资源

## 关联概念
- [[Robust Search Primitive]]
- [[Probability Enhancement Search Strategy]]
- [[Harmonic Robustness Score]]
- [[Robust Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]
- [[Cell-based Search Space]]


## 代码详情
### 每个epoch取当前架构的genotype
