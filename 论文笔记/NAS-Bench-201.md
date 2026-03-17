---
title: "NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search"
method_name: "NAS-Bench-201"
authors: [Xuanyi Dong, Yi Yang]
year: 2020
venue: ICLR
tags: [NAS, benchmark, reproducibility, cell-based-search-space]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2001.00326
local_pdf: D:/PRO/essays/papers/NAS-Bench-201 extending the scope of reproducible neural architecture search.pdf
local_code: D:/PRO/essays/code_depots/NAS-Bench-201 extending the scope of reproducible neural architecture search
created: 2026-03-17
---

# 论文笔记：NAS-Bench-201

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search |
| arXiv | https://arxiv.org/abs/2001.00326 |
| OpenReview | https://openreview.net/forum?id=HJxyZkBKDr |
| 代码 | https://github.com/D-X-Y/NAS-Bench-201 |
| 本地 PDF | `D:/PRO/essays/papers/NAS-Bench-201 extending the scope of reproducible neural architecture search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/NAS-Bench-201 extending the scope of reproducible neural architecture search` |

## 一句话总结
> 这篇工作把“NAS 算法对比”从重复训练和设置不一致中解耦出来：先固定一个可覆盖主流 cell-based NAS 的小搜索空间，再把全部 `15,625` 个架构在统一 protocol 下完整评测并提供 API 查询。

## 核心贡献
1. 提出一个对主流 NAS 算法更“算法无关（algorithm-agnostic）”的 tabular benchmark，核心是 edge-op cell 搜索空间（Sec. 2.1, Fig. 1）。
2. 在三套数据集上统一训练并发布每个架构的细粒度训练/验证/测试指标、参数量、FLOPs、延迟（Sec. 2.2-2.4, Table 1-2）。
3. 给出与 NAS-Bench-101 的系统对照，说明为何 NAS-Bench-201 对参数共享等方法更友好（Sec. 3, Table 3）。
4. 在同一 benchmark 上重跑 10 类 NAS 基线，给出可复用对比线与速度收益（Sec. 5, Table 4-5, Fig. 6-8）。

## 问题背景
### 他们想解决什么
现有 NAS 论文往往使用不同搜索空间、不同训练细节和不同数据划分，导致“算法性能”与“评测设置”纠缠，横向对比不公平（Sec. 1）。

### 为什么 NAS-Bench-101 还不够
作者指出 NAS-Bench-101 的若干约束会让部分方法（尤其参数共享/网络形变类）不能直接评测；同时想要更多数据集和更细粒度训练信息（Sec. 1, Sec. 3, Table 3）。

## 方法详解
### 1) 搜索空间定义（Sec. 2.1, Fig. 1）
- 宏观骨架：stem conv + 3 stages cell stack（每 stage 堆叠 `N=5`）+ 两个降采样 residual block + GAP + FC。
- 微观 cell：4 个节点（`V=4`）的有向无环图，每条有向边从 5 个操作中选 1 个：
  - `zeroize`
  - `skip-connect`
  - `1x1 conv`
  - `3x3 conv`
  - `3x3 avg-pool`
- 因为 4 节点完全有向图共有 6 条边，所以编码规模是 `5^6=15625`。

### 2) 数据与统一训练协议（Sec. 2.2-2.3, Table 1-2）
- 数据集：CIFAR-10、CIFAR-100、ImageNet-16-120。
- 统一超参主配置 `H†`：SGD+Nesterov，200 epochs，cosine LR，batch size 256，weight decay 5e-4，初始通道 16。
- 另提供短预算 `H‡`（12 epochs）以支持 bandit/HPO 风格算法。
- 提供 train/valid/test 的 loss/acc 轨迹，以及 params/FLOPs/latency。

### 3) 诊断信息与 API（Sec. 2.4, Appendix D）
- 诊断层面：逐 epoch 曲线、计算开销、已训练权重。
- 使用层面：API 支持按架构字符串或 index 查询指标、成本和 trial 细节。
- 本地仓库 `nas_201_api/api_201.py` 对应了 `NASBench201API`、`get_more_info`、`query_index_by_arch` 等关键入口。

### 4) 基线评测协议（Sec. 5, Table 4-5）
- 评测 10 种 NAS：RS/REA/REINFORCE/BOHB、DARTS/GDAS/SETN/ENAS/RSPS 等。
- 对“是否参数共享”进行分块分析，同时单列 BN 统计策略对 one-shot 方法的影响（Fig. 7-8, Table 7）。

