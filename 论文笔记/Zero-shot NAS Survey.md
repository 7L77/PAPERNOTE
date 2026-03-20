---
title: "Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities"
method_name: "Zero-shot NAS Survey"
authors: [Guihong Li, Duc Hoang, Kartikeya Bhardwaj, Ming Lin, Zhangyang Wang, Radu Marculescu]
year: 2024
venue: IEEE TPAMI
tags: [NAS, zero-shot-nas, training-free-nas, survey, hardware-aware-nas]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2307.01998v3
local_pdf: D:/PRO/essays/papers/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities.pdf
local_code: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities
created: 2026-03-20
---

# 论文笔记：Zero-shot NAS Survey

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Zero-Shot Neural Architecture Search: Challenges, Solutions, and Opportunities |
| 期刊 | IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2024 |
| arXiv | https://arxiv.org/abs/2307.01998 |
| HTML | https://arxiv.org/html/2307.01998v3 |
| DOI | 10.1109/TPAMI.2024.3395423 |
| 代码 | https://github.com/SLDGroup/survey-zero-shot-nas |
| 本地 PDF | `D:/PRO/essays/papers/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search Challenges, Solutions, and Opportunities` |

## 一句话总结

> 这篇 TPAMI 综述把 [[Zero-shot NAS]] 统一拆成“代理指标设计 -> benchmark 与硬件建模 -> 受约束/非受约束实验 -> future directions”，核心结论是：很多花哨 proxy 在大范围搜索里并不稳定地优于朴素的 `#Params/#FLOPs`，真正困难的是把高精度候选、硬件约束和泛化能力同时建模好。

## 核心贡献

1. 给出 [[Zero-shot Proxy]] 的统一分类法，把现有方法分成 gradient-based 与 gradient-free 两大类，并且用 [[Expressive Capacity]]、[[Generalization Capacity]]、[[Trainability]] 三个维度解释它们在理论上到底在测什么。
2. 系统比较 NASBench-201、NATS-Bench、TransNAS-Bench-101、ImageNet-1K、COCO、ADE20K、ViT 模型空间和 [[Hardware-aware NAS]] 场景，补上“这些 proxy 在真实大规模任务里到底好不好用”这件事。
3. 明确指出很多 proxy 在 unconstrained search space 上并不稳定优于 `#Params/#FLOPs`，而且一旦把关注点缩到 top-5% 高精度架构，相关性会显著掉。
4. 把硬件侧问题单独拉出来讨论，结合 HW-NAS-Bench、BRP-NAS、HELP、NN-Meter 分析 proxy 与 [[Hardware Performance Model]] 怎样一起进入硬件约束搜索流程。
5. 给出后续研究方向：更真实的 [[NAS Benchmark]]、同时覆盖精度与硬件指标的 benchmark、兼顾表达性/可训练性/泛化性的 proxy，以及针对不同网络家族定制的 proxy。

## 问题背景

### 这篇综述在回答什么

- 如果我们不训练候选网络，只在随机初始化时看某种打分，能不能足够可靠地替代 NAS 里的昂贵训练评估？
- 这些 zero-shot proxy 到底在测网络的哪一面，是表达能力、收敛速度，还是泛化能力？
- 这些指标在 hardware-oblivious 和 [[Hardware-aware NAS]] 两种情境下，是否都一样有效？

### 为什么这件事重要

- 多次训练候选网络的 multi-shot NAS 成本高得离谱，one-shot NAS 虽然便宜，但依然要训练 supernet。
- 对 edge AI 和部署友好的 NAS，除了精度之外还要同时考虑 latency、energy、memory 等硬件指标。
- 如果 zero-shot proxy 真能稳定工作，搜索阶段的成本会比一遍遍训练模型低很多。

## 方法详解

### 1. 设计 proxy 的理论标准

作者先给出一个很重要的判断框架：好的 [[Zero-shot Proxy]] 不该只盯着某一个统计量，而应尽量反映三件事。

- [[Expressive Capacity]]：网络是否有能力表示复杂函数与复杂模式。
- [[Generalization Capacity]]：网络能否把学到的东西迁移到未见样本，而不是只会“记住训练集”。
- [[Trainability]]：网络在优化上是不是好训练、好收敛。

