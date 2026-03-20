---
title: "LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance"
method_name: "LLMENAS"
authors: [Xu Zhai, Xiaoyan Sun, Huan Zhao, Shengcai Liu, Rongrong Ji]
year: 2025
venue: arXiv
tags: [NAS, LLM, evolutionary-search, one-shot-nas]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2501.13154v2
local_pdf: D:/PRO/essays/papers/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance.pdf
local_code: D:/PRO/essays/code_depots/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance
created: 2026-03-13
---

# 论文笔记：LLMENAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance |
| arXiv | https://arxiv.org/abs/2501.13154 |
| HTML | https://arxiv.org/html/2501.13154v2 |
| 代码 | https://github.com/LLMENAS/LLMENAS |
| 本地 PDF | `D:/PRO/essays/papers/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance` |

## 一句话总结
> LLMENAS 用大语言模型替代传统进化搜索中的交叉与变异算子，并结合 [[One-shot NAS]] 与 [[Surrogate Predictor]]，在更低搜索代价下找到更优 NAS 架构。

## 核心贡献
1. 把进化 NAS 的核心操作（交叉、变异）改造成可解释的 LLM 指导操作（Sec. 4.2）。
2. 提出面向架构编码的 prompt 规则，利用 LLM 的语义先验做结构重组（Fig. 2, Sec. 4.2）。
3. 引入预测器和 one-shot 评估以减少真实训练开销，实现低样本低 GPU-day 搜索（Sec. 4.3, 4.4）。
4. 在 CIFAR-10、ImageNet-16-120 和鲁棒性评估上优于多种基线（Sec. 5, Tab. 1/2/4/5）。

## 问题背景
### 要解决的问题
- 传统 [[Evolutionary Neural Architecture Search]] 的交叉与变异操作通常依赖随机或人工规则，容易陷入局部最优，搜索效率也偏低。

### 提出的问题

its low output diversity often traps the search process in **local optima**
in complex search spaces, the LLM’s inherent propensity for **hallucination** can yield invalid architectures.
Combining the strength of evolutionary algorithms with the efficiency of gradient-based methods presents a highly promising direction【进化算法的优势与基于梯度的方法的结合】
	**requires careful coordination** of exploration and exploitation during the search process


### 现有方法局限
- 纯进化策略：探索能力受启发式规则限制。
- 纯强化学习/梯度搜索：计算开销大或搜索偏置明显。
- 现有 LLM4NAS 工作：多用于结构描述/建议，较少直接替代核心进化算子。

### 本文动机
- LLM 对“结构重组”的语义能力可作为进化搜索的先验，减少无效架构探索。

## 方法详解
### 1) 搜索空间与表示
- 采用 cell-based 架构表示，normal/reduction cell 的操作来自候选算子集（Sec. 4.1）。
- 用矩阵/离散编码表示架构个体，形成种群进行迭代搜索（Sec. 4.2）。

### 2) LLM 指导的进化算子
- 交叉：`LLM_Crossover(P^A, P^B, p_C)`，由 prompt 约束融合两父代优点（Eq. 3）。
- 变异：`LLM_Mutation(G^C, p_M, H)`，结合历史性能统计 `H=[f_best,f_avg,f_min]` 进行扰动（Eq. 4, Eq. 5）。
- 交叉概率与变异率动态调节，强化前期探索、后期收敛（Eq. 2）。

### 3) 代理评估与 one-shot 加速
- 用预测器 `g_phi(E(P))` 估计候选架构性能，降低全训练评估次数（Eq. 6）。
- 配合 one-shot 权重共享快速筛选候选，再进行更高精度评估（Sec. 4.3, 4.4）。

### 4) 整体流程
- 初始化种群 -> LLM 交叉/变异生成后代 -> 代理评估与筛选 -> 更新种群并迭代（Algorithm 1, Sec. 4.5）。

## 关键公式
### Eq. (1) 种群表示
$$
f(X)=\{G_i\}_{i=1}^{N_P}
$$
- 含义：把搜索状态表示为种群个体集合。

### Eq. (2) 动态变异率
$$
m_i=\frac{2}{F_B}\exp\left(1-\frac{G}{G_{\max}}\right)
$$
- 含义：随代数变化调节变异强度，兼顾探索与收敛。

### Eq. (3) LLM 交叉
$$
G^{C}=\mathrm{LLM\_Crossover}(P^A,P^B,p_C)
$$
- 含义：使用 LLM 在父代架构间做受约束重组。

### Eq. (4) LLM 变异
$$
G^{M}=\mathrm{LLM\_Mutation}(G^C,p_M,H)
$$
- 含义：在当前个体和历史统计指导下做结构突变。

### Eq. (5) 历史性能统计
$$
H=[f_{best},f_{avg},f_{min}]
$$
- 含义：为 LLM 提供上下文，避免盲目随机变异。

### Eq. (6) 代理预测器
$$
s=g_{\phi}(E(P))
$$
- 含义：把架构编码映射到性能估计分数，降低真实评估成本。

### Eq. (7) 目标
$$
\max_{P\in S}\mathcal{L}=\mathrm{acc}(P)
$$
- 含义：在搜索空间中最大化目标精度（以分类精度为主）。

## 关键图表与结果
### Figure references
- Fig. 1: LLMENAS 总体框架（搜索循环 + 评估流程）。

![[Pasted image 20260319231646.png]]

