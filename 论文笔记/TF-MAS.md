---
title: "TF-MAS: Training-free Mamba2 Architecture Search"
method_name: "TF-MAS"
authors: [Yi Fan, Yu-Bin Yang]
year: 2025
venue: NeurIPS
tags: [NAS, training-free-NAS, Mamba2, zero-cost-proxy]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/TF-MAS Training-free Mamba2 Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/TF-MAS Training-free Mamba2 Architecture Search
created: 2026-03-16
---

# 论文笔记：TF-MAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | TF-MAS: Training-free Mamba2 Architecture Search |
| 会议 | NeurIPS 2025 |
| Code | https://github.com/fanyi-plus/tf-nas |
| 本地 PDF | `D:/PRO/essays/papers/TF-MAS Training-free Mamba2 Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/TF-MAS Training-free Mamba2 Architecture Search` |

## 一句话总结
> TF-MAS 把 [[Rank Collapse]] 思想从注意力层迁移到 [[State Space Duality (SSD)]]，构建了首个面向 Mamba2 的 [[Training-free NAS]] 代理，并在相关性与搜索结果上都优于现有训练免费代理。

## 核心贡献
1. 提出首个面向 Mamba 类架构的 training-free NAS 代理（Sec. 1, Sec. 3.1）。
2. 给出适配 Mamba2 的代理计算方式：不是直接用 FC 权重，而是先解映射矩阵 `U W_X = X`（同理 `W_B`, `W_C`），并区分 `T=W`, `T<W`, `T>W` 三种情形（Sec. 3.1, Eq. (2)-(5)）。
3. 用“计算预算驱动”的搜索空间构造法自动确定 4 个可调超参范围（Sec. 3.2, Eq. (7)）。

## 问题背景
### 要解决的问题
- Mamba2 架构搜索已有工作多数依赖训练过程，搜索代价高。
- 训练免费代理在 CNN/Transformer 已有较多进展，但 Mamba 架构缺口明显。

### 现有方法局限
- 许多传统代理与 Mamba2 结构错配，相关性不如参数量基线（Table 1）。
- 直接把 Transformer/CNN 代理迁移到 Mamba2 的效果有限。

### 本文动机
- SSD 与注意力在计算形态上存在对应关系，可借鉴 rank-collapse 分析设计新代理。

## 方法详解
### 1) 代理定义（TF-MAS）
- Mamba2 块中输入 `U` 经过 FC + Conv1D + SiLU 生成 `X, B, C`，因此 `U->X/B/C` 不是“单层 FC 权重”等价。
- 作者将 `U->X/B/C` 视为待求映射矩阵 `W_X, W_B, W_C`，再按核范数与梯度核范数构造代理（Sec. 3.1, Eq. (6)）。
- 关键点：`W_X/W_B/W_C` 需显式估计，不能偷换为 FC 层权重（Table 3 明确验证）。

### 2) 三种矩阵求解情形
- 情形 A (`T = W`)：可逆时直接 `W_X = U^{-1}X`（Eq. (2)）。
- 情形 B (`T < W`)：欠定系统，用最小 2-范数解，得到 `W_X = U^+ X`，其中 `U^+` 是 [[Moore-Penrose Pseudoinverse]]（Eq. (3), Eq. (4)）。
- 情形 C (`T > W`)：超定系统，无精确解，转为最小二乘近似 `argmin ||U W_X - X||_F`（Eq. (5)）。

### 3) 搜索空间设计
- 4 个 AH（可调超参）：深度 `D`、宽度 `W`、状态维度 `N`、头数 `H`（Sec. 3.2）。
- SSMamba2：`N,H` 全层共享；VWSSMamba2：`N,H` 可按层变化。
- 用目标开销 `c0` 及参考模型参数推导立方方程，求比例系数 `k`，再把 AH 范围设在虚拟基准模型的 `0.6x ~ 1.6x`（Eq. (7), Sec. 4.4）。

