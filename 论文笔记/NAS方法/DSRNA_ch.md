---
title: "DSRNA_ch"
type: method
language: zh-CN
source_method_note: "[[DSRNA]]"
source_paper: "DSRNA: Differentiable Search of Robust Neural Architectures"
source_note: "[[DSRNA]]"
authors: [Ramtin Hosseini, Xingyi Yang, Pengtao Xie]
year: 2021
venue: CVPR
tags: [nas-method, zh, robust-nas, differentiable-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# DSRNA 中文条目

## 一句话总结
> DSRNA 把“鲁棒性”直接放进可微 NAS 的优化目标里（而不是只靠对抗训练间接提高），从而搜索出在攻击下更稳定的架构。

## 来源
- 论文: [DSRNA: Differentiable Search of Robust Neural Architectures](https://arxiv.org/abs/2012.06122)
- HTML: https://arxiv.org/html/2012.06122
- 代码: Not found（论文/CVPR/arXiv 页面未给官方仓库）
- 英文方法笔记: [[DSRNA]]
- 论文笔记: [[DSRNA]]

## 适用场景
- 问题类型: 面向图像分类的鲁棒神经架构搜索。
- 前提假设: 搜索空间是可微的，架构变量可通过双层优化更新。
- 数据形态: 监督学习（CIFAR-10、ImageNet 迁移、MNIST）。
- 规模与约束: DSRNA-CB 计算重；DSRNA-Jacobian 更轻量。
- 适用原因: 显式优化鲁棒性指标，目标函数层面就对齐“抗攻击”。

## 不适用或高风险场景
- 搜索预算很小，无法承担 certified bound 传播带来的开销。
- 搜索空间不可微，无法沿用 DARTS 风格框架。
- 必须依赖官方端到端代码才能开展实验复现。

## 输入、输出与目标
- 输入: 可微 NAS 超网、训练/验证集、攻击预算参数、权衡系数 `gamma`。
- 输出: 搜到的鲁棒架构（DSRNA-CB / DSRNA-Jacobian / DSRNA-Combined）。
- 优化目标: 在降低验证损失的同时提高鲁棒性指标。
- 核心假设: 鲁棒性指标 `R` 对架构变量可微。

## 方法拆解

### 阶段 1: 定义架构层面的鲁棒性指标
- 两条路：
  - 用线性界传播得到 certified lower bound；
  - 用一阶近似得到 Jacobian norm bound。
- Source: Sec. 3.1.1, Sec. 3.1.2, Eq. (1)-(15)

### 阶段 2: 做鲁棒双层 NAS 优化
- 外层优化架构变量：
  `min_alpha L_val(w*(alpha),alpha) - gamma * R(w*(alpha),alpha)`。
- 内层在训练集上优化权重，外层在验证集上优化架构。
- Source: Sec. 3.2, Eq. (16)

### 阶段 3: 三个变体
- DSRNA-CB：`R` 取 certified lower bound。
- DSRNA-Jacobian：`R` 取 Jacobian norm bound。
- DSRNA-Combined：两种 `R` 相加。
- Source: Sec. 3.2

## 伪代码
```text
Algorithm: DSRNA
Input: 带架构变量 alpha 的超网, 训练集 Dtr, 验证集 Dval, gamma
Output: 鲁棒架构 alpha*

1. 初始化网络权重 w 和架构变量 alpha。
   Source: Sec. 3.2 (DARTS-style setup)
2. 每个搜索 step:
   2.1 用训练损失更新 w。
       Source: Eq. (16), inner problem
   2.2 用一步梯度更新近似 w*(alpha)。
       Source: Sec. 3.2 (Eq. 16 后文字描述)
   2.3 计算外层目标:
       J(alpha)=L_val(w*(alpha),alpha)-gamma*R(w*(alpha),alpha)。
       Source: Eq. (16)
   2.4 对 alpha 做梯度更新。
       Source: Eq. (16)
3. 从优化后的 alpha 离散化得到最终架构。
   Source: Inference from source
```

## 训练流程
1. 搜索阶段：联合更新权重和架构变量，优化“精度 + 鲁棒性”目标。
2. 架构导出：根据架构变量选出离散操作。
3. 最终训练：堆叠 cell 后从头训练目标网络。

Sources:
- Sec. 3.2, Sec. 4.2.2

## 推理流程
1. 用搜索得到的架构进行标准推理。
2. 在无攻击与多种攻击下报告性能（PGD/FGSM/C&W/AutoAttack）。
3. 可用文中认证流程报告 certifiable lower bound。

Sources:
- Sec. 4.3.1, Sec. 4.3.2, Table 1-6

## 复杂度与效率
- 时间复杂度: 论文未给完整闭式公式。
- 空间复杂度: 论文未给完整闭式公式。
- 运行特征（单 GTX1080Ti）:
  - CIFAR-10 搜索：DSRNA-CB 4 GPU days；DSRNA-Jacobian 0.4 GPU days。
  - MNIST 搜索：DSRNA-CB 1 GPU day；DSRNA-Jacobian 0.2 GPU day。
- 扩展性: CB 更稳健但更慢，Jacobian 更快但鲁棒性略弱。

## 实现备注
- 搜索空间沿用 PC-DARTS（8 个候选算子）。
- 搜索网络：8 cells，50 epochs，初始通道 16。
- 最终训练（CIFAR-10/MNIST）：20 cells，600 epochs，初始通道 36。
- 关键权衡系数：`gamma = 0.01`。
- 代码情况：未发现论文官方仓库链接，本地无可归档官方实现。

## 与相关方法关系
- 对比 [[SDARTS-ADV]] / [[PC-DARTS-ADV]]:
  DSRNA 是“显式鲁棒目标”，而非主要依赖对抗扰动正则。
- 对比 [[RobNet]]:
  DSRNA 在鲁棒性与 clean accuracy 上更均衡。
- 主要优势: 指标可解释、结果稳定、且有 verification-based 证据支持。
- 主要代价: CB 版本搜索成本较高，且官方代码缺失影响复现。

## 证据与可追溯性
- 关键图: Fig. 1（方法总览）
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 5, Table 6
- 关键公式: Eq. (12)-(16)，以及 Eq. (1)-(11) 的界传播
- 关键算法: Sec. 3.2 描述的双层优化流程（详细算法在补充材料）

## 参考链接
- arXiv: https://arxiv.org/abs/2012.06122
- HTML: https://arxiv.org/html/2012.06122
- 代码: Not found
- 本地实现: Not archived
