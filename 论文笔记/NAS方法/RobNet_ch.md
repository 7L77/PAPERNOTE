---
title: "RobNet_ch"
type: method
language: zh-CN
source_method_note: "[[RobNet]]"
source_paper: "When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks"
source_note: "[[RobNet]]"
authors: [Minghao Guo, Yuzhe Yang, Rui Xu, Ziwei Liu, Dahua Lin]
year: 2020
venue: CVPR
tags: [nas-method, zh, robust-nas, one-shot-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# RobNet 中文条目

## 一句话总结
> RobNet 通过“鲁棒 one-shot 搜索 + 架构统计规律 + FSP 过滤”三步，从大搜索空间中高效筛出更抗对抗攻击的 CNN 架构家族。

## 来源
- 论文: [When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks](https://arxiv.org/abs/1911.10695)
- HTML: https://openaccess.thecvf.com/content_CVPR_2020/html/Guo_When_NAS_Meets_Robustness_In_Search_of_Robust_Architectures_Against_CVPR_2020_paper.html
- 代码: https://github.com/gmh14/RobNets
- 英文方法笔记: [[RobNet]]
- 论文笔记: [[RobNet]]

## 适用场景
- 问题类型: 面向图像分类的对抗鲁棒 NAS。
- 前提假设: 可以用 supernet 共享权重近似评估大量候选架构。
- 数据形态: 有监督图像数据 + 对抗训练流程。
- 规模与约束: 适合“逐候选完整训练成本过高”的搜索场景。
- 适用原因: 通过短微调和统计筛选显著降低大规模鲁棒评估成本。

## 不适用或高风险场景
- 你需要攻击无关的理论鲁棒保证（而非经验鲁棒）。
- 搜索空间难以表示成边操作组合，无法套用其统计规则。
- 你需要完整开源的“搜索 + 过滤”实现细节（官方仓库主要是已搜索模型训练/评测）。

## 输入、输出与目标
- 输入: 搜索空间 `S`、训练集 `D`、攻击配置（`epsilon`、PGD 步数等）、采样预算 `K`。
- 输出: RobNet-small/medium/large/free 等鲁棒架构。
- 优化目标: 在统一训练协议下提升 adversarial accuracy，并总结可迁移的结构规律。
- 核心假设: one-shot 排序 + 短对抗微调足以反映候选架构鲁棒性差异。

## 方法拆解

### 阶段 1: 鲁棒 supernet 训练
- 构建覆盖候选操作的 supernet。
- 每个 batch 随机采样子网络并执行 min-max 对抗训练。
- Source: Sec. 3.1, Sec. 3.2, Eq. (1)

### 阶段 2: 候选采样与鲁棒评估
- 从 supernet 随机采样候选架构。
- 对每个候选做少量 epoch 的对抗微调，再用 PGD white-box 测鲁棒精度。
- Source: Sec. 3.2, Fig. 3

### 阶段 3: Cell-based 规律挖掘
- 对高鲁棒/低鲁棒候选做结构统计，得到“密连接更鲁棒”与“小预算优先 direct edge 卷积”的规则。
- Source: Sec. 3.3, Eq. (2), Fig. 4/5; Sec. 3.4, Fig. 6

### 阶段 4: Cell-free FSP 过滤
- 在更大搜索空间中，用 clean/adv 的 FSP 距离先过滤高风险候选，再做微调评估。
- Source: Sec. 3.5, Eq. (3), Eq. (4), Fig. 7

## 伪代码
```text
Algorithm: RobNet 鲁棒架构发现流程
Input: 搜索空间 S, 数据 D, 攻击配置 A, 采样预算 K
Output: 鲁棒架构集合 R*

1. 构建包含所有候选边操作的 supernet。
   Source: Sec. 3.2
2. 训练阶段循环:
   2.1 随机采样一个子网络路径（path dropout）。
       Source: Sec. 3.2
   2.2 用 min-max 目标执行对抗训练。
       Source: Eq. (1)
3. 从训练后 supernet 采样 K 个候选架构。
   Source: Sec. 3.2
4. 对每个候选:
   4.1 做短轮数对抗微调。
       Source: Sec. 3.2, Fig. 3
   4.2 在 PGD white-box 下测 adversarial accuracy。
       Source: Sec. 3.2
5. Cell-based 模式下，依据密度 D 与 direct-conv 比例筛选鲁棒模式。
   Source: Sec. 3.3, Eq. (2), Fig. 5; Sec. 3.4, Fig. 6
6. Cell-free 模式下，计算每层 FSP loss，先剔除高损候选再微调。
   Source: Sec. 3.5, Eq. (3), Eq. (4), Fig. 7
7. 选取代表性结构组成 RobNet 家族。
   Source: Sec. 4.1, Table 1-3
```

## 训练流程
1. 定义搜索空间并构建 supernet。
2. 执行 PGD 对抗训练。
3. 采样候选并做短微调。
4. 按鲁棒精度排序并提取结构规律。
5. 选出 RobNet 代表结构并执行统一对抗训练评测。

Sources:
- Sec. 3.2-3.5
- Sec. 4.1

## 推理流程
1. 加载 RobNet 结构编码与权重。
2. 在 clean 与对抗样本上做测试。
3. 报告 white-box 与 transfer-based black-box 指标。

Sources:
- Sec. 4.2, 4.3
- Table 1, Table 2

## 复杂度与效率
- Cell-based 搜索规模约 `~10^8`（文中设定 `N=4`）。
- Cell-free 会随层数指数膨胀（文中讨论 `(10^8)^L` 级别）。
- one-shot + 短微调使“大规模鲁棒架构分析”可落地。
- FSP 过滤用于在大空间中减少昂贵候选评估。

## 实现备注
- 本地代码: `D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks`
- `main.py`: 训练模式将 `num_steps` 设为 7，对齐论文训练协议。
- `attack.py`: 实现 PGD（随机起点 + 符号梯度迭代 + 投影裁剪）。
- `architecture_code.py`: 保存 `robnet_large_v1/v2` 与 `robnet_free` 架构编码。
- `models/basic_operations.py`: `00/01/10/11` 对应 zero/sepconv/identity/res-sepconv 的代码实现。
- 与论文差异: 仓库重点是“已搜索模型训练与评估”；完整搜索与 FSP 过滤流程未完全公开。

## 与相关方法关系
- 对比 [[One-shot NAS]] 的自然精度导向搜索: RobNet 显式面向对抗鲁棒目标。
- 对比人工架构（如 DenseNet/ResNet）: 在相近或更小参数量下可获得更高鲁棒精度。
- 主要优势: 规则清晰、可执行、实验收益稳定。
- 主要代价: 依赖对抗训练和攻击配置，计算开销仍然不低。

## 证据与可溯源性
- 关键图: Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6, Fig. 7
- 关键表: Table 1, Table 2, Table 3, Table 4
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (4)
- 关键算法: Appendix robust search pseudocode（Sec. 3.2 提及）

## 参考链接
- arXiv: https://arxiv.org/abs/1911.10695
- HTML: https://openaccess.thecvf.com/content_CVPR_2020/html/Guo_When_NAS_Meets_Robustness_In_Search_of_Robust_Architectures_Against_CVPR_2020_paper.html
- 代码: https://github.com/gmh14/RobNets
- 本地实现: D:/PRO/essays/code_depots/When NAS Meets Robustness In Search of Robust Architectures against Adversarial Attacks
