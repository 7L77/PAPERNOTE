---
title: "GEN-TPC-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[GEN-TPC-NAS]]"
source_paper: "Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers"
source_note: "[[GEN-TPC-NAS]]"
authors: [Jun-Hua Ko, Tzi-Dar Chiueh]
year: 2025
venue: IJCNN
tags: [nas-method, zh, zero-shot-nas, self-supervised-learning, transformer]
created: 2026-03-17
updated: 2026-03-17
---

# GEN-TPC-NAS 中文条目

## 一句话总结

> GEN-TPC-NAS 采用“两阶段 zero-shot 进化搜索”：先用 TPC 分数保证表达性，再在 TPC 下界约束内用 Entropy 分数筛选泛化更好的架构。

## 来源

- 论文: [Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers](https://doi.org/10.1109/IJCNN64981.2025.11229357)
- HTML: https://ieeexplore.ieee.org/document/11229357
- 代码: 论文未提供公开仓库链接
- 英文方法笔记: [[GEN-TPC-NAS]]
- 论文笔记: [[GEN-TPC-NAS]]

## 适用场景

- 问题类型: 低标注场景下的 Transformer zero-shot NAS（CV + NLP）。
- 前提假设: TPC 可衡量表达性，特征谱熵可近似泛化潜力。
- 数据形态: 无标签预训练 + 少量标签微调。
- 规模与约束: 完整训练每个候选代价过高时最有价值。
- 适用原因: 兼顾“搜索速度”和“泛化导向”，比单代理更稳。

## 不适用或高风险场景

- 需要完整代码级可复现实验，但论文未公开官方仓库。
- 目标模型不是 Transformer 风格结构，Eq. (5) 适配性不足。
- 代理与真实表现相关性在目标域不稳定（初始化或数据分布差异大）。

## 输入、输出与目标

- 输入: 搜索空间 S、约束 K（FLOPs/参数量/层数）、迭代次数 M、种群大小 N、阈值 T0。
- 输出: 最优架构 Fmax 及其代理分数（TPC, Entropy）。
- 优化目标: 在约束下找到兼顾表达性与泛化性的高性能架构。
- 核心假设: 高表达性是必要条件；在表达性达标后，谱熵更能区分低标注泛化能力。

## 方法拆解

### 阶段 1: TPC 引导探索

- 种群初始化后通过变异/交叉生成候选。
- 用 TPC 分数 St 评估并保留 top-N。
- Source: Sec. III-C, Alg. 1 (lines 1-18), Eq. (6)

### 阶段 2: TPC 收敛触发切换

- 监控当前种群中 St(Fmax)-St(Fmin)。
- 当该差值 <= T0 时，记录 TPCThreshold 并切换到 Entropy 评分阶段。
- Source: Sec. III-C, Alg. 1 (lines 29-31)

### 阶段 3: 带 TPC 下界的 Entropy 优选

- 先过滤 St <= TPCThreshold 的候选。
- 对达标候选计算 Se，用 Se 进行排序。
- Source: Sec. III-C, Alg. 1 (lines 19-24), Eq. (1)-(2)

### 阶段 4: 输出架构并进行 SSL 训练

- 迭代结束后输出最终最高分架构。
- 在下游实验中使用 SSL 预训练 + 全标注/低标注微调评估。
- Source: Sec. III-C; Sec. IV-A/B

## 伪代码

```text
Algorithm: GEN-TPC-NAS
Input: Search space S, constraints K, max depth D, iterations M, population size N, threshold T0
Output: Best architecture Fmax

1. Initialize population P with N random architectures.
   Source: Alg. 1, lines 1-4
2. Generate candidate F_hat via mutation or crossover, then enforce K and D constraints.
   Source: Alg. 1, lines 5-13
3. Compute TPC score St(F_hat) and insert candidate.
   Source: Alg. 1, lines 14-18, Eq. (6)
4. If switchFlag is False and St(Fmax)-St(Fmin) <= T0:
      set TPCThreshold = St(Fmin), switchFlag = True.
   Source: Alg. 1, lines 29-31
5. If switchFlag is True:
      keep candidate only when St(F_hat) > TPCThreshold,
      then compute entropy score Se(F_hat) and rank by Se.
   Source: Alg. 1, lines 19-24; Eq. (1)-(2)
6. Maintain population size N by removing lowest-score individual.
   Source: Alg. 1, line 28
7. Return Fmax after M iterations.
   Source: Alg. 1, line 33
```

## 训练流程

1. 在目标搜索空间内执行 GEN-TPC-NAS 搜索。
2. 选出架构（如 GEN-TPC-Tiny / GEN-TPC-GPT2）。
3. 用 SSL 目标预训练（ViT 用 MIM，GPT2 用自回归 LM）。
4. 在标准与低标注设置下微调并评估。

Sources:

- Sec. III-C, Sec. IV-A, Table III

## 推理流程

1. 搜索时先做 TPC 评分筛选。
2. 当种群 TPC 差异缩小时切换到 Entropy 评分。
3. 产出最优架构后按常规模型推理部署。

Sources:

- Sec. III-C, Alg. 1

## 复杂度与效率

- 时间复杂度: 论文未给闭式。
- 空间复杂度: 论文未给闭式。
- 运行特征: ImageNet-1K 设置下搜索成本报告为 0.02 GPU-days。
- 扩展性说明: 搜索阶段不做完整训练，主要成本转移到后续预训练/微调。

## 实现备注

- 报告超参: population=100, generations=1000, T0=0.5。
- 候选先过硬约束（FLOPs/参数/层数）再入池评分。
- Transformer 搜索维度: embed dim, QKV dim, head dim, MLP ratio。
- Entropy 依赖每层每头特征谱（SVD + 归一化熵）。
- T0 太小会退化为 TPC-only，T0 太大会偏 Entropy 导致表达性不足。

## 与相关方法关系

- 对比 [[TPC-NAS]]: 增加了泛化导向 Entropy 阶段和切换机制。
- 对比 [[MaskTAS]]: 保留 SSL，但用 zero-shot 代理搜索替代 one-shot supernet 搜索。
- 主要优势: 低搜索预算下达到较强标准/低标注性能。
- 主要代价: 代码可复现证据不足，依赖代理有效性。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 2, Fig. 5, Fig. 6, Fig. 7, Fig. 8
- 关键表: Table I-IX（重点 IV, VI, VIII, IX）
- 关键公式: Eq. (1)-(6)
- 关键算法: Algorithm 1

## 参考链接

- DOI: https://doi.org/10.1109/IJCNN64981.2025.11229357
- HTML: https://ieeexplore.ieee.org/document/11229357
- 代码: 论文未提供公开仓库链接
- 本地实现: Not archived (no official repository link found in paper)

