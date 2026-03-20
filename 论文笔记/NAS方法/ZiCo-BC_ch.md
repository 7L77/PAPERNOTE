---
title: "ZiCo-BC_ch"
type: method
language: zh-CN
source_method_note: "[[ZiCo-BC]]"
source_paper: "ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks"
source_note: "[[ZiCo-BC]]"
authors: [Kartikeya Bhardwaj, Hsin-Pai Cheng, Sweta Priyadarshi, Zhuojin Li]
year: 2023
venue: ICCV Workshops
tags: [nas-method, zh, nas, training-free, zero-cost-proxy, bias-correction]
created: 2026-03-20
updated: 2026-03-20
---

# ZiCo-BC 中文条目

## 一句话总结

> ZiCo-BC 不是重新发明一个 zero-cost proxy，而是在原始 ZiCo 上减去一个与特征图分辨率和通道宽度相关的惩罚项，纠正 repeated-block 搜索空间里“偏爱更深更窄网络”的问题。

## 来源

- 论文: [ZiCo-BC: A Bias Corrected Zero-Shot NAS for Vision Tasks](https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html)
- PDF: https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf
- 代码: 本次整理时未找到公开的官方 ZiCo-BC 仓库
- 英文方法笔记: [[ZiCo-BC]]
- 论文笔记: [[ZiCo-BC]]

## 适用场景

- 问题类型: repeated-block 微架构搜索中的 training-free 排序与候选筛选。
- 前提假设: 原始 ZiCo 这类按层累加的梯度 proxy 在当前搜索空间里确实存在深度/宽度偏置。
- 数据形态: 用任务损失在初始化点做少量前向/反向，算 proxy，不更新参数。
- 规模与约束: 适合 latency-aware evolutionary NAS，需要快速评估大量候选模型的场景。
- 适用原因: 它只改排序分数，不改原有搜索框架，插入成本很低。

## 不适用或高风险场景

- 候选来自差异很大的 macro topology，因为统一的深度惩罚可能会不公平地压制浅层骨干。
- 搜索空间同时变化输入分辨率时，因为当前惩罚默认输入大小固定。
- 需要马上复现实验工程时，因为论文没有公开 ZiCo-BC 的官方实现。

## 输入、输出与目标

- 输入: 候选架构 `A`、任务损失 `L`、原始 ZiCo 的梯度统计、每层特征图尺寸 `(H_l, W_l, C_l)`、超参数 `\beta`。
- 输出: 标量分数 `ZiCo-BC(A)`，用于排序和搜索。
- 优化目标: 纠正 ZiCo 在微架构搜索里对“更深更窄”模型的过度偏好，从而提升最终 latency/accuracy trade-off。
- 核心假设: 在 repeated-block 搜索空间里，原始 ZiCo 的按层累加方式会系统性高估深度带来的收益。

## 方法拆解

### 阶段 1: 计算原始 ZiCo

- 在初始化点上，用原始 ZiCo 的方式根据梯度统计得到 base score。
- 这一步完全复用原始 ZiCo，不改公式主体。
- Source: Sec. 2, Eq. (1)

### 阶段 2: 计算结构惩罚项

- 对每一层读取特征图高度 `H_l`、宽度 `W_l` 和通道数 `C_l`。
- 构造惩罚 `\beta \sum_l \log(H_l W_l / \sqrt{C_l})`。
- Source: Sec. 3, Eq. (2)

### 阶段 3: 得到修正后的排序分数

- 用 `ZiCo-BC = ZiCo - penalty` 得到最终代理分数。
- 然后把这个分数直接送进现有的搜索流程。
- Source: Sec. 3, Eq. (2); Sec. 4

### 阶段 4: 在任务与硬件约束下完成搜索

- 语义分割实验里使用带手机延迟约束的 NSGA-II 搜索。
- 分类与检测实验里，在 EfficientNet / EfficientDet 风格搜索空间中用 ZiCo-BC 排候选。
- Source: Sec. 2, Sec. 4, Table 1-4

## 伪代码

