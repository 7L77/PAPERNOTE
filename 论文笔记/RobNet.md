---
title: "When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks"
method_name: "RobNet"
authors: [Minghao Guo, Yuzhe Yang, Rui Xu, Ziwei Liu, Dahua Lin]
year: 2020
venue: CVPR
tags: [nas, robust-nas, adversarial-robustness, one-shot-nas, cvpr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/1911.10695
local_pdf: D:/PRO/essays/papers/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks.pdf
local_code: D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks
created: 2026-03-15
---

# 论文笔记：RobNet

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks |
| 会议 | CVPR 2020 |
| arXiv | https://arxiv.org/abs/1911.10695 |
| 项目页 | http://www.mit.edu/~yuzhe/robnets.html |
| 代码 | https://github.com/gmh14/RobNets |
| 本地 PDF | `D:/PRO/essays/papers/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks` |

## 一句话总结
> 这篇论文把对抗鲁棒性问题转成“鲁棒架构模式挖掘”：先用 [[One-shot NAS]] + [[PGD Attack]] 高效评估大量候选，再提炼三条设计规律，最终得到更抗攻击的 RobNet 系列。

## 核心贡献
1. 提出一个面向鲁棒性的 NAS 研究框架：在一套统一搜索空间中系统分析架构与鲁棒性的关系（Sec. 3.2-3.5）。
2. 发现并验证三条关键规律：密连接更鲁棒；小预算下“direct edge 上加卷积”更有效；深层 [[Flow of Solution Procedure Matrix]] 差异可作为鲁棒性指示器（Sec. 3.3-3.5）。
3. 基于上述规律设计 RobNet 家族，在 CIFAR-10/SVHN/CIFAR-100/Tiny-ImageNet 上均优于常用人工架构（Sec. 4）。
4. 给出结构层面的鲁棒性证据，说明鲁棒提升不只来自训练算法，也来自架构本身（Sec. 5）。

## 问题背景
### 论文要解决什么问题
- 对抗鲁棒研究大多聚焦训练目标或正则，而“架构本身如何影响鲁棒性”缺少系统结论。
- 直接对大量候选网络逐个完整对抗训练代价太高。

### 现有方法不足
- 缺少可规模化的“架构-鲁棒性”统计研究路径。
- 鲁棒 NAS 常常只给最终模型，不清楚哪类连接模式真正重要。

### 本文思路
- 利用 [[One-shot NAS]] 的权重共享能力，快速获得大量候选结构的鲁棒评分。
- 对高鲁棒与低鲁棒架构做统计分析，抽取可操作的设计规则，再构造 RobNet。

## 方法详解
### 1) 鲁棒搜索空间设计（Sec. 3.2, Fig. 2）
- 采用 [[Cell-based Search Space]]，每条边的候选操作简化为 `3x3 sep conv / identity / zero`。
- 允许两节点之间出现多操作组合，不再限制“每条边只能选一个操作”，从而覆盖更广拓扑（包括类似 ResNet/DenseNet 的连接模式）。
- 架构参数记为 `alpha`，边操作由 `alpha` 决定。

### 2) 鲁棒 one-shot 搜索（Sec. 3.2, Eq. (1)）
- 先把所有 `alpha` 置 1 构建 supernet。
- 训练时每个 batch 随机采样子网络（path dropout），并按 min-max 目标做对抗训练：
\[
\min_{\theta}\ \mathbb{E}_{(x,y)\sim D}\left[\max_{x' \in S} L(y, M(x';\theta))\right]
\]
- 其中 `S={x' : ||x-x'||_p < eps}`，文中重点是 `l_infinity` 约束 + PGD。

### 3) 候选评估与快速微调（Sec. 3.2, Fig. 3）
- supernet 训练后随机采样候选架构。
- 对每个候选先做少量 epoch 的对抗微调，再在 PGD white-box 上测 adversarial accuracy。
- 作者观察到“短微调后”鲁棒指标更稳定，适合用于架构比较。

