---
title: "MaAS_ch"
type: method
language: zh-CN
source_method_note: "[[MaAS]]"
source_paper: "Multi-agent Architecture Search via Agentic Supernet"
source_note: "[[MaAS]]"
authors: [Guibin Zhang, Luyang Niu, Junfeng Fang, Kun Wang, Lei Bai, Xiang Wang]
year: 2025
venue: ICML
tags: [nas-method, zh, llm-agent, agentic-search]
created: 2026-03-20
updated: 2026-03-20
---

# MaAS 中文条目

## 一句话总结

> MaAS 不再给所有 query 共用一个固定 agent workflow，而是学习一个按 query 条件化的工作流分布，并从中采样兼顾效果与成本的多智能体系统。

## 来源

- 论文: [Multi-agent Architecture Search via Agentic Supernet](https://arxiv.org/abs/2502.04180)
- HTML: https://arxiv.org/html/2502.04180v2
- 代码: https://github.com/bingreeky/MaAS
- 英文方法笔记: [[MaAS]]
- 论文笔记: [[MaAS]]

## 适用场景

- 问题类型: 自动设计 LLM-agent workflow，尤其适合数学推理、代码生成、工具调用这类 query 难度差异大的任务。
- 前提假设: 任务能拆成一组可复用 operator，并且能从环境拿到正确率或 reward 一类标量反馈。
- 数据形态: benchmark 训练/测试划分，训练阶段要真实执行 LLM API。
- 规模与约束: 当 token / API 成本很重要，而且不同 query 所需推理深度差异明显时最有价值。
- 适用原因: MaAS 会显式权衡性能和成本，并允许简单 query 提前早停。

## 不适用或高风险场景

- 你必须部署完全固定、可审计、不可变的 workflow。
- 你承担不起训练阶段的大量在线 LLM 调用。
- 任务缺少稳定自动评测信号，导致 controller 更新非常噪声。

## 输入、输出与目标

- 输入: query `q`、operator 集合 `O`、supernet 分布参数 `pi`、执行后的环境反馈。
- 输出: 每个 query 对应的采样 workflow `G`，以及训练完成后的优化 supernet。
- 优化目标: 同时提高任务表现、降低执行成本，见 Eq. (5) 与 Eq. (10)。
- 核心假设: query 和 operator 描述的文本表示足够有区分度，能支持条件化路由。

## 方法拆解

### 阶段 1: 定义 operator 空间与 supernet

- 把 prompt / tool / 多轮交互组合成 [[Agentic Operator]]。
- 用 `L` 层 [[Agentic Supernet]] 表示 workflow 分布，而不是单一图结构。
- Source: Sec. 3.1 / Def. 3.1 / Def. 3.2 / Eq. (1)-(4)

### 阶段 2: 按 query 采样 workflow

- controller 读取 query 与历史已选 operator，逐层为候选 operator 打分。
- 每层会一直选到累计概率超过阈值，因此同一层可激活多个 operator。
- 如果采到 [[Early Exit]]，就提前终止后续层。
- Source: Sec. 3.2 / Eq. (6)-(9)

### 阶段 3: 执行采样到的 workflow

- 将选中的 operator 组装成 query-specific 多智能体系统。
- 执行该系统，得到答案、成本和反馈信号。
- Source: Sec. 3.2-3.3 / Alg. 1

### 阶段 4: 更新分布参数

- 用 Monte Carlo 近似计算分布参数梯度。
- 重要性权重同时考虑答对没答对，以及花了多少成本。
- Source: Eq. (10)-(11)

### 阶段 5: 用文本梯度更新 operator

- 因为 prompt、tool 使用与结构变化不可微，所以改用 [[Textual Gradient]]。
- 文字梯度负责提出 prompt、temperature、node structure 的修改建议。
- Source: Eq. (12) / Fig. 3

## 伪代码

```text
Algorithm: MaAS
Input: query q, operator library O, L-layer supernet A = {pi, O}, controller Q_theta
Output: query 对应的 workflow G，以及优化后的 supernet

1. 初始化 operator 集与 L 层 agentic supernet。
   Source: Def. 3.1 / Def. 3.2 / Eq. (1)-(4)
2. 对每个训练 query，controller 逐层给 operator 打分。
   Source: Sec. 3.2 / Eq. (6)-(7)
3. 在每一层中选到累计分数超过阈值为止。
   Source: Eq. (9)
4. 若当前层采到 Early Exit，则停止更深层采样。
   Source: Eq. (8)
5. 执行采样得到的 workflow G，收集正确率与成本反馈。
   Source: Eq. (6) / Alg. 1
6. 用 cost-aware Monte Carlo 梯度更新分布参数 pi。
   Source: Eq. (10)-(11)
7. 用 textual gradient 更新 prompt / temperature / node structure。
   Source: Eq. (12) / Fig. 3
8. 推理时直接从已训练 supernet 中为新 query 采样 workflow。
   Source: Alg. 1
```

## 训练流程

1. 准备 benchmark 训练集与 operator 库。
2. 用轻量句向量模型编码 query 与 operator 描述。
3. controller 为每个 query 采样多层 workflow。
4. 执行 workflow，得到 score、cost 与 log-prob。
5. 用类似 `score - lambda * cost` 的 utility 更新 controller / distribution。
6. 若启用 textual gradient，再对 prompt 或 operator 做文字层面的自演化。

Sources:

- Sec. 3.2-3.3
- Alg. 1
- Code evidence: `examples/maas/optimize.py`, `maas/ext/maas/models/controller.py`, `maas/ext/maas/benchmark/benchmark.py`

## 推理流程

1. 编码输入 query。
2. 用训练好的 controller 逐层选 operator。
3. 到达最大层数或采到 `EarlyStop` 就终止。
4. 执行最终 workflow 并返回答案。

Sources:

- Sec. 3.2
- Fig. 5 / Fig. 6
- Code evidence: `maas/ext/maas/scripts/optimized/*/graph.py`

## 复杂度与效率

- 时间复杂度: 论文没有给出显式渐进式复杂度。
- 空间复杂度: 论文没有给出显式渐进式复杂度。
- 运行特征: 主要瓶颈是训练阶段反复调用在线 LLM / tools。
- 扩展性说明: 更深的 supernet 与更大的采样次数 `K` 会提升灵活性，但代价更高。
- 论文证据: 在 MATH 上，MaAS 训练成本 `3.38$`，推理成本 `0.42$`，明显低于 AFlow。

## 实现备注

- 架构: 公开代码中的 `MultiLayerController` 采用 4 层 selector + MiniLM 句向量。
- 超参数: 论文主设定为 `L=4`, `K=4`, `thres=0.3`, 再用 `lambda` 控制成本惩罚。
- 约束 / masking: 公开代码里第一层会强制包含 `Generate`，并避免第一层直接 `EarlyStop`。
- 技巧: repo 用 `loss = -(logprobs * utilities).mean()` 做 REINFORCE 式更新，`utilities = score - 3 * cost`。
- 注意事项: 当前公开 repo 没有完整覆盖论文中的所有 operator 与 benchmark，严格复现实验表格仍有限制。

## 与相关方法的关系

- 对比 [[AFlow]]: AFlow 搜的是单个最终 workflow，MaAS 学的是按 query 变化的 workflow 分布。
- 对比 [[AgentSquare]]: AgentSquare 侧重 agent 设计自动化，MaAS 更强调条件化路由与成本感知采样。
- 主要优势: 能按 query 动态分配资源，而不是所有样本一刀切。
- 主要代价: 训练链路更复杂，也更依赖外部 LLM 反馈质量。

## 证据与可溯源性

- 关键图: Fig. 1 / Fig. 2 / Fig. 3 / Fig. 5 / Fig. 6 / Fig. 7
- 关键表: Tab. 1 / Tab. 2 / Tab. 3 / Tab. 4
- 关键公式: Eq. (1) / Eq. (5) / Eq. (8) / Eq. (9) / Eq. (10) / Eq. (11) / Eq. (12)
- 关键算法: Alg. 1

## 参考链接

- arXiv: https://arxiv.org/abs/2502.04180
- HTML: https://arxiv.org/html/2502.04180v2
- 代码: https://github.com/bingreeky/MaAS
- 本地实现: D:/PRO/essays/code_depots/Multi-agent Architecture Search via Agentic Supernet

