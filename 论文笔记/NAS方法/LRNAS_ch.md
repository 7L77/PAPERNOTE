---
title: "LRNAS_ch"
type: method
language: zh-CN
source_method_note: "[[LRNAS]]"
source_paper: "LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture"
source_note: "[[LRNAS]]"
authors: [Yuqi Feng, Zeqiong Lv, Hongyang Chen, Shangce Gao, Fengping An, Yanan Sun]
year: 2025
venue: IEEE TNNLS
tags: [nas-method, zh, robustness, differentiable-nas, lightweight]
created: 2026-03-15
updated: 2026-03-15
---

# LRNAS 中文条目

## 一句话总结
> LRNAS 用 Shapley 估计每个 search primitive 对自然精度和对抗鲁棒性的联合贡献，再在参数预算约束下用贪心策略拼装最终架构，实现“鲁棒 + 轻量 + 可微搜索”。

## 来源
- 论文: [LRNAS: Differentiable Searching for Adversarially Robust Lightweight Neural Architecture](https://doi.org/10.1109/TNNLS.2024.3382724)
- HTML: https://doi.org/10.1109/TNNLS.2024.3382724
- 代码: 论文与公开链接中未给出明确官方仓库（截至 2026-03-15）
- 英文方法笔记: [[LRNAS]]
- 论文笔记: [[LRNAS]]

## 适用场景
- 问题类型: 面向图像分类的对抗鲁棒轻量架构搜索。
- 前提假设: supernet 阶段 primitive 的边际贡献可反映最终架构质量。
- 数据形态: 有监督分类任务，可进行对抗训练和对抗评测。
- 规模与约束: 适配 cell-based differentiable NAS，并带模型参数上限约束。
- 适用原因: 同时把精度、鲁棒性和模型规模纳入搜索与选型流程。

## 不适用或高风险场景
- 需要可认证鲁棒性（certified robustness）而非经验攻击鲁棒性。
- 搜索空间无法拆成 primitive 贡献（难以做 Shapley 式评估）。
- 算力预算过低，无法承受排列采样估计开销。

## 输入、输出与目标
- 输入: 搜索空间 `S={o(i,j)}`、数据集、warm-up 轮数 `Nw`、搜索轮数 `Ns`、参数阈值 `lambda`。
- 输出: 最终架构 `A`。
- 优化目标: 在参数预算内最大化自然精度与对抗鲁棒性。
- 核心假设: primitive 的 Shapley 边际贡献与最终表现存在稳定关联。

## 方法拆解

### 阶段 1：超网初始化与 warm-up
- 初始化超网权重 `omega` 与架构参数 `alpha`。
- warm-up 期间只更新 `omega`，不更新基于价值的架构参数。
- Source: Sec. III-B, Alg. 1 (lines 1-7)

### 阶段 2：Shapley primitive 价值评估
- 对每个 primitive 定义联合边际增益：`DeltaA + DeltaR`。
- 用采样排列的无偏估计近似真实 Shapley 值。
- Source: Sec. III-C, Eq. (3)-(8), Theorem 1

### 阶段 3：架构参数更新
- 用动量平滑价值向量 `V_i`。
- 用归一化 `V_i` 更新 `alpha`。
- Source: Sec. III-C, Eq. (9)-(10)

### 阶段 4：预算约束下贪心组网
- 先取每条边上 `alpha` 最大的 primitive。
- 按 `alpha` 值全局降序。
- 在 `ModelSize < lambda` 条件下贪心加入最终架构。
- Source: Sec. III-D, Algorithm 2

## 伪代码
```text
Algorithm: LRNAS
Input: S={o(i,j)}, Nw, Ns, dataset D, threshold lambda
Output: architecture A

1. 初始化 supernet 参数 (omega, alpha)，A 置空。
   Source: Alg. 1 lines 1-2
2. 对 i=1...Nw+Ns:
   2.1 训练 supernet 更新 omega。
       Source: Alg. 1 line 4
   2.2 若 i>Nw，按采样排列估计 primitive 价值:
       Vhat_o(i,j)=(1/n)sum_t[DeltaA_o(i,j)(p_t)+DeltaR_o(i,j)(p_t)]。
       Source: Eq. (3)-(8)
   2.3 用 Eq. (9)-(10) 更新 Vi 与 alpha。
       Source: Eq. (9)-(10)
3. 每条边取 alpha 最大 primitive，形成候选集合。
   Source: Eq. (2), Alg. 2 lines 2-5
4. 候选按 alpha 降序。
   Source: Alg. 2 line 6
5. 逐个尝试加入 A，若 ModelSize(A U {primitive}) < lambda 则加入。
   Source: Alg. 2 lines 7-11
6. 返回 A。
   Source: Alg. 2 line 12
```

## 训练流程
1. 搜索阶段将数据划分为 supernet 训练与验证两部分。
2. 总搜索 60 epoch，其中 warm-up 15 epoch。
3. 搜索时使用 FGSM（8/255）参与鲁棒性价值评估。
4. 得到架构后进行对抗训练（如 CIFAR 上 7-step PGD）。

Sources:
- Sec. IV-C.1, Sec. IV-C.2, Sec. V-A

## 推理流程
1. 使用最终架构 `A` 进行常规前向推理。
2. 鲁棒性评测按 FGSM/PGD/C&W 协议执行。

Sources:
- Sec. IV-C.2, Sec. V-A

## 复杂度与效率
- 搜索主复杂度: `O(n * |O| * |E|)`。
- 选型复杂度: `O(|O| * |E|)`。
- 论文报告搜索成本约 `0.4 GPU days`。

## 实现备注
- warm-up 主要提升搜索稳定性与自然精度。
- `lambda` 控制精度-鲁棒-参数折中；文中在 CIFAR-10 上选 `2.0M`。
- greedy 组件在消融中显著提升鲁棒性并减少参数。
- 官方代码未明确公开，复现需按论文算法细节自行实现。

## 与相关方法关系
- 对比 [[DARTS]]: LRNAS 增加了显式鲁棒贡献估计，而不是仅靠梯度权重竞争。
- 对比 [[E2RNAS]] 等鲁棒 NAS: LRNAS 更强调 primitive 价值分解与预算约束组装。
- 主要优势: 参数规模更小且鲁棒性强。
- 主要代价: 采样估计会带来额外计算开销。

## 证据与可溯源性
- 关键图: Fig. 2-7
- 关键表: Table I-IX
- 关键公式: Eq. (2)-(10)
- 关键算法: Algorithm 1, Algorithm 2

## 参考链接
- DOI: https://doi.org/10.1109/TNNLS.2024.3382724
- HTML: https://doi.org/10.1109/TNNLS.2024.3382724
- 代码: Not officially released (as of 2026-03-15)
- 本地实现: Not archived
