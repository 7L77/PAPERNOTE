---
title: "L-SWAG_ch"
type: method
language: zh-CN
source_method_note: "[[L-SWAG]]"
source_paper: "L-SWAG: Layer-Sample Wise Activation with Gradients Information for Zero-Shot NAS on Vision Transformers"
source_note: "[[L-SWAG]]"
authors: [Sofia Casarin, Sergio Escalera, Oswald Lanz]
year: 2025
venue: CVPR
tags: [nas-method, zh, nas, zero-cost-proxy, training-free, vision-transformer]
created: 2026-03-20
updated: 2026-03-20
---

# L-SWAG 中文条目

## 一句话总结
> L-SWAG 用“选层后的梯度方差统计”乘以“层级激活模式表达性”做 zero-shot 排序，LIBRA 再用相关性/信息增益/偏置匹配挑 3 个 proxy 组合，提升跨基准稳定性。

## 来源
- 英文方法笔记: [[L-SWAG]]
- 论文: https://openaccess.thecvf.com/content/CVPR2025/papers/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.pdf
- HTML: https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html
- 代码: 论文页/补充材料页未给出明确官方仓库

## 适用场景
- 问题类型: CNN/ViT 搜索空间中的训练自由架构排序与快速搜索。
- 前提假设: 初始化时的梯度方差与激活模式多样性能反映后续性能潜力。
- 数据形态: 打分阶段无需训练网络；若用 LIBRA，需要先有 benchmark 级 proxy 统计。
- 约束条件: 候选规模大、预算有限，不适合全量训练评估。
- 适用原因: 保持 zero-shot 低开销，同时在异构基准上比单一 proxy 更稳。

## 不适用或高风险场景
- 完全无法做反向传播（L-SWAG 需要梯度统计）。
- 没有可用 benchmark 统计来做 LIBRA 校准。
- 项目要求严格依赖官方开源代码可复现。

## 输入、输出与目标
- 输入: 随机初始化架构 `N`、batch `(X,y)`、层区间 `[l_hat, L_hat]`、可选 proxy 集合 `Z`。
- 输出: 架构排序分数（L-SWAG），或 LIBRA 选出的 `{z1,z2,z3}` 组合。
- 目标: 提高 proxy 排名与真实验证精度排名的一致性（Spearman rho）。
- 核心假设: “层重要性不均匀 + trainability/expressivity 互补”能提升跨空间泛化。

## 方法拆解
### 阶段 1：梯度统计提取 trainability
- 在选定层段上统计梯度绝对值方差并聚合为 `Lambda`。
- Source: Sec. 3.1, Eq. (1), Eq. (5), Fig. 2

### 阶段 2：激活模式提取 expressivity
- 计算层级 sample-wise activation pattern 集合基数作为 `Psi`。
- Source: Sec. 3.1, Def. 1, Def. 2, Eq. (7), Eq. (8)

### 阶段 3：组合成 L-SWAG
- 最终分数 `s = Lambda * Psi`。
- Source: Sec. 3.1, Eq. (1)

### 阶段 4：LIBRA 组合（可选）
- `z1` 取最高相关，`z2` 取最小 IG，`z3` 取 bias matching。
- Source: Sec. 3.2, Alg. 1, Eq. (9)

## 伪代码
```text
Algorithm: L-SWAG + LIBRA
Input: 架构 N, 初始化参数 theta, 批次 (X,y), proxy 集合 Z
Output: 排序分数 s（或组合分数）

1. 根据梯度百分位峰值确定层区间 [l_hat, L_hat]
   Source: Sec. 3.1, Fig. 2, Eq. (6)
2. 在该区间计算梯度方差聚合项 Lambda
   Source: Sec. 3.1, Eq. (1), Eq. (5)
3. 计算层级激活模式基数 Psi
   Source: Sec. 3.1, Def. 1-2, Eq. (7-8)
4. 计算 s = Lambda * Psi，并按 s 排序候选架构
   Source: Sec. 3.1, Eq. (1)
5. 可选：LIBRA 选 z1/z2/z3 进行 proxy 组合并重排序
   Source: Sec. 3.2, Alg. 1, Eq. (9)
```

## 训练流程
1. L-SWAG 本身不需要训练候选架构。
2. 对采样架构做少量前后向，提取梯度与激活统计。
3. 根据基准统计选择有效层段。
4. 若使用 LIBRA，先离线计算 proxy 相关性与偏置。

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4

## 推理流程
1. 对每个候选架构在初始化状态计算 L-SWAG 分数。
2. 按分数排序并筛选 top 架构进入后续搜索。
3. 若使用 LIBRA，按 `{z1,z2,z3}` 组合分数重排。

Sources:
- Sec. 4.1, Sec. 4.2, Tab. 1, Tab. 2

## 复杂度与效率
- 时间开销: 主要来自梯度/激活统计提取。
- 空间开销: 取决于选层区间的中间激活与梯度缓存；文中报告约 10GB（1000 个 ViT）。
- 运行特征: 文中给出 1000 个 ViT 梯度统计约 31 分钟，层选择后 L-SWAG 计算约 4 分钟。
- 扩展性: 在 NB101/NB301/TransNAS/AutoFormer 上均有较稳定提升。

## 实现备注
- 选层是关键，不建议全层同权直接聚合。
- 去掉 `mu` 项是核心设计之一，消融里整体更稳。
- 对 ViT 场景，expressivity 项不可省略。
- LIBRA 中强候选过滤窗口为 `rho_best - 0.1 < rho <= rho_best`。
- 代码未公开时，流程需按论文细节自行实现。

## 与相关方法关系
- 对比 [[ZiCo-BC]]: L-SWAG 去均值并引入层级 expressivity 乘积结构。
- 对比 [[SWAP-NAS]]: L-SWAG 在 SWAP 思路上叠加梯度统计与层区间选择。
- 主要优势: 跨基准、跨架构类型（CNN/ViT）的排序稳定性更高。
- 主要代价: 需要梯度与激活双统计，并为不同基准做轻量校准。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4
- 关键表: Tab. 1, Tab. 2, Tab. 3, Tab. 4
- 关键公式: Eq. (1), Eq. (5), Eq. (7), Eq. (8), Eq. (9)
- 关键算法: Algorithm 1 (LIBRA)

## 参考链接
- arXiv: Not provided in accessed source
- HTML: https://openaccess.thecvf.com/content/CVPR2025/html/Casarin_L-SWAG_Layer-Sample_Wise_Activation_with_Gradients_Information_for_Zero-Shot_NAS_CVPR_2025_paper.html
- 代码: 论文页/补充页未发现官方仓库
- 本地实现: Not archived
