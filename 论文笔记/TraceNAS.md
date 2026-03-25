---
title: "TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation"
method_name: "TraceNAS"
authors: [Prajna G. Malettira, Manish Nagaraj, Arjun Roy, Shubham Negi, Kaushik Roy]
year: 2026
venue: arXiv
tags: [LLM, structured-pruning, training-free-nas, zero-shot-proxy]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2602.02891v1
local_pdf: D:/PRO/essays/papers/TraceNAS Zero-shot LLM Pruning via Gradient Trace Correlation.pdf
created: 2026-03-23
---

# 论文笔记：TraceNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation |
| 日期 | 2026-02-02 (arXiv v1) |
| arXiv | https://arxiv.org/abs/2602.02891v1 |
| HTML | https://arxiv.org/html/2602.02891v1 |
| 本地 PDF | `D:/PRO/essays/papers/TraceNAS Zero-shot LLM Pruning via Gradient Trace Correlation.pdf` |
| 官方代码 | 论文声明有匿名评审仓库，但当前无可公开克隆的官方仓库链接 |

## 一句话总结
> TraceNAS 把 LLM 结构化剪枝建模为训练自由 NAS：用“稀疏度加权的梯度轨迹 Pearson 对齐”作为零样本代理，直接搜索最有恢复潜力的非均匀深度/宽度子网。

## 核心贡献
1. 提出联合深度与宽度剪枝的训练自由搜索框架 TraceNAS（Sec. 3.1-3.5）。
2. 提出面向“功能继承”的零样本 proxy：比较候选子网与基座模型的低秩梯度轨迹对齐（Sec. 3.4）。
3. 给出可扩展实现：in-place 掩码 + 低秩梯度子空间，显著降低搜索显存与计算开销（Sec. 3.3, 3.4）。
4. 在 Llama-2/3.1 与 Qwen-2.5 上验证：相较 training-aware 方法，搜索成本可降约 10x，同时保持竞争性能（Fig. 1, Tab. 2-3）。

## 问题背景
### 要解决的问题
- LLM 结构化剪枝（删 block / 通道）比非结构化剪枝更易破坏全局表征流，局部重要性分数难以反映跨层耦合。
- 现有高性能方法多为 training-aware search，搜索过程本身代价很高，接近一次恢复训练。

### 现有方法局限
- 局部启发式（如按层权重/激活/Hessian）通常“层内有效、层间不可比”。
- 训练自由 proxy 常偏向“可训练性（trainability）”，而不是预训练知识“可继承性（inheritance）”。

### 本文动机
- 直接衡量候选模型是否仍位于基座模型的优化盆地附近，即是否保留可恢复的功能结构。
- 需要一个对结构剪枝引起的尺度变化不敏感、又能表达全局依赖的代理分数。

## 方法详解
### 1) 搜索空间：联合深度与宽度
- 候选模型编码为 `(d, κ)`：
  - `d ∈ {0,1}^L`：是否保留第 `l` 个 Transformer block（`d_l=0` 走残差直通）。
  - `κ_l=(r_attn^(l), r_mlp^(l))`：每层注意力与 MLP 子块保留比例。
- 在参数预算约束 `P(M_sub) <= C` 下最大化代理分数 `Φ`（Sec. 3.1, 3.2）。

### 2) 候选实现：in-place 掩码
- 用激活加权权重幅值生成宽度掩码（O(d^2) 级别），避免二阶方法 O(d^3) 的开销（Sec. 3.3）。
- 不为每个候选单独实例化模型，而是在基座权重上“临时改写-评估-恢复”，支持高频搜索打分。

### 3) 核心代理：梯度轨迹相关性
- 先用校准集计算基座梯度轨迹 `g_base = E_b[∇_θ L(M_base(b;θ))]` 作为功能锚点。
- 候选子网同样计算 `g_sub`，并在每层低秩子空间内算 Pearson 相关 `ρ^(l)`（Sec. 3.4, Eq. 1）。
- 最终分数是按保留率加权的相关和 `Φ`（Eq. 2），强调高容量子块，抑制重剪枝噪声。

### 4) 进化搜索
- 初始化：基于全局重要性先验采样候选。
- 演化：深度走离散交叉/突变，宽度走连续插值交叉 + 高斯扰动。
- 迭代保留 top-k 精英并繁殖下一代（Sec. 3.5；附录 Alg. 1）。