本文最重要的批评点之一就是：多数现有 proxy 只覆盖这三者中的一小部分，因此在真实 NAS 中常常不稳。

### 2. Proxy taxonomy

#### 2.1 Gradient-based proxies

这些方法仍然需要 backward，但不需要完整训练。

- Gradient norm：看各层梯度范数之和，偏向度量训练时信号传播的强弱。
- SNIP / Synflow：基于参数与梯度的乘积，关注参数重要性与可剪枝性。
- GraSP：引入 Hessian 与梯度的二阶信息，更直接地刻画梯度流和收敛性。
- GradSign：看不同样本梯度符号的一致性。
- Fisher information：从激活与梯度估计二阶信息，刻画神经元/通道的重要性。
- Jacob cov：基于输入梯度的 Jacobian 协方差，作者把它归到更偏表达性的 proxy。
- Zen-score：看随机扰动前后中间表示变化，并叠加 BN scaling；偏重表达性。
- NTK Condition Number：衡量 NTK 谱条件数，作者认为它和泛化/优化动力学的关系最直接。

#### 2.2 Gradient-free proxies

- Number of Linear Regions：用 ReLU 网络对输入空间的分段线性划分数量近似表示能力。
- Logdet：基于 linear region 的编码矩阵行列式，继续度量输入空间被网络切分得多“丰富”。
- Topology-inspired proxies：例如 NN-Mass、NN-Degree，把 skip connection、宽度、深度与可训练性/表达性联系起来，尤其适合受约束的网络家族。

### 3. Benchmark 与硬件建模

#### 3.1 NAS benchmarks

- NASBench-101：经典 cell-based benchmark。
- NASBench-201 / NATS-Bench-TSS：固定 cell 拓扑搜索空间，在 CIFAR-10/CIFAR-100/ImageNet16-120 上可查表。
- NATS-Bench-SSS：大小/宽度搜索空间。
- TransNAS-Bench-101：跨任务 benchmark，覆盖分类、重建、像素级任务等。

作者的批评很明确：这些 benchmark 大多还是 DARTS-style cell search space，和真实工业常用的 MobileNet/FBNet 式空间不完全一致。

#### 3.2 Hardware performance models

[[Hardware-aware NAS]] 里光有 accuracy proxy 不够，还要能快速估计 latency/energy。

- BRP-NAS：按 layer-level 图结构建模，迁移性较弱，RMSE 4.6 ms。
- HELP：把硬件属性也作为输入，迁移性高，RMSE 0.12 ms。
- NN-Meter：分析到 kernel 粒度，精度更高，RMSE 1.2 ms，但迁移性不如 HELP。

作者想表达的是：硬件预测器本身也是 NAS pipeline 的关键部件，不是单独附属品。

### 4. 实验主线

#### 4.1 Unconstrained search space

- 在 NASBench-201 上，`#Params` 通常是最稳的；一些 gradient-based proxy 如 Grad norm、SNIP、GraSP、Fisher 也能跟上，但不是稳定全面超过。
- 在 NATS-Bench 上，`#Params` 与 Zen-score 效果较好。
- 在 TransNAS-Bench-101 上，`#Params/#FLOPs` 依然是最稳定的高相关指标。

这部分的核心信号是：如果你把整个搜索空间都算进去，很多 proxy 并不会明显优于极其简单的 `#Params/#FLOPs`。

#### 4.2 Constrained search space

- 当只关注 top-5% 高精度网络时，几乎所有 proxy 的相关性都会显著掉，包括 `#Params/#FLOPs`。
- 这件事对 NAS 很致命，因为我们真正关心的本来就是最优附近的那一小撮网络。

作者把这当成 zero-shot NAS 的根本短板：proxy 在“整体排序”上看起来还行，不代表它在“最优候选筛选”上也靠谱。

#### 4.3 Specific network families

- 在 ResNet / Wide-ResNet 家族上，SNIP、Zen-score、`#Params/#FLOPs`、NN-Mass 都能达到很高相关性，Spearman ρ 可超过 0.9。
- 在 MobileNet-v2 家族上，Grad norm、SNIP、Fisher、Synflow、Zen-score、NN-Mass 会略优于 `#Params/#FLOPs`。

