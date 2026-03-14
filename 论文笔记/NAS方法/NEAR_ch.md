---
title: "NEAR_ch"
type: method
language: zh-CN
source_method_note: "[[NEAR]]"
source_paper: "NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance"
source_note: "[[NEAR]]"
authors: [Raphael T. Husistein, Markus Reiher, Marco Eckhoff]
year: 2025
venue: ICLR
tags: [nas-method, zh, nas, training-free, zero-cost-proxy, effective-rank]
created: 2026-03-14
updated: 2026-03-14
---

# NEAR 中文条目

## 一句话总结
> NEAR 通过累加各层预激活/后激活矩阵的有效秩（Effective Rank）来给未训练网络打分，用于训练前的架构筛选。

## 来源
- 论文: [NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance](https://arxiv.org/abs/2408.08776)
- HTML: https://arxiv.org/html/2408.08776
- 代码: https://github.com/ReiherGroup/NEAR
- 英文方法笔记: [[NEAR]]
- 论文笔记: [[NEAR]]

## 适用场景
- 问题类型: training-free NAS 排序、候选架构预筛选。
- 前提假设: 随机输入下的激活几何结构与最终性能相关。
- 数据形态: 论文主要验证在 NAS 基准上，也扩展到其他任务。
- 约束: 没有标签、无法做完整训练时尤其有价值。

## 不适用或高风险场景
- 需要区分性能非常接近的头部模型。
- 训练动力学因素远强于表示能力因素。
- 目标以硬件时延为主，且无法由该代理有效刻画。

## 输入、输出与目标
- 输入: 模型结构、输入数据采样器（dataloader）、重复次数。
- 输出: 标量 NEAR 分数。
- 目标: 让代理分数与最终精度尽可能保持高相关。
- 核心假设: 激活表示越均衡、越不塌缩，模型潜力越好。

## 方法拆解

### 阶段 1: 构建激活矩阵
- 对每层构建预激活 `Z_l` 与后激活 `H_l` 矩阵。
- Source: Sec. 3.1-3.2

### 阶段 2: 计算有效秩
- 对奇异值归一化后做熵，再取指数:
  `erank(A) = exp(-sum_k p_k log p_k)`。
- Source: Eq. (4), Eq. (5)

### 阶段 3: 层间聚合
- 计算:
  `s_NEAR = sum_l [ erank(Z_l) + erank(H_l) ]`。
- Source: Definition 3.2, Sec. 3.2

### 阶段 4: 重复并平均
- 多次随机初始化/采样后取平均，减少波动。
- Source: Sec. 3.2 (stability recommendation), code `get_near_score(...)`

### 阶段 5: CNN 计算加速
- 卷积特征图先重排成矩阵，再做子矩阵采样近似计算。
- Source: Sec. 3.3

## 伪代码
```text
Algorithm: NEAR Scoring
Input: 模型 F, 数据采样器 D, 重复次数 R
Output: 平均 NEAR 分数 s

1. scores <- []
2. for r in 1..R:
   2.1 用前向 hook 收集各层激活输出。
       Source: Sec. 3.2; code hook collection in near_score.py
   2.2 构建矩阵表示（CNN 时做重排和子采样）。
       Source: Sec. 3.3
   2.3 计算每个矩阵的 erank。
       Source: Eq. (4)-(5)
   2.4 累加得到单次分数 s_r。
       Source: Definition 3.2
   2.5 重置模型参数，进入下一次重复。
       Source: code __reset_weights; Inference from source
3. 返回 mean(scores)。
   Source: code get_near_score(...)
```

## 训练流程（方法使用视角）
1. NEAR 打分阶段不需要完整训练。
2. 仅前向计算代理分数并排序候选。
3. 选出候选后再做标准训练与评估。

Sources:
- Sec. 1, Sec. 4
- Source: Inference from source

## 推理流程
1. 按 NEAR 排序选择结构。
2. 对所选结构进行常规训练/微调。
3. 使用标准推理流程做最终评测。

Sources:
- Sec. 4
- Source: Inference from source

## 复杂度与效率
- 封闭形式复杂度: 论文未显式给出。
- 主要开销: 多层激活矩阵 SVD。
- 实务优势: 不依赖标签、无需反向传播，显著低于完整 NAS 训练成本。
- CNN 场景: 通过子矩阵采样控制秩计算成本。

## 代码实现备注
- 有效秩实现: `src/near_score/near_score.py:get_effective_rank`。
- 层收集: 对含权重层和激活层注册 forward hook。
- 卷积输出: `transpose + flatten` 后做截取近似。
- 多次平均 + 重置参数: `get_near_score` 内完成。
- 层宽估计接口: `estimate_layer_size(...)`。

## 与相关方法关系
- 相比 ReLU 限制的方法，NEAR 对激活函数更通用。
- 相比依赖标签的梯度代理，NEAR 可在无标签场景使用。
- 相比只在单一空间强势的方法，NEAR 的跨空间稳定性更强。

## 证据与可溯源性
- 关键章节: Sec. 3.2, Sec. 3.3, Sec. 4
- 关键公式: Eq. (4), Eq. (5), Definition 3.2
- 关键表格: Table 1, Table 2, Table 3, Table 4, Table 7, Table 8
- 关键代码: `src/near_score/near_score.py`, `example.py`

## 参考链接
- arXiv: https://arxiv.org/abs/2408.08776
- HTML: https://arxiv.org/html/2408.08776
- 代码: https://github.com/ReiherGroup/NEAR
- 本地实现: D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance

