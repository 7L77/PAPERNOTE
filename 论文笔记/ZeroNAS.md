---
title: "ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning"
method_name: "ZeroNAS"
authors: [Caixia Yan, Xiaojun Chang, Zhihui Li, Weili Guan, Zongyuan Ge, Lei Zhu, Qinghua Zheng]
year: 2022
venue: TPAMI
tags: [NAS, GAN, ZSL, GZSL, differentiable-search]
zotero_collection: ""
image_source: local
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/ZeroNAS_Differentiable_Generative_Adversarial_Networks_Search_for_Zero-Shot_Learning.pdf
local_code: D:/PRO/essays/code_depots/ZeroNAS Differentiable Generative Adversarial Networks Search for Zero-Shot Learning
created: 2026-03-17
---

# 论文笔记：ZeroNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning |
| DOI | https://doi.org/10.1109/TPAMI.2021.3127346 |
| 代码 | https://github.com/caixiay/ZeroNAS |
| 本地 PDF | `D:/PRO/essays/papers/ZeroNAS_Differentiable_Generative_Adversarial_Networks_Search_for_Zero-Shot_Learning.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/ZeroNAS Differentiable Generative Adversarial Networks Search for Zero-Shot Learning` |

## 一句话总结
> ZeroNAS 把 [[Differentiable Architecture Search]] 引入 [[Zero-Shot Learning]] 的 GAN 特征生成范式，通过联合搜索生成器/判别器结构，在多个 ZSL/GZSL 基准上稳定超过手工架构。

## 核心贡献
1. 首次把 NAS 显式用于 ZSL 场景中的 GAN 架构设计，不再固定手工 G/D 结构。
2. 构造了适合特征合成的 MLP DAG 搜索空间，支持可变隐藏层维度与多种 FC 类操作。
3. 提出面向 GAN 的双层对抗搜索优化：G 和 D 的结构参数与权重参数交替更新，并做边剪枝+算子剪枝得到离散架构。

## 问题背景
### 要解决的问题
- 现有 GAN-based ZSL（如 f-CLSWGAN、LisGAN、AFC-GAN）常依赖人工设计结构，跨数据集泛化不稳定。
- 直接套用图像生成 GAN 的 NAS 方法（AutoGAN/AGAN/DEGAS）并不适合 ZSL 的“特征生成”目标。

### 本文动机
- 对 [[Generative Adversarial Network]] 而言，G 与 D 强耦合，单独搜索 G 容易破坏对抗平衡。
- 因此应在统一搜索过程中联合优化 G/D 结构。

## 方法详解
### 1) 搜索空间（Sec. 3.2, Fig. 2）
- 以 DAG 表示 MLP：3 个输入节点（语义、噪声、拼接）+ 多个中间节点 + 输出节点。
- 每条边是混合操作 `MixedLayer`，候选操作为 8 类 FC 变体：`fc_relu/fc_lrelu/fc_bn_relu/fc_bn_lrelu` 及对应 dropout 版本。
- 每个中间节点聚合所有前驱，且前驱边与边内操作都用 softmax 权重。

### 2) 关键公式
#### Eq. (1) GAN 目标（WGAN + 分类）
$$
\min_{u_g}\max_{u_d}\;L_{WGAN}(u_g,u_d)+\lambda_1 L_{CLS}(u_g\mid u_c^*)
$$
- `u_g/u_d` 是 G/D 网络参数，`u_c^*` 是预训练分类器参数。

#### Eq. (2) 边内混合操作
$$
M(v_i\!\to\!v_j)=\sum_{o_k\in O}
\frac{\exp(\alpha^{\{v_i,v_j\}}_k)}{\sum_m \exp(\alpha^{\{v_i,v_j\}}_m)}\,o_k(f_i)
$$
- `alpha` 决定某条边上各候选算子的权重。

#### Eq. (3) 节点聚合
$$
f_j=\sum_{i<j}
\frac{\exp(\beta_i^{v_j})}{\sum_n\exp(\beta_n^{v_j})}
\sum_{o_k\in O}\frac{\exp(\alpha_k)}{\sum_m\exp(\alpha_m)}o_k(f_i)
$$
- `beta` 决定前驱边重要性，`alpha` 决定边内操作重要性。

