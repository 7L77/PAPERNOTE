---
title: "TraceNAS_ch"
type: method
language: zh-CN
source_method_note: "[[TraceNAS]]"
source_paper: "TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation"
source_note: "[[TraceNAS]]"
authors: [Prajna G. Malettira, Manish Nagaraj, Arjun Roy, Shubham Negi, Kaushik Roy]
year: 2026
venue: arXiv
tags: [nas-method, zh, llm-pruning, training-free-nas, zero-shot-proxy]
created: 2026-03-23
updated: 2026-03-23
---

# TraceNAS 中文条目

## 一句话总结
> TraceNAS 用“候选子网与基座模型的梯度轨迹相关性”作为训练自由代理分数，在参数预算约束下搜索非均匀深度/宽度的 LLM 结构化剪枝架构。

## 来源
- 论文: [TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation](https://arxiv.org/abs/2602.02891v1)
- HTML: https://arxiv.org/html/2602.02891v1
- 代码: 论文提到评审期匿名仓库，当前无公开官方仓库
- 英文方法笔记: [[TraceNAS]]
- 论文笔记: [[TraceNAS]]

## 适用场景
- 问题类型: 预训练 LLM 的联合深度-宽度结构化剪枝。
- 前提假设: 与基座模型梯度方向更一致的子网，后续恢复训练潜力更高。
- 数据形态: 小规模校准集用于 zero-shot 排序，后接可选 CPT。
- 规模与约束: 大模型场景，无法承受 training-aware 搜索成本。
- 适用原因: 通过低秩梯度对齐替代搜索时训练，兼顾可扩展性与排名质量。

## 不适用或高风险场景
- 需要在搜索目标中直接内置硬件延迟/吞吐等多目标优化。
- 无法进行任何搜索期前后向（连校准梯度也不可用）。
- 需要完全公开代码复现链路的严格工业流程。

## 输入、输出与目标
- 输入: 预训练模型 `M_base`、预算 `C`、校准集 `B`、候选编码 `(d, kappa)`。
- 输出: 满足预算的最优子网 `M_sub_hat`。
- 优化目标: 最大化 `Phi(M_sub, M_base)`，约束 `P(M_sub) <= C`。
- 核心假设: 梯度轨迹方向对齐可作为“功能继承（functional inheritance）”的代理。

## 方法拆解

### 阶段 1: 候选编码与结构实现
- 用 `d` 编码层保留/跳过，用 `kappa` 编码每层 attention/MLP 保留率。
- 使用激活加权权重幅值构造宽度掩码，并采用 in-place 方式实现候选。
- Source: Sec. 3.2, Sec. 3.3, Fig. 2

### 阶段 2: 功能锚点与低秩梯度轨迹
- 先计算基座梯度轨迹 `g_base` 作为功能锚点。
- 再在低秩子空间计算候选轨迹 `g_sub`，降低内存与计算负担。
- Source: Sec. 3.4

### 阶段 3: 代理打分
- 每层计算标准化后 `g_sub` 与 `g_base` 的 Pearson 相关 `rho^(l)`。
- 用稀疏度加权聚合得到 `Phi`，突出高容量子块贡献。
- Source: Sec. 3.4 Eq. (1)-(2)

### 阶段 4: 进化搜索
- 选取 top-k 精英个体，执行交叉/突变演化深度与宽度编码。
- 迭代若干轮后返回最高分架构。
- Source: Sec. 3.5, Appendix A.4 Algorithm 1

## 伪代码
```text
Algorithm: TraceNAS
Input: 基座模型 M_base, 预算 C, 校准集 B, 精英数 k, 迭代数 T
Output: 最优剪枝子网 M_sub_hat

1. 在 M_base 上加入低秩适配模块，计算 g_base。
   Source: Sec. 3.4
2. 初始化候选群体 P0（深度掩码 d + 宽度比例 kappa）。
   Source: Sec. 3.2, Sec. 3.5
3. for t = 1..T:
   3.1 对 Pt 中每个候选:
       - in-place 实现结构掩码
       - 若超预算，赋极低分
       - 计算 g_sub
       - 分层计算 rho^(l)
       - 稀疏度加权聚合为 Phi
       Source: Sec. 3.3-3.4, Eq. (1)-(2)
   3.2 按 Phi 选 top-k 精英并交叉/突变生成下一代
       Source: Sec. 3.5, Appendix A.4 Alg. 1
4. 返回最终种群中分数最高候选。
   Source: Appendix A.4 Alg. 1
```

## 训练流程
1. 仅用 proxy 完成进化搜索（搜索期不训练候选模型）。
2. 选出预算下的最佳架构（如 2.7B / 4.6B / 8.4B）。
3. 对选中架构执行 post-pruning CPT。

Sources:
- Sec. 4.1
- Tab. 2-3

## 推理流程
1. 使用 CPT 后的剪枝模型进行推理。
2. 在 MMLU/PIQA/ARC/HellaSwag 等任务评估。
3. 可额外分析 prefill/decode 速度与显存。

Sources:
- Sec. 4.3
- Appendix D.1

## 复杂度与效率
- 时间复杂度: 评分由一阶梯度与 O(d^2) 级掩码构造主导，避免 O(d^3) 二阶重建。
- 空间复杂度: 通过低秩梯度子空间显著降低梯度存储成本。
- 运行特征: 文中 A100 基线搜索约 8.5 GPU-hours（H200 配置约 2 小时）。
- 扩展性: proxy 在不同校准样本数、上下文长度、梯度秩下保持稳定相关性。

## 实现备注
- 搜索超参（文中）：population=30, elite=10, iterations=50, crossover=0.7, mutation=0.2。
- 每候选校准 token：65,536。
- 对 GQA 模型不剪 `Wk/Wv`，保持 KV-cache 兼容。
- MLP 隐层维度按 32 对齐，提升算子效率。
- 代码现状: 当前笔记为 paper-derived（缺少公开官方仓库）。

## 与相关方法的关系
- 对比 [[DarwinLM]]:
  TraceNAS 无需搜索时训练，搜索开销更低，恢复后精度有竞争力。
- 对比 [[ShearedLLaMA]]:
  TraceNAS 明确做联合非均匀深度/宽度搜索，而非更固定的剪枝模式。
- 主要优势: 高效搜索 + 强排名相关性。
- 主要代价: 仍需校准梯度与后续 CPT 恢复。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3
- 关键表: Tab. 1, Tab. 2, Tab. 3
- 关键公式: Eq. (1), Eq. (2)
- 关键算法: Appendix A.4 Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2602.02891v1
- HTML: https://arxiv.org/html/2602.02891v1
- 代码: Not publicly available
- 本地实现: Not archived
