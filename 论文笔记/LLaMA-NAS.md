---
title: "LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models"
method_name: "LLaMA-NAS"
authors: [Anthony Sarah, Sharath Nittur Sridhar, Maciej Szankin, Sairam Sundaresan]
year: 2024
venue: arXiv
tags: [NAS, LLM, PEFT, LoRA, multi-objective-search]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2405.18377v1
local_pdf: D:/PRO/essays/papers/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models.pdf
local_code: D:/PRO/essays/code_depots/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models
created: 2026-03-14
---

# 论文笔记: LLaMA-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models |
| arXiv | https://arxiv.org/abs/2405.18377 |
| HTML | https://arxiv.org/html/2405.18377v1 |
| 项目页 | https://llama-nas.github.io/ |
| 代码链接 | https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning |
| 本地 PDF | `D:/PRO/essays/papers/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models` |

## 一句话总结
> LLaMA-NAS 在 [[One-shot NAS]] 框架下，为每层引入 [[Mixed-Rank Adapter]] 形成 [[Super-network]]，再用 [[NSGA-II]] 在精度与参数量之间搜索 [[Pareto Front]]，实现 LLM 高效适配。

## 核心贡献
1. 把 LLM 适配问题形式化为“任务性能 + 适配器参数量”的双目标搜索，减少手工 rank 选择。
2. 设计 mixed-rank adapter 超网，使同一训练好的 super-adapter 可导出不同预算子网（Sec. 3.1-3.2）。
3. 在 commonsense、math、quantized adapter、跨模型实验中，展示了比启发式 rank 选择更稳定的精度-效率权衡（Table 2-5）。

## 问题背景
### 要解决的问题
- 传统 [[Low-Rank Adapter]] / [[Parameter-Efficient Fine-Tuning]] 需要手工设置统一 rank，难以在不同层、不同任务下都最优。
- 全量微调成本高；简单启发式 rank 又常常错过更优精度-效率组合。

### 现有方法局限
- 单一 rank 方案忽略层间敏感度差异。
- 只用规则（如按层比例降 rank）不能直接优化全局 Pareto 最优。

### 本文动机
- 先训练一个可弹性导出子网的 super-adapter，再做低成本搜索，能同时得到高效和高精度适配器。

## 方法详解
### 1) 超网构建
- 在每个 Transformer 层放置 mixed-rank adapter（多个 rank 候选分支），形成 [[Super-network]]。
- 通过 one-shot 训练共享参数，减少每个候选结构独立训练的成本。
- Source: Sec. 3.1

### 2) 架构搜索
- 定义双目标：maximize 任务指标，minimize adapter 参数规模。
- 使用 [[NSGA-II]] 在离散 adapter 配置空间中搜索 Pareto 解集。
- Source: Sec. 3.2

### 3) 子网导出与评估
- 从 Pareto 集合选择满足预算的子网，直接评估下游任务。
- 论文同时报告启发式配置与 NSGA-II 配置的对比。
- Source: Sec. 4, Table 2-5

## 关键公式
### 多目标搜索目标
\[
\max_{a \in \mathcal{A}} \; \text{Perf}(a), \quad \min_{a \in \mathcal{A}} \; \text{Params}(a)
\]

含义:
- 在 adapter 架构空间 \(\mathcal{A}\) 里，同时追求更高任务性能与更小参数规模。
- 最终输出的是 Pareto 解集，而不是单个固定结构。
- Source: Sec. 3.2 (paper description of search objective)

## 关键结果
### Table 2: Heuristic vs NSGA-II（关键数字）
- Llama-2-7B commonsense:
  heuristic 4.194M / 70.89 vs NSGA-II 2.621M / 71.42
- Llama-2-13B commonsense:
  heuristic 6.291M / 73.39 vs NSGA-II 3.932M / 73.95
- Llama-2-7B math:
  heuristic 6.291M / 8.31 vs NSGA-II 3.932M / 8.34
- Llama-2-13B math:
  heuristic 8.389M / 8.89 vs NSGA-II 5.243M / 8.53

结论:
- 多数设置下 NSGA-II 同时降参数并保持/提升精度；
- 也存在个别任务（13B math）精度小幅回落，说明 Pareto 选择需结合任务偏好。

### Table 3: 与 baselines 对比（commonsense）
- 7B: LLaMA-NAS 71.42，优于 LoRA 70.95、QLoRA 67.54、LoNAS 70.89。
- 13B: LLaMA-NAS 73.95，优于 LoRA 73.59、QLoRA 71.27、LoNAS 73.39。

### Table 4: Quantized adapters
- LLaMA-NAS-Q 在 7B/13B 分别 70.58/73.66，优于 QLoRA 的 67.54/71.27。

### Table 5: 跨模型泛化
- 在 Llama-3-8B、Mistral-7B、Mistral-v0.3 上均给出 competitive 结果，说明方法并非只对单模型有效。

## 与代码归档的核对
- 项目页提供的 GitHub 为 IntelLabs 研究集合仓库。
- 截至 2026-03-14，本地归档仓中未发现明确命名为 “LLaMA-NAS” 的独立目录或复现实验脚本。
- 因此实现细节以论文为主，代码链接保留为项目页官方入口。

## 批判性思考
### 优点
1. 把 LLM adapter 设计从手工调参推进到可搜索、可权衡框架。
2. 结果覆盖 commonsense、math、quantized、跨模型，实验面较全。
3. 以 Pareto 形式输出候选，便于按部署预算选型。

### 局限
1. 搜索和评估仍在有限任务集合，跨更多 domain 的稳健性待验证。
2. 论文主张的实现与公开代码入口之间存在对应关系不够直接的问题。
3. 13B math 场景出现精度-压缩冲突，提示搜索目标可能需要任务自定义。

### 复现性评估
- [x] 有官方项目页与代码入口
- [ ] 论文同名实现路径清晰可定位
- [x] 方法与实验设置在论文中描述较完整
- [ ] 一键复现实验未直接给出

## 关联概念
- [[Neural Architecture Search]]
- [[One-shot NAS]]
- [[Super-network]]
- [[Mixed-Rank Adapter]]
- [[Low-Rank Adapter]]
- [[Parameter-Efficient Fine-Tuning]]
- [[NSGA-II]]
- [[Pareto Front]]
