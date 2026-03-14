---
title: "SWAP-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[SWAP-NAS]]"
source_paper: "SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS"
source_note: "[[SWAP-NAS]]"
authors: [Yameng Peng, Andy Song, Haytham M. Fayek, Vic Ciesielski, Xiaojun Chang]
year: 2024
venue: ICLR
tags: [nas-method, zh, nas, training-free, zero-cost-proxy, swap]
created: 2026-03-14
updated: 2026-03-14
---

# SWAP-NAS 中文条目

## 一句话总结
> SWAP-NAS 用“样本维度激活模式去重计数”做 training-free 评分，并把正则化后的分数接入进化搜索，在极低搜索成本下得到有竞争力的 NAS 结果。

## 来源
- 论文: [SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS](https://arxiv.org/abs/2403.04161)
- HTML: https://arxiv.org/html/2403.04161
- 代码: https://github.com/pym1024/SWAP
- 英文方法笔记: [[SWAP-NAS]]
- 论文笔记: [[SWAP-NAS]]

## 适用场景
- 问题类型: training-free 架构排序与快速进化 NAS。
- 前提假设: 候选网络可在随机初始化下稳定提取 ReLU 中间激活。
- 数据形态: 主要是图像任务的 NAS 搜索空间。
- 规模与约束: 候选规模大、无法逐个完整训练的场景。
- 适用原因: SWAP 分数计算便宜且区分度高。

## 不适用或高风险场景
- 目标是严格硬件时延而不是 proxy 相关性。
- 架构不是 ReLU 主导，激活模式信号弱。
- 需要仓库直接提供完整 SWAP-NAS 搜索脚本时。

## 输入、输出与目标
- 输入: 候选架构、一个 mini-batch、可选正则参数 \(\mu,\sigma\)、进化搜索超参。
- 输出: SWAP/regularized SWAP 分数与最终选中架构。
- 优化目标: 以极小计算成本最大化“proxy 排序 vs 真实性能”的一致性。
- 核心假设: 样本维激活模式的基数能反映网络表达能力与潜在性能。

## 方法拆解

### 阶段 1: 构造样本维激活模式
- 在 ReLU 上注册 forward hook，收集中间激活。
- 对激活取 sign 做二值化，形成样本维模式向量。
- Source: Sec. 3.2 / Def. 3.2；代码 `src/metrics/swap.py`

### 阶段 2: 计算 SWAP 分数
- 将激活矩阵从 `(samples, neurons)` 转成 `(neurons, samples)`。
- 对行做 unique 计数，得到 \(\Psi\)。
- Source: Sec. 3.2 / Def. 3.3 / Eq. (4)

### 阶段 3: 正则化与尺寸控制
- 使用 \(f(\Theta)=\exp(-(\Theta-\mu)^2/\sigma)\)。
- 得到 \(\Psi'=\Psi\cdot f(\Theta)\) 引导目标参数量区间。
- Source: Sec. 3.3 / Def. 3.4-3.5 / Eq. (5)-(6)

### 阶段 4: 接入进化搜索
- 初始化种群、抽样、交叉、变异、保优汰劣。
- Source: Algorithm 1（附录 C）

## 伪代码
```text
Algorithm: SWAP-NAS
Input: 种群大小 P, 迭代轮数 C, 抽样规模 S, 变异次数 M, 正则参数 (mu, sigma)
Output: 最优架构 a*

1. 随机初始化种群并计算每个个体 SWAP/regularized SWAP 分数。
   Source: Algorithm 1 Step 1-6
2. 对每轮 c:
   2.1 从种群随机抽样 S 个候选。
       Source: Algorithm 1 Step 8
   2.2 选择 parent（best 或 best+second-best 交叉后的更优体）。
       Source: Algorithm 1 Step 9
   2.3 对 parent 进行多次变异产生子代并打分。
       Source: Algorithm 1 Step 10-13
   2.4 把最优子代加入种群并移除最差个体。
       Source: Algorithm 1 Step 14-15
3. 返回种群中得分最优架构。
   Source: Inference from source
```

## 训练流程
1. 从目标数据集取 mini-batch 输入。
2. 候选架构随机初始化后计算 SWAP 分数（可多次重采样平均）。
3. 在预算内执行进化搜索。
4. 对最终选中架构做标准训练并报告测试指标。

Sources:
- Sec. 4.1, Sec. 4.2, Algorithm 1
- `correlation.py`（评分流程实现）

## 推理流程
1. 固定搜索得到的架构。
2. 按目标任务配置训练/微调。
3. 常规前向推理评测。

Sources:
- Sec. 4.2, Table 1/2
- Source: Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给封闭式公式。
- 空间复杂度: 论文未给封闭式公式。
- 运行特征: 报告搜索成本 CIFAR-10 约 0.004 GPU days，ImageNet 约 0.006 GPU days。
- 扩展性: 正则化在 cell-based 空间上可提升相关性并提供控尺寸能力。

## 实现备注
- 核心评分器: `src/metrics/swap.py`
- 相关性实验脚本: `correlation.py`
- 关键算子: ReLU hook + sign 二值化 + `torch.unique` 去重计数。
- 正则实现与 Eq. (5) 一致: `exp(-((params-mu)^2)/sigma)`。
- 代码与论文差异: 仓库主要发布评分器和相关性复现，未完整打包论文附录中的搜索流程脚本。

## 与相关方法关系
- 相比 NWOT/TE-NAS/ZiCo: 论文报告 SWAP 在多搜索空间上相关性更强或更稳。
- 主要优势: 打分代价低、排序信号强。
- 主要代价: 对 proxy 有效性与 \(\mu,\sigma\) 选择敏感。

## 证据与可溯源性
- 关键图: Fig. 3, Fig. 4, Fig. 5
- 关键表: Table 1, Table 2, Table 3
- 关键公式: Eq. (3), Eq. (4), Eq. (5), Eq. (6)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2403.04161
- HTML: https://arxiv.org/html/2403.04161
- 代码: https://github.com/pym1024/SWAP
- 本地实现: D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS

