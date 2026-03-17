---
title: "TF-MAS_ch"
type: method
language: zh-CN
source_method_note: "[[TF-MAS]]"
source_paper: "TF-MAS: Training-free Mamba2 Architecture Search"
source_note: "[[TF-MAS]]"
authors: [Yi Fan, Yu-Bin Yang]
year: 2025
venue: NeurIPS
tags: [nas-method, zh, nas, training-free-nas, mamba2]
created: 2026-03-16
updated: 2026-03-16
---

# TF-MAS 中文条目

## 一句话总结
> TF-MAS 面向 Mamba2 设计了训练免费 NAS 代理：先估计 `U->X/B/C` 的映射矩阵，再用“矩阵核范数 × 梯度核范数”聚合为架构评分。

## 来源
- 论文: TF-MAS: Training-free Mamba2 Architecture Search
- 本地 PDF: `D:/PRO/essays/papers/TF-MAS Training-free Mamba2 Architecture Search.pdf`
- 代码: https://github.com/fanyi-plus/tf-nas
- 英文方法笔记: [[TF-MAS]]
- 论文笔记: [[TF-MAS]]

## 适用场景
- 问题类型: 在计算预算受限时，对 Mamba2 架构做低成本搜索与排序。
- 前提假设: 候选网络遵循 Mamba2/SSD 结构范式。
- 数据形态: 训练免费代理评估 + 演化搜索。
- 规模与约束: 候选架构较多，无法逐个完整训练。
- 适用原因: 代理直接针对 Mamba2 内部结构构造，而非生搬 CNN/Transformer 代理。

## 不适用或高风险场景
- 目标网络与 Mamba2 差异大，`U->X/B/C` 映射假设不成立。
- 你需要“现在就能完整复现”的官方代码。
- 你要求在所有任务上都具备非常高且稳定的排序相关性。

## 输入、输出与目标
- 输入: 候选架构 `A`、输入批次 `D`、中间张量 `U/X/B/C` 与输出层权重。
- 输出: 代理分数 `TF-MAS`（用于排序候选架构）。
- 优化目标: 最大化代理排序与真实性能排序的 [[Kendall's Tau]]。
- 核心假设: SSD 堆叠中的 [[Rank Collapse]] 信息可反映最终架构质量。

## 方法拆解

### 阶段 1: 求解映射矩阵
- 对每层求 `U W_X = X`，`W_B/W_C` 同理。
- 根据 `T` 与 `W` 的关系，分别用逆矩阵、[[Moore-Penrose Pseudoinverse]] 或最小二乘近似。
- Source: Sec. 3.1 / Eq. (2)-(5)

### 阶段 2: 计算梯度项
- 通过一次反向传播获得与 `X/B/C/out` 相关的梯度。
- `W_X/W_B/W_C` 不是可训练参数，梯度通过链式法则间接得到。
- Source: Sec. 3.1 / Eq. (6) / Appendix D

### 阶段 3: 聚合代理分数
- 按层、按矩阵类型 (`X/B/C/out`) 累加
  `||W||_nuc * ||dL/dW||_nuc`。
- Source: Eq. (6), Appendix D Algorithm 1

### 阶段 4: 搜索空间与演化搜索
- 定义 AH: `D/W/N/H`，通过预算方程解缩放系数 `k`，生成搜索范围。
- 在 SSMamba2 / VWSSMamba2 上执行演化搜索，最后从头训练验证。
- Source: Sec. 3.2 / Eq. (7) / Sec. 4.2 / Appendix G

## 伪代码
```text
Algorithm: TF-MAS
Input: 架构 A，输入 batch D
Output: 代理分数 s

1. 初始化候选架构 A，提取每层输出权重 W_out。
   Source: Appendix D, Alg. 1 line 1-2
2. 前向得到每层 U, X, B, C。
   Source: Appendix D, Alg. 1 line 2
3. 反向得到与 X/B/C/W_out 相关梯度。
   Source: Appendix D, Alg. 1 line 3
4. 按列维度分组并 batch 化拼接方程。
   Source: Appendix D, Alg. 1 line 4-8
5. 若 T=W 用逆矩阵，否则用 SVD + 伪逆求解 W。
   Source: Sec. 3.1 Eq. (2)-(5), Appendix D line 9-16
6. 回填每层 W_X/W_B/W_C，并用链式法则得到对应梯度。
   Source: Sec. 3.1, Appendix D line 17-18
7. 计算并累加 s = Σ_i Σ_{x in {X,B,C,out}} ||W_x^(i)||_nuc * ||dL/dW_x^(i)||_nuc。
   Source: Eq. (6), Appendix D line 19
8. 返回 s。
   Source: Appendix D line 20
```

## 训练流程
1. 基于预训练 Mamba2 通过 [[Weight Entanglement]] 构建候选架构集。
2. 对候选架构计算 TF-MAS 分数并排序。
3. 演化搜索选择高分候选。
4. 对搜索结果从头训练并测试真实性能。

Sources:
- Sec. 4.1, Sec. 4.2
- Table 1-3, Appendix G

## 推理流程
1. 在 AH 范围内采样候选架构。
2. 计算 TF-MAS 分数。
3. 选取 Top 候选进入完整训练阶段。

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4.2

## 复杂度与效率
- 时间复杂度（单层）: `O(WHP min(W,P) + WHN min(W,N))`。
- 空间复杂度: 论文未给统一封闭式。
- 运行特征: 4 张 V100 上搜索耗时约 0.6-0.7 天（文中设置）。
- 扩展性: 作者给出随 `W/N/H/P` 增大近线性增长的分析。

Sources:
- Appendix C.7
- Sec. 4.2

## 实现备注
- 关键不是 FC 权重本身，而是 `U->X/B/C` 的等效映射矩阵估计。
- 伪代码包含按形状分组后批量 SVD/伪逆求解，利于加速。
- 文中预算约束示例为参数量不超过 130M。
- BWE 变体会按层代理值优先变异弱层，并在交叉时按层择优继承。
- 官方仓库已归档到本地，但当前仅公开占位 README，完整模块尚未发布。

## 与相关方法的关系
- 对比 DSS++: TF-MAS 把 rank-collapse 逻辑迁移到 SSD/Mamba2 内部表示。
- 对比 GraSP/SNIP 等 CNN 代理: TF-MAS 在文中 Mamba2 bench 上相关性更强。
- 主要优势: 首个 Mamba 定制 training-free 代理，并给出搜索实证。
- 主要代价: 现阶段代码不完整、部分数据集相关性仍有提升空间。

## 证据与可溯源性
- 关键图: Figure 1, Figure 2, Figure 3
- 关键表: Table 1, Table 2, Table 3, Table 4-6
- 关键公式: Eq. (2)-(7), Eq. (17)
- 关键算法: Appendix D Algorithm 1

## 参考链接
- 论文笔记: [[TF-MAS]]
- 代码: https://github.com/fanyi-plus/tf-nas
- 本地实现: D:/PRO/essays/code_depots/TF-MAS Training-free Mamba2 Architecture Search
