---
title: "Task Adaptation RL-NAS Transfer_ch"
type: method
language: zh-CN
source_method_note: "[[Task Adaptation RL-NAS Transfer]]"
source_paper: "Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning"
source_note: "[[Task Adaptation of Reinforcement Learning-Based NAS Agents Through Transfer Learning]]"
authors: [Amber Cassimon, Siegfried Mercelis, Kevin Mets]
year: 2024
venue: arXiv
tags: [nas-method, zh, reinforcement-learning, transfer-learning, transnasbench-101]
created: 2026-03-17
updated: 2026-03-17
---

# Task Adaptation RL-NAS Transfer 中文条目

## 一句话总结
> 先在源任务上预训练 RL-NAS agent，再把参数迁移到目标任务进行少量或完整训练，通常能同时提升目标性能并缩短达到基线性能的训练时间。

## 来源
- 英文方法笔记: [[Task Adaptation RL-NAS Transfer]]
- arXiv: https://arxiv.org/abs/2412.01420
- HTML: https://arxiv.org/html/2412.01420v2
- 代码: 论文正文未给出官方仓库

## 适用场景
- 问题类型: 基于强化学习的 NAS 跨任务迁移。
- 前提假设: 源任务与目标任务共享或兼容同一搜索空间/环境接口。
- 数据形态: 基准驱动的 RL 交互训练（非端到端监督训练）。
- 适配原因: 迁移初始化权重可以减少目标任务冷启动成本。

## 不适用或高风险场景
- 任务间搜索空间不兼容。
- 奖励分布差异很大且未做归一化/塑形。
- 源任务预训练策略本身质量不足。

## 输入、输出、目标
- 输入: 源任务 `Ts`、目标任务 `Tt`、源任务预训练参数 `theta_s`。
- 输出: 目标任务适配后的参数 `theta_t` 及其搜索到的架构。
- 目标: 降低目标任务训练成本，同时保持或提升最终性能。
- 关键假设: 架构编辑行为在任务间有可迁移性。

## 方法拆解
### 阶段 1: 任务选择
- 基于 TransNAS-Bench-101 的 Kendall tau 相关矩阵选取相关性较低的任务组合。
- Source: Sec. 3.1 / Fig. 1

### 阶段 2: 源任务预训练
- 每个源任务先训练 `1e7` timesteps。
- Source: Sec. 4

### 阶段 3: 迁移到目标任务
- 将源任务参数作为目标任务初始化，并执行三种策略之一:
  - 零样本迁移（zero-shot）,
  - 微调（+`1e6` steps）,
  - 完整再训练（+`1e7` steps）。
- Source: Sec. 4 / Figs. 5-7

### 阶段 4: 分割任务奖励塑形
- 对语义分割任务使用 `R'(s,a)=R(s,a)^gamma`，`gamma=0.478`。
- Source: Sec. 3.2 / Figs. 2-4

## 伪代码
```text
Algorithm: Task Adaptation RL-NAS Transfer
Input: task set T, source task Ts, target task Tt, RL-NAS agent A
Output: adapted target-task agent At and searched architectures

1. 在 Ts 上预训练 As，训练 1e7 timesteps。
   Source: Sec. 4
2. 用 As 参数初始化 At。
   Source: Sec. 3 (transfer setup)
3. 若 Tt 为 segmentsemantic，使用奖励塑形:
      R'(s,a) = R(s,a)^gamma, gamma = 0.478
   Source: Sec. 3.2 / Figs. 2-4
4. 选择训练策略:
   4.1 zero-shot: 不再训练，直接评估
       Source: Sec. 4
   4.2 fine-tuning: 在 Tt 上再训 1e6 steps
       Source: Sec. 4
   4.3 re-training: 在 Tt 上再训 1e7 steps
       Source: Sec. 4
5. 与从零训练 baseline 比较均值/方差/95%CI。
   Source: Sec. 4.1-4.3 / Figs. 5-13
```

## 训练流程
1. 构建 TransNAS-Bench-101 任务环境。
2. 在源任务上进行 Ape-X 风格分布式 Q-learning 训练。
3. 迁移到目标任务继续训练（按 regime）。
4. 使用测试集指标评估性能（训练期使用验证指标）。

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4.

## 推理流程
1. 用已适配 agent 在架构邻域中执行迭代编辑。
2. 依据策略/价值输出筛选候选架构。
3. 返回目标任务的候选或最优架构。

Sources:
- Source: Inference from source

## 复杂度与效率
- 时间成本主导项: `1e7 + (1e6 or 1e7)` 级别交互步数。
- 空间成本主导项: replay buffer + 模型参数。
- 经验结论: 迁移通常能减少达到 scratch 参考性能所需时间，但并非所有任务对都同样受益。

## 实现要点
- 使用 double Q-learning、dueling heads、3-step bootstrap + PEB。
- Adam 学习率 `5e-5`，梯度裁剪 `L2=40`。
- target network 每 8192 steps 更新。
- prioritized replay: 容量 `25k`，`alpha=0.6`，`beta=0.4`。
- 论文正文未提供官方实现仓库链接。

## 与相关方法对比
- 对比从零训练 RL-NAS: 迁移方案在多数任务对上更快且更好。
- 对比 zero-shot-only: 加少量目标训练（`1e6`）就能明显改善。
- 主要优势: 降低新任务启动成本。
- 主要代价: 受任务配对与共享搜索空间假设影响较大。

## 参考
- arXiv: https://arxiv.org/abs/2412.01420
- HTML: https://arxiv.org/html/2412.01420v2
- 代码: Not linked in paper
- 本地实现: Not archived

