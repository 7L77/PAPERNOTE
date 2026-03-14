---
title: "W-PCA Based Gradient-Free Proxy for Efficient Search of Lightweight Language Models"
method_name: "W-PCA"
authors: [Shang Wang]
year: 2025
venue: ICLR
tags: [NAS, training-free-nas, zero-shot-proxy, lightweight-language-model, pca]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2504.15983v1
local_pdf: D:/PRO/essays/papers/W-PCA Based Gradient-Free Proxy for Efficient Search of Lightweight Language Models.pdf
created: 2026-03-14
---

# 论文笔记：W-PCA

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | W-PCA Based Gradient-Free Proxy for Efficient Search of Lightweight Language Models |
| arXiv | https://arxiv.org/abs/2504.15983 |
| OpenReview | https://openreview.net/forum?id=L2fV7f9VWf |
| Code | https://github.com/ra225/W-PCA |
| 本地 PDF | `D:/PRO/essays/papers/W-PCA Based Gradient-Free Proxy for Efficient Search of Lightweight Language Models.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/W-PCA BASED GRADIENT-FREE PROXY FOR EFFICIENT SEARCH OF LIGHTWEIGHT LANGUAGE MODELS`（仅失败日志 `ARCHIVE_FAILED.txt`，未完成源码归档） |

## 一句话总结

> 本文提出一个面向轻量语言模型 NAS 的无梯度代理 `W-PCA = #Params × V-PCA`，在 [[Training-free NAS]] 场景下兼顾排名相关性与搜索效率。

## 核心贡献

1. 提出基于 FFN 隐状态 PCA 维度统计的零训练代理 `V-PCA`（Sec. 3.2, Eq. (1)-(7)）。
2. 进一步提出 `W-PCA = w × S(X)`（Sec. 3.3, Eq. (8)），把参数规模信息与 PCA 信息融合，提升排序稳定性。
3. 在 FlexiBERT、GLUE、SQuAD 与附录中的 CLM 设置上展示较强表现与较低搜索代价（Sec. 5-6, App. I）。

## 问题背景

### 要解决的问题

在轻量语言模型搜索中，one-shot NAS 仍需要训练 supernet，代价高；纯代理方法又常有偏置和稳定性不足。

### 现有方法局限

- 许多 [[Zero-Cost Proxy]] 在 NLP 结构上的排序相关性较弱（Sec. 5.2, Table 1）。
- 依赖梯度的代理会增加搜索成本。
- 单一特征（只看参数量或只看某种梯度信号）容易造成偏置。

### 本文动机

作者观察到训练过程中，[[Principal Component Analysis]] 指标与 GLUE 性能趋势一致（Fig. 3），且初始化阶段 PCA 对最终排序有预测力，于是构建无梯度 PCA 代理并与参数量结合。

## 方法详解

### 1) Vanilla PCA Proxy（V-PCA）

- 对每层 FFN 中间激活 `H = XW1 + b1` 做 PCA。
- 用达到阈值 `eta` 的最小主成分数 `k = PCA_dim(X, eta)` 作为层分数（Eq. (1), Eq. (6)）。
- 全模型分数 `S(X) = sum_f Sf(X)`（Eq. (7)）。

### 2) Weight-Weighted PCA（W-PCA）

- 令 `w` 为模型参数量，定义：
  - `W-PCA(X) = w × S(X)`（Eq. (8)）。
- 直觉：`S(X)` 捕捉表征结构，`w` 约束容量；两者乘积兼顾信息量和规模。

### 3) 搜索空间与搜索过程

- 设计面向 NLU 的搜索空间（Sec. 4, Fig. 4）。
- `m=12` 层，`n=6` 候选尺度，块类型含 BERT-base / MobileBERT 变体（Sec. 6.2.1）。
- 使用遗传算法搜索（App. E）：population=50, generations=40, mutation=0.1。

### 4) 训练与蒸馏

- 搜索后对选中结构进行预训练 + 下游微调（Sec. 6.2.2）。
- 使用 [[Knowledge Distillation]] 损失（App. F, Eq. (9)-(11)）。

## 关键公式

### Eq. (6): PCA 维度阈值定义