这说明“按网络家族定制 proxy”是有希望的。也就是说，通用 proxy 很难做强，但针对受约束、常用的子空间，也许能做好。

#### 4.4 Large-scale tasks and ViTs

- 在 200 个 ImageNet-1K CNN 上，`#Params/#FLOPs` 仍优于大多数 zero-shot proxy。
- 在 COCO detection 与 ADE20K segmentation 上，结论基本延续。
- 在 100 个 ImageNet-1K ViTs 上，`#Params/#FLOPs` 依然比现有 zero-shot proxy 更稳。

所以这篇综述并没有替 zero-shot proxy“背书到大规模真实任务”，反而比较诚实地展示了它们现阶段的边界。

#### 4.5 Hardware-aware search

- 在 HW-NAS-Bench 的 energy-constrained 场景里，约束很紧时，不少 proxy 都还能靠近真实 [[Pareto Frontier]]；约束一放松，很多方法就开始偏离。
- 在 NATS-Bench 的 latency-constrained 场景里，大约 50 ms 附近只有 `#Params`、SNIP、Zen-score 还能较接近真实 Pareto-optimal 网络。

作者的解释是：硬件约束放松时，真正的 Pareto-optimal 网络往往落在高精度区域，而现有 proxy 恰好最不擅长那里。

## 关键公式

### Eq. (1) Gradient norm

$$
G \triangleq \sum_{i=1}^{D} \|\nabla_{\theta_i} L\|_2
$$

含义：把每一层参数梯度的二范数累加，近似看网络在初始化时是否“容易被训练信号有效驱动”。

### Eq. (2)-(3) SNIP 与 Synflow

$$
\text{SNIP} \triangleq \sum_i |\langle \theta_i, \nabla_{\theta_i} L \rangle|,\qquad
\text{Synflow} \triangleq \sum_i \langle \theta_i, \nabla_{\theta_i} L \rangle
$$

含义：参数值与梯度耦合后，可近似反映参数重要性与梯度传播。

### Eq. (4) GraSP

$$
\text{GraSP} \triangleq \sum_i -\langle H_i \nabla_{\theta_i} L, \theta_i \rangle
$$

含义：引入 Hessian，刻画二阶层面的梯度流保留与收敛特性。

### Eq. (6) Fisher information proxy

$$
\sum_i \langle \nabla_{z_i} L, z_i \rangle^2
$$

含义：利用激活与其梯度估计神经元/通道的重要性。

### Eq. (10) Jacob cov

$$
\text{Jacob cov} \triangleq - \sum_{i=1}^{B}\left[(\lambda_i+\epsilon)+(\lambda_i+\epsilon)^{-1}\right]
$$

含义：基于输入 Jacobian 的协方差谱，刻画网络表示的分散程度与表达性。

### Eq. (11) Zen-score

Zen-score 计算 `f_e(x)` 与 `f_e(x+\alpha\epsilon)` 的差异，并叠加 BatchNorm 的 scaling 项。

含义：如果随机微扰会显著改变中间表示，说明网络在初始化时具有更强的表示敏感性/表达性。

### Eq. (15) NTK Condition Number

$$
\text{NTK Cond} \triangleq \mathbb{E}_{X,\Theta}\frac{\lambda_m}{\lambda_1}
$$

含义：NTK 谱条件数越小，作者总结的经验是网络越容易训练，最终精度往往更高。

### Eq. (18) Logdet

$$
\text{Logdet} \triangleq \log |H|
$$

含义：利用 linear region 编码矩阵的行列式，间接表示输入空间分割的丰富程度。

### Eq. (19) NN-Mass

$$
\text{NN-Mass} \triangleq \sum_{\text{cell } c}\rho_c w_c d_c
$$

含义：把 skip connection 密度、宽度、深度一起揉进一个 topology-aware proxy，专门服务受约束搜索空间。

## 关键图表

### Fig. 1: NAS 三大范式总览

- multi-shot、one-shot、zero-shot 在搜索成本和精度上的关系一图说清。
- 这张图为全文定下基调：zero-shot 的价值首先是省训练成本，其次才是排序质量。

### Table 2: Proxy taxonomy

