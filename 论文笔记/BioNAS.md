---
title: "Neural Architecture Search with Mixed Bio-inspired Learning Rules"
method_name: "BioNAS"
authors: [Imane Hamzaoui, Riyadh Baghdadi]
year: 2025
venue: ECAI 2025 (arXiv preprint)
tags: [nas, bio-inspired-learning, adversarial-robustness, darts, evolutionary-search]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2507.13485v1
local_pdf: D:/PRO/essays/papers/Neural Architecture Search with Mixed Bio-inspired Learning Rules.pdf
code_url: https://anonymous.4open.science/r/LR-NAS-DFE1
code_archive_status: "failed: repository not found at anonymous.4open.science (checked 2026-03-25)"
created: 2026-03-25
---

# 论文笔记: BioNAS

## TL;DR
> BioNAS 把“每层用什么算子”与“每层用什么生物启发学习规则”一起做 NAS 搜索，在保持生物可解释性的同时，把准确率和鲁棒性一起推高。

## 元信息
| 条目 | 内容 |
|---|---|
| 论文 | Neural Architecture Search with Mixed Bio-inspired Learning Rules |
| arXiv | https://arxiv.org/abs/2507.13485 |
| HTML | https://arxiv.org/html/2507.13485v1 |
| PDF | https://arxiv.org/pdf/2507.13485 |
| 本地 PDF | `D:/PRO/essays/papers/Neural Architecture Search with Mixed Bio-inspired Learning Rules.pdf` |
| 代码链接（论文声明） | https://anonymous.4open.science/r/LR-NAS-DFE1 |
| 本地代码归档 | 未归档（匿名仓库地址当前返回 repository not found） |

## 核心贡献
1. 提出 **BioNAS**：首次把“学习规则”作为 NAS 搜索变量，而不是只搜索网络算子/拓扑。
2. 证明“**混合学习规则**（不同层不同规则）”比“全网统一单一规则”更好，准确率与对抗鲁棒性都提升。
3. 在 CIFAR-10/CIFAR-100/ImageNet16-120/ImageNet 上给出生物启发范式下的强结果，并报告多种攻击下鲁棒性。

## 问题背景
### 要解决的问题
- 生物启发学习规则（FA/uSF/brSF/frSF 等）通常更生物合理、也常更鲁棒，但准确率与可扩展性往往不如 BP。
- 现有 NAS 通常只搜结构，不搜学习规则，忽略了“不同层可能适合不同学习机制”。

### 本文的关键假设
- 层间使用异构学习规则可以提供更稳定的优化动态（文中用梯度方差分析支持）。
- 在 NAS 中联合搜索“算子 + 学习规则”比固定规则更有表达力。

## 方法详解
### 1) 学习规则建模（Sec. 3.1, Eq. (1)-(5), Fig. 1）
- 从标准 BP 更新出发（Eq. (1)），再替换反馈路径得到生物启发规则。
- 重点规则：
  - `FA`: 用固定随机反馈矩阵替代转置权重反馈。
  - `uSF`: 反馈方向与前向权重符号一致，幅值统一。
  - `brSF`: 符号一致，幅值按 batch 随机。
  - `frSF`: 符号一致，幅值为固定随机量。
- 论文同时讨论了 `Hebbian` 与 `Predictive Coding` 卷积模块的可插拔性。

### 2) 搜索空间扩展（Sec. 3.2）
- 原 DARTS/EG-NAS 搜索空间上，将候选操作扩为“算子 + 学习规则”二元组。
- 候选覆盖 sep conv、dilated conv、pooling、skip、zero 等操作。
- 论文给出的量级结论：当每个操作配 `R` 个学习规则时，搜索空间约扩展为原来的 `R` 倍（文中示例为 4 倍级别）。

### 3) BioNAS-DARTS（Sec. 3.3, Eq. (6)-(10), Fig. 2）
- 沿用 DARTS 双层优化框架：训练集更新权重、验证集更新架构参数（Eq. (6),(7)）。
- 通过连续松弛与一阶近似进行交替更新（Eq. (8),(9)）。
- 节点输出由候选“算子-规则对”的加权和构成（Eq. (10)），最终离散化取每条边概率最高项。

### 4) BioNAS-EG（Sec. 3.3, Eq. (11)）
- 在 EG-NAS / CMA-ES 框架中，同样用“算子-规则对”编码个体。
- 进化更新分布参数，网络权重用 SGD 更新，实现“进化搜架构 + 梯度训参数”的组合。

### 5) 对抗评估协议（Sec. 3.5）
- 攻击包括 `FGSM/PGD/TPGD/APGD/One-Pixel/Square/Transfer`。
- 兼顾白盒与黑盒攻击，强调“混合学习规则”在强攻击下的韧性。

## 关键图表与结果
### Figure 1
- 对比 BP 与 FA 类反馈方式，并给出生物回路启发图；核心信息是“反馈路径可被替换，不必依赖严格对称反传”。

### Figure 2
- 展示 BioNAS 搜索过程：每条边同时选择操作与学习规则。

### Figure 3
- 梯度方差曲线：混合规则配置整体方差更低，支持“优化更稳”的经验结论。

### Table 1（CIFAR 测试误差）
- BioNAS-DARTS: **4.84% (CIFAR-10)**, **23.52% (CIFAR-100)**。
- 在生物启发组内明显优于单规则 ResNet 与 SoftHebb/FastHebb；与 BP 系 NAS 仍有差距但缩小明显。

### Table 2（ImageNet Top-1）
- BioNAS-DARTS: **60.51%**，BioNAS-EG: **57.01%**。
- 显著高于部分生物启发基线（如 SoftHebb/FastHebb），但低于经典 BP NAS（如 DARTS/EG-NAS）。

### Table 3（搜索阶段效率）
- 报告了搜索验证精度与 GPU-days。
- BioNAS-EG 搜索代价约 **0.35 GPU-days**，BioNAS-DARTS 约 **1.37 GPU-days**。

### Table 4（对抗鲁棒性）
- BioNAS-DARTS 在多项攻击下表现稳定：
  - Clean: **95.16**
  - FGSM: **61.1**
  - PGD: **60.6**
  - APGD: **67.0**
- 论文强调很多单规则模型在强攻击下会出现明显退化（部分接近 0）。

### Table 5（随机规则分配）
- 随机混合规则也能保持较高准确率（约 94.8% 左右），说明收益不只来自某个“特定固定模式”。

## 批判性思考
### 优点
1. 问题定义新颖：把学习规则显式纳入 NAS 搜索变量。
2. 证据链较完整：精度、鲁棒性、效率、梯度方差都覆盖。
3. 兼容性强：同一思想可落在 DARTS 与 EG 两类框架。

### 局限
1. 公式与实验细节有些地方写得较粗，部分符号/超参在主文表达不够干净。
2. 代码链接是匿名评审地址，当前不可访问，复现实操存在障碍。
3. 在大规模标准 BP NAS 上仍有性能差距，方法定位更偏“生物启发路线强化”而非全面 SOTA 替代。

## 关联概念
- [[Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Evolutionary Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Feedback Alignment]]
- [[Hebbian Learning]]
- [[Predictive Coding]]

