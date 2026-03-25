---
title: "A Neural Architecture Dataset for Adversarial Robustness"
method_name: "NARes"
authors: [Bowen Zheng, Ran Cheng, Shihua Huang, Zhichao Lu, Vishnu Boddeti]
year: 2025
venue: ICLR 2025 (OpenReview submission)
tags: [NAS, adversarial-robustness, robustness-dataset, WRN, macro-search-space]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=AZVvTBxTdZ
created: 2026-03-23
pdf_archive_status: "failed (OpenReview 403, 2026-03-23)"
code_archive_status: "official repo not publicly linked in current OpenReview/PDF version (checked 2026-03-23)"
---

# 论文笔记: NARes

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | A Neural Architecture Dataset for Adversarial Robustness |
| 作者 | Bowen Zheng, Ran Cheng, Shihua Huang, Zhichao Lu, Vishnu Boddeti |
| 会议/版本 | ICLR 2025 投稿版（OpenReview） |
| OpenReview | https://openreview.net/forum?id=AZVvTBxTdZ |
| PDF | https://openreview.net/pdf/adb9acc706c4b858a6448cb218e58621b71dd419.pdf |
| 本地 PDF | 归档失败（OpenReview 403） |
| 本地代码 | 未归档（该版本未给出公开仓库链接） |

## 一句话总结
> NARes 把 WRN 宏观架构空间做成了可直接查询的对抗鲁棒性数据集：覆盖 15,625 个架构、四类攻击与多种诊断指标，并提供 4 个 checkpoint/架构，显著降低鲁棒 NAS 研究门槛。

## 核心贡献
1. 在 WRN 宏观搜索空间上做了大规模、统一协议的对抗训练与评测（15,625 架构）。
2. 除常规鲁棒精度外，提供了训练过程与诊断指标（如 [[Stable Accuracy]]、经验 [[Lipschitz Constant]]）。
3. 将该数据集作为“time-free”鲁棒 NAS 基准，验证了一些既有经验法则的局限。

## 问题背景
### 要解决的问题
- 从“网络架构设计”角度研究 [[Adversarial Robustness]] 成本极高，常规研究难以在大规模空间中系统比较。

### 现有数据集局限
- 以往 AR 架构数据集多聚焦 micro/cell 空间（如 NAS-Bench-201），与 WRN 宏观设计研究存在鸿沟。
- 模型容量偏小，且包含较多失效模型，和高容量鲁棒训练场景不完全匹配。
- 指标粒度不足，且未系统纳入 AutoAttack 维度。

## 数据集与方法细节
### 1) 搜索空间（Sec. 3.1, Fig. 1）
- 基础骨干：[[Wide Residual Network]]（pre-activation block）。
- 决策向量：`[D1, W1, D2, W2, D3, W3]`。
- 深度候选：`D_i in {4, 5, 7, 9, 11}`；宽度候选：`W_i in {8, 10, 12, 14, 16}`。
- 总规模：`5^6 = 15,625` 架构，参数量约 `23.25M ~ 266.80M`。

### 2) 训练协议（Sec. 3.1, Table 1）
- 数据：CIFAR-10。
- 训练：标准 PGD 对抗训练，100 epochs。
- 学习率：在 epoch 75 与 90 衰减 0.1。
- 为缓解 [[Robust Overfitting]]：基于独立验证集的 PGD-CW40 准确率做 early stopping。
- 每个架构保留 4 个 checkpoint：epoch 74、89、99、best epoch。
- 训练总成本：约 `13.1K GPU days (~36 GPU years)`。

### 3) 指标与诊断（Sec. 3.2, Eq. (1), Table 1）
- 验证集：CIFAR-10.1（2K 图像）。
- 记录：每 epoch 的对抗训练 loss/acc、验证 clean 与 PGD20/PGD-CW40 准确率、对应稳定准确率与经验 Lipschitz。
- 测试集评测攻击：FGSM、PGD20、PGD-CW40、AA-Compact（`epsilon=8/255`）。
- 评测总成本：约 `2.9K GPU days (~8 GPU years)`。

### 4) 关键公式（Sec. 3.2）
#### 稳定准确率（Stable Accuracy）
\[
\text{StableAcc}=\frac{\left|\{x \sim D_{val}: f_{\theta}(x)=f_{\theta}(\hat{x})\}\right|}{|D_{val}|}
\]
- 直观：攻击后预测不变的样本比例。

#### 经验 Lipschitz（Eq. (1)）
\[
L(B,\epsilon)=\frac{1}{|D_{val}|}\sum_{x\in D_{val}}
\frac{\|f_{\theta}(x)-f_{\theta}(\hat{x})\|_1}{\|x-\hat{x}\|_{\infty}}
\]
- 直观：攻击邻域内输出变化幅度的经验度量。

## 主要实验结论
### 统计结论（Sec. 4）
1. 相比只增参数量，增加 MACs 预算对鲁棒性提升更稳定。
2. [[Stable Accuracy]] 与鲁棒精度相关性更稳定；低 LIP 是高鲁棒性的必要条件之一。
3. “末段容量应减小”这类经验规则在该大规模空间中并不稳健。
4. 架构鲁棒性由 `D1..W3` 联合决定，单一 ratio 难完整刻画。

### NAS 基准结果（Sec. 5, Table 2）
- 在最多 500 次查询（约 3.2% 空间）下比较 Random Search / Local Search / RE / BANANAS。
- RE 与 BANANAS 整体优于随机与局部搜索，BANANAS 在验证集目标上最好且更稳定。
- 测试鲁棒性上，RE 与 BANANAS 搜到的最优架构接近。

## 局限与使用建议（Sec. 6.1）
1. 单次全空间 sweep 仍含噪声，建议做分布层面统计分析，不要过度解读单个架构点。
2. 当前主要在 CIFAR-10，跨数据集泛化需额外验证。
3. 验证集与测试集准确率相关性不高，给 NAS 搜索稳定性带来挑战。

## 与现有数据集关系
- 与 [[NADR-Dataset]]（2023，NAS-Bench-201 micro 空间）不同，NARes强调 WRN 宏观空间与高容量对抗训练场景。
- 两者可互补：前者适合 cell 拓扑研究，后者适合 depth/width 宏观设计与鲁棒 NAS 验证。

## 关联概念
- [[Neural Architecture Search]]
- [[Robust Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Wide Residual Network]]
- [[Stable Accuracy]]
- [[Lipschitz Constant]]
- [[Robust Overfitting]]
- [[AutoAttack]]

