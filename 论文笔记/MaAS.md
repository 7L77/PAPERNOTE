---
title: "Multi-agent Architecture Search via Agentic Supernet"
method_name: "MaAS"
authors: [Guibin Zhang, Luyang Niu, Junfeng Fang, Kun Wang, Lei Bai, Xiang Wang]
year: 2025
venue: ICML
tags: [llm-agents, multi-agent, architecture-search, agentic-supernet]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2502.04180v2
local_pdf: D:/PRO/essays/papers/Multi-agent Architecture Search via Agentic Supernet.pdf
local_code: D:/PRO/essays/code_depots/Multi-agent Architecture Search via Agentic Supernet
created: 2026-03-20
---

# 论文笔记: MaAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Multi-agent Architecture Search via Agentic Supernet |
| arXiv | https://arxiv.org/abs/2502.04180 |
| HTML | https://arxiv.org/html/2502.04180v2 |
| 会议 | ICML 2025, PMLR 267 |
| 代码 | https://github.com/bingreeky/MaAS |
| 本地 PDF | `D:/PRO/essays/papers/Multi-agent Architecture Search via Agentic Supernet.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Multi-agent Architecture Search via Agentic Supernet` |

## 一句话总结
> MaAS 不再为所有 query 搜一个固定工作流，而是学习一个 [[Agentic Supernet]]，按 query 难度和领域动态采样多智能体结构，在更低 token / API 成本下取得更高任务表现。

## 核心贡献
1. 把“自动设计一个固定 agent workflow”改写成“优化一个条件化的 agent 架构分布”，提出 [[Agentic Supernet]] 这一建模对象（Sec. 1, Sec. 3.1）。
2. 用 controller 按 query 条件化选择 [[Agentic Operator]]，并用 [[Early Exit]] 让深度随样本难度变化（Sec. 3.2, Eq. 8-9）。
3. 用两类更新共同优化 supernet：对分布参数用 Monte Carlo / policy-gradient 风格更新，对 operator 内容用 [[Textual Gradient]] 更新（Sec. 3.3, Eq. 10-12, Fig. 3, Alg. 1）。
4. 在数学、代码、工具使用任务上同时报告性能和成本，强调“高性能 + 低推理资源”的联合目标（Tab. 1-4, Fig. 4-7）。

## 问题背景

### 论文要解决什么
- 现有自动 agent workflow 搜索方法大多寻找一个 one-size-fits-all 的最终系统。
- 这种静态系统对简单 query 往往过度调用 LLM / tool，对跨领域 benchmark 又缺少足够适配性。
- 论文希望得到的是“按 query 动态分配推理资源”的 agent 系统，而不是单一固定拓扑。

### 现有方法为什么不够
- 手工系统依赖 prompt、角色、通信模式的人为设计，迁移成本高。
- 自动方法如 ADAS、AgentSquare、AFlow 虽能搜索 workflow，但目标仍是单个最终解。
- 这样会在 easy query 上浪费资源，在 mixed-domain benchmark 上难以兼顾不同任务。

## 方法详解

### 1. 搜索空间：operator + DAG + supernet
- 基本单元是 [[Agentic Operator]]，即一个可包含多个 LLM 调用、prompt 与 tools 的复合算子（Def. 3.1, Eq. 1）。
- 一个多智能体系统表示为 DAG `G = {V, E}`，其中节点是 operator，边表示调用依赖（Eq. 2）。
- [[Agentic Supernet]] `A = {pi, O}` 由 `L` 层 operator 分布组成，每层给出在当前上下文下激活哪些 operator 的概率（Def. 3.2, Eq. 3-4）。

### 2. Query-conditioned controller
- 给定 query，controller `Q_theta` 在每层根据 query 表示与前序层已选 operator 进行条件化采样（Eq. 6-7）。
- 为了避免每个样本都走满 `L` 层，作者加入 [[Early Exit]] operator；一旦采样到它，就提前停止后续层（Eq. 8）。
- 每层不是只选一个 operator，而是按 score 排序后，直到累计概率超过阈值 `thres` 为止，因此每层激活个数也是 query-dependent 的（Eq. 9）。

