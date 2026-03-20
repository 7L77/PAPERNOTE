---
title: "Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models"
method_name: "APD"
authors: [Haidong Kang, Lihong Lin, Hanling Wang]
year: 2025
venue: NeurIPS
tags: [NAS, training-free-nas, zero-cost-proxy, llm-guided-search, reinforcement-learning]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models.pdf
local_code: D:/PRO/essays/code_depots/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models
created: 2026-03-16
updated: 2026-03-20
---

# 论文笔记：APD

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models |
| OpenReview PDF | https://openreview.net/pdf/4de84ad7c65b21c88fbadfd0dda141113b8c3017.pdf |
| NeurIPS Poster | https://nips.cc/virtual/2025/poster/120003 |
| Code | https://github.com/yohbii/APD |
| 本地 PDF | `D:/PRO/essays/papers/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models` |

## 一句话总结
> 本文提出 APD：用 [[LLM-guided Search]] 自动生成并进化 [[Zero-Cost Proxy]]，再用 [[Actor-Critic Reinforcement Learning]] 学习“初始化/变异/交叉”提示策略，把训练免费 NAS 从手工 proxy 设计推进到自动发现范式。

## 核心贡献
1. 提出 LLM 驱动的代理自动发现框架 APD，用提示+上下文生成可执行 proxy（Sec. 3.1, Fig. 4）。
2. 引入 actor-critic 调度器，把代理进化操作学习成策略优化问题（Sec. 3.1, Eq. (5), Algorithm 1）。
3. 在 NAS-Bench-201/101、DARTS、TransNAS-Bench-101、OoD-ViT-NAS 上给出一致增益（Sec. 4, Table 2/3/4/5）。
4. 给出不同 LLM 的稳定性和组件消融，说明“进化 + actor-critic”组合是关键（Table 6/7）。

## 问题背景
### 要解决的问题
- 现有 training-free NAS 的 zero-cost proxy 多靠人工启发式，设计成本高，迁移到新搜索空间时相关性不稳定。

### 现有方法局限
- 手工 proxy 相关性不稳，甚至被参数量/FLOPs 这类简单指标击败（Sec. 2, Fig. 3）。
- 直接用 LLM 一次性生成 proxy（naive prompt）相关性偏低，缺少有效反馈闭环（Sec. 2, Table 6）。

### 本文动机
- 如果让 LLM 生成 proxy，再用 RL 奖励信号驱动“提示策略”迭代，就能形成“生成-评估-策略更新”闭环，提高 proxy 质量和效率。

## 方法详解
### 1) Proxy Candidate Generator
- 每一代向 LLM 输入操作类型 `op ∈ {init, mut, cross}` 与上下文窗口 `C_t`，生成候选 proxy。
- proxy 以 `(T, C)` 表示：`T` 是自然语言 thought，`C` 是可执行代码（Sec. 3.1）。

### 2) Fitness Evaluator
- 对候选 proxy 在基准架构集合上计算与真实精度排序的相关性，作为适应度：
\[
\phi(f) = \rho(f(a), p) - \beta \,\mathrm{cost}(f)
\]
- 其中 `ρ` 采用 [[Spearman's Rank Correlation]] / [[Kendall's Tau]]，并考虑运行代价（Sec. 3.1, Eq. (4)）。

### 3) RL Evolution Scheduler
- 用 actor-critic 根据历史状态选择动作（init/mut/cross）。
- 用平均适应度作为奖励更新策略，优化下一代提示选择（Sec. 3.1, Eq. (5)）。

### 4) 进化主循环
- 初始化种群 `P0`。
- 每代执行：动作采样 -> LLM 生成 -> 评估 -> 策略更新 -> 种群替换（Algorithm 1）。
- 文中报告在 NAS-Bench-201 上约 30 代可达 `Spearman > 0.80`（Sec. 3.2）。

### 5) 论文展示的代表性 APD 代理
- Table 1 给出的代表 proxy 形态（以 BN 输出稳定秩和 Conv 权重范数组合）：
\[
s_{\mathrm{APD}}=
\left(\sum_{l\in B}\frac{\|M_l(\theta)\|_F^2}{\|M_l(\theta)\|_2^2}\right)
\times
\left(\sum_{l\in C}\frac{\|W_l(\theta)\|_1}{\|W_l(\theta)\|_2}\right)
\]
- 本地仓库 `proxy_used_for_nb201.py` 中 `proxy4` 与该形式一致（BN stable-rank × Conv L1/L2 比值）。

## 关键公式
### Eq. (1) 目标
\[
\max_{f\in \mathcal{F}} \mathbb{E}_{a\subseteq A}\big[\rho(f(a), p(a))\big]
\]
- 含义：在候选 proxy 空间中最大化“proxy 分数排序”和“真实精度排序”的一致性。

