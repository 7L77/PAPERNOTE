---
title: "UP-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[UP-NAS]]"
source_paper: "UP-NAS: Unified Proxy for Neural Architecture Search"
source_note: "[[UP-NAS]]"
authors: [Yi-Cheng Huang, Wei-Hua Li, Chih-Han Tsou, Jun-Cheng Chen, Chu-Song Chen]
year: 2024
venue: "CVPR Workshops"
tags: [nas-method, zh, nas, training-free, zero-cost-proxy, predictor-based-nas]
created: 2026-03-20
updated: 2026-03-20
---

# UP-NAS 中文条目

## 一句话总结
> UP-NAS 先把多个 zero-cost proxy 融成一个统一目标，再用 MPE 从架构潜变量预测这些 proxy，最后直接在潜空间里做梯度上升来找更好的架构。

## 来源
- 论文 PDF: `D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf`
- 代码: https://github.com/AI-Application-and-Integration-Lab/UP-NAS
- 英文方法笔记: [[UP-NAS]]
- 论文笔记: [[UP-NAS]]

## 适用场景
- 问题类型: 训练自由 NAS、零成本代理驱动的架构搜索、多代理融合搜索。
- 前提假设: 架构可以被编码到平滑的连续潜空间里，而且若干 proxy 的线性加权对目标任务仍有可迁移的排序意义。
- 数据形态: 需要一批架构的 proxy 分数来训练 MPE，还需要一个小型 benchmark 子集来搜索 proxy 权重。
- 规模与约束: 当单次代理计算不便宜、但希望把搜索本身做得很快时尤其合适。
- 适用原因: 它把“多代理打分”变成了“可微的潜空间优化”，避免一轮轮离散枚举。

## 不适用或高风险场景
- 搜索空间没有可靠的 encoder-decoder，无法把潜变量稳健地解码回合法架构。
- proxy 与真实性能的关系跨数据集变化太大，导致固定权重失效。
- 当前就需要完整官方实现做复现；归档到本地的官方仓库还没有公开代码。

## 输入、输出与目标
- 输入: 架构 `A`、多个 zero-cost proxy 分数、架构编码器/解码器、代理权重 `lambda`。
- 输出: 搜索到的架构 `A*` 以及它的统一代理分数。
- 优化目标: 最大化 `UP(A)=sum_i lambda_i f^i_zc(A)`。
- 核心假设: 多 proxy 融合比单 proxy 更稳，而潜空间梯度步能对应到更优的离散架构。

## 方法拆解
### 阶段 1: 学习架构潜空间
- 用 DAG 的邻接矩阵和操作矩阵表示 cell。
- 采用 [[Variational Graph Autoencoder]] 风格的 autoencoder，并用 [[Graph Isomorphism Network]] 做编码。
- 得到连续 [[Architecture Embedding]]，后续搜索都在这里进行。
- Source: Sec. 3.2 / Eq. (2) / Fig. 3

### 阶段 2: 训练 MPE
- 把架构潜向量送进两层隐藏层的 MLP。
- 一次性预测全部 proxy，而不是预测真实精度。
- 用 proxy 向量的均方误差训练。
- Source: Sec. 3.3 / Eq. (3)-(4)

