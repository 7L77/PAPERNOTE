---
title: "Variation-Matters_ch"
type: method
language: zh-CN
source_method_note: "[[Variation-Matters]]"
source_paper: "Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation"
source_note: "[[Variation-Matters]]"
authors: [Pavel Rumiantsev, Mark Coates]
year: 2025
venue: arXiv
tags: [nas-method, zh, zero-shot-nas, training-free-nas, statistical-testing]
created: 2026-03-16
updated: 2026-03-16
---

# Variation-Matters 中文条目

## 一句话总结
> 该方法把零训练 NAS 的多次 proxy 打分当作随机样本，用统计显著性比较（而非均值比较）来决定架构优劣，从而提升搜索稳定性与最终选中质量。

## 来源
- 论文: [Variation Matters: from Mitigating to Embracing Zero-Shot NAS Ranking Function Variation](https://arxiv.org/abs/2502.19657)
- HTML: https://arxiv.org/html/2502.19657v1
- 代码: 论文与 arXiv 页面未提供官方仓库（检查时间：2026-03-16）
- 英文方法笔记: [[Variation-Matters]]
- 论文笔记: [[Variation-Matters]]

## 适用场景
- 问题类型: 零训练 NAS 中存在显著打分噪声的候选架构比较。
- 前提假设: 每个架构可重复评估 `V` 次，proxy 与真实性能存在正相关趋势。
- 数据形态: 离线 benchmark 搜索（NAS-Bench / TransNAS-Bench）。
- 规模与约束: 无法对所有候选做完整训练，但可承担少量重复 proxy 计算。
- 适用原因: 利用分布信息替代单均值，可减少随机波动导致的误判。

## 不适用或高风险场景
- proxy 几乎无随机性，统计检验带来的收益很小。
- 每个架构样本数过少，检验功效不足。
- 任务要求严格理论最优保证而非经验改进。

## 输入、输出与目标
- 输入: 架构集合、ranking function `r`、batch size `B`、重复次数 `V`、显著性阈值 `alpha`。
- 输出: 搜索得到的最优架构或 top-k。
- 目标: 在给定预算下，提升搜索结果质量与稳定性。
- 核心假设: 多次评估样本可近似反映架构分布式表现。

## 方法拆解

### 阶段 1：度量 ranking 波动
- 为每个架构收集 `M_i={r(arch_i,d_v)}_{v=1}^V`。
- 通过全空间平均 [[Coefficient of Variation]] 评估该 ranking function 稳定性。
- Source: Sec. 4.1 / Eq. (1)

### 阶段 2：统计比较器
- 两架构比较时使用单侧 [[Mann-Whitney U Test]]。
- 仅在 `p < alpha` 时认定一方统计占优。
- Source: Sec. 4.2 / Algorithm 1

### 阶段 3：嵌入搜索流程
- Random Search：用 `Stat-MAX` 代替“均值最大”。
- REA / FreeREA / Greedy：父代选择与最终选择改为统计排序。
- Source: Sec. 4.2 / Sec. 5.2 / Sec. 5.3 / Appendix B

## 伪代码
```text
Algorithm: Variation-Matters Comparator-in-Search
Input: ranking function r, candidate set A, repeat count V, threshold alpha
Output: selected architecture a*

1. 对每个被访问架构 a，收集 V 次打分样本:
   S(a) = {r(a, d_v)}_{v=1}^V
   Source: Sec. 4.1 / Sec. 4.2

2. 定义 StatBetter(a, b):
   对 S(a), S(b) 执行单侧 Mann-Whitney U-test；
   若 p < alpha 且 a 统计占优，则返回 True
   Source: Sec. 4.2 / Algorithm 1

3. 定义 Stat-MAX:
   维护当前最优 m；若 StatBetter(x, m) 成立，则 m <- x
   Source: Algorithm 1

4. 在搜索中替换比较器:
   - random search 的最终选择
   - REA/FreeREA 的锦标赛选择和最终选择
   Source: Sec. 4.2 / Appendix B

5. 对架构样本 S(a) 做缓存，避免重复评估造成决策反复
   Source: Sec. 5.3 / Appendix F
```

## 训练流程
1. 构建 benchmark 接口并采样候选架构。
2. 每次评估时执行 `V` 次 proxy 计算（文中典型 `V=10`）。
3. 在搜索循环中调用统计比较器而非均值比较器。
4. 以 benchmark 真值准确率统计最终表现。

Sources:
- Sec. 5.2 / Sec. 5.3
- Appendix B

## 推理流程
1. 在固定搜索预算下运行统计比较版搜索。
2. 输出统计排序下的最优架构。
3. 可在 `alpha≈0.025~0.075` 区间调参。

Sources:
- Sec. 4.2
- Appendix E

## 复杂度与效率
- 时间复杂度: 论文未给解析式；相对均值比较增加统计检验开销。
- 空间复杂度: 需缓存每个架构的多次评分样本。
- 运行特征: 额外开销通常较小，且可换来更稳搜索质量。
- 扩展性: 在进化搜索中，缓存策略非常关键。

## 实现备注
- 不要过早将多次评估压缩为单一均值。
- 未显著占优时要有稳定 tie-break（文中相当于随机打破平局）。
- `alpha` 是关键超参数。
- 对 SynFlow/LogSynFlow 类低批次随机指标，收益可能不稳定。
- 目前无官方代码仓库可直接复现。

## 与相关方法关系
- 对比均值聚合：保留分布信息，减少噪声主导的错误选择。
- 对比 `mean+CV` 朴素融合：统计比较在多空间下更一致。
- 主要优势：几乎不改搜索框架即可提升质量。
- 主要代价：实现与调参复杂度增加。

## 证据与可溯源性
- 关键图: Fig. 1 / Fig. 3 / Fig. 4 / Fig. 5
- 关键表: Table 1 / Table 2 / Table 3 / Table 7
- 关键公式: Eq. (1), Eq. (2)
- 关键算法: Algorithm 1, Algorithm 2/3/4

## 参考链接
- arXiv: https://arxiv.org/abs/2502.19657
- HTML: https://arxiv.org/html/2502.19657v1
- 代码: Not found
- 本地实现: Not archived

