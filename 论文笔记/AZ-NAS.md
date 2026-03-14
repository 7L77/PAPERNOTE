---
title: "AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search"
method_name: "AZ-NAS"
authors: [Junghyup Lee, Bumsub Ham]
year: 2024
venue: CVPR
tags: [nas, training-free-nas, zero-cost-proxy, cvpr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2403.19232
local_pdf: D:/PRO/essays/papers/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search
created: 2026-03-14
---

# 论文笔记：AZ-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search |
| arXiv | https://arxiv.org/abs/2403.19232 |
| 项目页 | https://cvlab.yonsei.ac.kr/projects/AZNAS |
| 代码 | https://github.com/cvlab-yonsei/AZ-NAS |
| 本地 PDF | `D:/PRO/essays/papers/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search` |

## 一句话总结
> AZ-NAS 通过组合四类互补 zero-cost proxies（表达性、渐进性、可训练性、复杂度）并用非线性排名聚合，显著提升了训练前 NAS 排名与真实性能的一致性。

## 核心贡献
1. 提出多代理协同的 training-free NAS 视角，不再依赖单一 proxy（Sec. 1, Sec. 3）。
2. 设计四个可在一次前后向中高效计算的 proxy：`sE/sP/sT/sC`（Sec. 3.1）。
3. 提出非线性排名聚合 `sum(log(rank/m))`，显式惩罚“短板代理”（Sec. 3.2, Eq. 12）。
4. 在 NAS-Bench-201、MobileNetV2、AutoFormer 三类空间上取得更好搜索质量与成本比（Sec. 4.2）。

## 问题背景
### 要解决的问题
- 训练自由 NAS 的核心是：不用完整训练也能把候选架构排对序。
- 现实中单 proxy 往往相关性不足，导致“挑出来的最优架构”并不优。

### 现有方法局限
- 单一 proxy 覆盖的信息维度窄。
- 一些方法计算代价高（例如依赖额外多次前后向或复杂核矩阵）。
- 简单线性聚合难以处理“某一维明显很差”的情况。

### 本文动机
- 让不同视角的 proxy 互补，并通过聚合机制强化“全面强”而非“单项强”的架构。

## 方法详解
### 1) `sE`：Expressivity（表达性）
- 在各主干 block 特征上做协方差分解，计算主成分归一化后熵值。
- 直观上：特征越各向同性，表达能力越强（Sec. 3.1, Eq. 1-4）。

### 2) `sP`：Progressivity（渐进性）
- 定义为相邻 block 表达性差值的最小值：`min_l (sE_l - sE_{l-1})`（Eq. 5）。
- 约束“深层特征空间应持续扩展”，不是只看某个局部峰值。

### 3) `sT`：Trainability（可训练性）
- 目标是衡量梯度传播稳定性（谱范数接近 1 更好）。
- 通过 Hutchinson 风格随机向量近似 block Jacobian，再构造训练性分数（Eq. 6-11）。

### 4) `sC`：Complexity（复杂度）
- 直接使用 FLOPs 作为复杂度 proxy，在预算内偏好更高算力利用架构（Sec. 3.1）。

### 5) 非线性排名聚合
- 最终分数：对每个 proxy 的排名做 `log(rank/m)` 后求和（Eq. 12）。
- 作用：某一 proxy 排名很差会被明显惩罚，避免被其他高分项“冲掉”。

### 6) 搜索流程
- 采用进化式搜索（Algorithm 1）：
1. 计算当前架构四类 proxy；
2. 用非线性聚合算 AZ-NAS 分；
3. 从 top-k 中选父代变异生成新架构；
4. 迭代至预算结束，输出最高分架构。

## 关键公式（含解释）
### Eq. (3) 表达性熵
\[
s_l^E=\sum_i -\tilde{\lambda}_l(i)\log \tilde{\lambda}_l(i)
\]
- `\tilde{\lambda}` 是主成分方差的 L1 归一化系数。
- 熵高意味着主成分贡献更均匀，特征不塌缩。

### Eq. (5) 渐进性
\[
s^P=\min_l (s_l^E-s_{l-1}^E)
\]
- 关注最差“层间增长幅度”，确保深度方向持续提升。

### Eq. (11) 可训练性
\[
s^T=\frac{1}{L-1}\sum_{l=2}^{L}\left(-\sigma_l-\frac{1}{\sigma_l}+2\right)
\]
- `\sigma_l` 为近似 Jacobian 的谱范数。
- 当 `\sigma_l=1` 时单层项最大，偏离 1 会受罚。

### Eq. (12) 聚合分数
\[
s_{AZ}(i)=\sum_{M\in\{E,P,T,C\}}\log \frac{\mathrm{Rank}(s_M(i))}{m}
\]
- `Rank` 是在候选集中的升序排名。
- 对低排名项的惩罚更强，鼓励均衡表现。

## 关键图示解读
### Figure 1
- 横轴是 Kendall's Tau，纵轴是选中架构精度，气泡大小/颜色反映运行时。
- 结论：AZ-NAS 在“排序一致性 + 最终精度 + 计算成本”三者之间给出更优平衡。

### Figure 2
- 展示 `sE` 的直观含义：特征分布越各向同性，主成分系数越均匀，熵越高。
- 说明 `sE` 能检测特征塌缩与表达冗余。

### Figure 3
- 展示各 proxy 间相关性：`sT` 与其余 proxy 相关性更低。
- 解释了为什么“低相关代理的组合”可带来更明显增益。

## 关键实验结果
### NAS-Bench-201（Table 1）
- AZ-NAS 在 Kendall's Tau 上显著领先：
1. CIFAR-10: `0.741`
2. CIFAR-100: `0.723`
3. ImageNet16-120: `0.710`
- 对比 ZiCo（`0.589/0.590/0.584`）和 GradSign（`0.618/0.594/0.575`）均有明显提升。
- 运行时 `42.7 ms/arch`，远低于 TE-NAS（`1311.8 ms/arch`）与 GradSign（`1823.9 ms/arch`）。

### MobileNetV2 搜索空间（Table 2）
- 在 450M/600M/1000M FLOPs 约束下分别达到：
1. `78.6 ± 0.2`
2. `79.9 ± 0.3`
3. `81.1 ± 0.1`
- 同时保持低搜索成本（约 `0.4~0.7` GPU days）。

### AutoFormer（Table 3）
- Tiny/Small/Base 大多数设置优于 AutoFormer 和 TF-TAS，且搜索成本更低。
- 论文脚注说明：ViT 场景不使用 `sP`（progressivity），仍能保持竞争力。

### 消融与扩展（Table 4/5）
- 多代理明显优于单代理。
- 非线性聚合优于线性聚合（例如全代理：`0.741/0.723/0.710` vs `0.697/0.681/0.663`）。
- 把 AZ-NAS 代理并入 SynFlow/ZiCo 也能持续提升 Kendall's Tau。

## 与代码实现的对照
- 官方仓库：`https://github.com/cvlab-yonsei/AZ-NAS`（已归档到本地）。
- MobileNetV2 分支中 `ZeroShotProxy/compute_az_nas_score.py` 与论文一致实现 `sE/sP/sT/sC`。
- `evolution_search_az.py` 使用 `np.log(rank/l)` 聚合，和 Eq. (12) 对齐。
- AutoFormer 分支 `lib/training_free/indicators/az_nas.py` 仅计算 `expressivity/trainability/complexity`，与论文脚注“ViT 不用 progressivity”一致。

## 批判性思考
### 优点
1. 方法简单直接，可插拔到已有 search loop。
2. 精度-效率折中好，尤其是排序一致性提升明显。
3. 代理设计与聚合机制有清晰可解释性。

### 局限
1. 仍依赖“proxy 与真实性能相关”这一经验前提，跨域泛化需更多验证。
2. 当前主要集中在图像分类搜索空间，其他任务（检测/分割/NLP）证据不足。
3. `sC=FLOPs` 在某些硬件目标上可能与真实 latency 不一致。

### 复现性评估
- [x] 代码开源
- [x] 算法流程清晰
- [ ] 一键复现实验门槛低（仍需准备较重数据与环境）
- [ ] 跨任务统一复现脚本完善

## 关联概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
- [[NAS-Bench-201]]
- [[Non-linear Ranking Aggregation]]
- [[Kendall's Tau]]
- [[Hutchinson Estimator]]
- [[Spectral Norm]]
