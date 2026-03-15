---
title: "NADAR_ch"
type: method
language: zh-CN
source_method_note: "[[NADAR]]"
source_paper: "Neural Architecture Dilation for Adversarial Robustness"
source_note: "[[NADAR]]"
authors: [Yanxi Li, Zhaohui Yang, Yunhe Wang, Chang Xu]
year: 2021
venue: NeurIPS
tags: [nas-method, zh, robust-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# NADAR 中文条目

## 一句话总结
> NADAR 在不改动强 backbone 主体结构的前提下，搜索一个逐层附加的 dilation 分支，并通过标准损失约束与 FLOPs 约束实现“鲁棒性提升、精度损失可控”。

## 来源
- 论文: [Neural Architecture Dilation for Adversarial Robustness](https://openreview.net/forum?id=55FrYwhCN6)
- HTML: https://openreview.net/forum?id=55FrYwhCN6
- 代码: https://github.com/liyanxi12/NADAR（截至 2026-03-15 不可访问）
- 英文方法笔记: [[NADAR]]
- 论文笔记: [[NADAR]]

## 适用场景
- 问题类型: 图像分类中的对抗鲁棒架构优化。
- 前提假设: 已有在干净样本上精度较高的 backbone。
- 数据形态: 有标签图像数据，可运行对抗训练。
- 规模与约束: 不希望从零做 robust NAS，但可接受一定搜索成本。
- 适用原因: 只优化增量分支，成本与风险小于整网重搜。

## 不适用或高风险场景
- 没有可用的高质量 backbone。
- 需要可证明鲁棒性（certified robustness）而非经验攻击鲁棒性。
- 模型结构不支持 block 对齐与逐层相加融合。

## 输入、输出与目标
- 输入: backbone `f_b`、dilation 搜索空间、攻击配置、FLOPs 预算偏好。
- 输出: hybrid 架构 `f_hyb = f_b + f_d` 及其训练权重。
- 优化目标: 在标准损失约束下最小化对抗验证损失，并限制计算开销。
- 核心假设: dilation 分支能学习到与 backbone 互补的鲁棒特征。

## 方法拆解

### 阶段 1: 构建 Dilation Hybrid 网络
- backbone 按分辨率切成 `L` 个 block。
- 每个 block 附加一个 NAS cell，输出逐元素相加。
- Source: Sec. 3.1 / Fig. 1 / Eq. (2)

### 阶段 2: 可微搜索 + FLOPs 建模
- 在 NASNet-like cell 空间中做可微结构优化。
- 用 partial channel connections 降低搜索开销。
- 通过结构概率估计期望 FLOPs。
- Source: Sec. 3.1 / Sec. 3.3 / Eq. (8) / Eq. (9) / Eq. (10) / Eq. (11)

### 阶段 3: ADMM 约束双层优化
- 上层优化架构参数，下层优化网络权重。
- 两层都加入标准性能约束。
- Source: Sec. 3.4 / Eq. (12)-(22)

### 阶段 4: 离散化与重训练
- 从 supernet 导出离散架构后再重训评估。
- Source: Sec. 5.2 / Sec. 5.5 / Inference from source

## 伪代码
```text
Algorithm: NADAR
Input: 预训练 backbone f_b, dilation 搜索空间 S_d, 训练/验证数据, 攻击配置 A
Output: 鲁棒 hybrid 网络 f_hyb*

1. 将 f_b 按分辨率划分为 L 个 block。
   Source: Sec. 3.1
2. 为每个 block 挂接可搜索 dilation cell，并按 Eq. (2) 做逐层相加融合。
   Source: Fig. 1 / Eq. (2)
3. 构建对抗目标与标准损失约束。
   Source: Eq. (3) / Eq. (4) / Eq. (7) / Eq. (13) / Eq. (14)
4. 加入 FLOPs-aware 目标项。
   Source: Eq. (10) / Eq. (11) / Eq. (12)
5. 交替更新:
   - 架构参数 alpha_d 与拉格朗日乘子 lambda_1
   - 权重 omega_d 与拉格朗日乘子 lambda_2
   Source: Eq. (15)-(22)
6. 导出离散架构并在目标 AT 配置下重训练。
   Source: Sec. 5.2 / Inference from source
```

## 训练流程
1. 准备强 backbone（高标准精度）。
2. 在对抗训练循环中搜索 dilation 分支。
3. 保持标准约束与 FLOPs 约束。
4. 导出离散架构并按 PGD/FAT/TRADES 等设置重训。

Sources:
- Sec. 3.1-3.4
- Sec. 5.1-5.6

## 推理流程
1. 输入同时经过 backbone block 与 dilation cell。
2. 按 block 级别相加融合特征。
3. 分类头输出预测结果。

Sources:
- Eq. (2)
- Inference from source

## 复杂度与效率
- 额外开销来自 dilation 分支参数与计算量。
- FLOPs 约束可显著压缩增量开销（NADAR-B 相比 NADAR-A）。
- 搜索阶段仍偏重，因为需要对抗训练。

## 实现备注
- 搜索空间: NASNet-like cell。
- 关键优化: ADMM 约束优化 + partial channel connections + FreeAT。
- 消融结论: 去掉标准约束会明显恶化鲁棒/精度平衡（Table 7）。
- 代码状态: 官方链接已失效，当前未能本地归档。

## 与相关方法关系
- 对比 [[RACL]]: NADAR 用增量分支替代整网结构重参数化，并显式加入标准损失约束。
- 对比 [[RobNet]]: NADAR 更强调“固定 backbone + 结构扩张”。
- 主要优势: 在文中设定下鲁棒提升更明显且自然精度下降较小。
- 主要代价: 仍需额外搜索与重训成本。

## 证据与可溯源性
- 关键图: Fig. 1
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 6, Table 7
- 关键公式: Eq. (1), Eq. (2), Eq. (7), Eq. (10), Eq. (12), Eq. (15)-(22)
- 关键算法: Sec. 3.4 的 ADMM 交替更新

## 参考链接
- OpenReview: https://openreview.net/forum?id=55FrYwhCN6
- 代码: https://github.com/liyanxi12/NADAR（截至 2026-03-15 不可访问）
- 本地实现: Not archived