## 关键公式
### Eq. (2): 代理映射方程
\[
U W_X = X
\]
- 含义：将复杂算子链（FC+Conv+SiLU）在给定输入下等效为线性映射。

### Eq. (3)-(5): 分情形最优化
\[
\min \|W_X\|_2 \;\; \text{s.t.} \;\; U W_X = X
\]
\[
W_X = U^+X
\]
\[
\min \|U W_X - X\|_F
\]
- 含义：根据 `T` 与 `W` 的关系，分别用逆矩阵或伪逆最小二乘求近似映射。

### Eq. (6): TF-MAS 评分
- 对每层、每类矩阵 (`X/B/C/out`) 聚合
  `核范数(权重) * 核范数(对应梯度)`。
- 直观解释：同时看结构强度与可训练信号强度。

### Eq. (7): 预算约束下的 AH 缩放方程
\[
(2D_rW_rN_r + 193D_rW_rH_r)k^3 + (2VW_r + D_rW_r + 387D_rH_r + 10D_rN_r)k^2 + W_rk = c_0
\]
- 含义：将“预算约束”转化为可解方程，避免拍脑袋设搜索范围。

## 关键图表与实验结论
### Figure 1
- 展示 Mamba2 与 TF-MAS 对接位置：代理在每层 Mamba2 block 上计算。

### Table 1（VMSSMamba2Bench_2.7B 上相关性）
- TF-MAS 在 LAMBADA(ACC) 上 `0.661`，高于参数量基线 `0.437`。
- 多数对比代理相关性明显偏低，甚至接近 0 或负值。
- TF-MAS 计算时间 `1.31s`，虽高于参数量基线（`0.07s`），但仍属训练免费范畴可接受。

### Table 2（130M 条件下搜索结果）
- `Mamba-2-130M`: 128.932M params, 8.249G FLOPs, latency 0.160s
- `opt Mamba2`: 127.130M, 8.133G, 0.171s
- `opt VWMamba2`: 119.104M, 7.620G, 0.151s
- `opt VWMamba2 w/ bwe`: 122.572M, 7.842G, 0.125s
- 结论：在不增大预算下，搜索后模型在多项任务指标上更优。

### Table 3（替换映射矩阵为 FC 权重的消融）
- `w/o wfc` 相关性显著高于 `w/ wfc`，验证“必须显式估计 `W_X/W_B/W_C`”。

### Table 4/5 与 Figure 3
- 4 个 AH 都有贡献，不是只靠单一维度变化。
- `0.6x ~ 1.6x` 的范围经验在实验指标上合理。

## 与代码实现的对照
- 归档仓库：`tf-nas` 已存于本地。
- 当前公开仓库仅含占位 README，作者说明“代码将于后续逐步开放”，因此目前无法逐行对照代理实现细节。
- 这意味着本文的“方法可读性”强于“现阶段可复现实操性”。

## 批判性思考
### 优点
1. 目标明确，填补 Mamba training-free NAS 空白。
2. 数学处理严谨，三种形状情形与误差传播有专门分析。
3. 除相关性外还给出真实搜索并从头训练验证，避免“只看 tau”的片面性。

### 局限
1. 现有公开代码尚未释放，短期复现门槛高。
2. 主体验证集中在 Mamba2，跨 Mamba 变体泛化仍待确认。
3. 某些数据集上的相关性仍不算非常高，代理稳定性在更复杂任务中仍需检验。

### 复现性评估
- [x] 论文方法描述较完整（含附录伪代码）
- [x] 关键实验和消融较充分
- [ ] 完整可运行公开代码（当前仓库未实质开源）
- [ ] 一键复现实验脚本

## 关联概念
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Neural Architecture Search]]
- [[Kendall's Tau]]
- [[Rank Collapse]]
- [[State Space Duality (SSD)]]
- [[Moore-Penrose Pseudoinverse]]
- [[Weight Entanglement]]

