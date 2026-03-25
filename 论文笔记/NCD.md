---
title: "Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS"
method_name: "NCD"
authors: [Haidong Kang, Lianbo Ma, Pengjun Chen, Guo Yu, Xingwei Wang, Min Huang]
year: 2025
venue: ICCV
tags: [nas, training-free-nas, zero-cost-proxy, activation-based-proxy, ncd]
zotero_collection: ""
image_source: online
arxiv_html: https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html
local_pdf: D:/PRO/essays/papers/Beyond the Limits Overcoming Negative Correlation of Activation-Based Training-Free NAS.pdf
created: 2026-03-14
---

# 论文笔记：NCD

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Beyond the Limits: Overcoming Negative Correlation of Activation-Based Training-Free NAS |
| 会议 | ICCV 2025 |
| 论文页 | https://openaccess.thecvf.com/content/ICCV2025/html/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.html |
| PDF | https://openaccess.thecvf.com/content/ICCV2025/papers/Kang_Beyond_the_Limits_Overcoming_Negative_Correlation_of_Activation-Based_Training-Free_NAS_ICCV_2025_paper.pdf |
| Supplementary | https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf |
| 代码 | Not found on ICCV page/supplementary (checked 2026-03-14) |
| 本地 PDF | `D:/PRO/essays/papers/Beyond the Limits Overcoming Negative Correlation of Activation-Based Training-Free NAS.pdf` |

## 一句话总结
> 论文发现 activation-based 训练自由 NAS 会随卷积层数增加出现“负相关”，并提出 NCD（SAM + NIR）把相关性从负值拉回正值并提升跨搜索空间稳定性。

## 核心贡献
1. 系统揭示 [[Negative Correlation in Training-free NAS]]：AZP（如 NWOT、SWAP）在深子空间相关性会显著下降甚至变负（Sec. 3, Fig. 2, Table 1）。
2. 提出 AZP 设计原则，强调 proxy 分数需与结构属性一致并反映真实非线性（Sec. 2.2）。
3. 提出 [[Stochastic Activation Masking]]（SAM），通过随机掩码减轻卷积中的非线性累积（Eq. 4）。
4. 提出 [[Non-linear Rescaling]]（NIR），分析 BN/LN 中求和机制并在 AZP 评估中缓解非线性放大（Sec. 4.2, Theorem 4.1/4.2）。

## 问题背景
### 要解决的问题
- [[Training-free NAS]] 依赖 [[Zero-Cost Proxy]] 排序候选架构；若 proxy 与真实性能相关性失真，会直接误导搜索方向。

### 现有方法的局限
- 在 NAS-Bench-201 的深子空间（例如 77 convolutions）中，NWOT/SWAP 相关性降到负值，排序方向反转（Table 1）。
- 论文认为根因是非线性累积导致 proxy 分数幅值异常下降（Sec. 3.2, Eq. 3）。

### 本文动机
- 让 AZP 同时满足“排序有效 + 与结构属性一致 + 非线性可解释”，并在高复杂架构中保持稳健。

## 方法详解
### Step 1: 负相关诊断
- 先复盘 activation pattern 与 NWOT/SWAP 的定义（Eq. 1, Eq. 2）。
- 在分层子空间（5/17/29/41/53/65/77 conv）上测相关性，验证负相关随深度加重（Sec. 3.1, Table 1）。

### Step 2: SAM（Stochastic Activation Masking）
- 在卷积计算时引入 Bernoulli 掩码：每次卷积随机屏蔽部分激活值，掩码概率由 `alpha` 控制（Eq. 4）。
- 目的：减少“固定位置裁剪”引起的信息丢失和高非线性累积，同时保持排序一致性。

### Step 3: NIR（Non-linear Rescaling）
- 论文先分析 BN 中均值项来自大量 ReLU 激活加权求和（Theorem 4.1, Eq. 5-9）。
- 再说明 LN 场景下（初始化零均值权重）对非线性放大更可控，可缓解负相关（Theorem 4.2, Eq. 10, Remark 2）。
- 实践上在 AZP 评估阶段配合 SAM/NIR 构成 NCD 版本的 proxy（NCD-NWOT/NCD-SWAP）。

## 关键公式
### Activation pattern 二值化（Eq. 1）
\[
H(x) = \begin{cases}
0,& x < 0\\
1,& x \ge 0
\end{cases}
\]
- 用于把中间特征映射转换为离散激活模式。

### NWOT 评分（Eq. 2）
\[
S_{\text{NWOT}} = \log|K_H|
\]
- \(K_H\) 由样本间 Hamming 距离构造；分数越大表示表达能力越强。

### 非线性累积示意（Eq. 3）
\[
y^{(l+1)} = \sum_{i=1}^{n}\sigma(x_i^{(l)})
\]
- 论文用它解释“层数增加导致非线性增强”的机制。

### SAM 掩码卷积（Eq. 4）
\[
y = \sum (W \odot M \odot X),\quad M(i,j,k)\sim Bernoulli(1-\alpha)
\]
- 以随机掩码方式减少激活求和项，缓和 proxy 幅值塌缩。

## 关键实验结论
### Table 1：相关性从负值拉回正值
- 77-conv 子空间中：SWAP 从 `-0.246` 提升到 `0.715`；NWOT 从 `-0.734` 提升到 `0.679`。
- 平均 Spearman 相关：SWAP 系列由 `0.387` 提升到 `0.773`；NWOT 系列由 `0.180` 提升到 `0.622`。

### Table 2：NB-201 / NB-101
- NCD-NWOT（alpha=0.95）在 NB-201 上达到 `94.00/71.99/45.27`（C10/C100/ImageNet16-120）。
- NB-101 达到 `93.49`，且 runtime `29.01 ms/arch`。

### Table 3：DARTS 搜索空间
- 报告在 CIFAR 与 ImageNet1k 上相对多种 NAS 基线保持竞争力；NCD-NWOT 搜索成本最低到 `0.002 GPU-days` 量级。

### Table 7/8：消融与稳定性
- SAM、NIR 单独加入都有效，联合效果最好。
- `alpha` 在一定区间内表现稳定，论文强调对不同搜索空间存在偏置差异但整体不敏感。

## 论文与代码对照
- 目前未在 ICCV 论文页和补充材料中看到官方仓库链接（检查日期：2026-03-14）。
- 论文给出了完整方法与附录算法描述，可按文中公式和 Algorithm 1 复现主流程。
- 论文方法对应的关键算法位于 **Supplementary 的 Algorithm 1**：  
  https://openaccess.thecvf.com/content/ICCV2025/supplemental/Kang_Beyond_the_Limits_ICCV_2025_supplemental.pdf

## 批判性思考
### 优点
1. 把“负相关”这个先前少被显式讨论的问题做了定量化和机制化分析。
2. SAM/NIR 改动简单，能直接加到现有 AZP 上，工程改造成本低。
3. 覆盖 12 个搜索空间、4 个任务，实验外延较广。

### 局限
1. 公开页面未提供官方代码，复现门槛仍高于“开箱即用”方法。
2. 超参数 `alpha` 的跨空间迁移虽稳定但仍需经验调参。
3. 机制解释依赖若干理论近似（如初始化条件下的统计性质），在不同训练设定下可能偏离。

### 可复现性评估
- [x] 论文公开
- [x] 补充材料公开
- [ ] 官方代码公开链接
- [x] 关键公式/实验设置可定位

## 关联概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Sample-Wise Activation Pattern]]
- [[Stochastic Activation Masking]]
- [[Non-linear Rescaling]]
- [[Negative Correlation in Training-free NAS]]
- [[Spearman's Rank Correlation]]