## 关键公式
### 公式 1：层级梯度轨迹 Pearson 对齐（Sec. 3.4, Eq. 1）
\[
\rho^{(l)}=\frac{1}{N_l}\left\langle
\frac{g_{sub}^{(l)}-\mu(g_{sub}^{(l)})}{\sigma(g_{sub}^{(l)})},
\frac{g_{base}^{(l)}-\mu(g_{base}^{(l)})}{\sigma(g_{base}^{(l)})}
\right\rangle
\]

含义：比较方向一致性，并通过标准化去除结构剪枝导致的幅值偏移。

### 公式 2：稀疏度加权全局代理（Sec. 3.4, Eq. 2）
\[
\Phi(M_{sub},M_{base})=
\sum_{l\in Attn} r_{attn}^{(l)}\rho^{(l)}+
\sum_{l\in MLP} r_{mlp}^{(l)}\rho^{(l)}
\]

含义：将“相关性”与“容量权重”结合，突出关键子块对功能继承的贡献。

## 关键图表与结果
### Figure 1（搜索效率）
- TraceNAS 搜索约 8.5 GPU-hours（A100 基线），对比 training-aware 方法约 10x 降本。

### Table 1（proxy 相关性）
- `TraceNAS (Ours)` 在平均准确率相关性上最好：SP=0.94, KT=0.82。
- 在 MMLU 相关上也优于 Dot/Cosine/Unweighted 变体：SP=0.54, KT=0.39。

### Table 2（Llama-2-7B -> 2.7B）
- 在相同 20B CPT 下，TraceNAS 平均准确率 62.81，高于 DarwinLM(62.24) 与 ShearedLLaMA(60.86)。
- 搜索 token 仅 98M（对比 DarwinLM 常见 1B 级）。

### Table 3（Llama-3.1-8B / Qwen-2.5-14B）
- Llama-3.1-8B -> 4.6B：TraceNAS 平均 66.60，优于 DarwinLM(66.22) 与 Uniform(61.50)。
- Qwen-2.5-14B -> 8.4B：TraceNAS 平均 70.34，优于 DarwinLM(69.80) 与 E3(65.13)。

## 实验设置速记
- 基座模型：Llama-2-7B、Llama-3.1-8B、Qwen-2.5-14B。
- 搜索：population=30，iterations=50，候选总量约 1500。
- 每候选校准数据：65,536 tokens（16 序列）。
- CPT：20B tokens；H200 集群训练，峰值 lr=1e-4，WSD 调度。

## 批判性思考
### 优点
1. 把“可恢复性”作为剪枝搜索目标，而非仅局部可剪性，问题定义准确。
2. 代理公式有明确动机：Pearson 去尺度偏移，稀疏度加权抗噪声层干扰。
3. 工程实现可扩展（低秩梯度 + in-place），对大模型更友好。

### 局限
1. 仍依赖校准样本与后续 CPT，不是“零成本”压缩。
2. 代理主要是一阶对齐信号，未显式建模曲率/长期优化动力学（论文 limitations 也承认）。
3. 当前主要验证语言模型，跨模态与硬件感知多目标搜索尚未完整覆盖。

### 对当前 NAS/LLM 压缩工作的启发
1. 若你已有剪枝搜索框架，可优先替换 scoring：`local saliency -> gradient-trace alignment`。
2. 在资源紧张时，可用低秩子空间（小 r）先筛候选，再对 top-k 做高精打分。
3. 可把该 proxy 扩展到多目标版本（例如再并入 latency/显存约束）做 Pareto 搜索。

## 关联概念
- [[Training-free NAS]]
- [[Structured Pruning]]
- [[Gradient Trace Correlation]]
- [[Functional Inheritance]]
- [[Low-Rank Adapter]]
- [[Pearson Correlation Coefficient]]
- [[Evolutionary Neural Architecture Search]]
- [[Gradient Alignment]]

## 速查卡片
> [!summary] TraceNAS
> - 核心问题: 结构化剪枝下如何快速找到“可恢复”的非均匀子网  
> - 核心方法: 稀疏度加权的梯度轨迹 Pearson 对齐 proxy + 联合深度/宽度进化搜索  
> - 关键结果: 相关性 SP/KT=0.94/0.82（Avg. Acc.），搜索成本约降 10x  
> - 工程要点: 低秩梯度、in-place mask、预算约束下的精英进化
