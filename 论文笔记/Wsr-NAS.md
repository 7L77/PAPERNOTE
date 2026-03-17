---
title: "Neural Architecture Search for Wide Spectrum Adversarial Robustness"
method_name: "Wsr-NAS"
authors: [Zhi Cheng, Yanxi Li, Minjing Dong, Xiu Su, Shan You, Chang Xu]
year: 2023
venue: AAAI
tags: [NAS, adversarial-robustness, robust-nas, one-shot-nas]
zotero_collection: ""
image_source: online
arxiv_html: https://doi.org/10.1609/aaai.v37i1.25118
local_pdf: D:/PRO/essays/papers/Neural architecture search for wide spectrum adversarial robustness.pdf
local_code: D:/PRO/essays/code_depots/Neural architecture search for wide spectrum adversarial robustness
created: 2026-03-17
---

# 论文笔记: Wsr-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Neural Architecture Search for Wide Spectrum Adversarial Robustness |
| DOI | https://doi.org/10.1609/aaai.v37i1.25118 |
| 代码 | https://github.com/zhicheng2T0/Wsr-NAS |
| 本地 PDF | `D:/PRO/essays/papers/Neural architecture search for wide spectrum adversarial robustness.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Neural architecture search for wide spectrum adversarial robustness` |

## 一句话总结
> Wsr-NAS 通过把多强度对抗鲁棒性直接放进 NAS 搜索信号，并用 [[Adversarial Noise Estimator]] + [[Validation Loss Estimator]] 降低计算开销，得到在更宽攻击强度范围内更稳的架构。

## 核心贡献
1. 提出 [[Wide Spectrum Adversarial Robustness]] 目标，不再只对单一或少量固定攻击强度优化。
2. 提出轻量 [[Adversarial Noise Estimator]]（AN-Estimator），用少量真实 PGD 噪声生成更多目标强度噪声。
3. 提出 EWSS（含 [[Validation Loss Estimator]] 与 [[Robust Search Objective]]），避免每次都在大规模对抗验证集上反传架构梯度。
4. 在 CIFAR-10 搜索、CIFAR-10 与 ImageNet 复训验证，报告相对朴素多强度搜索约 40% 搜索时间下降且整体鲁棒性提升。

## 问题背景
### 要解决的问题
- 现有 robust NAS 往往在单一或很少几个噪声强度上优化，导致面对更强/未见强度攻击时鲁棒性掉得快。

### 现有方法局限
- 直接扩大强度集合会让搜索成本暴涨：对抗样本生成更贵，验证阶段架构更新也更贵。

### 本文动机
- 用更丰富的鲁棒搜索信号找架构，但把新增计算量压住。

## 方法详解
### 1) 超网与可微搜索骨架
- 基于 [[One-shot NAS]] 与 [[Super-network]]：单元内边上操作由可学习架构参数控制（Eq.2）。

### 2) AN-Estimator（噪声生成降本）
- 目标：给定输入图像和少数已生成强度噪声，预测其他目标强度噪声（Eq.3）。
- 训练：最小化预测噪声与目标噪声的 MSE（Eq.5）。
- 设计对比：WA-ANE、A-ANE、E-ANE，文中实证 A-ANE 最优（Table 5）。

### 3) EWSS（架构更新降本）
- 用 VLE 预测某架构在 clean 与多强度对抗集上的验证损失向量（Eq.8, Eq.9）。
- 通过 [[Robust Search Objective]] 聚合 clean 与多强度损失（Eq.10），再更新架构权重。

### 4) 总体流程
- 先 warm-up 超网、AN-Estimator、VLE，再进入搜索循环（Algorithm 1）。
- 搜索中交替进行：模型训练、AE memory 更新、AN-Estimator 更新、VLE 更新、架构更新。

## 关键公式
### Eq.(1) 对抗攻击目标
$$
\delta = \arg\max_{\|\delta\|<\epsilon} L(\mathcal{N}, x+\delta, y)
$$
含义：在扰动范数约束下最大化损失，构造最坏样本。

### Eq.(3) AN-Estimator
$$
\hat{\delta}_{\hat{\epsilon}}=\Phi(x,\delta_{\epsilon_1},\ldots,\delta_{\epsilon_{N_1}},\hat{\epsilon})
$$
含义：由输入与少量已知强度噪声估计目标强度噪声。