### 4) 三条设计规律（Sec. 3.3-3.5）
#### 4.1 密连接有利于鲁棒性（Sec. 3.3, Fig. 4-5, Eq. (2)）
- 定义 [[Architecture Density]]：
\[
D=\frac{|E_{connected}|}{|E|}=\frac{\sum_{i,j,k}\alpha_k^{(i,j)}}{|E|}
\]
- 在 1000 个采样架构中，密度与对抗精度正相关。

#### 4.2 小预算下 direct edge 卷积更有效（Sec. 3.4, Fig. 6）
- 同等预算内，卷积数量增加通常提升鲁棒性。
- 尤其在 small/medium budget，direct edge 卷积占比越高，鲁棒性越好。

#### 4.3 Cell-free 场景可用 FSP 距离筛选（Sec. 3.5, Eq. (3)(4), Fig. 7）
- 定义每个 cell 的 FSP 矩阵：
\[
G_l(x;\theta)=\frac{1}{h\times w}\sum_{s=1}^{h}\sum_{t=1}^{w} F_{l,s,t}^{in}(x;\theta)\times F_{l,s,t}^{out}(x;\theta)
\]
- clean 与 adversarial 的 FSP 距离：
\[
L^{FSP}_l=\frac{1}{N}\sum_x \|G_l(x;\theta)-G_l(x';\theta)\|_2^2
\]
- 深层 cell 的 FSP 距离与 `(clean acc - adv acc)` 更相关，可用于先过滤非鲁棒架构。

## 关键实验结论
### CIFAR-10 White-box（Table 1）
- RobNet-free 在 PGD100 下 `52.57%`，显著高于 DenseNet-121 的 `47.46%` 与 WideResNet-28-10 的 `46.90%`。
- RobNet-large-v2 在更大参数量下 PGD100 达 `50.26%`，说明“结构设计 + 规模”可叠加。

### CIFAR-10 Black-box（Table 2）
- RobNet-free 在 transfer 攻击下 `FGSM 65.06% / PGD100 63.17%`，优于对照架构。

### 跨数据集迁移（Table 3）
- 把 CIFAR-10 上搜索到的 RobNet 直接迁移到 SVHN/CIFAR-100/Tiny-ImageNet，鲁棒性仍保持优势。

### 与其他鲁棒技术可叠加（Table 4）
- RobNet + feature denoising 继续提升鲁棒精度，说明方法与已有防御技巧是正交的。

## 与代码实现的对照
- 官方仓库主要提供“已搜索好的 RobNet 架构 + 对抗训练/评估代码”，路径：`main.py`, `attack.py`, `models/`, `experiments/`。
- `main.py` 在训练模式会把 `attack_param.num_steps` 设为 7，与论文中 PGD-7 对抗训练设置对齐。
- `attack.py` 实现了 PGD 生成流程（随机起点、迭代符号梯度步进、epsilon 投影）。
- `architecture_code.py` 直接给出 `robnet_large_v1/v2` 与 `robnet_free` 的结构编码。
- 注意：仓库不包含论文里完整的鲁棒搜索与 FSP 过滤流水线（更偏向“复现实验模型训练/评测”而非“重新搜索”）。

## 批判性思考
### 优点
1. 从“结构归纳”角度解释鲁棒性，结论可落地到架构设计规则。
2. 数据集和攻击设置覆盖较广，且同时报告 white-box / black-box。
3. 结论具有工程可用性（例如小预算优先在 direct edge 加卷积）。

### 局限
1. 搜索与分析主要基于 `l_infinity + PGD`，对其它威胁模型的结论外推需谨慎。
2. FSP 指标在更大规模模型和任务上的稳定性仍需更多验证。
3. 开源代码未完整公开搜索流程，复现实验“从零搜索”门槛仍较高。

### 可复现性
- [x] 论文与代码公开
- [x] 已搜索模型与训练脚本可直接运行
- [ ] 完整搜索阶段（含 FSP 过滤）代码未在仓库中完全公开

## 关联概念
- [[Robust Neural Architecture Search]]
- [[One-shot NAS]]
- [[Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[PGD Attack]]
- [[FGSM]]
- [[Cell-based Search Space]]
- [[Architecture Density]]
- [[Flow of Solution Procedure Matrix]]

