---
title: "Neural Architecture Design and Robustness: A Dataset"
method_name: "NADR-Dataset"
authors: [Steffen Jung, Jovita Lukasik, Margret Keuper]
year: 2023
venue: ICLR
tags: [NAS, robustness-dataset, NAS-Bench-201, adversarial-robustness]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=p8coElqiSDw
local_pdf: D:/PRO/essays/papers/Neural architecture design and robustness a dataset.pdf
local_code: D:/PRO/essays/code_depots/Neural architecture design and robustness a dataset
created: 2026-03-17
---

# 论文笔记: NADR-Dataset

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Neural Architecture Design and Robustness: A Dataset |
| 会议 | ICLR 2023 |
| OpenReview | https://openreview.net/forum?id=p8coElqiSDw |
| 项目页 | http://robustness.vision/ |
| 代码 | https://github.com/steffen-jung/robustness-dataset |
| 数据下载 | http://data.robustness.vision/ |
| 本地 PDF | `D:/PRO/essays/papers/Neural architecture design and robustness a dataset.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Neural architecture design and robustness a dataset` |

## 一句话总结
> 这篇工作把 [[NAS-Bench-201]] 的 6,466 个非同构架构在 [[Adversarial Robustness]] 与 [[Common Corruptions]] 上做了全量评测，形成可复用的鲁棒性数据集，并展示了其在代理指标评估和鲁棒 NAS 中的用途。

## 核心贡献
1. 首次对完整 NAS 搜索空间（NAS-Bench-201）做鲁棒性全量评估，覆盖对抗攻击与常见腐蚀。
2. 公开结构化数据与配套代码接口，使鲁棒性研究可以像 tabular NAS 一样可复现、可比较。
3. 通过三类 use case 证明：架构拓扑对鲁棒性高度敏感，即使参数量相同也可出现接近 2x 的鲁棒差距。

## 问题背景
### 要解决的问题
- 以往 NAS 常关注 clean accuracy，而鲁棒评估（尤其对抗攻击）成本很高，难以系统比较架构设计与鲁棒性的关系。

### 现有工作的局限
- 多数工作只评估少量架构或“野生”架构集合，缺少在同一完整搜索空间上的可比性基线。
- 缺少类似 NAS-Bench 的“鲁棒性版”结构化数据集，不利于快速验证新想法。

### 本文动机
- 复用 NAS-Bench-201 的统一训练协议，增加攻击与腐蚀维度，形成“架构设计-鲁棒性”研究基础设施。

## 数据集与方法详解
### 1) 搜索空间与评估规模（Sec. 3.1, Appx A.1）
- 搜索空间: [[NAS-Bench-201]]，cell 有 4 个节点、6 条边，操作集合为 `{1x1 conv, 3x3 conv, 3x3 avg pool, skip, zero}`。
- 架构规模: 总计 15,625 个编码架构，其中 6,466 个为非同构架构。
- 数据集: CIFAR-10, CIFAR-100, ImageNet16-120。
- 总评测模型数: `3 x 6,466 = 19,398` 个预训练模型。

### 2) 对抗鲁棒性评测（Sec. 3.2）
- 攻击类型:
  - [[FGSM]]（Eq. 1）
  - [[PGD Attack]]（Eq. 2）
  - [[AutoAttack]] 的 APGD-CE 与 [[Square Attack]]（Eq. 3）
- 评测记录:
  - `accuracy`
  - `confidence`
  - `confusion matrix`
- 每个攻击在多个 epsilon 下评测（详见 Table 2）。

### 3) 腐蚀鲁棒性评测（Sec. 3.3）
- 使用 CIFAR-10-C / CIFAR-100-C 的 15 种腐蚀、5 个 severity，共 75 个腐蚀设置。
- 与攻击评测一致，记录 accuracy / confidence / confusion matrix。

### 4) 数据集生成算法（Appx Alg. 1, Fig. 9）
- 对每个架构 `a`、每个数据集 `d`、每种攻击/腐蚀 `c`：
  1. 加载对应预训练权重；
  2. 构造被攻击/被腐蚀数据；
  3. 执行评估得到三类结果；
  4. 写入 `R[d][c]` 的对应字段。

## 关键公式
### Eq. (1): FGSM 扰动
\[
\tilde{x} = x + \epsilon \cdot sign(\nabla_x J(\theta, x, y))
\]
- 含义: 单步沿损失梯度符号方向扰动输入，预算为 `epsilon`。

### Eq. (2): PGD 迭代攻击
\[
\tilde{x}_{n+1} = clip_{\epsilon, x}\left(\tilde{x}_n - \alpha \cdot sign(\nabla_{\tilde{x}_n} J(\theta, \tilde{x}_n, \tilde{y}))\right)
\]
- 含义: 在 `L_inf` 约束球内多步迭代，更强但更耗时。

### Eq. (3): Square Attack 目标
\[
\min_{\tilde{x}} \left(f_{y,\theta}(\tilde{x}) - \max_{k \ne y} f_{k,\theta}(\tilde{x})\right),\quad \text{s.t. } \lVert \tilde{x} - x \rVert_\infty \le \epsilon
\]
- 含义: 无梯度黑盒攻击，通过随机搜索压低真类 margin。

### Eq. (4): Jacobian 与稳定性关系
\[
f_{\theta,c}(x+\delta)-f_{\theta,c}(x)\approx \sum_d J_{\theta,c;d}(x)\,\delta_d
\]
- 含义: 输出变化与 Jacobian 分量相关，支撑用 Jacobian 范数作为鲁棒代理。

## 关键图表与结果
### Figure 1 (架构定义)
- 给出 NAS-Bench-201 的 macro/cell 结构和 6 条边的操作语义，是后续拓扑分析的基础。

### Figure 2 / Figure 3 (攻击结果与排序相关性)
- 现象 1: 各攻击下准确率分布跨度大，说明架构对鲁棒性影响显著。
- 现象 2: clean 排名与 robust 排名相关性并不稳定，跨攻击更明显不一致（[[Kendall's Tau]]）。

### Figure 4 / Figure 5 (腐蚀结果与相关性)
- 与攻击结论一致：不同架构对不同腐蚀敏感性差异大，clean 排名难直接代表 corruption 排名。

### Figure 6 (训练无关代理评估)
- [[Jacobian Norm Bound]] 与 [[Hessian Spectrum]] 在较小 epsilon 场景有一定相关性；
- epsilon 变大后相关性下降，提示代理可用于粗筛但不能等价替代鲁棒评测。

### Table 1 (NAS on robustness, CIFAR-10)
- Clean 目标下，方法可接近 clean 最优（如 Local Search clean 94.65），但鲁棒项较弱。
- 改为 FGSM(epsilon=1) 目标后，FGSM/PGD/APGD 等鲁棒指标普遍提升。
- 例: Local Search 在 FGSM 目标下达到 FGSM 69.10，接近最优 69.24。

### Figure 7 (同参数量拓扑分析)
- 在“2 个 3x3 conv、无 1x1 conv”的同参数量子集里，平均对抗鲁棒可从约 0.21 到 0.40。
- 论文观察到卷积堆叠路径更常出现在高鲁棒拓扑中，说明拓扑细节本身就能显著影响鲁棒性。

### Table 2 / 3 / 4 (附录: 可复现细节)
- Table 2: 各攻击超参（例如 PGD 40 iter, APGD 100 iter, Square 5000 iter）。
- Table 3: 数据键命名（clean / 各攻击 / 各腐蚀）。
- Table 4: 文件组织规则（`{key}_{measurement}.json`）。

## 与本地代码实现对照
- 仓库核心是 `robustness_dataset.py` 的读取与查询接口，以及 `dataset.ipynb` 示例。
- `RobustnessDataset.query()` 支持按 `data/key/measure` 组合查询，`get_uid()` 处理 [[Isomorphic Architectures]] 映射。
- 代码层面的攻击 key 使用了 `@Linf` 后缀（如 `pgd@Linf`），与论文正文记法一致但更工程化。
- 注意: 仓库主要提供数据访问与可视化辅助，不包含论文中的完整大规模采集脚本集群流水线。

## 批判性思考
### 优点
1. 数据覆盖系统化且规模足够大，极大降低鲁棒 NAS 研究门槛。
2. 同时给出攻击与腐蚀两类鲁棒性，便于研究“鲁棒性是否可迁移”。
3. 提供了从代理指标、NAS 搜索到拓扑分析的完整示例闭环。

### 局限
1. 评测空间限定在 NAS-Bench-201，跨搜索空间泛化仍需验证。
2. 主要聚焦 `L_inf` 攻击与 CIFAR 系数据，真实世界分布漂移仍不足。
3. 代码仓库偏向“数据接口”，复现实验采集过程仍需较强工程能力。

### 对你当前研究的启发
1. 可把该数据集作为训练无关 proxy 的标准离线评测平台，先验证相关性再上完整训练。
2. 适合做“拓扑微扰 vs 鲁棒变化”分析，减少训练噪声干扰。
3. 可直接作为 robust proxy 组合学习（例如集成多 proxy）训练目标数据源。

## 关联概念
- [[Neural Architecture Search]]
- [[Robust Neural Architecture Search]]
- [[NAS-Bench-201]]
- [[Adversarial Robustness]]
- [[Common Corruptions]]
- [[FGSM]]
- [[PGD Attack]]
- [[AutoAttack]]
- [[Square Attack]]
- [[Jacobian Norm Bound]]
- [[Hessian Spectrum]]
- [[Kendall's Tau]]
- [[Isomorphic Architectures]]

