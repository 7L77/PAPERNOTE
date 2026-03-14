---
title: "Zero-Shot Neural Architecture Search with Weighted Response Correlation"
method_name: "WRCor"
authors: [Kun Jing, Luoyu Chen, Jungang Xu, Jianwei Tai, Yiyu Wang, Shuaimin Li]
year: 2025
venue: arXiv
tags: [NAS, zero-shot-nas, training-free-proxy, response-correlation]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2507.08841v2
local_pdf: D:/PRO/essays/papers/Jing 等 - 2025 - Zero-Shot Neural Architecture Search with Weighted Response Correlation.pdf
local_code: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation
created: 2026-03-14
---

# 论文笔记：WRCor

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | Zero-Shot Neural Architecture Search with Weighted Response Correlation |
| arXiv | https://arxiv.org/abs/2507.08841 |
| HTML | https://arxiv.org/html/2507.08841v2 |
| 代码 | https://github.com/kunjing96/ZSNAS-WRCor |
| 本地 PDF | `D:/PRO/essays/papers/Jing 等 - 2025 - Zero-Shot Neural Architecture Search with Weighted Response Correlation.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation` |

## 一句话总结

> 论文提出 [[Weighted Response Correlation]]（WRCor）：在未训练网络上统计不同样本在多层激活与梯度响应的相关系数矩阵，并对高层响应做指数加权，以更稳健地做 zero-shot NAS 排序。

## 核心贡献

1. 提出基于“响应相关性”的统一代理框架：同时覆盖可表达性（activation）与泛化相关性（gradient）。
2. 提出按层指数加权的 WRCor（底层到顶层权重 `2^l`），强调高层语义区分能力（Sec. 3.3.2, Eq. (10)-(11)）。
3. 提出投票代理 SPW/SJW，在不同搜索空间和设置下提升稳健性（Sec. 3.3.3）。
4. 在 NAS-Bench-101/201 和 MobileNetV2 搜索空间给出 zero-shot NAS 结果；RE-SJW 在 ImageNet-1k 上以 0.17 GPU day 达到 21.9% top-1 error（Table 10）。

## 问题背景

### 要解决的问题

现有 zero-shot proxy 往往在“效果、稳定性、泛化性”三者之间顾此失彼，且并不总能稳定优于 Params/FLOPs 这类朴素基线。

### 现有方法局限

- 很多 proxy 只刻画单一侧面（仅表达性或仅可训练性）。
- 部分 proxy 对结构或激活函数有额外约束，通用性不足。
- 搜索空间变大时，相关性指标可能明显退化（如 NB101 相比 NB201）。

### 本文动机

作者认为架构质量可由“跨样本响应是否线性独立”刻画，并且高层响应更关键，因此构造 response-correlation + layer weighting 的 proxy。

## 方法详解

### 1) 响应定义

- 响应包括：激活（activations）和对隐藏特征图的梯度（gradients）。
- 核心统计对象：同一层中，不同输入样本之间的相关系数矩阵（Sec. 3.1, 3.2）。

### 2) ACor / GCor / RCor

- ACor：仅聚合激活相关矩阵，偏向表达性。
- GCor：仅聚合梯度相关矩阵，偏向训练动态/泛化能力。
- RCor：把激活与梯度相关矩阵统一到同一 log-det 评分形式（Eq. (8)-(9)）。

### 3) WRCor（核心）

- 观察：好模型更依赖高层特征做区分，顶层响应相关性更能反映最终可分性。
- 设计：对层级相关矩阵做指数加权（bottom-to-top），权重随层数几何增长（Eq. (10)-(11)）。
- 直觉：允许底层存在一定相关性，但更强调顶层“跨样本可区分性”。

### 4) 投票代理 SPW / SJW

- SPW: SynFlow + PNorm + WRCor。
- SJW: SynFlow + JacCor + WRCor。
- 使用多数投票整合多 proxy，缓解单一 proxy 的场景脆弱性（Sec. 3.3.3）。

### 5) 搜索策略

- 随机搜索（R）
- 强化学习（RL，policy gradient）
- 规则化进化（RE，tournament + mutation）
- 最终都从探索集合中选 proxy 评分最优架构（Sec. 3.4, Alg. 1-2）。

## 关键公式

### Eq. (1): 相关矩阵聚合

\[
\mathbf{K}^{A/G}=\sum_{i=1}^{N_a}|\mathbf{C}^{A/G}_i|^{x}
\]