## 关键图表（论文主证据）
### Figure 1（搜索空间结构）
- 说明 macro skeleton 与 4-node cell + edge-op 编码，是 benchmark 设计的核心。

### Figure 2（全空间性能概览）
- 显示全部架构在三数据集上的表现分布，并与 ResNet 对照。

### Figure 3（跨数据集排名）
- 观察到跨数据集排名总体相关但并不完全一致，提示“可迁移但有域差”。

### Figure 4（相关性热图）
- 同数据集内 `val-test` 相关性高于跨数据集相关性；高精度区间相关性下降更明显。

### Figure 5（动态排名）
- 不同训练时刻的验证排名会逐步逼近最终测试排名，支持早停/代理信号研究。

### Figure 6-8（算法表现与训练动态）
- 对比非参数共享与参数共享方法表现；展示 DARTS 在该空间的退化行为及 BN 策略影响。

### Table 1（统一训练超参）
- 固定优化器、学习率策略、数据增强和训练时长，减少评测协议差异。

### Table 2（可查询指标）
- 明确每个数据集上可用的 train/valid/test 统计项。

### Table 3（与 NAS-Bench-101 对比）
- NAS-Bench-201：15.6K 架构、3 数据集、5 操作、无 edge 数约束、提供更细粒度诊断信息。

### Table 4（加速收益）
- 对多类 NAS，benchmark 能直接加速评估；对部分方法也能显著加速搜索流程。

### Table 5（10 类 NAS 核心结果）
- 非参数共享方法整体更强：REA/REINFORCE/RS 在 CIFAR-10 test 约 `93.9/93.85/93.70`。
- GDAS 在参数共享方法中较稳（CIFAR-10 test 约 `93.61`），DARTS-V1/V2 在该空间出现明显退化（约 `54.30`）。
- 全空间最优（optimal）约：CIFAR-10 test `94.37`，CIFAR-100 test `73.51`，ImageNet-16-120 test `47.31`。

### Table 6（短预算相关性）
- 12-epoch 收敛策略（`H‡`）对后续全训练表现更有参考意义，适合 bandit/HPO。

### Table 7（one-shot 代理相关性）
- DARTS 概率/OSVA 与真值相关性偏低；GDAS 在概率与 OSVA 上相关性更高，BN 统计处理会显著影响 one-shot 评估质量。

## 关键结论
1. NAS-Bench-201 在“可对比性”和“可复现实验效率”上明显推进了 NAS 基准化（Sec. 7）。
2. 对参数共享 NAS，BN 统计策略和架构导出策略是成败关键（Sec. 5, Fig. 7-8, Table 7）。
3. 该基准能降低搜索评估成本，但也带来“对 benchmark 过拟合”的风险，论文专门给出使用规范（Sec. 6）。

## 与代码实现的对照
- 论文附录给出 API 用法，仓库 `README.md` 与 `nas_201_api` 实现保持一致。
- 代码中明确支持 `NAS-Bench-201-v1_0` 与 `v1_1` 文件，且后续维护迁移到 NATS-Bench（仓库 README 首段）。
- 代码可复现“查询式 benchmark 工作流”，但不包含重新训练全 15,625 架构的完整计算资产（需额外下载大体量数据文件）。

## 批判性思考
### 优点
1. 把 NAS 研究重心从“重复训模型”转移到“搜索策略本身”。
2. 对 benchmark 的接口化设计（API + 诊断信息）非常实用。
3. 同时给出方法层与工程层建议（如反过拟合规则）。

### 局限
1. 搜索空间仍较小，外推到更大空间的结论需要谨慎。
2. 统一训练超参会引入“某些架构受益/受损”的偏置（作者在 Sec. 6 直接承认）。
3. 该基准当前代码仓库已标记 deprecated，生态实际向 NATS-Bench 迁移。

### 可复现性评估
- [x] 代码与 API 开源
- [x] 数据格式与查询接口清晰
- [ ] 全量训练资产体量大，下载与复现门槛高
- [ ] 结论跨搜索空间泛化仍需更多证据

## 关联概念
- [[Neural Architecture Search]]
- [[Cell-based Search Space]]
- [[Differentiable Architecture Search]]
- [[One-shot NAS]]
- [[Evolutionary Neural Architecture Search]]
- [[Parameter Sharing in NAS]]
- [[Search Space Isomorphism]]

