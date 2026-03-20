---
title: "Fisher Pruning for Gaze Prediction_ch"
type: method
language: zh-CN
source_method_note: "[[Fisher Pruning for Gaze Prediction]]"
source_paper: "Faster Gaze Prediction With Dense Networks and Fisher Pruning"
source_note: "[[Faster gaze prediction with dense networks and Fisher pruning]]"
authors: [Lucas Theis, Iryna Korshunova, Alykhan Tejani, Ferenc Huszar]
year: 2018
venue: arXiv
tags: [nas-method, zh, pruning, saliency, distillation]
created: 2026-03-20
updated: 2026-03-20
---

# Fisher Pruning for Gaze Prediction 中文条目

## 一句话总结
> 这套方法先用 DeepGaze 风格 teacher 做蒸馏，再用基于经验 Fisher 的 feature-map 剪枝信号配合 FLOPs 正则，得到更快的 saliency / gaze prediction 网络。

## 来源
- 论文: [Faster Gaze Prediction With Dense Networks and Fisher Pruning](https://arxiv.org/abs/1801.05787)
- HTML: https://arxiv.org/html/1801.05787
- 代码: 论文和作者页未提供官方代码（检查时间 2026-03-20）
- 英文方法笔记: [[Fisher Pruning for Gaze Prediction]]
- 论文笔记: [[Faster gaze prediction with dense networks and Fisher pruning]]

## 适用场景
- 问题类型: 静态图像显著性 / 注视点预测，并且关心 CPU 推理延迟。
- 前提假设: 已有强 teacher；feature map 对输出分布的梯度敏感度能反映其保留价值。
- 数据形态: fixation 标注 + teacher 生成的 saliency map。
- 规模与约束: 卷积网络、通道剪枝能带来真实速度收益的场景。
- 适用原因: 它不是只看权重大小，而是直接优化“任务损失上涨 vs 计算量下降”的权衡。

## 不适用或高风险场景
- 你需要的是 training-free 的架构评分，而不是先训练再压缩。
- 模型不具备清晰的通道结构，删 feature map 不能转化成实际加速。
- 没有可靠 teacher 或没有概率型监督，经验 Fisher 信号会变得不稳。

## 输入、输出与目标
- 输入: 图像 `I`、fixation 标签 `z`、teacher saliency map、student backbone 特征、当前 feature-map 激活。
- 输出: 剪枝后的 saliency 模型，以及像素级 fixation probability map。
- 优化目标: 在尽量保持 saliency 交叉熵的同时，显著降低 FLOPs。
- 核心假设: 局部二阶损失变化可由经验 Fisher 对角近似；FLOPs 的降低能对应到实际推理速度收益。

## 方法拆解

### 阶段 1: 构建更轻量的 saliency student
- 用 VGG-11 或 DenseNet-121 替代 DeepGaze II 的重型 VGG-19 多层特征堆叠。
- 先做 readout 再上采样，并把 Gaussian blur 做成 separable 形式。
- Source: Sec. 2, Eq. (1)

### 阶段 2: 用 teacher 做蒸馏训练
- 先训练 DeepGaze II teacher，并对 SALICON 生成 teacher saliency map。
- student 用 fixation 交叉熵和 teacher-map 交叉熵的加权和训练。
- Source: Sec. 2.4

### 阶段 3: 用 Fisher pruning 给 feature map 打分
- 给每个 feature map 引入二值 mask，并用平方梯度估计删除该通道的损失增量。
- 通过经验 Fisher 近似避免显式 Hessian 计算。
- Source: Sec. 2.1, Eq. (2)-(9), Supplementary Sec. S1/S2

### 阶段 4: 在计算约束下做贪心剪枝
- 先计算当前网络的 FLOPs，再把 `DeltaL` 和 `DeltaC` 合并成一个拉格朗日目标。
- 每轮删除综合代价最小的 feature map，继续训练，再重复。
- Source: Sec. 2.2, Eq. (10)-(13)

### 阶段 5: 选择或自动选择 trade-off 权重
- 可以手动调固定 `beta`，也可以按 `beta_i = -DeltaL_i / DeltaC_i` 直接排序。
- 论文发现自动版本在轻度剪枝时不错，但重度剪枝不一定最优。
- Source: Sec. 2.3, Eq. (14)-(16), Sec. 3.1

## 伪代码

```text
Algorithm: Fisher Pruning for Gaze Prediction
Input: fixation 数据集、teacher saliency 模型、候选 student backbone、tradeoff beta
Output: 剪枝后的 saliency 网络

1. 训练或复用强 DeepGaze teacher，并在额外数据上生成 teacher saliency map。
   Source: Sec. 2.4
2. 用 fixation CE + teacher-map CE 训练更小的 student。
   Source: Sec. 2.4
3. 在每个 feature map 上加入 mask mk，并在若干训练步中累计梯度。
   Source: Sec. 2.1, Eq. (8)-(9)
4. 估计每个 feature 的剪枝损失 Delta_k = (1 / 2N) sum_n g_nk^2。
   Source: Sec. 2.1, Eq. (7), Eq. (9)
5. 计算当前结构下删除该 feature 对 FLOPs 的变化 DeltaC_k。
   Source: Sec. 2.2, Eq. (10)-(11)
6. 选择使 DeltaL_k + beta * DeltaC_k 最小的 feature map 并删掉。
   Source: Sec. 2.2, Eq. (12)-(13)
7. 继续训练、更新 pruning signal 与 cost，然后重复，直到达到目标预算。
   Source: Sec. 2.4, Fig. 1
8. 若使用无超参数版本，则按 beta_k = -DeltaL_k / DeltaC_k 排序。
   Source: Sec. 2.3, Eq. (15), Inference from source
```

## 训练流程
1. 用 SALICON + MIT1003 训练 DeepGaze II teacher。
2. 用 10 个 teacher ensemble 给 SALICON 生成蒸馏监督。
3. 训练 FastGaze 或 DenseGaze，真值损失与 teacher 损失权重分别为 `0.1` 和 `0.9`。
4. 收敛后进入剪枝阶段：每累计 10 个 step 的信号，删除 1 个 feature map。
5. 剪枝期使用 SGD，学习率 `0.0025`，momentum `0.9`。

Sources:
- Sec. 2.4

## 推理流程
1. 用剪枝后的 FastGaze / DenseGaze backbone 提取图像特征。
2. 经 readout 后上采样、Gaussian blur，并加上 center-bias prior。
3. 最后用 softmax 输出像素级 fixation probability distribution。

Sources:
- Sec. 2, Eq. (1), Fig. 4

## 复杂度与效率
- 时间复杂度: 论文未给出完整解析式。
- 空间复杂度: 论文未报告。
- 运行特征: 以 CPU 单图延迟为主要优化目标。
- 扩展性说明: MIT300 报告里，DeepGaze II 为 `240.6 GFLOP`，FastGaze / DenseGaze 降到约 `10.7 / 12.8 GFLOP`。
- 实际效果: 在 CAT2000 上，同等 AUC 大约 `10x` 加速；重剪枝模型按不同指标可达 `39x` 甚至 `75x` 量级加速。

## 实现备注
- 剪的是通道，不是单个稀疏权重，因为真正的部署加速依赖 dense tensor shape 的变化。
- 每轮剪枝后都要重新估计 feature 的计算代价，否则邻层变化会让旧 cost 失效。
- 该方法基于概率型 saliency 输出，因此梯度是针对 log-probability 计算的。
- 强蒸馏在这篇里很关键，因为 fixation 数据不足以安全地全量微调大 backbone。
- 由于没有官方代码，teacher ensemble、蒸馏集构造和 pruning schedule 需要按论文手工复原。

## 与相关方法的关系
- 对比 [[DeepGaze II]]: 保留 saliency 输出形式，但显著缩小 backbone 并做激进通道剪枝。
- 对比 Molchanov 类 pruning: 思路相近，但本文给出更清晰的 Fisher 推导，并把 FLOPs 正则做得更直接。
- 主要优势: 同时考虑任务敏感度和真实计算代价。
- 主要代价: 它是 post-training compression 流程，不是从零直接搜索架构。

## 证据与可溯源性
- 关键图: Fig. 1-4
- 关键表: Table 1, Table 2
- 关键公式: Eq. (1), Eq. (7)-(16)
- 关键算法: 论文无显式算法框；剪枝流程根据 Sec. 2.1-2.4 与 Fig. 1 整理

## 参考链接
- arXiv: https://arxiv.org/abs/1801.05787
- HTML: https://arxiv.org/html/1801.05787
- 代码: 未官方发布（检查时间 2026-03-20）
- 本地实现: Not archived

