---
title: "RBFleX-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[RBFleX-NAS]]"
source_paper: "RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection"
source_note: "[[RBFleX-NAS]]"
authors: [Tomomasa Yamasaki, Zhehui Wang, Tao Luo, Niangjun Chen, Bo Wang]
year: 2025
venue: TNNLS
tags: [nas-method, zh, training-free-nas, rbf-kernel, activation-search]
created: 2026-03-16
updated: 2026-03-16
---

# RBFleX-NAS 中文条目

## 一句话总结

> RBFleX-NAS 在训练前同时利用“激活输出相似性 + 最后层输入特征图相似性”，并通过 HDA 自动选取 RBF 核参数，从而提升 NAS 候选架构排序质量。

## 来源

- 论文: [RBFleX-NAS: Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection](https://arxiv.org/abs/2503.22733)
- HTML: https://arxiv.org/html/2503.22733v3
- 代码: https://github.com/Edge-AI-Acceleration-Lab/RBFleX-NAS
- 英文方法笔记: [[RBFleX-NAS]]
- 论文笔记: [[RBFleX-NAS]]

## 适用场景

- 问题类型: 训练前（training-free）架构评分与排序。
- 前提假设: 初始化阶段的跨样本表征几何结构与最终精度排序相关。
- 数据形态: mini-batch 输入即可，不依赖标签监督。
- 规模与约束: 适合需要快速筛选 top-k 架构、无法逐个完整训练的场景。
- 适用原因: 双视角相似性（`X` 与 `Y`）比单视角 proxy 更稳定，HDA 减少手动调参。

## 不适用或高风险场景

- 需要直接预测绝对精度，而不是相对排序。
- 网络极大导致激活特征采集开销过高。
- 输入分布极不稳定，mini-batch 统计不可靠。

## 输入、输出与目标

- 输入: 候选架构 `f`、mini-batch 输入、`gamma_k` 与 `gamma_q`。
- 输出: 架构评分 `score(f)`。
- 优化目标: 让高性能架构在排序前列，降低后续高成本训练范围。
- 核心假设: 初始化时样本间差异结构可作为性能先验。

## 方法拆解

### 阶段 1: 构建两类表示矩阵

- 从激活层输出构建 `X`（每个样本拼接展平）。
- 从最后层输入特征图构建 `Y`。
- Source: Sec. III-A, Fig. 4, Fig. 5

### 阶段 2: 列归一化

- 对 `X` 和 `Y` 按列归一化到 `[0,1]`，保留样本之间关系。
- Source: Sec. III-A, Eq. (1)

### 阶段 3: 构建双 RBF 相似矩阵

- `K_ij = exp(-gamma_k ||x_i-x_j||^2)`。
- `Q_ij = exp(-gamma_q ||y_i-y_j||^2)`。
- Source: Sec. III-A, Eq. (2), Eq. (3), Eq. (4), Eq. (5)

### 阶段 4: 评分聚合

- 用 `log|K ⊗ Q|`，再化简为 `N(log|K| + log|Q|)`。
- Source: Sec. III-A, Eq. (6), Eq. (7)

### 阶段 5: HDA 自动选核参数

- 通过均值差与方差构造候选 `G_ij`。
- 分别在 `G_k` 与 `G_q` 取最小有效值作为 `gamma_k`、`gamma_q`。
- Source: Sec. III-B, Eq. (8)-(16), Fig. 6, Fig. 8

## 伪代码

```text
Algorithm: RBFleX-NAS Scoring
Input: Candidate architecture f, mini-batch B={b_1...b_N}, M sampled nets for HDA
Output: score(f)

1. 在 M 个候选网络上检测 gamma_k 与 gamma_q：
   - 采集激活向量与最后层输入向量；
   - 计算候选 G，并取最小有效项作为 gamma。
   Source: Sec. III-B, Eq. (8)-(16), Fig. 6

2. 对待评估网络 f，采集每个样本的两类向量：
   - x_i: 激活输出拼接向量
   - y_i: 最后层输入特征图拼接向量
   Source: Sec. III-A, Fig. 4, Fig. 5

3. 组装 X 与 Y，并做列归一化。
   Source: Sec. III-A, Eq. (1)

4. 计算 RBF 相似矩阵：
   K_ij = exp(-gamma_k * ||x_i - x_j||^2)
   Q_ij = exp(-gamma_q * ||y_i - y_j||^2)
   Source: Sec. III-A, Eq. (2)-(5)

5. 计算分数：
   score = N * (log|K| + log|Q|)
   Source: Sec. III-A, Eq. (6)-(7)

6. 按 score 排序候选架构，选择 top-k 进入后续完整训练。
   Source: Sec. IV-F, Sec. IV-G
```

## 训练流程

1. 从设计空间采样候选架构。
2. 先运行 HDA（可复用）得到 `gamma_k`、`gamma_q`。
3. 对每个候选在初始化状态计算 RBFleX 分数。
4. 选择高分架构并进行基准查询或完整训练验证。

Sources:

- Sec. III, Sec. IV, Table III.

## 推理流程

1. 输入新候选架构并初始化。
2. 计算 RBFleX 分数。
3. 与候选池比较得到排序位置。
4. 输出 top-k 架构供下游训练。

Sources:

- Sec. III-A, Sec. IV-G.

## 复杂度与效率

- 时间复杂度: 论文报告评分部分约为 `O(N^2.373)`。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: 在多个基准上，搜索时间与精度整体优于或不劣于主流 training-free 基线。
- 扩展性说明: 激活特征维度越大，采集与核矩阵计算开销越高。

## 实现备注

- 官方仓库按基准拆分脚本：`RBFleX_NAS-Bench-201.py`、`RBFleX_NATS-Bench-SSS.py`、`RBFleX_TransNAS_*.py`、`RBFleX_NAFBee_BERT.py`。
- 通过 `register_forward_hook` 收集特征：
  - ReLU 输出累积到 `network.K`；
  - 最后层输入累积到 `network.Q`。
- `Simularity_Mat` 实现 `exp(-gamma*dist2)`。
- 使用 `torch.linalg.slogdet` 计算对数行列式并组合评分：
  - `score = batch_size_NE * (K + Q)`。
- `HDA.py` 中候选 gamma 计算为 `M/(2*(s1+s2))`，最终取最小值。
- 核心路径使用 float64 以减轻小 gamma 场景下的数值问题。

## 与相关方法关系

- 对比 [[NASWOT]] / [[DAS]]: 不再仅依赖 ReLU 二值模式，加入最后层输入特征视角，低精度区间可分性更强。
- 对比 grad norm / snip / synflow 等梯度代理: 不依赖标签和损失，同时保持竞争力。
- 主要优势: 排序判别力强，支持激活函数搜索。
- 主要代价: 特征采集与核矩阵计算开销高于极简代理。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 4, Fig. 5, Fig. 6, Fig. 8, Fig. 9-17
- 关键表: Table I, Table II, Table III, Table IV, Table V
- 关键公式: Eq. (1)-(7), Eq. (8)-(16)
- 关键算法: HDA（Sec. III-B）与搜索实验流程（Sec. IV-G）

## 参考链接

- arXiv: https://arxiv.org/abs/2503.22733
- HTML: https://arxiv.org/html/2503.22733v3
- 代码: https://github.com/Edge-AI-Acceleration-Lab/RBFleX-NAS
- 本地实现: D:/PRO/essays/code_depots/RBFleX-NAS Training-Free Neural Architecture Search Using Radial Basis Function Kernel and Hyperparameter Detection