### 阶段 3: 学习统一代理权重
- 在 NAS-Bench-201-CIFAR-10 的小子集上，用 [[Tree-structured Parzen Estimator]] 搜索权重。
- 优化目标是让统一代理与真实性能的 [[Kendall's Tau]] 尽量高。
- 学到的权重随后迁移到别的空间和数据集。
- Source: Sec. 3.4-3.5 / Table 1

### 阶段 4: 潜空间梯度上升搜索
- 随机取一个初始架构并编码成 `Z`。
- 冻结 encoder、MLP 和 `lambda`。
- 最大化 `F(Z)=sum_i lambda_i f_MLP(Z;W)_i`。
- 优化后把 `Z` 解码回离散架构。
- Source: Sec. 3.4 / Eq. (5)-(6)

## 伪代码
```text
Algorithm: UP-NAS
Input: 搜索空间 S, 多个 proxy {f^i_zc}, 架构自编码器 Enc/Dec, 用于训练 MPE 的样本架构
Output: 最优架构 A*

1. 预训练架构 autoencoder，学习潜空间表示。
   Source: Sec. 3.2 / Eq. (2)
2. 为一批样本架构计算 proxy 分数，并编码成潜向量。
   Source: Sec. 3.3 / Sec. 3.5
3. 训练 MPE，从潜向量回归全部 proxy 分数。
   Source: Eq. (3)-(4)
4. 用 TPE 搜索 proxy 权重 lambda，使统一代理与真实性能的 Kendall's tau 最大。
   Source: Sec. 3.4-3.5 / Table 1
5. 随机采样初始架构 A0，并编码成 Z0。
   Source: Sec. 3.4
6. 对 F(Z)=sum_i lambda_i f_MLP(Z;W)_i 做梯度上升。
   Source: Eq. (5)-(6)
7. 把最终潜向量解码成离散架构 A*。
   Source: Fig. 3 / Sec. 3.4
8. 按 benchmark 训练流程评估 A*。
   Source: Sec. 4
```

## 训练流程
1. 预训练架构自编码器。
2. 计算或加载样本架构的 zero-cost proxy。
3. 用 proxy 向量监督训练 MPE。
4. 在小 benchmark 上搜索全局代理权重。
5. 固定所有模块，进入搜索阶段。

Sources:
- Sec. 3.2-3.5, Table 1

## 搜索/推理流程
1. 从目标搜索空间采样初始架构。
2. 编码到潜空间。
3. 对冻结的统一代理目标做梯度上升。
4. 解码得到候选架构。
5. 对最终架构按标准 recipe 训练与测试。

Sources:
- Sec. 3.4, Fig. 2, Sec. 4

## 复杂度与效率
- 时间特征:
  - DARTS 上 `grasp` 约 `10 sec/architecture`
  - 其他 12 个 proxy 大约 `1 sec/architecture`
  - MPE 在 NAS-Bench-201 和 DARTS 上训练都少于 `2 minutes`
  - DARTS 搜索本身约 `5 sec`
- 扩展性说明: 搜索步数越多，MPE 代替重复 proxy 计算的收益越明显。
- 空间开销: 主要来自 proxy 缓存和 encoder/MLP 参数。

## 实现备注
- 架构表示:
  - 邻接矩阵 `A`
  - 操作 one-hot 矩阵 `X`
  - 用 `A + A^T` 做增强
- 解码器:
  - 边存在性通过 `sigmoid(z_i^T z_j)` 重建
  - 操作用 `softmax(W_o Z + b_o)` 重建
- 潜维度:
  - NAS-Bench-201: `128`
  - DARTS: `352`
- MPE:
  - 两层隐藏层
  - `linear + batch norm + ReLU`
  - 监督目标是 proxy 向量，而非最终精度
- 代理集合:
  - `snip`, `flops`, `params`, `l2 norm`, `grasp`, `gradnorm`, `synflow`, `jacov`, `EPENAS`, `Zen`, `fisher`, `plain`, `Nwot`
- 关键权重现象:
  - 正权重大头是 `jacov`, `synflow`, `flops`
  - 负权重主要是 `params`, `fisher`, `snip`, `l2 norm`
  - `UPselected` 最后只保留 `flops`, `synflow`, `jacov`, `Nwot`
- 代码状态:
  - 本地归档目录是 `D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search`
  - 当前官方仓库归档提交 `2601145` 只有 `README.md` 和 `LICENSE`
  - 所以这里的实现细节主要来自论文，不是代码核实

## 与相关方法的关系
- 对比 [[NAO]]: 都在连续架构空间里搜索，但 UP-NAS 优化的是统一代理，而不是直接预测真实性能。
- 对比 [[ProxyBO]]: 都做多 proxy 融合，但 UP-NAS 走的是“固定权重 + 潜空间梯度上升”，不是 BO。
- 主要优势: 搜索快，而且多代理融合与搜索流程衔接得很自然。
- 主要代价: 很依赖潜空间质量，以及“一个全局权重向量能迁移”的假设。

## 证据与可溯源性
- 关键图: Fig. 1-5
- 关键表: Table 1-7
- 关键公式: Eq. (1)-(6)
- 关键算法: 论文没有单独算法框；核心搜索流程由 Eq. (5)-(6) 和 Fig. 2 给出。

## 本地路径
- 论文 PDF: `D:/PRO/essays/papers/UP-NAS Unified Proxy for Neural Architecture Search.pdf`
- 代码归档: `D:/PRO/essays/code_depots/UP-NAS Unified Proxy for Neural Architecture Search`
