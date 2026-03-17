---
title: "RNAS-CL_ch"
type: method
language: zh-CN
source_method_note: "[[RNAS-CL]]"
source_paper: "Robust neural architecture search by cross-layer knowledge distillation"
source_note: "[[RNAS-CL]]"
authors: [Utkarsh Nath, Yancheng Wang, Yingzhen Yang]
year: 2023
venue: ICLR 2023 Workshop
tags: [nas-method, zh, robustness, knowledge-distillation]
created: 2026-03-17
updated: 2026-03-17
---

# RNAS-CL 中文条目

## 一句话总结
> RNAS-CL 用可微分的 Gumbel-Softmax 同时搜索“学生层该向哪一层老师学”和“每层用多少通道”，在延迟约束下得到更鲁棒且更紧凑的架构。

## 来源
- 论文: [Robust neural architecture search by cross-layer knowledge distillation](https://openreview.net/forum?id=VQfWcqPjJP)
- PMLR: https://proceedings.mlr.press/v220/nath23a.html
- 代码: https://github.com/Statistical-Deep-Learning/RNAS-CL
- 英文方法笔记: [[RNAS-CL]]
- 论文笔记: [[RNAS-CL]]
- 本地代码: `D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation`

## 适用场景
- 问题类型: 需要在图像分类里同时优化鲁棒性与效率的 NAS。
- 前提假设: 已有可用的鲁棒教师模型，且教师中间层信息对学生有效。
- 数据形态: 有监督分类，支持对抗评测；可选对抗再训练。
- 规模约束: 适合 FBNetV2 风格的可微超网搜索。
- 适用原因: 方法把鲁棒监督和延迟约束放进同一个搜索目标。

## 不适用或高风险场景
- 需要可认证鲁棒性（certified robustness）。
- 没有鲁棒教师权重可用。
- 搜索空间不能做可微架构参数化。

## 输入、输出与目标
- 输入: 数据集 `D`、鲁棒教师 `T`、学生超网 `S`、温度退火策略 `tau`、损失权重与延迟项。
- 输出: 离散化后的最终架构与层级 tutor 映射。
- 目标: 在延迟/算力约束下提升 clean + adversarial 表现。
- 核心假设: 学生层自动选 tutor 能显著提升鲁棒性。

## 方法拆解

### 阶段 1：构建跨层 teacher-student 搜索图
- 给每个学生层连到所有教师层，建立可学习的 tutor 权重。
- Source: Sec. 3.1, Sec. 3.2, Fig. 2

### 阶段 2：可微 tutor 搜索
- 用 Gumbel-Softmax 近似离散层匹配。
- 通过温度退火从软分配走向近 one-hot 分配。
- Source: Sec. 3.2, Eq. (1) context

### 阶段 3：可微通道搜索
- 每个卷积块通道数通过 Gumbel 权重搜索（FBNetV2 风格）。
- 与延迟项联合优化。
- Source: Sec. 3.3, Sec. 3.4

### 阶段 4：离散化并训练最终模型
- 对 tutor 与通道选择做 argmax 离散化。
- 用训练阶段损失重训；可选 TRADES 进一步提升鲁棒性。
- Source: Sec. 3.4, Sec. 4.1, Appendix A.3

## 伪代码
```text
Algorithm: RNAS-CL
Input: teacher T, supernet S, dataset D, temperature schedule tau
Output: final architecture A, tutor mapping M

1. 初始化超网参数与 tutor 分配参数。
   Source: Sec. 3.2, Fig. 2
2. 在搜索循环中:
   2.1 前向得到 student/teacher 输出与中间特征。
       Source: Sec. 3.1, Sec. 3.4
   2.2 用 gumbel tutor 权重计算跨层 KD 对齐项。
       Source: Sec. 3.2, Eq. (1)
   2.3 用 latency-aware 搜索损失更新网络与架构参数。
       Source: Sec. 3.4, Eq. (2)
   2.4 按退火策略更新 tau。
       Source: Appendix A.1
3. 对 tutor 与通道选项做 argmax，得到离散架构。
   Source: Sec. 3.4
4. 按训练阶段目标重训模型（可替换为 TRADES 目标）。
   Source: Eq. (3), Sec. 4.1 / Appendix A.3
```

## 训练流程
1. Search phase: 联合更新网络参数与架构/层匹配参数。
2. Discretization: 把 soft 选择变成 hard 选择。
3. Train phase: 从头训练离散架构，必要时加 TRADES。

Sources:
- Sec. 3.4, Sec. 4, Appendix A.1/A.3, plus `imageNetDA/search.py` and `imageNetDA/train.py`.

## 推理流程
1. 仅使用离散后的最终架构推理。
2. clean 评测按普通分类流程。
3. robust 评测按 FGSM/PGD/MI-FGSM 协议。

Sources:
- Sec. 4, Table 1, Appendix A.2.

## 复杂度与效率
- tutor 搜索原始空间是指数级 `n_t^{n_s}`，通过 Gumbel-Softmax 可微近似。
- 延迟项与主损失联合优化。
- CIFAR-10 报告从超小模型（0.11M）到大模型（11M）的可扩展配置。

## 实现备注
- 搜索脚本: `imageNetDA/search.py`
- 训练脚本: `imageNetDA/train.py`
- 温度配置: `base_temperature=5.0`, `temp_factor=-0.045`
- 复现提醒: 论文强调 attention-map 对齐；公开代码核心模块更突出卷积权重级 KL 对齐，建议复现时优先以代码为准并记录差异。

## 与相关方法关系
- 对比 [[DARTS]] / [[PC-DARTS]]:
- 增加了跨层 tutor 搜索和鲁棒蒸馏目标。
- 对比 Hydra/LWM 等鲁棒剪枝:
- 在论文给定设置中，clean 准确率更高，同时保持可比对抗鲁棒性。
- 主要优势: 同一套搜索兼顾鲁棒与效率。
- 主要代价: 对教师质量和实现细节较敏感。

## 证据与可溯源性
- 关键图: Fig. 1-5
- 关键表: Table 1-4
- 关键公式: Eq. (1)-(3)
- 关键算法位置: Sec. 3.2-3.4

## 参考链接
- OpenReview: https://openreview.net/forum?id=VQfWcqPjJP
- PMLR: https://proceedings.mlr.press/v220/nath23a.html
- Code: https://github.com/Statistical-Deep-Learning/RNAS-CL
- 本地实现: D:/PRO/essays/code_depots/Robust neural architecture search by cross-layer knowledge distillation
