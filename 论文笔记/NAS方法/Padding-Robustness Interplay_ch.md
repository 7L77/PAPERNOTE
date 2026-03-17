---
title: "Padding-Robustness Interplay_ch"
type: method
language: zh-CN
source_method_note: "[[Padding-Robustness Interplay]]"
source_paper: "On the Interplay of Convolutional Padding and Adversarial Robustness"
source_note: "[[Padding-Robustness Interplay]]"
authors: [Paul Gavrikov, Janis Keuper]
year: 2023
venue: ICCV Workshop
tags: [nas-method, zh, adversarial-robustness, cnn-padding]
created: 2026-03-17
updated: 2026-03-17
---

# Padding-Robustness Interplay 中文条目

## 一句话总结
> 这篇工作不是提出新网络，而是做了一个系统化实验框架，分析卷积 padding 方式如何影响对抗鲁棒性评估与结论。

## 来源
- 论文: [On the Interplay of Convolutional Padding and Adversarial Robustness](https://arxiv.org/abs/2308.06612)
- HTML: https://arxiv.org/html/2308.06612
- 代码: 论文未提供官方仓库链接
- 英文方法笔记: [[Padding-Robustness Interplay]]
- 论文笔记: [[Padding-Robustness Interplay]]

## 适用场景
- 问题类型: 需要分析 CNN 结构细节（尤其边界处理）对鲁棒性的影响。
- 前提假设: 主干网络固定，仅切换 padding 与 kernel size。
- 数据形态: 监督学习图像分类（类似 CIFAR）。
- 规模约束: 能负担多攻击、多配置、多随机种子的评估。
- 适用原因: 该框架能把“训练策略影响”和“padding 影响”拆开看。

## 不适用或高风险场景
- 你要的是一个新的 SOTA 鲁棒模型，而不是诊断分析框架。
- 你希望直接推广到 Transformer 或检测/分割任务。
- 你无法做多攻击评估，只能跑单一攻击。

## 输入、输出与目标
- 输入: backbone、padding mode、kernel size、训练方式、攻击集合。
- 输出: clean/robust accuracy、扰动分布、解释图偏移、运行时开销。
- 目标: 找到 padding 选择对鲁棒性结论的真实影响与评估偏差。
- 核心假设: 感受野与边界 padding 区域的相互作用会改变攻击行为。

## 方法拆解

### 阶段 1: 构建受控实验网格
- padding mode: zeros / reflect / replicate / circular。
- kernel size: 3/5/7/9，并按 same padding 设置边界。
- 同时训练普通模型与 FGSM 对抗训练模型。
- Source: Sec. 3, Training Details

### 阶段 2: 多攻击鲁棒性评估
- 评估 APGD-CE、FAB、Square、AutoAttack。
- 同时看聚合分数与分攻击排名。
- Source: Sec. 3.2, Fig. 3, Table 2

### 阶段 3: 机制与代价分析
- 扰动边界分布分析（Fig. 4）。
- LayerCAM 决策偏移分析（Fig. 5）。
- padding/卷积时延基准（Table 3）。
- 无 padding 变体（Table 4）。
- Source: Sec. 3.3-3.6

## 伪代码
```text
Algorithm: Padding-Robustness Interplay Evaluation
Input: 数据集 D, 主干 B, padding 集合 M, kernel 集合 K, 攻击集合 A, 训练模式 T
Output: clean/robust 指标与机制分析结果

1. 对每个 t in T、每个 (m,k) in MxK 训练模型 B_{t,m,k}。
   Source: Sec. 3, Training Details
2. 对每个模型计算 clean accuracy 与各攻击 robust accuracy。
   Source: Sec. 3.1, Sec. 3.2
3. 统计成功攻击样本的扰动分布（边界异常）。
   Source: Sec. 3.3, Fig. 4
4. 计算 LayerCAM 在 clean 与 adversarial 之间的偏移。
   Source: Sec. 3.5, Fig. 5
5. 测量不同 padding 的算子耗时与卷积总耗时。
   Source: Sec. 3.4, Table 3
6. 测试无 padding 及其补偿方案并对比。
   Source: Sec. 3.6, Table 4
7. 输出按训练模式与攻击协议区分的建议。
   Source: Sec. 4
```

## 训练流程
1. CIFAR-10 标准归一化与随机翻转。
2. SGD + Nesterov，75 epochs。
3. 对抗训练采用 FGSM Linf 8/255，按 PGD 鲁棒性早停。
4. 关键结果取多随机种子平均。

Sources:
- Sec. 3, Training Details

## 推理/评估流程
1. 在给定预算下生成攻击样本。
2. 统计不同配置模型的 clean/robust 准确率。
3. 做按攻击类型与聚合指标的双重比较。

Sources:
- Sec. 3.1, Sec. 3.2

## 复杂度与效率
- 时间复杂度: 论文未给解析式。
- 空间复杂度: 论文未给解析式。
- 运行特征: 在他们的 GPU 基准里，zero padding 的 padded-conv 最快。
- 扩展性说明: 增大 kernel 在该设置下常提升鲁棒性，但效果受训练模式影响。

## 实现备注
- 论文未给出官方代码仓库，复现需自行实现评测脚本。
- 仅看 AutoAttack 聚合值可能掩盖分攻击上的反转现象。
- 对抗训练场景下 circular 表现最差，reflect/replicate 常有竞争力。
- 去掉 padding 的替代方案整体不推荐。

## 与相关方法关系
- 对比 [[Adversarial Training]]: 本文是结构因素分析，不是替代训练算法。
- 对比仅用 [[AutoAttack]] 的常规评估: 本文强调分攻击报告的重要性。
- 主要优势: 给出可执行的工程建议（padding 选择 + 评测方式）。
- 主要代价: 证据范围仅 CIFAR-10 + ResNet-20。

## 证据与可溯源性
- 关键图: Fig. 1, 3, 4, 5, 6
- 关键表: Table 1, 2, 3, 4
- 关键公式: Eq. (1)
- 关键算法: 无新算法，核心是实验协议设计

## 参考链接
- arXiv: https://arxiv.org/abs/2308.06612
- HTML: https://arxiv.org/html/2308.06612
- 代码: 论文未报告官方链接
- 本地实现: Not archived (no official paper code link found as of 2026-03-17)

