---
title: "Neural Architecture Search by Learning a Hierarchical Search Space"
method_name: "MCTS-Learned Hierarchy"
authors: [Anonymous authors]
year: 2025
venue: ICLR (under review)
tags: [NAS, MCTS, one-shot-nas, search-space-design]
zotero_collection: ""
image_source: online
arxiv_html: ""
created: 2026-03-20
local_pdf: D:/PRO/essays/papers/Neural Architecture Search by Learning a Hierarchical Search Space.pdf
---

# 论文笔记：MCTS-Learned Hierarchy

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Neural Architecture Search by Learning a Hierarchical Search Space |
| 发表状态 | ICLR 2025 under review（匿名） |
| 本地 PDF | `D:/PRO/essays/papers/Neural Architecture Search by Learning a Hierarchical Search Space.pdf` |
| 官方代码 | 未在论文中给出明确官方仓库（匿名投稿） |

## 一句话总结
> 论文将 NAS 中 MCTS 的“手工层级树”替换为“按架构输出相似性学习得到的层级树”，在不额外正则化的情况下提升搜索效率与架构质量。

## 核心贡献
1. 从概率分解角度统一分析 NAS 采样策略：独立概率、联合概率、条件概率（Fig.1, Sec.1/3）。
2. 提出基于输出向量距离矩阵的层次聚类树构建方式，替代默认按层展开的树（Sec.4, Fig.2）。
3. 在 Pooling、NAS-Bench-Macro 与 ImageNet MobileNetV2-like 空间上验证学习树结构的收益（Sec.5, Tab.1/4/5）。

## 问题背景
### 要解决的问题
- 默认 MCTS 树的早期分支不够“可区分”时，后续节点访问率低，导致奖励估计慢、搜索效率差。

### 现有方法的局限
- [[Differentiable Architecture Search]] 的节点独立假设会损失节点间交互信息。
- 扁平 [[Boltzmann Sampling]] 需要估计全局联合分布，在大搜索空间中代价高。
- 默认树 + regularization 依赖树同构与软独立假设，泛化到复杂结构受限。

### 本文动机
- 在 NAS 中，“遍历顺序”不是问题定义的一部分，因此可以学习更有判别性的分支顺序，以便更早过滤低质量架构。

## 方法详解
### 1) 学习层级搜索树（核心）
- 先用均匀采样预训练 supernet。
- 对每个架构在验证 mini-batch 上前向，收集输出向量。
- 用输出向量两两距离构建距离矩阵，再做 [[Hierarchical Agglomerative Clustering]] 构造二叉树（Sec.4, Algorithm 1）。

### 2) 树上采样与奖励更新
- 在每个父节点的子节点间按 Boltzmann 分布采样（Eq.2）。
- 奖励采用 UCT：平滑精度项 + 探索项（Eq.3, Eq.4），与 [[Upper Confidence Bound (UCB)]] 思路一致。

### 3) 搜索流程
- 训练阶段：root 到 leaf 逐层采样 -> 更新模型权重 -> 叶到根回传更新奖励（Algorithm 1）。
- 搜索阶段：设 `lambda=0` 关闭探索，采样候选并按验证性能排序选最优（Sec.4/5）。

## 关键公式
### 条件概率分解（Sec.3）
\[
p(a)=p(a_t|a_{<t})\cdots p(a_2|a_1)p(a_1)
\]
含义：把整体架构概率分解为树路径上的条件概率，支持逐层决策。

### Boltzmann 节点采样（Eq.2）
\[
p(a_i)=\frac{\exp(R(a_i)/T)}{\sum_j\exp(R(a_j)/T)}
\]
- `R(a_i)`: 节点奖励
- `T`: 温度，控制分布尖锐程度

### UCT 奖励（Eq.3）
\[
R(a_i)=C(a_i)+\lambda\sqrt{\frac{\log |parent(a_i)|}{|a_i|}}
\]
- `C(a_i)`: 节点平滑准确率
- `|a_i|`: 节点访问次数
- `lambda`: 探索-利用平衡系数

### 平滑准确率更新（Eq.4）
\[
C(a_i) = \beta C(a_i) + (1-\beta)\,Acc(f_a(X_{val},w))
\]
- `beta`: EMA 平滑系数，用于降低 mini-batch 噪声

## 关键图表与实验结论
### Figure
- Fig.1：独立/联合/条件概率三种分解方式对比。
- Fig.2：默认树 vs 学习树示意。
- Fig.3：树质量对收敛速度与最终精度的影响。

### Table
- Tab.1（Pooling, CIFAR10）：`MCTS + Learned` 平均精度 `91.72±0.12`，优于 `MCTS + Reg` 的 `91.42±0.11`。
- Tab.2（距离度量）：KL 与 L2 都优于 cross-entropy，其中 KL 在平均精度上最好（`91.72±0.12`）。
- Tab.3（零成本分支编码）：向量/one-hot 分支比默认方法好，但不如输出向量相似度构树。
- Tab.4（NAS-Bench-Macro）：`MCTS + Learned` 达到 `93.13`（Best Rank=1, Avg Rank=6）。
- Tab.5（ImageNet）：`MCTS + Learned` Top-1 `76.3`，与 MTC_NAS-C 持平，但 GPU days 约 `~7`（低于 `>12` 的 MCTS+Reg 复现）。

## 复杂度与局限
- 构树复杂度由推理 `O(N)` 与距离/聚类 `O(N^2)` 组成，文中写成 `aN^2+bN`（Appendix C.5）。
- 作者指出该方法在 `N < 10k` 搜索空间更合适；超大空间需额外预算控制或近似策略。

## 批判性思考
### 优点
1. 把“树结构质量”显式作为可优化对象，命中 MCTS 在 NAS 中的关键瓶颈。
2. 与现有 SPOS/MCTS 训练框架兼容，改造成本相对低。
3. 在多个基准上兼顾精度、排名与算力成本。

### 局限
1. 依赖预训练 supernet 才能构建相似度矩阵，存在前置成本。
2. 距离矩阵与层次聚类二次复杂度限制了超大搜索空间扩展。
3. 论文匿名且无官方代码，工程细节可复现性受限。

## 关联概念
- [[Neural Architecture Search]]
- [[One-shot NAS]]
- [[Parameter Sharing in NAS]]
- [[Monte-Carlo Tree Search]]
- [[Boltzmann Sampling]]
- [[Upper Confidence Bound (UCB)]]
- [[Hierarchical Agglomerative Clustering]]
- [[KL Divergence]]