$$
k = \min \left\{k' \;\middle|\; \frac{\sum_{i=1}^{k'} \lambda_i}{\sum_{i=1}^{D'} \lambda_i} \ge \eta \right\}
$$

含义：在每层中找到最少主成分数量，使累计贡献率达到阈值 `eta`（即 [[Cumulative Explained Variance]]）。

### Eq. (7): 全模型 V-PCA

$$
S(X) = \sum_{f=1}^{m} S_f(X)
$$

含义：把各层 PCA 分数求和，得到模型级代理分数。

### Eq. (8): W-PCA

$$
W\text{-}PCA(X) = w \times S(X)
$$

含义：用参数规模对 V-PCA 加权，提升排序鲁棒性与可分辨性。

### Eq. (11): KD 总损失（附录）

$$
L = \sum_{i=1}^{m}\left(L_i^{attn}+L_i^{hidd}\right)+L_{embd}+\gamma L_{pred}
$$

含义：对齐中间表示与预测层，预训练阶段设 `gamma=0`，微调阶段 `gamma=1`。

## 关键图表与结果

### Figure 2（排序相关性）

- 在 FlexiBERT 500 架构上，`W-PCA` 的相关性高于多个 zero-shot 代理。

### Table 1（FlexiBERT 排名）

- `W-PCA`: Kendall tau = 0.526, Spearman rho = 0.698。
- `Vanilla PCA`: 0.466 / 0.677。

### Table 2（GLUE test）

- `W-PCA-Small`（15.6M, 54ms）平均分 78.3。
- `W-PCA-Tiny`（9.6M, 38ms）平均分 75.9。

### Table 3（GLUE dev + 搜索时间）

- `W-PCA-Small`: 0.5 GPU day, Avg 81.4。
- 相比 EfficientBERT（58 GPU days, Avg 80.4）搜索成本显著降低。

### Table 4（SQuAD）

- `W-PCA-Small` 在 v1.1 与 v2.0 上均优于若干同规模轻量基线。

### Table 5（消融）

- `W-PCA`（81.4）优于仅 `#Params`（80.3）与仅 `V-PCA`（80.8）。

## 实验与实现细节

- `eta=0.99`（主文 Sec. 6.2.1，附录 D 给出不同 `eta` 的鲁棒性）。
- proxy 计算不需要反向传播，主要依赖前向与 PCA 分解。
- 论文报告 Table 1 中 1000 次代理计算时间：W-PCA 74s，Vanilla PCA 61s。
- 训练细节（Sec. 6.2.2）：pretrain batch=256；finetune batch=32；CoLA 50 epochs，其他 10 epochs。

## 与代码实现的对照

- 官方代码仓库：`https://github.com/ra225/W-PCA`。
- 本次尝试本地归档失败原因：
  - `git clone/fetch` 多次出现 `early EOF`；
  - `Invoke-WebRequest` 下载连接被远端提前关闭；
  - 已记录时间：2026-03-14。
- 已写入占位目录与失败日志：`D:/PRO/essays/code_depots/W-PCA BASED GRADIENT-FREE PROXY FOR EFFICIENT SEARCH OF LIGHTWEIGHT LANGUAGE MODELS/ARCHIVE_FAILED.txt`。
- 因此本文方法解读与伪代码依据论文正文与附录完成，未做本地代码级核查。

## 批判性思考

### 优点

1. 方法非常直接：`PCA × 参数量`，工程上好实现。
2. 只需前向 + 线性代数，明显降低 NAS 搜索成本。
3. 在 ranking、GLUE、SQuAD 与 CLM 附录上都给出实证支持。

### 局限

1. 代理构造含显式规模项，跨搜索空间时可能仍带 size bias。
2. 关键论断强依赖作者定义的搜索空间与训练流程，外推性需更多验证。
3. 代码未能在本地复核，当前结论仅基于论文文本可追踪部分。

### 可复现性评估

- [x] 论文可获取
- [x] 代码链接公开
- [ ] 本地代码归档完成
- [x] 关键公式与表格可追踪

## 关联概念

- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
- [[Principal Component Analysis]]
- [[Cumulative Explained Variance]]
- [[Knowledge Distillation]]
- [[Genetic Algorithm]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]
