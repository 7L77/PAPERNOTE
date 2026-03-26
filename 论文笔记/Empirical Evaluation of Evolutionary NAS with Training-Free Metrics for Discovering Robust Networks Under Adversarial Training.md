---
title: "Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training"
method_name: "TF-MONAS-Eval"
authors: [Can Do, Ngoc Hoang Luong, Quan Minh Phan]
year: 2025
venue: RIVF
tags: [nas, evolutionary-nas, training-free-metrics, adversarial-robustness, multi-objective]
zotero_collection: ""
image_source: online
doi: "10.1109/RIVF68649.2025.11365115"
created: 2026-03-25
updated: 2026-03-25
local_pdf: D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf
code_archive_status: "No official repository link is provided in the paper; no verifiable official code found as of 2026-03-25."
---

# 论文笔记: TF-MONAS-Eval

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training |
| 作者 | Can Do, Ngoc Hoang Luong, Quan Minh Phan |
| 会议 | IEEE RIVF 2025 |
| DOI | https://doi.org/10.1109/RIVF68649.2025.11365115 |
| 本地 PDF | `D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf` |
| 本地代码 | Not archived (no official link in paper) |

## 一句话总结
> 这篇工作不是提出新 NAS 算法，而是系统比较了训练式目标和训练自由指标在对抗训练场景下的 ENAS 表现，结论是：单目标下训练式目标更稳，而多目标下 `NSGA-II + SynFlow` 最优且更省算力。

## 问题与动机
- 过去很多 [[Training-free NAS]] 研究把鲁棒性评测放在“标准训练后”的网络上。
- 但真实部署常见的是 [[Adversarial Training]]，它会改变 clean/robust trade-off。
- 作者想回答：在“先做对抗训练再评测鲁棒性”的条件下，training-free 指标还是否可靠。

## 核心设置
- 搜索空间：NAS-Bench-201（15,625 个架构）。
- 参考基准：
- `[[NAS-Bench-Suite-Zero]]` 提供 SynFlow 分数。
- `[[NAS-RobBench-201]]` 提供对抗训练后的 clean 与 robust 精度。
- 算法与目标（4 个变体）：
- `GA (Val-Acc-12)`：单目标，最大化第 12 epoch 验证精度。
- `GA (SynFlow)`：单目标，最大化 [[Synaptic Flow]]。
- `NSGA-II (Val-Acc-12)`：多目标，最大化 Val-Acc-12 + 最小化 FLOPs。
- `NSGA-II (SynFlow)`：多目标，最大化 SynFlow + 最小化 FLOPs。
- 评测攻击：FGSM (3/255, 8/255)、PGD (3/255, 8/255)、[[AutoAttack]]。
- 统计：31 次独立运行，显著性检验使用 Student t-test (`p < 0.01`)。

## 方法流程（论文中的评测 pipeline）
1. 在 NAS-Bench-201 上用 GA / NSGA-II 搜索候选架构。
2. 对候选架构在 NAS-RobBench-201 协议下进行对抗训练评估。
3. SONAS 直接比较最优解；MONAS 用 CEC 2024 规则从 Pareto 集选代表解。
4. 比较 clean 与多种攻击精度，同时对比搜索成本。

## 关键结果
### 1) SONAS：`GA (Val-Acc-12)` 整体优于 `GA (SynFlow)`
- 在 CIFAR-10/CIFAR-100/ImageNet16-120 上，`GA (Val-Acc-12)` 大多数指标更高。
- 仅在 CIFAR-10 的强扰动（FGSM 8/255、PGD 8/255）中，`GA (SynFlow)`略好。
- 结论：在“对抗训练后评测”条件下，最高 SynFlow 分数并不等价于最高鲁棒精度。

### 2) MONAS：`NSGA-II (SynFlow)` 全面优于 `NSGA-II (Val-Acc-12)`
- Table II 中 3 个数据集、6 个指标全部由 `NSGA-II (SynFlow)` 更优。
- 论文解释：多目标返回多样架构，能提高命中高鲁棒解的概率。

### 3) 成本优势
- 在相同 3,000 次评估预算下，训练式目标需要反复训练，成本显著更高。
- 文中指出 `GA (Val-Acc-12)` 搜索成本超过 `GA (SynFlow)` 的 11 倍。

## 对这篇论文的理解
- 这篇文章的价值主要在“结论迁移纠偏”：
- 之前在非对抗训练基准上看起来强的 TF 指标，在 AT 条件下不一定同样强。
- 但 TF 指标在 MONAS 框架里依然非常有价值，尤其是 `SynFlow + NSGA-II`。
- 对你当前“鲁棒 NAS + 训练自由代理”的方向，最重要启发是：
- 代理指标不要只在单目标最优解上验证，要放进多目标/解集搜索框架评估。

## 局限与风险
1. 仍基于 NAS-Bench-201 系列基准，外推到更大搜索空间需要额外验证。
2. 搜索算法只覆盖 GA 与 NSGA-II，未覆盖更现代的 differentiable / predictor-based NAS。
3. 论文不提供可验证官方代码链接，复现实验主要依赖 benchmark 数据本身。

## 关联概念
- [[Evolutionary Neural Architecture Search]]
- [[Training-free NAS]]
- [[Synaptic Flow]]
- [[Single-objective NAS]]
- [[Multi-objective NAS]]
- [[NSGA-II]]
- [[Genetic Algorithm]]
- [[Adversarial Training]]
- [[NAS-RobBench-201]]
- [[NAS-Bench-Suite-Zero]]
- [[AutoAttack]]