```text
Algorithm: ZiCo-BC-guided micro-architecture search
Input: Candidate architecture A, task loss L, penalty coefficient beta, search loop S
Output: Ranked candidates or selected architecture A*

1. 在初始化点上计算原始 ZiCo(A)。
   Source: Sec. 2, Eq. (1)
2. 对每层读取 (H_l, W_l, C_l)。
   Source: Sec. 3, Eq. (2)
3. 计算 P(A) = beta * sum_l log(H_l W_l / sqrt(C_l))。
   Source: Sec. 3, Eq. (2)
4. 令 ZiCo-BC(A) = ZiCo(A) - P(A)。
   Source: Sec. 3, Eq. (2)
5. 在现有 evolutionary / candidate-selection 搜索环中，用 ZiCo-BC 作为排序信号。
   Source: Sec. 2, Sec. 4; Inference from source
6. 对最终选中的架构做完整训练与评估。
   Source: Sec. 4, Table 3-4; Inference from source
```

## 训练流程

1. 定义任务对应的搜索空间。
2. 对每个候选架构，在初始化点上计算原始 ZiCo 梯度统计。
3. 叠加结构惩罚，得到 ZiCo-BC。
4. 在搜索循环中保留 Pareto 或 top-ranked 候选。
5. 对选中的架构按标准任务配方完整训练。

Sources:

- Sec. 2
- Sec. 3, Eq. (2)
- Sec. 4

## 推理流程

1. ZiCo-BC 只用于搜索阶段，不参与测试时前向推理。
2. 搜索结束后，正常训练所选架构。
3. 部署时使用训练好的网络做标准推理。

Sources:

- Sec. 4
- Inference from source

## 复杂度与效率

- 时间复杂度: 主导项与 ZiCo 基本相同，因为新引入的只是按层读取形状并求一个 log-sum 惩罚。
- 空间复杂度: 与 ZiCo 基本一致。
- 运行特征: 论文没有单独汇报 bias correction 本身的 wall-clock 开销。
- 扩展性说明: 增大 `\beta` 会把搜索从“最大深度解”往中等深度、更宽的解上推。

## 实现备注

- 超参数: 分类和检测使用 `\beta = 1`，语义分割使用 `\beta = 2`。
- 调参经验: 如果 Pareto 候选大多都把 depth 顶满而 width 很小，就继续增大 `\beta`。
- 损失函数:
  - 分类用 cross-entropy。
  - 检测用 focal loss。
  - 分割沿用 FFNet 的训练损失。
- 搜索空间:
  - EfficientNet / EfficientDet: kernel size、channel size、repeats、regular/group convolution。
  - FFNet 风格分割: stage block 数、stage width、regular/group convolution。
- 代码状态: 本次没有找到官方 ZiCo-BC 仓库，所以这份方法笔记是 paper-derived，不是 code-verified。

## 与相关方法的关系

- 对比原始 ZiCo: 核心梯度 proxy 不变，只是显式惩罚过深过窄的结构。
- 对比手工 scaling: 它不是固定缩放规则，而是把修正后的 proxy 放进搜索里自动选结构。
- 主要优势: 改动极小、开销很低，但在相关性和下游任务上都给出了一致收益。
- 主要代价: 这是 search-space-specific 的启发式修正，不是普适、强理论化的新 proxy。

## 证据与可溯源性

- 关键图: Fig. 1
- 关键表: Table 1, Table 2, Table 3, Table 4
- 关键公式: Eq. (1), Eq. (2)
- 关键算法: 论文没有单独给算法框；搜索流程散落在 Sec. 2 和 Sec. 4

## 参考链接

- CVF HTML: https://openaccess.thecvf.com/content/ICCV2023W/RCV/html/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.html
- CVF PDF: https://openaccess.thecvf.com/content/ICCV2023W/RCV/papers/Bhardwaj_ZiCo-BC_A_Bias_Corrected_Zero-Shot_NAS_for_Vision_Tasks_ICCVW_2023_paper.pdf
- DOI: https://doi.org/10.1109/ICCVW60793.2023.00151
- 原始 ZiCo 论文: https://openreview.net/forum?id=qGWsrQhL0S
- 原始 ZiCo 代码: https://github.com/SLDGroup/ZiCo
- 本地实现: Not archived
