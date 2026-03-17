---
title: "RoBoT_ch"
type: method
language: zh-CN
source_method_note: "[[RoBoT]]"
source_paper: "Robustifying and Boosting Training-Free Neural Architecture Search"
source_note: "[[RoBoT]]"
authors: [Zhenfeng He, Yao Shu, Zhongxiang Dai, Bryan Kian Hsiang Low]
year: 2024
venue: ICLR
tags: [nas-method, zh, training-free-nas, bayesian-optimization]
created: 2026-03-17
updated: 2026-03-17
---

# RoBoT 中文条目

## 一句话总结
> RoBoT 先用 Bayesian Optimization 学到一个更稳健的训练免费指标加权组合，再把剩余预算用于对该组合的 Top 架构做贪心利用，从而提升最终搜到的架构质量。

## 来源
- 论文: [Robustifying and Boosting Training-Free Neural Architecture Search](https://arxiv.org/abs/2403.07591)
- HTML: https://arxiv.org/html/2403.07591v1
- 代码: https://github.com/hzf1174/RoBoT
- 英文方法笔记: [[RoBoT]]
- 论文笔记: [[RoBoT]]

## 适用场景
- 问题类型: 固定昂贵评估预算下的架构排序与选择。
- 前提假设: 多个 training-free 指标的加权组合比单指标更接近真实性能。
- 数据形态: 监督学习图像任务，且有候选架构池。
- 规模与约束: 候选很多、无法对每个候选完整训练。
- 适用原因: 把“便宜代理分数”和“昂贵真实性能查询”分开，并同时做探索与利用。

## 不适用或高风险场景
- 搜索空间缺少有效的 training-free 指标。
- 候选池很小，BO + 利用阶段的额外开销收益有限。
- 目标评估噪声非常大，导致 BO 反馈不稳定。

## 输入、输出与目标
- 输入: 候选集合 \(\mathcal{A}\)、训练免费指标集合 \(\mathcal{M}\)、目标评估指标 \(f\)、预算 \(T\)。
- 输出: 最终架构 \(\tilde{A}^*_{M,T}\)、稳健权重 \(\tilde{w}^*\)。
- 优化目标: 在有限 objective query 次数内最大化最终架构真实性能。
- 核心假设: 加权代理排名中的前列包含高质量架构，且可通过有限探索+贪心利用找到。

## 方法拆解

### 阶段 1: 构造加权代理指标
- 定义 \(M(A;w)=\sum_i w_i M_i(A)\)。
- 每个权重向量对应一个“当前最高分架构”。
- Source: Sec. 4.1, Eq. (1)

### 阶段 2: 用 BO 探索权重
- BO 迭代提议 \(w_t\)，并评估该权重下的 top 架构。
- 若架构已被查询则复用历史结果，否则新增 objective query。
- Source: Sec. 4.2, Alg. 1

### 阶段 3: 用 Precision@T 衡量估计缺口
- 通过 \(\rho_T(M,f)\) 衡量代理 top-T 与真实性能 top-T 的重合程度。
- Source: Sec. 4.3, Eq. (2), Theorem 1

### 阶段 4: 剩余预算贪心利用
- 令 \(T_0\) 为探索期真实查询到的不同架构数量。
- 在 \(M(\cdot;\tilde{w}^*)\) 排名上，对 top \(T-T_0\) 做贪心查询。
- Source: Sec. 4.3, Alg. 2

## 伪代码
```text
Algorithm: RoBoT
Input: 目标指标 f, 训练免费指标集合 M={M_i}, 架构池 A, 预算 T
Output: 最终架构 A_tilde_star, 稳健权重 w_tilde_star

1. 定义组合指标 M(A; w) = sum_i w_i * M_i(A)。
   Source: Sec. 4.1, Eq. (1)
2. 运行 BO 进行探索：
   - 提议权重 w_t，按 M(A; w_t) 排序并取 top 架构 A(w_t)；
   - 若 A(w_t) 未查询过则查询 f(A(w_t))，否则复用缓存。
   Source: Sec. 4.2, Alg. 1
3. 选择探索中观测到的最佳权重 w_tilde_star。
   Source: Alg. 1, line 14
4. 计算稳健排名 R_{M(.; w_tilde_star)}，并统计探索期不同架构数 T0。
   Source: Sec. 4.3, Alg. 2
5. 在稳健排名上对前 (T - T0) 个未查询架构做贪心查询。
   Source: Sec. 4.3, Alg. 2
6. 返回探索+利用阶段中真实性能最好的架构。
   Source: Sec. 4.3, Eq. (3), Alg. 2
```

## 训练流程
1. 准备每个候选架构的 training-free 指标值。
2. 对各指标做归一化（代码中是 min-max）。
3. 运行 BO 探索权重。
4. 在稳健指标排名上执行贪心利用。
5. 按目标协议评估所选架构。

Sources:
- Sec. 4.1-4.3
- `search_nb201.py`
- `search_tnb101.py`
- `darts_space/search.py`

## 推理流程
1. 给定新任务的候选池与指标值，先跑 BO 得到 \(\tilde{w}^*\)。
2. 用 \(M(\cdot;\tilde{w}^*)\) 对候选排序。
3. 用剩余预算查询 top 候选并返回最好者。

Sources:
- Sec. 4.2-4.3
- Alg. 1, Alg. 2

## 复杂度与效率
- 时间复杂度: 论文未给完整闭式复杂度。
- 实际计算特征:
  - 代理评分相对 objective query 成本很低；
  - objective query 次数受预算 \(T\) 限制；
  - 每次排名开销与候选数、指标数线性相关。
- 效率证据: 在 Table 2 / Table 4 给出有竞争力结果与较低搜索成本。

## 实现备注
- 核心脚本:
  - `search_nb201.py`
  - `search_tnb101.py`
  - `darts_space/search.py`
- 代码里的 BO 设置:
  - 权重范围是 \([-1,1]\)；
  - acquisition 使用 `ucb`。
- 利用阶段:
  - 代码显式按稳健排名补齐未查询架构直到预算用满。
- 依赖数据:
  - NAS-Bench-201 / TransNAS-Bench-101 使用预计算指标文件。
- 论文-代码差异:
  - 理论分析讨论 IDS 条件，而公开脚本采用 UCB 版本 BO。

## 与相关方法的关系
- 对比单一 [[Training-free NAS]] 指标:
  - RoBoT 通过加权集成提升跨任务稳健性。
- 对比只探索不利用:
  - RoBoT 增加了显式利用阶段来挖掘估计缺口收益。
- 主要优势: 稳健性与预算利用率兼顾。
- 主要代价: 需要额外 BO 调参，并依赖候选指标质量。

## 证据与可溯源性
- 关键图: Fig. 1-3, Fig. 5-10
- 关键表: Table 1-4, Table 8-9
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (5)
- 关键算法: Algorithm 1, Algorithm 2

## 参考链接
- arXiv: https://arxiv.org/abs/2403.07591
- HTML: https://arxiv.org/html/2403.07591v1
- 代码: https://github.com/hzf1174/RoBoT
- 本地实现: D:/PRO/essays/code_depots/Robustifying and Boosting Training-Free Neural Architecture Search
