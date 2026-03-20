---
title: "MCTS-Learned Hierarchy_ch"
type: method
language: zh-CN
source_method_note: "[[MCTS-Learned Hierarchy]]"
source_paper: "Neural Architecture Search by Learning a Hierarchical Search Space"
source_note: "[[MCTS-Learned Hierarchy]]"
authors: [Anonymous authors]
year: 2025
venue: ICLR (under review)
tags: [nas-method, zh, nas, mcts]
created: 2026-03-20
updated: 2026-03-20
---

# MCTS-Learned Hierarchy 中文条目

## 一句话总结
> 方法先从 supernet 输出相似性学习一棵“更有判别力”的架构层级树，再在树上做 Boltzmann+UCT 采样，以更少计算找到更好的 NAS 架构。

## 来源
- 论文: Neural Architecture Search by Learning a Hierarchical Search Space（本地 PDF）
- HTML: 源 PDF 未提供
- 代码: 匿名投稿，未给出官方仓库
- 英文方法笔记: [[MCTS-Learned Hierarchy]]
- 论文笔记: [[MCTS-Learned Hierarchy]]

## 适用场景
- 问题类型: 一次训练、多架构共享权重的 NAS 采样优化。
- 前提假设: 架构输出向量的距离能反映语义相近性。
- 数据形态: 监督学习（训练集更新权重，验证集估计奖励）。
- 规模与约束: 适合中小到中等规模搜索空间（文中建议 `<10k` 候选更稳妥）。
- 适用原因: 通过学习分支顺序，提高早期决策区分度，减少无效探索。

## 不适用或高风险场景
- 候选架构极大，无法承担 `O(N^2)` 距离矩阵与聚类成本。
- 无法做任何 warm-up 预训练。
- 需要官方代码级可复现而非论文级复现。

## 输入、输出与目标
- 输入: 搜索空间 `S`、supernet、训练/验证 mini-batch。
- 输出: 在 `lambda=0` 条件下从树中采样得到的最优架构。
- 优化目标: 在给定算力下提升架构质量与排名。
- 核心假设: 分支质量影响访问统计，访问统计影响奖励估计，最终影响搜索质量。

## 方法拆解
### 阶段 1: 均匀采样预训练
- 先用 uniform sampling 训练 supernet 到可用状态。
- Source: Algorithm 1 (pre-training), Sec.4.

### 阶段 2: 学习层级树
- 对候选架构提取输出向量，计算两两距离矩阵。
- 用层次凝聚聚类构造二叉树。
- Source: Sec.4 Tree design, Algorithm 1.

### 阶段 3: 树上训练
- 用 Boltzmann 在兄弟节点间采样。
- 用 UCT 形式更新奖励，并用 EMA 平滑验证精度。
- Source: Eq.(2), Eq.(3), Eq.(4), Algorithm 1.

### 阶段 4: 最终选择
- 关闭探索（`lambda=0`）采样候选并按验证性能选最优。
- Source: Sec.4 Search and training; Sec.5.

## 伪代码
```text
Algorithm: MCTS-Learned Hierarchy NAS
Input: 搜索空间 S, supernet f, 训练批 Xt, 验证批 Xv
Output: 最优架构 a*

1. 使用 uniform sampling 预训练 supernet。
   Source: Algorithm 1
2. 对每个候选架构 ai 提取输出 oi，构建距离矩阵 D。
   Source: Sec.4, Algorithm 1
3. 在 D 上做 agglomerative clustering 得到二叉树 T。
   Source: Sec.4, Algorithm 1
4. 在 T 上按 Eq.(2) 做 Boltzmann 采样路径。
   Source: Eq.(2)
5. 按 Eq.(3)(4) 回传更新奖励与平滑准确率。
   Source: Eq.(3), Eq.(4)
6. 训练后设 lambda=0，采样并选验证精度最高的架构。
   Source: Sec.4/5; Inference from source
```

## 训练流程
1. Uniform 预训练。
2. 构建输出相似度矩阵并生成树。
3. MCTS warm-up 后进入树上条件采样训练。
4. 叶到根更新奖励统计。

Sources:
- Sec.4, Eq.(2-4), Algorithm 1, Appendix B.1.

## 推理流程
1. 关闭探索项（`lambda=0`）。
2. 从树中采样 `k` 个候选。
3. 验证集排序并选择最优。

Sources:
- Sec.4 Search and training.

## 复杂度与效率
- 时间复杂度: 输出提取 `O(N)` + 距离/聚类 `O(N^2)`。
- 空间复杂度: 距离矩阵 `O(N^2)`。
- 扩展性: 文中指出当前形态在 `<10k` 候选时更稳健。

## 实现备注
- 奖励由 EMA 验证精度与 UCT 探索项组成。
- 关键超参: `beta=0.95`, `lambda=0.5`。
- CIFAR10 训练阶段比例大约 `40/25/35`（uniform/warm-up/MCTS）。
- 代码状态: 源论文未给官方仓库链接。

## 与相关方法关系
- 相比默认树 MCTS: 学习树结构替代固定按层展开，早期分支更有效。
- 相比 `MCTS + Reg.`: 不依赖额外正则也能达到或超过其结果。
- 相比扁平采样: 条件概率分解带来更好的访问分配与排名质量。

## 证据与可追溯性
- 关键图: Fig.1, Fig.2, Fig.3。
- 关键表: Table 1/2/3/4/5, Table 7。
- 关键公式: Eq.(2), Eq.(3), Eq.(4)。
- 关键算法: Algorithm 1。

## 参考链接
- arXiv: Not provided in source PDF
- HTML: Not provided in source PDF
- 代码: Not found (anonymous submission)
- 本地实现: Not archived