含义：对层内多个响应单元的相关矩阵做聚合，得到架构级统计矩阵。  
符号：
- \(\mathbf{C}^{A/G}_i\)：第 \(i\) 个激活/梯度响应的样本相关矩阵
- \(N_a\)：响应单元数
- \(x \in [0,1]\)：幂次系数

### Eq. (8)-(9): RCor

\[
S_{\text{RCor}}=\log(\det(\mathbf{K})),\quad
\mathbf{K}=\sum_i\left(|\mathbf{C}^{A}_i|+|\mathbf{C}^{G}_i|\right)
\]

含义：统一使用 log-det 将“跨样本线性独立性”映射为标量分数。  
分数越高，意味着非对角相关更小，样本响应更独立。

### Eq. (10)-(11): WRCor

\[
S_{\text{WRCor}}=\log(\det(\mathbf{K})),\quad
\mathbf{K}=\sum_{l=1}^{L}\sum_{i=1}^{N_a^l}2^l\cdot\left(|\mathbf{C}^{A}_{l,i}|+|\mathbf{C}^{G}_{l,i}|\right)
\]

含义：在 RCor 基础上对层级做指数加权，强化顶层响应贡献。  
符号：
- \(l\)：层索引（由浅到深）
- \(L\)：层数
- \(N_a^l\)：第 \(l\) 层非线性单元数

## 关键图表

### Figure 1（方法总览）

- 展示从前向/反向响应提取相关矩阵，再经加权聚合与 log-det 得到 WRCor 分数的流程。

### Figure 2（代理分数 vs 真实精度）

- WRCor 的散点分布更紧凑，和 test accuracy 呈现更好的单调关系（优于 SynFlow/JacCor，接近 ValAcc）。

### Table 2（CIFAR-10, NB201）

- WRCor real Spearman \(\rho=0.812\)，优于 NASWOT(0.780)、ZiCo(0.800)、RCor(0.803)。

### Table 3（加权策略消融）

- `expb2t`（WRCor）优于 no/linear/quad/expt2b；验证“高层更重要”假设。

### Table 4/5/6/7（跨数据集/批大小/初始化/搜索空间）

- WRCor 在 NB201 上整体稳定且强；NB101 上虽然下降，但仍优于多数基线。
- 使用随机噪声输入时 WRCor 仍有竞争力（Sec. 4.2）。

### Table 8/9（NAS-Bench 搜索）

- WRCor 与 SJW 在多搜索策略下显著优于 ZeroCost，且代价远低于 ValAcc-based 搜索。

### Table 10/11（MobileNetV2 + ImageNet-1k）

- RE-SJW: top-1 error 21.9%，FLOPs 592M，搜索代价 0.17 GPU day。
- 与 ZiCo/AZ-NAS 精度接近，但搜索代价更低或相当。

## 与代码实现的对照

- 关键实现位于 `foresight/pruners/measures/act_grad_cor_weighted.py`：
  - 在 ReLU 模块注册 forward/backward hook，分别收集输入激活和梯度相关矩阵。
  - 用 `weight = 2**i` 做层级指数加权，对应 Eq. (11)。
  - 用 `np.linalg.slogdet` 计算 log-det 分数。
- 未加权版本在 `act_grad_cor.py`，对应 RCor 思路。
- 搜索流程与论文 Alg. 1/2 对应代码在 `search.py`（`RL_NAS` / `Evolved_NAS` / `Random_NAS`）。
- 实现细节补充：代码默认 measure 名为 `act_grad_cor_weighted`，在 README 中与 `synflow + jacob_cor` 组合复现 SJW 风格搜索。

## 批判性思考

### 优点

1. 代理构造简洁，直接从统计矩阵出发，解释性强。
2. 在大量 setting 下结果稳定，且兼顾 proxy 质量与搜索效率。
3. 代码公开，关键模块与论文叙述一致，可追踪性好。

### 局限

1. 在更大搜索空间（NB101）上 WRCor/SJW 的相关性仍明显退化。
2. 论文也承认不存在“单一全场景最优 proxy”，因此仍依赖投票融合。
3. 相关矩阵与 log-det 对 batch 和数值稳定性仍有工程敏感性（虽然实验证明总体可控）。

### 可复现性评估

- [x] 论文公开
- [x] 官方代码公开
- [x] 本地代码已归档
- [x] 关键公式/算法/实验均可追踪

## 关联概念

- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Weighted Response Correlation]]
- [[Proxy Voting]]