#### Eq. (5) 对抗双层架构搜索
$$
\min_{v_g}\max_{v_d} L_{val}(u_g^*(v_g),u_d^*(v_d),v_g,v_d),\;\;
u_g^*,u_d^*=\arg\min_{u_g}\arg\max_{u_d} L_{tr}(u_g,u_d,v_g,v_d)
$$
- 上层优化架构参数 `v_g/v_d`，下层优化网络参数 `u_g/u_d`。

#### Eq. (10) 最终分类器训练
$$
\min_{u_c}-\frac{1}{|X|}\sum_i
\log\frac{\exp(u_c(y)^\top x_i)}{\sum_{y_j\in Y}\exp(u_c(y_j)^\top x_i)}
$$
- 用合成特征训练 softmax 分类器评估 ZSL/GZSL。

### 3) 搜索与剪枝（Sec. 3.3-3.4, Alg. 1）
- 交替更新四组参数：`v_d -> u_d -> v_g -> u_g`。
- 剪枝分两步：
1. 每个中间节点保留权重最高的两条入边。
2. 每条保留边只保留权重最高的一个操作。

## 重要图表与结论
### Figure 1
- 对比了手工 GAN、RL-based GAN NAS 与 ZeroNAS 的“联合搜索 G/D”思路。

### Figure 2
- 展示 DAG 搜索空间与 mixed operation。

### Figure 3
- 给出 CUB/FLO/SUN/AWA 的搜索后 G/D 结构，显示明显数据集依赖性。

### Figure 4
- t-SNE 可视化显示 ZeroNAS 生成的 unseen 特征与真实特征重叠更好。

### Figure 5
- 结构迁移性较弱：跨数据集直接迁移会明显掉点。

### Figure 6
- 搜索阶段收敛略慢于训练阶段，但整体效率可接受。

### Table 1（ZSL）
- 相比 f-CLSWGAN 手工结构，ZeroNAS 带来：
  - CUB: `57.3 -> 60.2`（+2.9）
  - FLO: `66.0 -> 69.0`（+3.0）
  - SUN: `58.9 -> 61.4`（+2.5）
  - AWA: `67.8 -> 71.3`（+3.5）

### Table 2（GZSL）
- 对 f-CLSWGAN 的 harmonic mean `Ah` 提升：
  - CUB +2.9，FLO +3.4，SUN +1.3，AWA +1.6。
- 在多个基线（LisGAN/GAZSL/AFC-GAN 等）上，重搜架构普遍继续提升。

### Table 3（消融）
- 只搜 G 或只搜 D 都优于 baseline；
- “Fixed D（只搜 G）”通常更强，说明生成器结构对最终表现更敏感；
- 同时搜索 G+D 最优。

## 代码对照（本地仓）
- `clswgan.py`：实现搜索阶段，训练集一分为二做 train/valid，四个优化器分别管理 G/D 的权重与架构参数。
- `model.py`：`MLP_search` 中 `edge_alpha` 与 `operation_alpha` 经 softmax 得到权重；`get_cur_genotype()` 实现“每节点 top-2 边 + 每边 top-1 操作”离散化。
- `clswgan_retrain.py`：固定 `genotype_G/genotype_D` 后从头训练，再用 `generate_feature.py` 做特征合成评估。
- `README.md`：明确“搜索性能 != 最终性能”，必须重训练后再评测。

## 批判性思考
### 优点
1. 把 GAN 对抗训练与可微 NAS 统一在一个可执行框架中，思路清晰。
2. 在多数据集、多 GAN 基线下都能稳定带来提升，实证充分。
3. 搜索成本相对可控（文中报告 FLO/CUB 约 1.5/2 GPU 小时）。

### 局限
1. 数据集依赖明显，跨数据集迁移差，需重复搜索。
2. 搜索空间仍是 MLP 特征生成范式，未覆盖更复杂生成器设计。
3. 官方实现依赖较老栈（Python 3.6 / PyTorch 0.3.1），现代复现实务成本偏高。

## 关联概念
- [[Zero-Shot Learning]]
- [[Generalized Zero-Shot Learning]]
- [[Generative Adversarial Network]]
- [[WGAN-GP]]
- [[Differentiable Architecture Search]]
- [[Neural Architecture Search]]

