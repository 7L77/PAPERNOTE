---
title: "L-SWAG: Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers"
method_name: "L-SWAG"
authors: [Sofia Casarin, Sergio Escalera, Oswald Lanz]
year: 2025
venue: CVPR
tags: [NAS, zero-cost-proxy, training-free, vision-transformer, proxy-ensemble]
zotero_collection: ""
image_source: online
arxiv_html: https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html
local_pdf: D:/PRO/essays/papers/L-SWAG Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers.pdf
created: 2026-03-20
---

# 论文笔记：L-SWAG

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | L-SWAG: Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers |
| 会议 | CVPR 2025 |
| 论文页 | https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html |
| PDF | https://openaccess.thecvf.com/content/CVPR2025/papers/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.pdf |
| 本地 PDF | `D:/PRO/essays/papers/L-SWAG Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers.pdf` |
| 官方代码 | 主文、Supplementary、CVPR 页面均未给出明确官方仓库（2026-03-20 检索） |

## 一句话总结
> L-SWAG 把“层级梯度方差”与“层级激活模式表达性”相乘做 ZC 打分，并用 LIBRA 在基准上按低信息增益和偏置重对齐组合 proxy，在 ViT/CNN 搜索空间上提升排序相关性与搜索结果。

## 核心贡献
1. 在 AutoFormer 小搜索空间上训练 2000 个 ViT（6 个任务），补齐了 ViT 场景下 ZC proxy 的系统评测。
2. 提出 **L-SWAG**：结合梯度统计（trainability）与激活模式基数（expressivity）的层级 ZC 指标（Sec. 3.1, Eq. 1）。
3. 提出 **LIBRA-NAS**：不训练 predictor 的 proxy 组合策略，按“高相关 + 最小信息增益 + 偏置匹配”选 3 个 proxy（Sec. 3.2, Alg. 1, Eq. 9）。
4. 在 19 个 benchmark-task 组合中，LIBRA 在 13 个任务优于已有组合方法；在 ImageNet1k 上报告 0.1 GPU day 找到 17.0% test error 架构（Tab. 2）。

## 问题背景
### 要解决的问题
- 现有 [[Zero-Cost Proxy]] 在经典 CNN 搜索空间能工作，但迁移到 ViT 搜索空间时，常常连简单的参数量/FLOPs baseline 都未必稳定超越。
- 单一 proxy 往往只看 trainability 或 expressivity 的一面，跨基准稳定性不足。

### 现有方法局限
- 多数 proxy 对“各层贡献”默认同权，忽略层间统计差异。
- proxy 融合方法常依赖额外 predictor 训练，严格意义上不再是纯 zero-shot 流程。

### 本文动机
- 用层级视角提取“更有信息量的层段”统计。
- 用轻量规则型组合（不训练 predictor）利用 proxy 互补性与偏置结构。

## 方法详解
### 1) L-SWAG 分数（Sec. 3.1）
- 主体形式：`L-SWAG = Lambda * Psi`（Eq. 1）。
- `Lambda`：对选定层区间 `[l_hat, L_hat]` 的梯度绝对值方差做统计并取 log 聚合，强调低方差稳定梯度。
- `Psi`：层级 [[Sample-Wise Activation Pattern]] 集合的基数，度量表达性（Def. 1/2, Eq. 7/8）。
  - 论文在定义层面未显式写“transpose/转置”操作；其写法是“每个中间激活位置构造跨样本二值向量并取集合基数”。
  - 与 [[SWAP-NAS]] 的关系：机制等价于按 `(neurons, samples)` 组织后做 unique 计数；但 SWAP 论文/实现会明确写出激活矩阵转置后再去重计数。
- 设计点：
  - 去掉 ZiCO 里的梯度均值项 `mu`，保留 “1 / sqrt(Var)” 结构并给出理论+实证支撑（Thm. 1, Eq. 5, Tab. 3）。
  - 引入层选择：只在信息峰值层段统计，提升相关性并降计算成本（Fig. 2a/2b）。
  - 将 ReLU 场景扩展到 GeLU 网络（ViT）表达性统计。

### 2) LIBRA 组合策略（Sec. 3.2）
- 输入：某 benchmark 上一组 proxy 的相关性与偏置信息。
- 选择过程（Alg. 1）：
  1. 选相关性最高的 `z1`。
  2. 在次优集合中，选 `IG` 最小的 `z2`（Eq. 9，[[Information Gain]]）。
  3. 再选与验证精度偏置（文中用参数量偏置）最接近的 `z3`。
- 输出：`{z1, z2, z3}` 组成组合评分用于搜索。

## 关键公式
### 公式 1：L-SWAG 主公式（Eq. 1）
\[
\text{L-SWAG} = \Lambda_{\hat L}\cdot \Psi_{\mathcal N,\theta}^{\hat L}
\]
含义：把 trainability 与 expressivity 作为互补信号做乘性耦合。

### 公式 2：一阶更新后的损失上界（Eq. 5）
\[
L_f(X,y;\hat a)\le \frac{1}{2}\left(M\sum_{j=1}^d \left[\sigma_j^2 + ((M\eta-1)\mu_j)^2\right]\right)
\]
含义：文中用它解释“仅追求高均值梯度并不总是有利”，支持去掉 `mu` 的经验策略。