- 全文最重要的一张表。
- 作者把每个 proxy 是否 gradient-based，以及它更偏向表达性、泛化性还是可训练性，统一列出来。
- 这张表也是后续“为什么 `#Params` 很强、为什么多数 proxy 会失败”的逻辑起点。

### Fig. 5: NASBench-201 搜索空间

- 说明 benchmark 里的 cell-based 架构长什么样。
- 也间接暴露作者批评的一点：现在常用 benchmark 过于偏 DARTS-style cell space。

### Fig. 6-9: unconstrained vs top-5% constrained correlation

- 最值得记住的结论图。
- 在 All architectures 上，若干 proxy 看起来相关性不差；切到 Top 5% 后，相关性普遍显著下降。

### Table 4: NB201 / NATS 最优架构精度

- `#Params/#FLOPs` 在多个设置下拿到最高或接近最高的最终架构精度。
- 这是本文最“反直觉但重要”的实证结果之一。

### Table 5: TransNAS-Bench-101

- 在 segmentation / surface normal / autoencoding 这些跨任务设置上，`#Params/#FLOPs` 依然非常有竞争力。

### Table 6: Proxy-based NAS vs one-shot NAS

- One-shot NAS：ImageNet-1K Top-1 74.39，COCO mAP 0.28，搜索成本 200 GPU hours。
- Zero-shot proxy-based：精度略低，但搜索成本能降到 0.03-37 GPU hours。
- 这张表说明 zero-shot NAS 的核心卖点仍然是“便宜”，不是“绝对最优”。

### Fig. 17: ViT correlation

- 在 ViT 模型空间上，`#Params/#FLOPs` 依然领先于现有 zero-shot proxy。
- 说明 CNN 上的 proxy 结论并不能自动迁移成“Transformer 时代同样成立的强 proxy”。

### Fig. 18-19: hardware-aware Pareto frontier

- 展示不同 proxy 搜索出的网络与真实 Pareto frontier 的距离。
- 约束越宽松，proxy 越容易在高精度区域失真。

## 代码与实现观察

- 官方仓库不是“某一个新 zero-shot NAS 算法”的完整实现，而是一个评估工具箱。
- `main.py` 负责枚举 benchmark 中的候选架构，并调用不同 proxy 计算分数。
- `measures/` 实现了 grad_norm、SNIP、GraSP、Fisher、Jacob_cov、Synflow 等 proxy。
- NTK、Logdet、Zen-score 的计算逻辑主要在 `main.py` 与 `measures/__init__.py`。
- 这和论文定位一致：作者更关心“如何系统比较 proxy”，而不是提出一个单一新搜索算法。

## 批判性思考

### 优点

1. 很诚实。作者没有强行得出“新 proxy 全面优于朴素 baselines”的结论，反而把 proxy 失效场景讲清楚了。
2. 结构完整，把理论、benchmark、硬件预测、跨任务、ViT、Pareto 分析串成一个闭环。
3. 对做硬件约束 NAS 的人尤其有价值，因为它不只谈 accuracy proxy，还讨论硬件预测器与 benchmark 的局限。

### 局限

1. 它是 survey，不提供一个新的统一 proxy；对“下一步该怎么做”更多是方向而不是解决方案。
2. 评测对象仍然以 2024 年前的 proxy 为主，后续如 ZiCo 这类方法只在 discussion 里点到为止。
3. 大量实验依赖现有 benchmark，而这些 benchmark 本身就被作者批评不够贴近真实部署空间。

### 对你现在做 NAS 的启发

1. 如果你的搜索空间是一个非常具体的家族，例如 MobileNet-like、ResNet-like、某个固定超网子空间，不要急着追求“通用 proxy”，先做 family-specific proxy 更现实。
2. 如果你的目标是高精度尾部候选筛选，那一定要专门测 top-k 区域相关性，不能只看 all-architecture correlation。
3. 如果你要做鲁棒性 NAS 或硬件约束 NAS，proxy 的排序质量和硬件预测器质量要一起看，不能把后者当成后处理。

## 关联概念

- [[Zero-shot NAS]]
- [[Zero-shot Proxy]]
- [[Hardware-aware NAS]]
- [[NAS Benchmark]]
- [[Hardware Performance Model]]
- [[Expressive Capacity]]
- [[Generalization Capacity]]
- [[Trainability]]
- [[Pareto Frontier]]

