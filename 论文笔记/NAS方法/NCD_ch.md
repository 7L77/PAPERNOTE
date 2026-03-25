---
title: "NCD_ch"
type: method
language: zh-CN
source_method_note: "[[NCD]]"
source_paper: "Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS"
source_note: "[[NCD]]"
authors: [Haidong Kang, Lianbo Ma, Pengjun Chen, Guo Yu, Xingwei Wang, Min Huang]
year: 2025
venue: ICCV
tags: [nas-method, zh, training-free-nas, activation-based-proxy, ncd]
created: 2026-03-14
updated: 2026-03-14
---

# NCD 中文条目

## 一句话总结
> NCD 的核心是给 activation-based proxy 加两步“稳态修正”（SAM + NIR），把深层子空间里的负相关拉回正相关，从而让训练自由 NAS 的排序重新可靠。

## 来源
- 论文: [Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS](https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html)
- PDF: https://openaccess.thecvf.com/content/ICCV2025/papers/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.pdf
- 补充材料: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf
- 代码: 未检索到官方仓库（2026-03-14）
- 英文方法笔记: [[NCD]]
- 论文笔记: [[NCD]]

## 适用场景
- 问题类型: 依赖 activation-based proxy 的训练自由 NAS 排序/搜索。
- 前提假设: 随网络非线性与深度提升，原始 AZP 会出现相关性塌缩甚至负相关。
- 数据形态: 以图像 NAS 搜索空间为主（NB-201/101、DARTS 等）。
- 规模与约束: 无法对大量候选逐个完整训练时。
- 适用原因: 不替换搜索框架，只修正 proxy 评分路径，迁移成本低。

## 不适用或高风险场景
- 你的系统不使用 activation-based proxy。
- 无法在目标空间对 `alpha` 做小规模调优。
- 必须依赖现成官方代码一键复现。

## 输入、输出与目标
- 输入: 候选架构、mini-batch、基础 AZP（NWOT/SWAP 等）、掩码比例 `alpha`。
- 输出: NCD 修正后的 proxy 分数与候选排序。
- 优化目标: 在几乎不增加搜索成本的前提下，提高 proxy 与真实性能的一致性。
- 核心假设: 负相关的主因是激活求和导致的非线性过度累积。

## 方法拆解

### 阶段 1: 负相关诊断
- 在不同卷积层数子空间上统计 Spearman 相关，定位相关性翻转位置。
- Source: Sec. 3.1, Fig. 2, Table 1

### 阶段 2: SAM
- 对卷积中的激活值施加 Bernoulli 随机掩码：
  \( y=\sum(W\odot M\odot X),\ M\sim Bernoulli(1-\alpha)\)。
- 作用是降低一次卷积中参与求和的激活数量，缓解非线性堆叠。
- Source: Sec. 4.1, Eq. (4), Supp. Alg. 1 lines 4-6

### 阶段 3: NIR
- 通过 BN/LN 求和机制分析（Theorem 4.1/4.2）说明为何需要重标定非线性。
- 在 AZP 评估路径中使用 LN 风格归一化以稳定分数。
- Source: Sec. 4.2, Eq. (5)-(10), Theorem 4.1/4.2, Supp. Alg. 1 lines 7-8

### 阶段 4: 代理替换与搜索
- 将原始 NWOT/SWAP 替换为 NCD-NWOT/NCD-SWAP，再接入原搜索流程。
- Source: Sec. 5, Fig. 5, Table 2/3

## 伪代码
> 对应论文 Supplementary 中的 **Algorithm 1**（NCD 主流程），下面给出便于阅读的完整整理版。
```text
Algorithm 1 (Readable): Training-Free NAS with NCD
Input:
  task T, dataset D, search space A
  number of sampled architectures N
  batch size B
  AZP scorer f_azp (e.g., NWOT / SWAP)
  masking ratio alpha
Output:
  best architecture F_best

1. score_best <- -inf, F_best <- None
2. for j in {1, ..., N} do
3.   Sample a mini-batch X = {s_i}_{i=1..B} from dataset D for task T
4.   Sample an architecture F_j(.) from search space A
5.   Forward F_j on X to obtain activation representations C_j
6.   Apply SAM on convolution scoring path:
       C'_j = SAM(C_j, alpha), with mask M ~ Bernoulli(1 - alpha)
7.   Apply NIR (LN-style non-linear rescaling) on C'_j:
       C''_j = NIR(C'_j)
8.   Compute NCD score:
       score_j = f_azp(C''_j)
9.   if score_j > score_best then
10.      score_best <- score_j
11.      F_best <- F_j
12.   end if
13. end for
14. return F_best

Subroutine: SAM (per convolution receptive field)
  y = sum(W ⊙ M ⊙ X),  M(i,j,k) ~ Bernoulli(1 - alpha)

Notes:
  - Step 6 corresponds to Sec. 4.1, Eq. (4)
  - Step 7 corresponds to Sec. 4.2, Eq. (5)-(10), Theorem 4.1/4.2
  - Overall loop corresponds to Supplementary Algorithm 1
```

## 训练流程
1. 从目标搜索空间采样候选。
2. 用 NCD 修正后的 proxy 对候选打分。
3. 保留高分候选并进行外层搜索迭代。
4. 对最终结构做标准完整训练，报告最终精度。

Sources:
- Sec. 5, Table 2, Table 3, supplementary App. B

## 推理流程
1. 对新候选运行一次 NCD 评分。
2. 在候选池中完成排序。
3. 输出 Top 架构进入后续训练/部署。

Sources:
- Sec. 4, Sec. 5

## 复杂度与效率
- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: NB-101 报告 29.01 ms/arch（NCD-NWOT）；DARTS 设置最低到 0.002 GPU-days。
- 扩展性说明: 深子空间中提升更明显，因为基线方法更容易发生负相关。

## 实现备注
- `alpha` 是关键超参；论文在 NB-201 上报告 `alpha=0.95` 表现最好。
- SAM/NIR 各自有效，联合最好（Table 7）。
- NCD 是“proxy 评分修正层”，可包裹到已有 AZP 管线。
- 代码状态: 截至 2026-03-14，ICCV 页面与补充材料未给官方仓库链接。

## 与相关方法的关系
- 对比 [[Zero-Cost Proxy]]（NWOT/SWAP）：重点解决深层子空间相关性符号翻转问题。
- 对比 [[AZ-NAS]]：NCD 不是多代理融合，而是单代理评分机制修正。
- 主要优势: 改动小、能显著修复负相关。
- 主要代价: 仍依赖 proxy 机制本身与 `alpha` 的空间适配。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 4, Fig. 5
- 关键表: Table 1, Table 2, Table 3, Table 7, Table 8
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5)-(10)
- 关键算法: Algorithm 1（Supplementary）

## 参考链接
- Paper: https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html
- PDF: https://openaccess.thecvf.com/content/ICCV2025/papers/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.pdf
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf
- Code: Not found
- 本地实现: Not archived
