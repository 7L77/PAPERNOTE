---
title: "Wsr-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[Wsr-NAS]]"
source_paper: "Neural Architecture Search for Wide Spectrum Adversarial Robustness"
source_note: "[[Wsr-NAS]]"
authors: [Zhi Cheng, Yanxi Li, Minjing Dong, Xiu Su, Shan You, Chang Xu]
year: 2023
venue: AAAI
tags: [nas-method, zh, robust-nas, adversarial-robustness]
created: 2026-03-17
updated: 2026-03-17
---

# Wsr-NAS 中文条目

## 一句话总结

> Wsr-NAS 把“多攻击强度鲁棒性”显式放进可微 NAS 搜索目标，并用 AN-Estimator 与 EWSS 降低多强度搜索的计算成本。

## 来源

- 论文: [Neural Architecture Search for Wide Spectrum Adversarial Robustness](https://doi.org/10.1609/aaai.v37i1.25118)
- HTML: https://doi.org/10.1609/aaai.v37i1.25118
- 代码: https://github.com/zhicheng2T0/Wsr-NAS
- 英文方法笔记: [[Wsr-NAS]]
- 论文笔记: [[Wsr-NAS]]

## 适用场景

- 问题类型: 需要在多个扰动强度上都保持鲁棒的图像分类 NAS。
- 前提假设: 存在可微 one-shot 超网，且可用验证损失估计器近似架构更新方向。
- 数据形态: 监督学习（文中搜索用 CIFAR-10，泛化到 ImageNet 复训评估）。
- 规模与约束: 直接在大规模多强度对抗验证集反传太贵时尤其适合。
- 适用原因: 将“多强度鲁棒信号获取”和“架构梯度更新”解耦并分别轻量化。

## 不适用或高风险场景

- 只关心单一强度下的最优鲁棒性。
- 需要可认证鲁棒性（certified robustness）而非经验鲁棒性。
- 搜索空间不是可微 one-shot 形式。

## 输入、输出与目标

- 输入: 超网架构参数 \(A\)、训练/验证划分、PGD 设置、目标强度集合。
- 输出: 搜索得到的 WsrNet 架构及其复训模型。
- 优化目标: 最小化 clean 损失与多强度对抗损失的加权组合。
- 核心假设: VLE 的损失预测足够可靠，AN-Estimator 生成噪声足够保真。

## 方法拆解

### 阶段 1: Warm-up 与记忆构建

- 先对采样架构做 warm-up。
- 构建用于 AN-Estimator 的 \(M_a\) 与用于 VLE 的 \(M_v\)。
- Source: Sec. Search Procedure, Alg.1 lines 1-18

### 阶段 2: 多强度对抗样本信号构建

- 用真实 PGD 生成少量基础强度噪声（\(N_1\)）。
- 用 AN-Estimator 生成其余目标强度噪声（\(N_2\)）。
- Source: Sec. Adversarial Noise Estimator, Eq. (3), Eq. (5), Eq. (7), Table 5

### 阶段 3: EWSS 预测损失向量

- VLE 根据架构编码预测 clean + 多强度验证损失。
- 在 \(M_v\) 上用 MSE 训练。
- Source: Sec. Efficient Wide Spectrum Searcher, Eq. (8), Eq. (9)

### 阶段 4: 鲁棒搜索目标更新架构

- 用 Eq.(10) 聚合 clean 与多强度损失，更新 \(A\)。
- 通过 \(\alpha,\beta,\beta_i\) 控制 clean 与不同强度鲁棒性的权衡。
- Source: Eq. (10), Alg.1 line 24

## 伪代码
```text
Algorithm: Wsr-NAS
Input: 超网参数 A, 训练集 Dt, 验证集 Dv, 强度集合 {eps_i}
Output: 搜索后的鲁棒架构

1. 对 warm-up 架构群逐个训练 1 epoch。
   Source: Alg.1 lines 2-5
2. 构建 AE memory M_a 与验证 memory M_v。
   Source: Alg.1 lines 6-17
3. 训练 AN-Estimator，用少量已知强度噪声预测其他强度噪声。
   Source: Alg.1 line 10, Eq.(5), Sec. AN-Estimator
4. 训练 VLE，预测 clean 与多强度验证损失。
   Source: Alg.1 line 18, Eq.(8)-(9)
5. 每轮搜索：
   5.1 采样架构并在 Dt 上做对抗训练。
       Source: Alg.1 lines 20-21
   5.2 更新 M_a、AN-Estimator 与 M_v（真实 PGD + 估计噪声）。
       Source: Alg.1 line 22; Inference from source code
   5.3 更新 VLE，并用 robust objective 更新 A。
       Source: Alg.1 lines 23-24, Eq.(10)
6. 从 A 解码最终 cell 架构并复训评估。
   Source: Sec. Preliminaries; Inference from source
```

## 训练流程

1. CIFAR-10 划分 \(D_t\)/\(D_v\)。
2. Gumbel 采样下 warm-up 超网。
3. 构建并更新 memory。
4. 训练 AN-Estimator 与 VLE。
5. 交替执行模型训练、预测器训练与架构更新。

Sources:

- Alg.1; Sec. Search Procedure; `search/robust_train_search_official.py`.

## 推理流程

1. 解码搜索后架构得到 WsrNet。
2. 用 PGD/TRADES/Fast-AT 等进行标准复训。
3. 在 clean 与多强度攻击下评估。

Sources:

- Sec. Experiments; Table 1/2/4; README scripts.

## 复杂度与效率

- 时间复杂度: 论文未给闭式公式。
- 空间复杂度: 论文未给闭式公式。
- 运行特征: 文中报告多强度搜索约 3.6-4.0 GPU days。
- 扩展性说明: AN-Estimator 显著降低“每增加一个强度”的额外成本。

## 实现备注

- 官方搜索主脚本: `search/robust_train_search_official.py`。
- 代码中 `AN_estimator_plus` 用于更高强度覆盖的 Plus 设定。
- 代码的目标权重先设 `[1,[1,2,3,5,7,10]]`，再按 `[0.8,0.2]` 归一化。
- VLE 在代码中是多头 LSTM predictor（clean + 6 个 epsilon 头）。
- 论文与代码总体一致，但具体强度配置和工程细节以代码为准。

## 与相关方法关系

- 对比 [[RobNet]]: Wsr-NAS 优化目标从单强度扩展到宽强度谱。
- 对比 [[AdvRush]]: Wsr-NAS 增加 AN-Estimator + VLE 以提升多强度搜索效率。
- 主要优势: 平均鲁棒性更稳，且搜索成本可控。
- 主要代价: 系统组件更多，复现门槛高于普通可微 NAS。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 5, Table 6
- 关键公式: Eq. (1), Eq. (3), Eq. (5), Eq. (7), Eq. (8), Eq. (9), Eq. (10)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: Not explicitly provided in paper metadata
- HTML: https://doi.org/10.1609/aaai.v37i1.25118
- 代码: https://github.com/zhicheng2T0/Wsr-NAS
- 本地实现: D:/PRO/essays/code_depots/Neural architecture search for wide spectrum adversarial robustness