### 3. 代价约束优化
- 目标函数同时最大化 utility、最小化 cost，本质上是性能和 token 开销的折中（Eq. 5, Eq. 10）。
- 对 supernet 分布参数，作者用 Monte Carlo 估计梯度，重要性权重 `m_k` 同时考虑正确率与 cost（Eq. 11）。
- 对 operator 本身，因 prompt / tool / 结构不可微，改用 [[Textual Gradient]] 产生 prompt、temperature、node-structure 层面的文字更新建议（Eq. 12, Fig. 3）。

### 4. 训练与推理
- 训练时：采样 query-specific workflow，执行，收集反馈，再同时更新分布与 operator（Alg. 1）。
- 推理时：直接从已优化的 supernet 中为当前 query 采样一个子图执行，不再穷举搜索。
- 论文强调这比“先搜一个固定结构，再所有样本共用”更适合真实部署。

## 关键公式

### Eq. (1): Agentic Operator
$$
O = \{\{M_i\}_{i=1}^{m}, P, \{T_i\}_{i=1}^{n}\}
$$
- 含义：一个 operator 由多个 LLM 实例、prompt 和工具组成。
- 这一定义把 CoT、Debate、ReAct、Refine 等都统一成可组合的搜索单元。

### Eq. (5): 条件化架构分布优化
$$
\max_{P(G|q)} \mathbb{E}_{(q,a)\sim D,\, G \sim P(G|q)} \left[ U(G;q,a) - \lambda C(G;q) \right],\ \text{s.t. } G \subseteq A
$$
- 含义：目标不是找单个最优图，而是学一个按 query 变化的架构分布。
- `U` 是任务表现，`C` 是成本，`lambda` 控制精度和成本权衡。

### Eq. (9): 每层 operator 选择
- 先计算所有 operator 对当前 query 的激活分数，再按分数排序并累计到阈值 `thres` 为止。
- 含义：复杂 query 会激活更多 operator，简单 query 可能很快早停。

### Eq. (11)-(12): 双路径更新
- 分布参数 `pi` 用 Monte Carlo / 重要性加权近似梯度更新。
- operator 内容用 [[Textual Gradient]] 给出 prompt、温度和结构修改建议。
- 这是论文最关键的“可搜索 + 可进化”组合。

## 关键图表与结果

### Fig. 1 / Fig. 2: 整体思想与框架
- Fig. 1 左边展示可选 building blocks，右边展示不同 query 会激活不同复杂度的 workflow。
- Fig. 2 给出完整训练闭环：query -> controller 采样 -> 执行 -> 环境反馈 -> 分布更新 + textual gradient 更新。

### Fig. 3 / Alg. 1: 文本梯度与训练流程
- Fig. 3 把 textual gradient 具体化为 prompt gradient、temperature gradient、operator gradient。
- Alg. 1 明确训练循环：逐层采样、执行 sampled MAS、基于 Eq. 11/12 更新。

### Tab. 1: 主结果
- 在 GSM8K / MATH / MultiArith / HumanEval / MBPP 上，MaAS 平均分 `83.59`，优于 AFlow 的 `82.25`。
- 单项上也全面领先，如 MATH `51.82` vs `51.28`，HumanEval `92.85` vs `90.93`。

### Tab. 2: GAIA
- MaAS 平均 `20.69`，显著高于 AgentSquare `16.34`、GPTSwarm `16.33`、AFlow `8.00`。
- 这组结果支持论文核心论点：跨 domain 工具使用任务更需要 query-dependent workflow。