- Fig. 2: LLM prompt 设计与交叉/变异模板。
- Fig. 3: 不同规模 LLM 对搜索效果的影响趋势。
- Fig. 4: 搜索阶段效率对比（样本数与 GPU days）。

### Table references
- Tab. 1 (CIFAR-10): LLMENAS error `2.52%`, params `3.42M`。
- Tab. 2 (ImageNet-16-120): Top-1 error `17.81%`（文中报告优于多基线）。
- Tab. 4 (Robustness, CIFAR-10-C): PGD `k=7` 为 `42.95%`，`k=20` 为 `40.30%`。
- Tab. 5 (LLM variants): Qwen2.5-72B 达到 `97.48%`，在对比中表现最优。

### 效率结论
- 文中报告：仅需 `340` 个样本与 `0.6` GPU days 即可找到高质量架构；
- 相比 direct-search 范式，样本量与搜索成本分别下降约 `77.3%` 和 `87.8%`（Sec. 5.3）。

## 实现与复现备注
- 论文方法包含完整“LLM 指导搜索”流程。
- 当前公开仓库主要提供 CIFAR-10 架构评估代码（README 明确说明“full code will be released upon paper acceptance”），搜索主流程代码尚不完整公开。
- 因此本笔记中的“搜索阶段实现细节”主要来自论文文本（paper-derived），评估阶段配置可直接参考仓库。

## 批判性思考
### 优点
1. 把 LLM 先验放到进化核心操作，方法设计直观且可解释。
2. 性能、鲁棒性和搜索效率三方面都有实证结果。
3. 兼容现有 NAS pipeline，工程接入成本相对可控。

### 局限
1. 搜索流程代码未完整公开，短期可复现性受限。
2. 方法依赖外部 LLM 的质量与调用成本。
3. prompt 设计对结果敏感，跨任务泛化仍需更多证据。

### 后续可做
1. 在更多搜索空间（如 ViT/多模态）验证泛化。
2. 用更小模型蒸馏 LLM 搜索策略，降低推理成本。
3. 引入约束优化（延迟/能耗）做多目标 LLMENAS。

## 关联概念
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]
- [[One-shot NAS]]
- [[Surrogate Predictor]]
- [[LLM-guided Search]]


## 解释论文

### propose
通用的分层优化框架a general hierarchical optimization framework
	dynamically designs fitness functions
a self-improving mechanism

### LLM-based Neural Architecture Search
Zheng et al. [58] introduced an innovative approach called GPT4 Enhanced Neural Architecture Search (GENIUS)
	which harnesses the generative power of GPT-4 as a black-box optimizer to search promising architectures.

Chen et al. [16] proposed combining evolutionary prompt engineering with soft prompt tuning, which consistently identifies diverse and highperforming models.

### Problem Formulation: A Hierarchical Optimization Framework
1. 传统 NAS 用固定 fitness function，不会随搜索过程变化，容易停在局部最优。

a hierarchical optimization framework
1. 把问题建成“上下两层优化”：
    - 下层：进化算法按当前 fitness 演化种群（马尔可夫转移）。
    - 上层：LLM 看历史轨迹 Hg​，动态生成下一代 fitness function。
2. 目标是让这个“LLM 设计 fitness 的策略”最小化下一步最优架构的验证损失（等价于提高后续搜索质量）。


#### DARTS
DARTS 是方法（以及其常用 cell 搜索空间）。
	NAS-Bench-301 (NB301) 是基于 **DARTS 搜索空间**做的 surrogate benchmark（用代理模型近似评估），不是 DARTS 的子模块

NB201 NB301 RB201
1. NB201：小而全的 tabular benchmark，空间固定（15625 编码），评估结果可查表，适合可复现对比。
2. NB301：大空间（DARTS 风格，超大规模），靠 surrogate 近似真实训练，适合更“真实”的大空间搜索评估。
3. RobustBench：DARTS 空间里一批已做对抗训练的架构集合（偏鲁棒性评测）。
4. NAS-Rob-Bench-201 (RB201)：基于 NB201 空间的鲁棒版基准（6466 非同构架构，含 clean + PGD/FGSM 等鲁棒指标）。

In the search space of DARTS, the cell is composed of N nodes and E edges, forming a directed acyclic graph (DAG)
	可微 NAS 的标准表述：把 cell 看成 DAG，每条边不是硬选一个算子，而是对候选算子做 softmax 加权混合；然后通过双层优化，一边在训练集上学 supernet 权重 w，一边在验证集上学架构参数 alpha。这一节真正想强调的是：这种连续松弛虽然高效，但也让 alpha 和 w 紧耦合，容易偏向 skip 这类无参数操作，进而出现 collapse 或陷入局部最优。所以作者写 III.B，本质是在回答“为什么后面要从 DARTS 式梯度搜索，转向 CMA-ES + LLM 动态设计 fitness”。

搜索阶段

1. 在 DARTS 这类可微 NAS 里，softmax 混合候选算子、同时优化 w 和 alpha，是为了让“架构选择”变得可导，这一步属于 **search phase**。
2. 搜索结束后，会把连续的 alpha **离散化**，例如每条边选权重最大的那个算子，得到最终架构。
3. 得到最终架构后，通常进入 **evaluation / retrain phase**：  
    这时不再保留 mixed op，也不再学 alpha，而是把选出来的离散网络从头训练，只学普通网络权重。

所以你可以这么记：
- search phase：学 w + alpha，边上是 mixed ops。
- final training phase：只学最终网络的权重，不再学 alpha