### Eq. (4) 适应度
\[
\phi(f) = \rho(f(a), p) - \beta\,\mathrm{cost}(f)
\]
- 含义：同时追求高相关性与低运行开销。

### Eq. (5) A2C 更新
\[
\theta \leftarrow \theta + \eta \nabla_\theta \log\pi_\theta(a_t|s_t)\,[r_t+\gamma V_\psi(s_{t+1})-V_\psi(s_t)]
\]
\[
\psi \leftarrow \psi - \eta_v \nabla_\psi \big(r_t+\gamma V_\psi(s_{t+1})-V_\psi(s_t)\big)^2
\]
- 含义：actor 用优势项做策略梯度，critic 逼近状态价值。

## 关键图表与结果
### Figure 1 / Figure 4
- Fig. 1 对比手工设计、naive LLM 与 APD。
- Fig. 4 给出 APD 完整闭环：prompt、LLM、评估器、actor-critic。

### Table 2（NB-201 / NB-101）
- APD 在 NB-201 上准确率达到：CIFAR-10 `93.76`、CIFAR-100 `72.22`、ImageNet16-120 `45.03`。
- 相对最优基线分别提升 `+0.07 / +0.52 / +0.69`，且运行时降到 `16.81 ms/arch`（表中给出的对比降幅约 50%+）。

### Table 3（DARTS）
- DARTS 搜索空间上，APD(C10) 报告 `97.63%`（CIFAR-10）与 `84.83%`（CIFAR-100），搜索成本 `0.004 GPU-days`。
- APD(Img) 在 ImageNet1k 报告 `Top-1 76.9 / Top-5 94.0`，同为 `0.004 GPU-days` 级别。

### Table 4（TransNAS-Bench-101）
- APD 在 autoencoding 任务 SSIM 达 `0.54±0.01`，scene classification 达 `54.0±0.6`，整体优于多数对比 proxy。

### Table 5（OoD-ViT-NAS-Ti）
- APD 在 ImageNet1k / A / R / D(Texture) / D(Material) 的相关性为 `0.79 / 0.82 / 0.88 / 0.12 / 0.15`，显示跨分布泛化能力。

### Table 6 / Table 7（消融）
- 不同 LLM 下 APD 平均相关性稳定在 ~73-81 区间，显著高于 naive GPT4o 的 `60.51`。
- 组件消融显示：naive -> +evolution -> +actor-critic 对 CIFAR-10/100 准确率逐步提升至 `93.76 / 72.22`。

## 实验设置与实现细节
- 搜索空间：NAS-Bench-201/101、DARTS、TransNAS-Bench-101、OoD-ViT-NAS。
- 任务：图像分类、自动编码、场景分类、拼图自监督。
- 附录配置（Table 8）：`episodes=10`, `steps=100`, `history_window=5`, `gamma=0.9`, `hidden=256`, `batch=16`, `repeats=5`。

## 与代码实现的对照（基于本地 APD 仓库）
- 已归档代码：`D:/PRO/essays/code_depots/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models`
- `main.py` 实现了 `get_new_pop -> evaluate -> actor-critic update -> topk replacement` 的主循环，与 Algorithm 1 主体一致。
- `src/utils.py` 里 action=0/1/2 对应 initialization/mutation/crossover prompt。
- `src/env.py` 通过动态 `exec` 执行 LLM 生成代码并评分，失败时记 `0` 分（论文写法是 contract fail 赋 `-∞`）。
- `src/agent.py` 采用 A2C 结构，但当前 `ValueNet` 对单输出做 `softmax`，会导致 value 退化为常数，和论文中 critic 价值估计存在实现偏差。
- 仓库当前缺少 `evaluate_nas201.py / evaluate_nas101.py / evaluate_trans101.py` 与 `prompt/` 文件夹，直接复现完整流程需要自行补齐。

## 批判性思考
### 优点
1. 框架范式清晰：把“proxy 设计”从人工经验转成可优化的自动发现流程。
2. 实证覆盖面广：CNN 搜索空间、ViT OoD 场景、多任务验证都有结果。
3. 讨论了 LLM 黑箱、代价与稳定性，并给出可观测反馈路径（Sec. 4.7 + 附录）。

### 局限
1. 适应度依赖小规模真值子集，严格意义上并非完全“零监督”。
2. 工程上需要执行 LLM 生成代码，安全沙箱与健壮性要求高。
3. 当前公开仓库与论文描述有缺口，复现门槛高于论文文字给出的直观印象。

### 可复现性评估
- [x] 论文公开
- [x] 官方代码链接公开
- [x] 本地代码已归档
- [ ] 一键复现实验完整（仓库缺少部分关键模块/资源）

## 关联概念
- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[LLM-guided Search]]
- [[Actor-Critic Reinforcement Learning]]
- [[Chain-of-Thought Prompting]]
- [[Spearman's Rank Correlation]]
- [[Kendall's Tau]]