### 公式 3：信息增益（Eq. 9）
\[
IG(z_j)=H(y|z_i)-H(y|z_i,z_j)
\]
含义：LIBRA 用它衡量加入新 proxy 后对验证精度分布的信息变化，并在候选中取最小 IG。

## 关键图表与结论
### Figure 1（总流程）
- 左侧是 L-SWAG 打分流程；右侧是 LIBRA 选 proxy 的三步流程。

### Figure 2（层选择动机）
- 梯度统计在特定深度百分位存在峰值；只取对应层段能明显提升相关性并提速。

### Figure 3/4（相关性总览）
- L-SWAG 平均 Spearman 相关性约 0.72，高于第二名 NWOT 的 0.62（Fig. 4）。
- 在多组 TransNAS-Bench 任务上优势明显，且对 Macro/Micro 迁移更稳。

### Table 1（组合方法对比）
- LIBRA 在 19 个 benchmark-task 中 13 个最优，4 个与 AZ-NAS 接近。

### Table 2（搜索结果）
- AutoFormer-Small + ImageNet1k：LIBRA 报告 17.0% test error，0.1 GPU day。
- DARTS/CIFAR-10、DARTS/ImageNet1k 上也优于多种 training-free 与传统 NAS baseline。

### Table 3/4（消融）
- 去 `mu`、层选择、expressivity 三者都贡献增益；其中层选择对不同搜索空间影响不同。
- LIBRA 里 `min IG` 和 bias matching 组合最稳。

## 实验设置速记
- 基准：[[NAS-Bench-201]]、NAS-Bench-101、NAS-Bench-301、[[TransNAS-Bench-101]]、AutoFormer-Small。
- 任务：覆盖分类、场景/目标识别、自动编码、布局、法向、分割等。
- 硬件：单张 RTX 3090Ti。
- 开销：1000 个 ViT 的梯度统计提取约 31 分钟；完成层选择后 L-SWAG 计算约 4 分钟（文中报告）。

## 批判性思考
### 优点
1. 把 ViT 纳入统一 ZC 评测，实证价值高。
2. L-SWAG 的构造有“公式-消融-跨基准”三重证据链，不是纯经验 trick。
3. LIBRA 不依赖训练 predictor，保持了 training-free 搜索的效率优势。

### 局限
1. LIBRA 仍是经验型组合规则，理论完备性弱于严格可证框架。
2. 偏置定义主要用参数量，面对其他偏置（拓扑、算子类型）是否同样有效仍待验证。
3. 官方代码未公开，工程复现细节主要依赖论文叙述与已有基准框架。

### 对你当前方向的启发
1. 可先在现有 proxy 管线中加入“层段选择”而不是全层同权统计。
2. 组合 proxy 时不一定要训练复杂 predictor，可先用 “best + min-IG + bias-match” 低成本策略做强 baseline。
3. 在 ViT/混合搜索空间里，建议把“是否优于 params/FLOPs”作为最低可接受门槛。

## 关联概念
- [[Zero-Cost Proxy]]
- [[Sample-Wise Activation Pattern]]
- [[Information Gain]]
- [[Spearman's Rank Correlation]]
- [[GELU]]
- [[Neural Architecture Search]]
- [[TransNAS-Bench-101]]

## 速查卡片
> [!summary] L-SWAG
> - 核心问题: 现有 ZC proxy 在 ViT 上相关性不足且跨空间不稳
> - 核心方法: 层级梯度方差 x 层级激活模式基数 + LIBRA 组合
> - 关键结果: 平均相关性优于现有 proxy；ImageNet1k 搜索达到 17.0% error / 0.1 GPU day
> - 代码状态: 未检索到官方仓库（截至 2026-03-20）


## 操作

### 1. 层段选择
先选“信息量高”的层段 [l_hat, L_hat]，不再全层同权统计
对每层/每个 block 计算梯度统计量（文中用梯度绝对值方差一类信号），把层号映射成深度百分位，找出出现峰值的区间，把该区间的起止层记作 l_hat, L_hat，之后 Lambda/Psi 的聚合都只在这段层上算。
很多 proxy 信号在某些层更“有信息”，全层同权会把噪声层的统计也混进去，相关性更差、计算也更慢。

先用少量架构在随机初始化下跑一次前后向，统计“梯度相关信号”在网络深度上的分布，发现它在某个深度百分位附近最有区分度，于是只取那一段连续层作为 [l_hat, L_hat] 来算 proxy，而不是把所有层同权加起来。

### 2.梯度绝对值方差
在该层段上算梯度绝对值方差并聚合成 Lambda（trainability 信号），并去掉了 ZiCO 里不稳定的梯度均值项 mu
<div style="margin-left: 2em;">
在选定层段 [l_hat, L_hat] 上统计参数梯度 |∂L/∂w| 的方差并做 log 聚合得到 Λ，用“梯度越稳定(方差越小)越可训练”刻画 trainability；同时去掉 ZiCo 中的梯度均值项 μ，避免“均值大但不稳定”的误判（理论上由一阶更新损失上界支撑，实证消融也验证）。
</div>
