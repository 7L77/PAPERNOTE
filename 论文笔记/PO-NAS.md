---
title: "Per-Architecture Training-Free Metric Optimization for Neural Architecture Search"
method_name: "PO-NAS"
authors: [Anonymous Author(s)]
year: 2025
venue: "NeurIPS 2025 (under review submission)"
tags: [nas, training-free-nas, zero-cost-proxy, surrogate-model, evolutionary-search]
zotero_collection: ""
image_source: online
arxiv_html: ""
project_page: "https://anonymous.4open.science/r/PO-NAS-2953"
local_pdf: D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf
local_code: "Not archived (anonymous repository not found as of 2026-03-16)"
created: 2026-03-16
---

# 论文笔记：PO-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Per-Architecture Training-Free Metric Optimization for Neural Architecture Search |
| 状态 | 投稿 NeurIPS 2025（匿名投稿） |
| 代码链接 | https://anonymous.4open.science/r/PO-NAS-2953 |
| 本地 PDF | `D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf` |
| 本地代码 | 未归档（匿名仓库不可访问） |

## 一句话总结
> PO-NAS 通过代理模型学习**每个架构专属的多元免训练指标融合权重**，并结合贝叶斯优化 + 进化搜索，在有限真实训练预算下显著提升 NAS 排序质量。

## 核心贡献
1. 提出架构专属的指标融合方法（而非全局权重融合）：\(S(A;w_A)=\sum_i w_{A,i}\tilde Z_i(A)\)（Eq. 1）。
2. 构建编码器 + 指标预测器 + 交叉注意力权重生成器的代理结构，学习**架构条件化**的指标权重（Sec. 3.3-3.4）。
3. 引入基于成对排序损失的 BO 驱动循环，再耦合进化阶段进行更广泛探索（Sec. 3.2, 3.5）。
4. 在 NAS-Bench-201、DARTS/ImageNet、TransNAS-Bench-101 上给出强基准结果（Table 1-3）。

## 问题背景
### 目标问题
- 在直接训练式 NAS 成本过高时，如何提升免训练 NAS 的架构排序质量。

### 现有方法局限
- 单一零成本代理指标在不同任务间迁移效果不稳定。
- 现有混合方法通常优化**全局**指标组合，忽略架构级别的敏感性差异。

### 本文动机
- PO-NAS 利用有限真实反馈学习每个架构的指标权重，再用预测分数扩展搜索探索。

## 方法详解

### 1) 架构专属评分与优化目标
给定 K 个免训练指标：

$$
S(A; w_A) = \sum_{i=1}^{K} w_{A,i}\,\tilde Z_i(A)
$$

- \(\tilde Z_i\)：归一化指标值
- \(w_A\)：架构专属权重向量（L1 归一化）

权重学习通过最大化 [[Kendall's Tau]]**排序一致性**（score 排序 vs 真实性能）实现：

$$
w_A^{(t+1)} = \arg\max_{w_A} \tau\big(\{S(A;w_A^{(t)})\}_{A\in A_t},\{f(A)\}_{A\in A_t}\big)
$$

### 2) 编码器预训练
- 使用 2 层 [[Graph Attention Network]](d:\PRO\essays\论文笔记\_概念\Graph%20Attention%20Network.md) 将架构图编码为嵌入向量（Sec. 3.3, Fig. 2）。
- 节点掩码重建 + 指标预测联合预训练：

$$
\mathcal{L}_{recon} = \frac{1}{|V_m|}\sum_{v\in V_m}\|\hat x_v-x_v\|_2^2,
\quad
\mathcal{L}_{metric} = \frac{1}{K}\sum_{i=1}^{K}\|P_z^i(h_G)-Z_i(G)\|_2^2
$$

### 3) 带符号指标效应的代理评分
归一化后，PO-NAS 将权重拆分为正/负激活：

$$
\hat S = \sum_{i=1}^{K}\big(\hat w_i^+\hat Z_i + \hat w_i^-(1-\hat Z_i)\big)
$$

直觉：同时保留指标与性能之间的正/负相关行为。

代理优化使用三个损失函数：
1. **对齐损失**：成对 score/性能差距分布对齐（Eq. 6）
2. **相关损失**：\(\mathcal{L}_{corr}=1-\rho(\hat S,f)\)（Eq. 7）
3. **方向损失**：\(\mathcal{L}_{dir}=\mathbb{E}[\mathrm{ReLU}(-\Delta_{pred}\Delta_{true})]\)（Eq. 8）

### 4) 搜索循环与进化
- 主循环：初始化 → 预训练 → BO 阶段 → 可选进化阶段（Algorithm 1）
- 进化阶段：最短操作路径交叉 + 邻域遍历变异（Algorithm 2）
- 进化中的配对分数：

$$
S_{pair} = N\,\tilde S_{cost} + (1-N)\,\tilde S_{pre}
$$

- N 是探索权重：早期高探索，后期低探索

## 关键实验结果

### NAS-Bench-201（Table 1）
- PO-NAS：**94.12±0.22 / 73.51±0.00 / 46.71±0.12**（CIFAR-10 / CIFAR-100 / ImageNet-16-120）
- 搜索成本：3162 GPU 秒

### DARTS on ImageNet（Table 2）
- PO-NAS：**23.9 top-1 error / 7.1 top-5 error**，6.3M 参数，0.64 GPU days

### TransNAS-Bench-101（Table 3）
- Micro 和 Macro 设置均表现接近最佳

## 复现要点
1. 六个基础指标：grad_norm、snip、grasp、fisher、synflow、jacob_cov
2. 预训练包括架构掩码和 100 epoch 调度
3. BO 阶段使用损失阈值和差距阈值 \(T_{th}\)（默认约 0.1）
4. DARTS 设置使用 10k 初始架构，有限真实训练预算（CIFAR 25 个，ImageNet 10 个）

## 批判性思考

### 优点
1. 解决了指标融合的真实痛点：架构间异质性
2. 混合设计实用：廉价指标 + 稀疏真实训练 + 引导搜索
3. 进化模块为大搜索空间设计

### 局限
1. 代理稳定性仍是已知问题
2. 方法复杂度高于单代理流水线
3. 匿名代码链接目前无法公开访问

### 后续想法
1. 尝试簇级指标权重（论文自己提出的未来方向）
2. 测试对每个搜索空间/任务指标子集变化的鲁棒性

## 关联概念
- [Training-free NAS](d:\PRO\essays\论文笔记\_概念\Training-free%20NAS.md)
- [Zero-Cost Proxy](d:\PRO\essays\论文笔记\_概念\Zero-Cost%20Proxy.md)
- [Surrogate Predictor](d:\PRO\essays\论文笔记\_概念\Surrogate%20Predictor.md)
- [Kendall's Tau](d:\PRO\essays\论文笔记\_概念\Kendall's%20Tau.md)
- [Bayesian Optimization](d:\PRO\essays\论文笔记\_概念\Bayesian%20Optimization.md)
- [Evolutionary Neural Architecture Search](d:\PRO\essays\论文笔记\_概念\Evolutionary%20Neural%20Architecture%20Search.md)
- [Graph Attention Network](d:\PRO\essays\论文笔记\_概念\Graph%20Attention%20Network.md)
- [NAS-Bench-201](d:\PRO\essays\论文笔记\NAS-Bench-201.md)
