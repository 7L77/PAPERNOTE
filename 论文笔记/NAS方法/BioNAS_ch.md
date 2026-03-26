---
title: "BioNAS_ch"
type: method
language: zh-CN
source_method_note: "[[BioNAS]]"
source_paper: "Neural Architecture Search with Mixed Bio-inspired Learning Rules"
source_note: "[[BioNAS]]"
authors: [Imane Hamzaoui, Riyadh Baghdadi]
year: 2025
venue: ECAI 2025 (arXiv preprint)
tags: [nas-method, zh, bio-inspired-learning, adversarial-robustness, darts, evolutionary-search]
created: 2026-03-25
updated: 2026-03-25
---

# BioNAS 中文条目

## 一句话总结
> BioNAS 把“架构算子选择”和“层级学习规则选择”放进同一个 NAS 流程里，实证显示混合规则配置比单一规则更稳、更准，也更抗攻击。

## 来源
- 论文: [Neural Architecture Search with Mixed Bio-inspired Learning Rules](https://arxiv.org/abs/2507.13485)
- HTML: https://arxiv.org/html/2507.13485v1
- 代码（论文声明）: https://anonymous.4open.science/r/LR-NAS-DFE1
- 英文方法笔记: [[BioNAS]]
- 论文笔记: [[BioNAS]]

## 适用场景
- 问题类型: 关注生物启发训练机制的 NAS。
- 前提假设: 不同网络层适配不同反馈/学习规则。
- 数据形态: 监督学习图像分类（CIFAR、ImageNet 系）。
- 规模与约束: 需要在准确率、鲁棒性、生物可解释性之间折中。
- 适用原因: 将学习规则从“固定超参”升级为“可搜索结构变量”。

## 不适用或高风险场景
- 只追求 BP 范式下的最高精度，不关心生物可解释性。
- 必须立即拿到可运行公开代码（匿名仓库当前不可访问）。
- 工程栈无法支持规则相关的反向传播实现差异。

## 输入、输出与目标
- 输入: 超网结构、候选算子集合、候选学习规则集合、训练/验证数据。
- 输出: 离散化后的最终架构（每条边包含算子+规则选择）及其训练模型。
- 优化目标: 提升验证性能与鲁棒性，同时保留生物启发信用分配机制。
- 核心假设: 异构规则组合能够带来更稳定优化动态。

## 方法拆解

### 阶段 1: 构建混合搜索空间
- 每条边的候选不再是单算子，而是 `(operation, learning-rule)` 二元组。
- Source: Sec. 3.2

### 阶段 2: BioNAS-DARTS 搜索
- 采用 DARTS 双层优化：训练集更新网络权重，验证集更新结构参数。
- 连续松弛 + 交替更新后，在每条边做离散选择。
- Source: Sec. 3.3, Eq. (6)-(10), Fig. 2

### 阶段 3: BioNAS-EG 搜索
- 用进化编码表示 op-rule 组合，结合 CMA-ES 做结构分布更新。
- 权重训练由 SGD 完成。
- Source: Sec. 3.3, Eq. (11)

### 阶段 4: 鲁棒性评估
- 白盒 + 黑盒攻击联合评估（FGSM/PGD/TPGD/APGD/One-Pixel/Square/Transfer）。
- Source: Sec. 3.5, Sec. 4.1, Table 4

## 伪代码
```text
Algorithm: BioNAS
Input:
  搜索图 G(边集 E)
  候选算子集合 O
  候选学习规则集合 R
  训练集 D_train, 验证集 D_val
Output:
  最终离散架构 A*（每条边给出一个 op-rule 选择）

1. 对每条边构建候选集合 C={(o,r) | o∈O, r∈R}。
   Source: Sec. 3.2
2. 初始化超网参数 w 与结构参数 alpha。
   Source: Sec. 3.3
3. 迭代搜索：
   3.1 在 D_train 上最小化 L_train 更新 w。
       Source: Eq. (6), Eq. (8)
   3.2 在 D_val 上最小化 L_val 更新 alpha。
       Source: Eq. (7), Eq. (9)
4. 每条边选择概率最高的 op-rule 组合并离散化得到 A*。
   Source: Eq. (10), Fig. 2
5. 重训并做 clean + adversarial 评测，输出最终结果。
   Source: Sec. 3.4-3.5, Table 1-4
```

## 训练流程
1. 构建 op-rule 混合搜索空间。
2. 运行 DARTS 或 EG 搜索。
3. 重训搜索得到的最终结构。
4. 报告准确率与鲁棒性指标。

Sources:
- Sec. 3.2-3.5
- Table 1-4

## 推理流程
1. 固定搜索后的结构与规则分配。
2. 对干净输入与攻击输入执行前向。
3. 统计 clean 与 robustness 指标。

Sources:
- Sec. 4.1
- Table 4

## 复杂度与效率
- 搜索空间增幅: 每条边从 `|O|` 扩到约 `|O| x |R|`。
- 报告的搜索成本:
  - BioNAS-EG: 0.35 GPU-days
  - BioNAS-DARTS: 1.37 GPU-days
- 报告性能:
  - CIFAR-10: 95.16
  - CIFAR-100: 76.48
  - ImageNet16-120: 43.42
  - ImageNet Top-1: 60.51

## 实现备注
- 主实验主要使用 FA/uSF/brSF/frSF。
- 也探索了 Hebbian 与 Predictive Coding 卷积（性能较低，但验证了框架可扩展）。
- 攻击评测覆盖梯度攻击与查询攻击。
- 代码归档状态: 论文匿名链接存在，但 2026-03-25 检查返回 `repository not found`。

## 与相关方法关系
- 对比 [[Differentiable Architecture Search]]:
  - BioNAS 不只搜操作，还搜学习规则。
- 对比 [[Evolutionary Neural Architecture Search]]:
  - 复用进化搜索框架，但基因表示加入规则维度。
- 对比单规则生物启发训练:
  - 混合规则在文中实验里更稳健、更高精度。
- 主要优势: 在生物可解释性约束下统一优化准确率与鲁棒性。
- 主要代价: 搜索空间更大、训练实现更复杂。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3
- 关键表: Table 1-5
- 关键公式: Eq. (1)-(11)
- 关键算法: Sec. 3.3 的 DARTS/EG 两条搜索实现

## 参考链接
- arXiv: https://arxiv.org/abs/2507.13485
- HTML: https://arxiv.org/html/2507.13485v1
- 代码: https://anonymous.4open.science/r/LR-NAS-DFE1
- 本地实现: Not archived（2026-03-25 检查不可访问）