### Tab. 3 / Fig. 4: 成本
- 在 MATH 上，MaAS 训练成本 `3.38$`，AFlow 为 `22.50$`。
- 推理成本上，MaAS 为 `0.42$`，低于 AFlow 的 `1.66$`。
- 推理 wall-clock 也更短：MaAS `19 min`，AFlow `23 min`。

### Fig. 5 / Fig. 6 / Fig. 7 / Tab. 4
- Fig. 5 直观看到 easy query 更容易早停，hard query 会走更多层。
- Fig. 6 给出 math / GAIA / HumanEval 的具体 workflow 案例。
- Fig. 7 显示 `L=4`、`K=4` 是较合理折中；更大 `lambda` 更省钱但会掉性能。
- Tab. 4 表明移除 textual gradient 掉点最大，说明 operator 自演化是关键组件。

## 实验设置
- 任务域：数学推理（GSM8K, MATH, MultiArith）、代码生成（HumanEval, MBPP）、工具使用（GAIA）。
- 主执行 LLM：gpt-4o-mini；还测试了 Qwen-2.5-72B 与 Llama-3.1-70B 的跨骨干迁移。
- 超参：`L = 4`，`K = 4`，`thres = 0.3`，`lambda in {1e-3, 5e-3, 1e-2}`（Sec. 4.1）。

## 代码对照与可复现性

### 仓库里能直接看到的实现
- 入口脚本 `examples/maas/optimize.py` 暴露 `dataset / sample / round / batch_size / lr / is_textgrad` 等参数。
- `maas/ext/maas/models/controller.py` 实现 4-layer controller，使用 `all-MiniLM-L6-v2` 做 query / operator embedding，并用阈值累计采样 operator。
- `maas/ext/maas/benchmark/benchmark.py` 中的训练损失是 `loss = -(logprobs * utilities).mean()`，其中 `utilities = score - 3 * cost`，对应论文的“性能 - 成本”思想。
- `maas/ext/maas/scripts/optimized/*/graph.py` 给出了具体 workflow 执行图，如 MATH 图会组合 `Generate / MultiGenerateCoT / Programmer / SelfRefine / ScEnsemble / EarlyStop`。

### 论文与公开代码的差异
- 论文正文写的是更一般的 operator 空间，包含 CoT、Debate、Self-Consistency、Self-Refine、Ensemble、Testing、ReAct、Early Exit（Appendix B.1）。
- 公开仓库当前主要支持 `MATH / GSM8K / HumanEval` 三个 benchmark，`experiment_configs.py` 中 operator 集也缩成 7 个。
- 代码里没有复现论文正文中的完整 GAIA / MBPP / MultiArith 设置，也没有把 Debate / ReAct 作为主训练入口开放出来。
- 因此当前仓库更像“论文核心思想的可运行公开版”，而不是 paper 全部实验的逐项一比一复刻版。

## 批判性思考

### 优点
1. 论文把 agent workflow search 从“离散搜单解”改成“学条件分布”，思路比只做 prompt / topology 小修小补更根本。
2. 成本指标被直接写进目标函数，这对真实 LLM 系统很重要。
3. 早停和多 operator 选择让系统自然具备 query-aware 资源分配能力。

### 局限
1. `Textual Gradient` 很强，但也让优化过程更依赖外部 LLM 的稳定性与提示质量。
2. 论文的完整 operator / benchmark 设定在公开代码里没有完全展开，复现实证会受限。
3. utility-cost 权衡目前仍依赖手工系数 `lambda`，不同部署预算下需要重新调参。

### 我自己的判断
- 这篇论文最值得记住的不是某个具体 operator，而是“把 agent system 看成 conditional supernet”这个抽象。
- 如果你以后想把 NAS / supernet 思维迁到 agentic workflow，这篇是一个很好的起点。
- 但如果你想严格复现论文表格，当前公开 repo 还不算完全对齐。

## 关联概念
- [[Agentic Supernet]]
- [[Agentic Operator]]
- [[Textual Gradient]]
- [[Early Exit]]
- [[Chain-of-Thought Prompting]]

