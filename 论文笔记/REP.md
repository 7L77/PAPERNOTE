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

## 一句话总结
REP 的核心是“先从搜索轨迹中识别鲁棒搜索基元，再在后续架构参数优化中提升这些基元被选中的概率”，从而同时兼顾自然精度与对抗鲁棒性。

## 方法主线
1. 运行基础可微 NAS（如 DARTS），记录搜索过程中出现的候选架构。
2. 对新出现的候选架构做对抗验证，得到鲁棒性分数。
3. 用相邻架构对 + 鲁棒性变化构造 `B1/B2`，交集得到鲁棒基元。
4. 构造鲁棒基元指示矩阵，在架构优化时加入距离正则项，拉近 `alpha` 与鲁棒基元模板。

## 公式（论文对应）
- 鲁棒基元指示矩阵：
  - 若 `(edge_m, op_n)` 属于鲁棒基元，则 `alpha_R[m,n]=1`，否则为 0。
- 距离正则：
  - `D(alpha) = ||alpha - alpha_R||^2`
- 搜索目标：
  - `min_alpha L_val(w*(alpha), alpha) + lambda * D(alpha)`
  - `s.t. w*(alpha) = argmin_w L_train(w, alpha)`

## 代码对应（CNN/darts）

### A. 架构池与鲁棒性分数如何收集
- 先跑普通可微 NAS，每个 epoch 搜索：
  - `train_search.py:74` 初始化 `archs = []`
  - `train_search.py:75` 初始化 `robustness = []`
  - `train_search.py:76` `for epoch in range(args.epochs)`
- 每个 epoch 取当前架构 `genotype`：
  - `train_search.py:89`
- 只保留新架构（去重）：
  - `train_search.py:91` `if genotype not in archs`
  - `train_search.py:92` `archs.append(genotype)`
- 对新架构做对抗验证并计分：
  - `train_search.py:95` 计算 FGSM 对抗精度
  - `train_search.py:96` 计算 PGD 对抗精度
  - `train_search.py:97` `R = 0.5 * (acc_FGSM + acc_PGD)`，写入 `robustness`
- 最终得到两条序列：
  - `train_search.py:101` 打印 `archs`
  - `train_search.py:102` 打印 `robustness`

### B. 攻击器细节在哪
- `train_search.py:170-171` FGSM（`eps=2/255`）
- `train_search.py:172-173` PGD（`eps=2/255, steps=4`）
- `train_search.py:175` 生成对抗样本 `adv_images`

### C. 鲁棒基元（B1/B2）如何得到
- `sample.py:17` 遍历相邻架构对
- `sample.py:21` 若 `R_i > R_{i+1}`，把差异基元加入 `B1`
- `sample.py:43` 若 `R_i < R_{i+1}`，把差异基元加入 `B2`
- `sample.py:70-76` 取 `B1` 与 `B2` 的交集，得到最终鲁棒基元集合

### D. 如何把鲁棒基元注入架构优化
- `architect.py:115-116` 取 `alphas_normal/reduce = softmax(alpha)`
- `architect.py:119-120` 计算到鲁棒模板的欧氏距离损失
- `architect.py:130` 将距离损失加入总损失 `loss += distance_loss_normal + distance_loss_reduction`

## 关键理解
- REP 不是直接改网络权重训练策略，而是改“架构参数 alpha 的优化偏好”。
- 架构池和鲁棒性分数是 REP 能工作的前提数据。
- `B1/B2` 交集的作用是降低偶然差异，保留更稳定的鲁棒基元信号。


### REP 里
**基元 (primitive)** 的粒度是 `(edge, op)`
	REP 的鲁棒基元是**某一条边上某个具体操作**，例如“(edge (2→4), 3×3 conv)” 被识别为鲁棒基元就意味着：在很多相邻架构对里，这个 `(edge,op)` 的出现/变化与鲁棒性提升一致。

为什么“edge 不等于 layer”
	**层（layer）** 通常指网络在前向传播路径上的一个计算模块（比如 conv+BN+ReLU），对应网络深度上的一个位置（macro layer）。
	**edge**是在 cell（micro-architecture）内部的连接：同一个 edge 在不同 cell 中会被重复堆叠（stack），因此一个 edge+op 并不是网络中单独一层，而是“某类局部连接”的模板，它在深网络里可以被复用多次（多个 cell）。
	可以把 _cell instance_ 当作一个宏观的“层/块（macro-layer）来处理（常用且合理）


Layer（宏观层 / macro layer）

Cell（微结构 / micro-architecture）
	整个网络由若干相同类型的 cell 被堆叠（repeat）组成。
	通常有两类 cell：**normal cell**（保持 spatial size）和 **reduction cell**（下采样）。

**Primitive（REP 里的基元）**：REP 把搜索空间量化为 `(edge, op)` 的粒度
	（cell 内某条边上选哪个操作）。这是一种 _微粒度_ 的结构元素