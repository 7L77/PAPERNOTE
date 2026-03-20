---
title: "Group Fisher Pruning_ch"
type: method
language: zh-CN
source_method_note: "[[Group Fisher Pruning]]"
source_paper: "Group Fisher Pruning for Practical Network Compression"
source_note: "[[Group Fisher Pruning]]"
authors: [Liyang Liu, Shilong Zhang, Zhanghui Kuang, Aojun Zhou, Jing-Hao Xue, Xinjiang Wang, Yimin Chen, Wenming Yang, Qingmin Liao, Wayne Zhang]
year: 2021
venue: ICML
tags: [nas-method, zh, pruning, model-compression, structured-pruning]
created: 2026-03-20
updated: 2026-03-20
---

# Group Fisher Pruning 中文条目

## 一句话总结

> Group Fisher Pruning 是一种面向复杂 CNN 结构的结构化通道剪枝方法：它先沿计算图自动找出必须同步删除的耦合通道组，再用 Fisher 近似估计共享 mask 的重要性，并按 memory reduction 做归一化贪心剪枝，从而把“理论压缩”尽量变成“真实 GPU 加速”。

## 来源

- 论文: [Group Fisher Pruning for Practical Network Compression](https://proceedings.mlr.press/v139/liu21ab.html)
- HTML: 本笔记采用的官方来源未提供 HTML 版
- arXiv: https://arxiv.org/abs/2108.00708
- 代码: https://github.com/jshilong/FisherPruning
- 英文方法笔记: [[Group Fisher Pruning]]
- 论文笔记: [[Group Fisher Pruning]]

## 适用场景

- 问题类型: 面向 CNN 的结构化通道剪枝与部署加速。
- 前提假设: 基模型已经训练到较稳定状态，且“删通道”是合法的压缩操作。
- 数据形态: 监督学习下的图像分类与目标检测。
- 规模与约束: 适合带残差、多分支、group/depth-wise conv、FPN 结构的 backbone 与 detector。
- 适用原因: 它显式建模跨层耦合通道，因此剪枝后结构仍然可部署，速度提升也更容易兑现到真实推理时间。

## 不适用或高风险场景

- 模型不具备清晰的 channel pruning 语义，例如以注意力模块为主、通道耦合关系不容易定义的结构。
- 你只能接受一次性剪枝，不愿意做迭代式 prune-finetune。
- 部署平台并非 GPU 风格，memory reduction 和 latency 的关系不稳定。

## 输入、输出与目标

- 输入: 已收敛的 dense 模型 `W^0`、训练数据、剪枝间隔 `d`、目标计算预算。
- 输出: 剪枝后的模型 `W` 与每个通道/通道组对应的二值 mask `m`。
- 优化目标: 迭代删除“单位开销下降下导致最小 loss 增长”的通道或通道组。
- 核心假设: 收敛点附近的 Taylor/Fisher 近似是有效的；耦合通道必须共享 mask 才能保持结构合法。

## 方法拆解

### 阶段 1: 通道 mask 参数化

- 给每个 Conv/FC 输入通道加一个二值 mask，并把它乘到输入特征上。
- 把某个 mask 置零，就等于剪掉对应输入通道。
- Source: Sec. 3, Sec. 3.1, Eq. (1)

### 阶段 2: 单通道 Fisher 重要性

- 用二阶 Taylor 展开近似“删掉通道 `i` 后 loss 会涨多少”。
- 再用 Fisher 近似 Hessian 对角项，把重要性写成 mask 梯度平方的形式。
- Source: Sec. 3.1, Eq. (1), Eq. (2), Eq. (3)

### 阶段 3: layer grouping 识别耦合通道

- 沿计算图做 DFS，给每个 Conv/FC 层找最近的 Conv 父节点。
- 若不同层共享父节点，说明它们的通道耦合，应分到同一组。
- 遇到 group conv 或 depth-wise conv 时，还要把组内输入输出通道耦合一起考虑。
- Source: Sec. 3.2, Fig. 3, Fig. 4, Algorithm 1

### 阶段 4: 组重要性与贪心剪枝

- 对共享同一个 mask 的所有通道，把跨层梯度先求和再平方，得到组重要性。
- 再用 memory reduction 而不是 FLOPs reduction 做归一化。
- 每隔 `d` 次迭代，删除当前归一化重要性最小的通道或通道组。
- Source: Sec. 3.2, Eq. (4), Sec. 3.3, Fig. 6, Algorithm 2

### 阶段 5: 结构落地与微调

- 达到目标预算后，把零 mask 真正切成更小的 Conv/BN 参数张量。
- 再对压缩后的紧凑模型做 fine-tune。
- Source: Sec. 3, Algorithm 2; 代码证据见 `deploy_pruning()`

## 伪代码

```text
Algorithm: Group Fisher Pruning
Input: 已收敛 dense 模型 W^0，训练数据 D，剪枝间隔 d，目标预算
Output: 剪枝模型 W，共享通道 mask m

1. 给所有 Conv/FC 层挂上二值输入 mask，初始全为 1。
   Source: Sec. 3, Sec. 3.1
2. 构建计算图并做 DFS，找到每个层最近的父卷积。
   Source: Fig. 4, Algorithm 1
3. 把结构上耦合的层分组，并让同组通道共享同一个 mask。
   Source: Sec. 3.2, Fig. 3, Algorithm 1
4. 在训练过程中累积 mask 梯度，估计每层/每组的 Fisher 重要性。
   Source: Eq. (2), Eq. (3), Eq. (4)
5. 用“重要性 / memory reduction”作为归一化分数。
   Source: Sec. 3.3, Fig. 6
6. 每隔 d 次迭代，剪掉分数最小的通道或通道组。
   Source: Algorithm 2
7. 重复累积与剪枝，直到达到目标 FLOPs 预算。
   Source: Algorithm 2
8. 按 mask 真正裁剪参数张量，并对紧凑模型做 fine-tune。
   Source: Inference from source; 代码证据见 deploy_pruning()
```

## 实现备注

- 架构: 公共代码把方法包装成 MMCV 的 `FisherPruningHook`。
- 超参数: 论文里分类任务每 `25` iter 剪一次，检测任务每 `10` iter 剪一次。
- 约束 / masking: 每个 Conv 都有 `in_mask` 和 `out_mask`；同一耦合组共享 `in_mask`。
- 技巧: 不是一次性删完，而是“边训练边估分边删”。
- 注意事项:
  - 公共仓库要求 `pytorch==1.3.0`，因为 layer grouping 依赖旧版 autograd graph。
  - 代码中的 `delta='acts'` 本质上就是 paper 里 memory-like proxy 的工程实现。
  - 公开仓库以 detection 为主，classification 代码没有完整公开。
  - `set_group_masks()` 里还有 `# TODO: support two stage model`，说明 paper 与公开代码覆盖范围并不完全一致。

## 与相关方法的关系

- 对比 [[Channel Pruning]] 里的 CP / ThiNet: 本方法是 global pruning，不需要手工做 layer-wise sensitivity analysis。
- 对比 IE / C-SGD 这类 heuristic coupling 方法: 它把共享 mask 的重要性直接建立在链式法则上，而不是启发式拼分数。
- 主要优势: 能把复杂结构里的 coupled channels 作为一等公民处理，并更关注真实 GPU 友好的效率提升。
- 主要代价: 工程复杂度高，且依赖迭代式训练与图结构分析。

## 证据与可溯源性

- 关键图: Fig. 3, Fig. 4, Fig. 5, Fig. 6
- 关键表: Table 1, Table 2, Table 3, Table 5, Table 6
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (4)
- 关键算法: Algorithm 1, Algorithm 2

## 参考链接

- PMLR: https://proceedings.mlr.press/v139/liu21ab.html
- arXiv: https://arxiv.org/abs/2108.00708
- 代码: https://github.com/jshilong/FisherPruning
- 本地实现: D:/PRO/essays/code_depots/Group Fisher Pruning for Practical Network Compression
