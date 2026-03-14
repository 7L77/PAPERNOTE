---
title: "WRCor_ch"
type: method
language: zh-CN
source_method_note: "[[WRCor]]"
source_paper: "Zero-Shot Neural Architecture Search with Weighted Response Correlation"
source_note: "[[WRCor]]"
authors: [Kun Jing, Luoyu Chen, Jungang Xu, Jianwei Tai, Yiyu Wang, Shuaimin Li]
year: 2025
venue: arXiv
tags: [nas-method, zh, zero-shot-nas, training-free-proxy, response-correlation]
created: 2026-03-14
updated: 2026-03-14
---

# WRCor 中文条目

## 一句话总结

> WRCor 在网络未训练状态下统计“跨样本激活/梯度响应相关矩阵”，按层做指数加权后取 log-det 作为代理分数，并将该分数用于随机/RL/进化 NAS 搜索。

## 来源

- 论文: [Zero-Shot Neural Architecture Search with Weighted Response Correlation](https://arxiv.org/abs/2507.08841)
- HTML: https://arxiv.org/html/2507.08841v2
- 代码: https://github.com/kunjing96/ZSNAS-WRCor
- 英文方法笔记: [[WRCor]]
- 论文笔记: [[WRCor]]

## 适用场景

- 问题类型: 图像分类场景下的大规模候选架构 zero-shot 排序。
- 前提假设: 初始化时响应相关结构与最终架构优劣具有统计关联。
- 数据形态: 可用目标数据小批次，也可用噪声输入（效果略降）。
- 规模与约束: 适合“候选多、算力紧”的 NAS 早筛阶段。
- 适用原因: 不需要完整训练即可给出可比较分数，且可融入多种搜索策略。

## 不适用或高风险场景

- 需要绝对精度预测而不仅是相对排序。
- 搜索空间过大导致 proxy-accuracy 相关性明显退化。
- 网络模块使相关矩阵估计不稳定或数值病态。

## 输入、输出与目标

- 输入: 候选架构、初始化参数、mini-batch 输入、反向损失函数。
- 输出: ACor/RCor/WRCor 分数，及可选投票分数 SPW/SJW。
- 优化目标: 用低成本代理排序，提升 top 架构命中率。
- 核心假设: 更优架构对应更低跨样本相关（非对角项更小），从而 log-det 更高。

## 方法拆解

### 阶段 1: 响应采样

- 前向收集 pre-activation 激活响应。
- 反向收集对隐藏特征图的梯度响应。
- Source: Sec. 3.1, Sec. 3.2, Sec. 3.3

### 阶段 2: 构建相关矩阵

- 对每层/单元在样本维度上计算相关系数矩阵。
- 取绝对值并聚合。
- Source: Sec. 3.3.1, Eq. (1), Eq. (8), Eq. (9)

### 阶段 3: WRCor 层级加权

- 按层从浅到深施加指数权重 \(2^l\)。
- 激活与梯度矩阵共同汇总到 \(K\)。
- Source: Sec. 3.3.2, Eq. (10), Eq. (11)

### 阶段 4: 标量打分

- 用 \( \log(\det(K)) \) 映射到代理分数（实现中用 `slogdet`）。
- 分数越高代表作者定义下更优架构。
- Source: Sec. 3.3.1, Eq. (6)-(8), code `act_grad_cor_weighted.py`

### 阶段 5: 搜索集成

- 在随机、RL、规则化进化搜索中作为估计器。
- 也可与 SynFlow/JacCor/PNorm 组合成投票代理。
- Source: Sec. 3.4, Alg. 1, Alg. 2, Sec. 3.3.3

## 伪代码

```text
Algorithm: WRCor-based Zero-shot NAS
Input: Search space S, budget N, minibatch X, proxy set M
Output: Best architecture a*

1. Sample architecture a from S (random / RL controller / evolution mutation).
   Source: Sec. 3.4, Alg. 1-2
2. Initialize a and run one forward pass on X; collect pre-activation responses.
   Source: Sec. 3.1, Sec. 3.3
3. Run backward pass; collect gradient responses per layer.
   Source: Sec. 3.2, Sec. 3.3
4. For each layer l and response unit i, compute correlation matrix C_{l,i} over samples.
   Source: Sec. 3.3.1, Eq. (1), Eq. (9)
5. Aggregate K = sum_l sum_i 2^l * (|C^A_{l,i}| + |C^G_{l,i}|).
   Source: Sec. 3.3.2, Eq. (11)
6. Score(a) = log(det(K)).
   Source: Eq. (10), code `slogdet`
7. Optionally combine with SynFlow/JacCor or SynFlow/PNorm via majority voting.
   Source: Sec. 3.3.3
8. Update search state and keep best architecture under budget N.
   Source: Sec. 3.4, Alg. 1-2
```

## 训练流程

1. 候选架构不做完整训练，仅做前后向计算 proxy。
2. 用 proxy 分数驱动搜索与筛选。
3. 只对最终入选架构做标准训练评估。

Sources:

- Sec. 1, Sec. 3, Sec. 4.1.4-4.1.5

## 推理流程

1. 给定候选架构并初始化。
2. 计算 WRCor（或投票分数）。
3. 在候选池内排序，选 top 架构。
4. 进入后续高成本训练与部署流程。

Sources:

- Sec. 3.3, Sec. 3.4, Sec. 4.3

## 复杂度与效率

- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: 文中报告 WRCor 单架构估计约 2 秒（NB201 语境）；RE-SJW 在 MobileNetV2 搜索约 0.17 GPU day。
- 扩展性说明: 大搜索空间上相关性会下降，需结合投票或更强 proxy。

## 实现备注

- 关键实现: `foresight/pruners/measures/act_grad_cor_weighted.py`。
- 通过 ReLU hook 收集激活与梯度，计算 `np.corrcoef`。
- 层权重实现为 `2**i`，对应 Eq. (11)。
- 评分实现为 `np.linalg.slogdet(net.K)`。
- 未加权 RCor 对应 `act_grad_cor.py`。
- 搜索主逻辑在 `search.py` 的 `Random_NAS`/`RL_NAS`/`Evolved_NAS`。

## 与相关方法关系

- 对比 NASWOT/JacCor 类方法: WRCor 同时纳入激活与梯度并加层级权重。
- 对比 ZiCo: 在 NB201 上相关性竞争力强，工程接入简单。
- 主要优势: 统一表达 + 跨设置稳定性较好。
- 主要代价: 并非全场景最优，尤其大搜索空间下仍需投票补强。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 2
- 关键表: Table 2, Table 3, Table 4, Table 7, Table 8, Table 9, Table 10
- 关键公式: Eq. (1), Eq. (8), Eq. (9), Eq. (10), Eq. (11)
- 关键算法: Alg. 1, Alg. 2

## 参考链接

- arXiv: https://arxiv.org/abs/2507.08841
- HTML: https://arxiv.org/html/2507.08841v2
- 代码: https://github.com/kunjing96/ZSNAS-WRCor
- 本地实现: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation


