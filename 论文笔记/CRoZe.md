---
title: "Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations"
method_name: "CRoZe"
authors: [Hyeonjeong Ha, Minseon Kim, Sung Ju Hwang]
year: 2023
venue: NeurIPS
tags: [NAS, robust-nas, zero-cost-proxy, training-free, perturbation-robustness]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2306.05031
local_pdf: D:/PRO/essays/papers/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations.pdf
local_code: D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations
created: 2026-03-15
---

# 论文笔记：CRoZe

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations |
| arXiv | https://arxiv.org/abs/2306.05031 |
| HTML | https://arxiv.org/html/2306.05031 |
| 代码 | https://github.com/HyeonjeongHa/CRoZe |
| 本地 PDF | `D:/PRO/essays/papers/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations` |
| 代码版本 | `3e89e3d` |

## 一句话总结

> CRoZe 提出一个面向 [[Robust Neural Architecture Search]] 的 [[Zero-Cost Proxy]]：在随机初始化下，用 clean/perturbed 两个 surrogate 网络的一步更新后 [[Feature Consistency]]、[[Parameter Consistency]]、[[Gradient Alignment]] 乘积打分，快速找到对多类扰动都更稳健的架构。

## 核心贡献

1. 提出 CRoZe：无需 adversarial supernet 训练，仅用单步近似评估鲁棒潜力。
2. 代理同时建模特征、参数、梯度三种一致性，避免只对单一攻击过拟合。
3. 在 [[NAS-Bench-201]] 与 DARTS 上，兼顾鲁棒性与搜索效率；在 DARTS/CIFAR-10 上相较 robust NAS 显著降成本。
4. 进一步分析显示：单步 proxy 与 fully-trained 排名高度相关（Spearman 最高到 0.970/0.995）。

## 问题背景

### 目标问题

传统 [[Neural Architecture Search]] 和不少 zero-shot NAS 主要优化 clean accuracy，忽略部署时的真实扰动（对抗攻击 + [[Common Corruptions]]）。

### 现有方法局限

- robust NAS（如 RobNet/AdvRush）通常依赖 adversarial training 的 one-shot supernet，开销大。
- clean zero-shot 代理（SynFlow/NASWOT 等）更偏 clean 可训练性，不保证跨扰动泛化。

### 论文动机

作者希望用 training-free 的方式逼近“最终鲁棒性排序”，并且不绑死单一攻击类型。

## 方法详解

### 1) 鲁棒性的核心判据（Sec. 3.1）

论文给出核心直觉：鲁棒模型应在 clean 与 perturbed 输入上保持表征一致：

\[
\|e_\phi(x)-e_\phi(x')\| \le \epsilon
\]

这对应 Eq. (2)。

### 2) 双 surrogate 网络（Sec. 3.2）

- clean 网络：`f_\theta`
- robust 网络：`f_{\theta^r}`，通过层级权重扰动构造（Eq. (3)）
- 在 `f_{\theta^r}` 上再做 FGSM 生成 `x'`（Eq. (4)）

这一步把“需要完整训练才能看出的鲁棒趋势”，压缩到单步近似。

### 3) 三种一致性组件（Sec. 3.3）

- **Feature consistency** `Z_m`（Eq. (5)）：层级特征余弦相似度。
- **Parameter consistency** `P_m`（Eq. (8)）：clean/robust 一步更新参数相似度。
- **Gradient consistency** `G_m`（Eq. (9)）：clean/robust 梯度方向绝对余弦相似度。

其中梯度定义与单步更新见 Eq. (6)(7)。

### 4) 最终代理（Eq. (10)）

\[
\text{CRoZe} = \sum_{m=1}^{M} Z_m \cdot P_m \cdot G_m
\]

分数越高，说明架构在 clean/perturbed 任务之间越“对齐”，越可能具备跨扰动鲁棒性。

## 关键图表

### Figure 1

- 左图：Clean NAS / Robust NAS / CRoZe 的任务目标差异。
- 右图：CRoZe 通过“单步更新 + 一致性乘积”打分。

### Figure 2

- 在 DARTS/CIFAR-10 上，CRoZe 在时间-鲁棒性能平衡上明显优于 robust NAS。

### Figure 3

- warmup + move 的采样策略能更快定位高 proxy 架构（样本数 < 50 也能找到强鲁棒候选）。

### Figure 4

- CRoZe 选出的架构在 18 类扰动上的 feature variance 最小，显示更强跨扰动稳定性。

### Figure 5

- 单步 proxy 与 fully-trained proxy 的 Spearman 相关高（0.970），10-step 更高（0.995）。

### Figure 6

- proxy top-5 架构在 clean/perturbed 下特征更一致，bottom-5 明显更不稳定。

### Table 1（NAS-Bench-201, adv-trained, CIFAR-10）

- CRoZe 在多攻击平均 Spearman 最高（Avg 0.465），高于 SynFlow (0.399)、GradNorm (0.400)。

### Table 2（NAS-Bench-201, standard-trained）

- CRoZe 在 CIFAR-10 / CIFAR-100 / ImageNet16-120 的 clean + FGSM + corruption 相关性整体领先。

### Table 3（DARTS end-to-end, standard training）

- CIFAR-10: CRoZe 的 FGSM 20.51、HRS 33.07，搜索时间 17,066 GPU sec。
- 对比 AdvRush：FGSM 提升约 5.57%，且搜索成本约降 14.7x。

### Table 4（adversarial training, CIFAR-10）

- CRoZe 在多攻击平均鲁棒性最高（Avg 55.94）。

### Table 5（组件消融）

- 三项一致性都保留时总体最好；只看单一项会明显丢失泛化能力。

### Table 6（proxy top/bottom 架构）

- top-5 与 bottom-5 在 clean 和 robust 指标上差距显著，支持 proxy 排序有效性。

## 实验设置（关键）

- 搜索空间：[[NAS-Bench-201]] + DARTS。
- 数据集：CIFAR-10/100, ImageNet16-120。
- 扰动：FGSM, PGD, CW, DeepFool, SPSA, LGV, AutoAttack + common corruptions。
- 训练：standard 200 epochs；adversarial training 用 PGD（`epsilon=8/255, step=2/255, steps=7`）。

## 与代码实现的对照

- `zero_cost_methods/pruners/measures/croze.py`
  - 构造 `advnet = copy.deepcopy(net)`；
  - `adj_weights(...)` 做参数扰动；
  - `fgsm_attack(...)` 生成 perturbed input；
  - 计算 `feat_sim * w_sim * grad_sim` 的层级指标并聚合。
- `zero_cost_methods/pruners/p_utils.py`
  - `adj_weights` 通过一次优化步构造权重扰动；
  - `get_layer_metric_array_adv_feats` 按层对齐 clean/robust 特征并计算代理项。
- `main.py`
  - `sample_arch` 实现 `random/mutate/warmup` 采样并用 proxy 选最好架构。
- `sampling.py`
  - DARTS 侧做架构随机/变异采样；
  - 与论文的 warmup+move 采样策略对应。

## 批判性思考

### 优点

1. 训练前即可评估鲁棒潜力，极大降低 robust NAS 成本。
2. 多一致性联合打分，比单 proxy 更不容易“偏科”。
3. 论文的分析实验（variance、predictiveness、top-vs-bottom）比较扎实。

### 局限

1. 代理仍依赖“单步近似”，对复杂任务/大模型是否稳定还需更多验证。
2. 指标是乘积形式，某一项异常可能放大波动。
3. 主要实验集中在 CNN/NAS-Bench-201 + DARTS，跨模态泛化未验证。

### 可复现性评估

- [x] 论文公开
- [x] 官方代码公开
- [x] 本地代码已归档
- [x] 关键指标和搜索脚本可定位

## 关联笔记

### 基于
- [[Zero-Cost Proxy]]
- [[Robust Neural Architecture Search]]
- [[Neural Architecture Search]]

### 相关概念
- [[Feature Consistency]]
- [[Parameter Consistency]]
- [[Gradient Alignment]]
- [[Common Corruptions]]
- [[Harmonic Robustness Score]]
- [[Spearman's Rank Correlation]]

## 速查卡片

> [!summary] CRoZe (NeurIPS 2023)
> - 核心：single-step robust proxy = feature × parameter × gradient consistency
> - 亮点：跨攻击泛化 + 大幅降搜索成本
> - 结果：DARTS/CIFAR-10 上相对 robust NAS 有明显成本优势且鲁棒性更好
> - 代码：https://github.com/HyeonjeongHa/CRoZe