### Eq.(8) VLE
$$
\hat{L}=\{\hat{L}_{natural},\hat{L}_{\epsilon_1},\ldots,\hat{L}_{\epsilon_{N_1+N_2}}\}=\Psi(H)
$$
含义：根据架构参数 \(H\) 直接预测多头验证损失。

### Eq.(10) Robust Search Objective
$$
\min_A \; \alpha \hat{L}_{natural} + \beta \sum_i \beta_i \hat{L}_{\epsilon_i}
$$
约束：\(\sum_i\beta_i=1,\alpha+\beta=1,\alpha,\beta,\beta_i>0\)。

## 关键图表
### Figure 1: 方法概览（代码仓库配图）
![Wsr-NAS overview](https://raw.githubusercontent.com/zhicheng2T0/Wsr-NAS/master/demo2.PNG)

### Figure 2: AN-Estimator 结构（代码仓库配图）
![AN-Estimator](https://raw.githubusercontent.com/zhicheng2T0/Wsr-NAS/master/ane.PNG)

### Figure 3: EWSS 结构（代码仓库配图）
![EWSS](https://raw.githubusercontent.com/zhicheng2T0/Wsr-NAS/master/ewss.PNG)

### Table 1/2 结论（论文）
- 在 TRADES-1 与 PGD-7 下，WsrNet-Basic/Plus 在保持可比 clean accuracy 时，平均鲁棒准确率优于多组 robust NAS 基线。
- WsrNet-Robust 在与 RobNet-L 接近 clean accuracy 下，鲁棒性更高。

### Table 3/6 结论（论文）
- 相比朴素多强度搜索，AN-Estimator + EWSS 显著降低搜索耗时。
- 文中报告单次循环从约 1953s 降至约 1251s（约 36%）。

## 实验设置与结果
### 数据与流程
- 搜索数据：CIFAR-10（train 拆分为 Dt 与 Dv）。
- 复训评估：CIFAR-10 + ImageNet。
- 攻击/训练：FGSM、PGD、TRADES；主文多用 \(L_{\infty}\) 约束。

### 关键设置
- WsrNet-Basic: \(N_1,N_2=(3,3)\)。
- WsrNet-Plus: \(N_1,N_2=(3,8)\)。
- 默认 clean/robust 权重平衡：\(\alpha=0.8,\beta=0.2\)（文中描述）。

### 主要发现
1. 搜索时覆盖更多强度，能带来更高平均鲁棒性。
2. 结构泛化到不同攻击与不同训练范式（PGD/TRADES）和数据集（ImageNet）。
3. 代价是低强度点（如 \(\epsilon=0.03\)）有时不及最强单点 SOTA（文中 limitation）。

## 论文-代码对照
- 官方实现入口：`search/robust_train_search_official.py`。
- 代码中 `search_objective_weights` 先设为 `[1,[1,2,3,5,7,10]]` 再按 `[0.8,0.2]` 归一化，与 Eq.(10) 的 clean/robust 分配一致。
- 代码里 AN-Estimator 有 `AN_estimator` 与 `AN_estimator_plus` 两版；后者用于 Plus 配置（README 说明）。
- 代码中 VLE 对应 predictor 多头输出（clean + 6 个强度头），与论文“多强度验证损失估计”思路一致。

## 批判性思考
### 优点
1. 目标定义清晰：明确追求“宽谱鲁棒”而非单点鲁棒。
2. 工程策略有效：AN-Estimator 与 EWSS 互补降本，确实让多强度搜索可用。
3. 报告了跨训练范式、跨数据集、跨攻击泛化。

### 局限
1. 搜索仍依赖 CIFAR-10，向更大搜索空间迁移成本与稳定性仍待验证。
2. 在最小强度点的鲁棒性有时不如某些单点优化模型。
3. 论文给出思路充分，但不少工程细节更依赖代码复核才能完全复现。

## 关联笔记
- 方法笔记: [[Wsr-NAS]]
- 相关方法: [[RACL]], [[AdvRush]], [[RobNet]]
- 核心概念: [[Wide Spectrum Adversarial Robustness]], [[Adversarial Noise Estimator]], [[Validation Loss Estimator]], [[Robust Search Objective]]

