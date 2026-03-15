---
title: "RACL_ch"
type: method
language: zh-CN
source_method_note: "[[RACL]]"
source_paper: "Adversarially Robust Neural Architectures"
source_note: "[[RACL]]"
authors: [Minjing Dong, Yanxi Li, Yunhe Wang, Chang Xu]
year: 2025
venue: TPAMI
tags: [nas-method, zh, robust-nas, differentiable-nas, lipschitz]
created: 2026-03-15
updated: 2026-03-15
---

# RACL 中文条目

## 一句话总结

> RACL 在可微 NAS 中不再把架构参数当作确定值，而是用对数正态分布采样并施加 `Pr(lambda_F <= lambda_bar_F) >= eta` 的置信约束，从而更稳定地搜索到对抗鲁棒架构。

## 来源

- 论文: [Adversarially Robust Neural Architectures](https://doi.org/10.1109/TPAMI.2025.3542350)
- HTML: 论文未提供
- 代码: 论文未提供官方仓库链接
- 英文方法笔记: [[RACL]]
- 论文笔记: [[RACL]]

## 适用场景

- 问题类型: 面向图像分类的对抗鲁棒架构搜索。
- 前提假设: 网络 Lipschitz 上界越低，通常鲁棒性越好。
- 数据形态: 监督学习，且有 train/val 划分用于双层优化。
- 规模与约束: DARTS/PC-DARTS 类 cell-based 可微搜索空间。
- 适用原因: 直接把“鲁棒性目标”绑定到架构采样概率，而不是仅靠后验对抗训练补救。

## 不适用或高风险场景

- 需要官方代码一键复现的工程场景。
- 非可微或非 cell-based 搜索空间。
- 更关注极低搜索成本而非鲁棒收益时。

## 输入、输出与目标

- 输入: 搜索空间 `O`、训练集划分 `D_T/D_V`、扰动预算、`eta` 与 ADMM 超参。
- 输出: 搜索得到的 normal/reduction cell 及重训后的鲁棒模型。
- 优化目标: 最小化分类损失 + 梯度范数项，同时满足置信 Lipschitz 约束。
- 核心假设: edge/node/network Lipschitz 项的对数正态近似在优化上足够准确。

## 方法拆解

### 阶段 1: 从攻击目标到鲁棒约束

- 先用对抗攻击目标与 Lipschitz 不等式建立损失扰动上界。
- 将 robust NAS 写成带 `lambda_F` 上下界约束的优化问题。
- Source: Sec. III-A, Eq. (1)-(4)

### 阶段 2: 在 NAS 超网中展开 Lipschitz 上界

- 使用 DARTS mixed operation 表达节点（`alpha` 管算子, `beta` 管边）。
- 推导网络上界为多个节点/Cell 项的乘积。
- Source: Sec. III-B, Eq. (5), Eq. (7)-(10)

### 阶段 3: 置信采样

- 令 `alpha ~ LN(mu_alpha, Sigma_alpha)`，`beta ~ LN(mu_beta, Sigma_beta)`。
- 利用对数正态的和/积性质传播到 edge、node、network 的 Lipschitz 分布。
- Source: Sec. III-C, Eq. (11)-(12), Fig. 1-2

### 阶段 4: 概率约束 + ADMM

- 施加 `Pr(lambda_F <= lambda_bar_F) >= eta`。
- 转为 CDF 约束后，用 ADMM 的 primal-dual 交替更新求解。
- Source: Sec. III-C, Eq. (13)-(19), Algorithm 1

## 伪代码
```text
Algorithm: RACL
Input: 搜索空间 O, 训练划分 D_T/D_V, 置信系数 eta, ADMM 惩罚 rho
Output: 鲁棒架构 A*

1. 初始化架构参数分布:
   alpha ~ LN(mu_alpha, Sigma_alpha), beta ~ LN(mu_beta, Sigma_beta)
   Source: Algorithm 1

2. 通过重参数化采样 alpha/beta，在 D_T 上更新超网权重 W:
   minimize L_CE + ||grad_x F||
   Source: Algorithm 1, Eq. (16)

3. 在 D_V 上更新 mu/sigma（对应 alpha/beta 的分布参数），
   并用 ADMM 处理置信 Lipschitz 约束
   Source: Eq. (17)-(19), Algorithm 1

4. 迭代至收敛后，从学习到的分布中采样离散 normal/reduction cell
   Source: Algorithm 1

5. 对采样架构从头重训（含对抗训练）并做白盒/黑盒鲁棒评估
   Source: Sec. IV-B/D/E
```

## 训练流程

1. 在 CIFAR-10 上进行搜索，训练集拆分为权重更新与架构更新两部分。
2. 搜索 50 epochs，batch 128，SGD 更新 `W`，Adam 更新分布参数。
3. 从分布中采样离散架构。
4. 构建 20-cell 网络做对抗重训并与基线统一评测。

Sources:

- Sec. IV-A
- Algorithm 1

## 推理流程

1. 用重训后的搜索架构做 clean 与 attack 下评估。
2. 白盒攻击包含 FGSM/MIM/PGD/CW/AutoAttack。
3. 迁移黑盒通过 source-target 交叉攻击评估可迁移性与抗迁移性。

Sources:

- Sec. IV-B/D/E
- Table I-VIII

## 复杂度与效率

- 时间复杂度: 论文未给封闭式表达。
- 空间复杂度: 论文未给封闭式表达。
- 运行特征: 搜索成本约 `0.5 GPU-day`。
- 扩展性: 搜索后仍需完整重训和多攻击评测，成本主要在后段。

## 实现备注

- 搜索算子: sep conv(3x3/5x5), dilated sep conv(3x3/5x5), max/avg pooling, skip, zero。
- 超网规模: 8 cells（6 normal + 2 reduction），每个 cell 6 个节点。
- 搜索超参: SGD `lr=0.1`, momentum `0.9`, wd `3e-4`; Adam `lr=6e-4`, wd `1e-3`。
- 重训超参: 100 epochs, SGD `lr=0.1`, momentum `0.9`, wd `2e-4`, grad clip `5`。
- 关键超参: 消融显示 `eta=0.9` 最优。

## 与相关方法的关系

- 对比 [[DARTS]] / [[PC-DARTS]]: 增加了面向鲁棒性的概率约束与置信采样。
- 对比 RobNet/ABanditNAS/AdvRush/DSRNA: 在同类攻击评测上多数场景鲁棒精度更好。
- 主要优势: 架构采样过程“可解释地”引入置信度。
- 主要代价: 对数正态近似依赖、且无官方代码。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- 关键表: Table I-X
- 关键公式: Eq. (2)-(4), Eq. (5), Eq. (7)-(12), Eq. (13)-(16), Eq. (17)-(19)
- 关键算法: Algorithm 1

## 参考链接
- DOI: https://doi.org/10.1109/TPAMI.2025.3542350
- HTML: Not provided
- 代码: Not found
- 本地实现: Not archived
