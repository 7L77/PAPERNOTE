---
title: "AZ-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[AZ-NAS]]"
source_paper: "AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search"
source_note: "[[AZ-NAS]]"
authors: [Junghyup Lee, Bumsub Ham]
year: 2024
venue: CVPR
tags: [nas-method, zh, nas, training-free, zero-cost-proxy]
created: 2026-03-14
updated: 2026-03-14
---

# AZ-NAS 中文条目

## 一句话总结
> AZ-NAS 通过组合四种互补 zero-cost proxy，并用非线性排名聚合压制“短板项”，显著提升 training-free NAS 的排序质量。

## 来源
- 论文: [AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search](https://arxiv.org/abs/2403.19232)
- HTML: https://arxiv.org/html/2403.19232
- 代码: https://github.com/cvlab-yonsei/AZ-NAS
- 英文方法笔记: [[AZ-NAS]]
- 论文笔记: [[AZ-NAS]]

## 适用场景
- 问题类型: 在不完整训练候选模型的前提下进行 NAS 排序与搜索。
- 前提假设: 架构可提取 block 级特征/梯度，并能计算 FLOPs。
- 数据形态: 主要是图像分类 NAS 基准与搜索空间。
- 规模与约束: 候选数量大、训练预算有限的场景。
- 适用原因: `sE/sP/sT/sC` 分别刻画表达性、深度渐进性、梯度稳定性、复杂度，信息互补。

## 不适用或高风险场景
- 目标是严格硬件延迟最优而非 FLOPs 预算。
- 架构形态不支持稳定的中间特征抽取。
- 任务域偏移很大，proxy 与真实性能相关性未知。

## 输入、输出与目标
- 输入: 候选架构、随机高斯 batch、预算约束、top-k 变异策略。
- 输出: 每个候选的 AZ 聚合分与最终最佳架构。
- 优化目标: 在低搜索成本下最大化排序与真实性能的一致性。
- 核心假设: 多 proxy 排序一致性提升会带来更优架构选择。

## 方法拆解

### 阶段 1: 计算四个 proxy
- `sE`：特征协方差主成分熵，衡量表达性。
- `sP`：相邻 block 表达性最小增量，衡量渐进性。
- `sT`：用 Rademacher 随机向量近似 Jacobian，基于谱范数构造可训练性分数。
- `sC`：直接使用 FLOPs 作为复杂度分数。
- Source: Sec. 3.1, Eq. (1)-(11)

### 阶段 2: 非线性排名聚合
- 对每个 proxy 在候选集上排名；
- 计算 `sum(log(rank/m))` 作为最终 AZ 分；
- 低排名项会被更强惩罚，避免被高分项抵消。
- Source: Sec. 3.2, Eq. (12)

### 阶段 3: 进化搜索
- 维护候选与 proxy 历史；
- 基于 AZ 分选 top-k 并变异生成新候选；
- 在预算内迭代并输出最优架构。
- Source: Algorithm 1, Sec. 4.1

## 伪代码
```text
Algorithm: AZ-NAS
Input: 搜索空间 Z, 迭代次数 T, 预算 B, top-k 大小 k
Output: 最优架构 F*

1. 初始化候选 F1 与历史集合 {F, SE, SP, ST, SC}。
   Source: Algorithm 1 (line 1-2)
2. 对 i = 1..T:
   2.1 计算 Fi 的 sE, sP, sT, sC。
       Source: Sec. 3.1, Eq. (1)-(11)
   2.2 记录 Fi 及 proxy 分数到历史。
       Source: Algorithm 1 (line 4-5)
   2.3 用非线性排名聚合计算 AZ 分。
       Source: Sec. 3.2, Eq. (12), Algorithm 1 (line 6)
   2.4 从 top-k 候选中选择并变异得到 Fi+1，满足预算 B。
       Source: Algorithm 1 (line 7)
3. 返回历史中 AZ 分最高的架构。
   Source: Algorithm 1 (line 9)
```

## 训练流程
1. 搜索阶段：随机初始化模型，用随机高斯输入计算 proxy。
2. 根据 AZ 分排序，执行进化更新。
3. 在参数/FLOPs 约束下选出最优结构。
4. 按标准训练配方重训并报告最终精度。

Sources:
- Sec. 4.1, Algorithm 1, Table 2/3

## 推理流程
1. 固定搜索得到的最终架构。
2. 按目标数据集设置训练或微调后评估。
3. 执行标准前向推理得到指标。

Sources:
- Sec. 4.2, Table 2, Table 3
- Source: Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给封闭式。
- 空间复杂度: 论文未给封闭式。
- 运行特征: NAS-Bench-201 上约 `42.7 ms/arch`，显著快于 TE-NAS 等高代价基线。
- 扩展性说明: 代理数量增加会小幅提高耗时，但排序一致性通常提升。

## 实现备注
- MBV2 代理实现：`ImageNet_MBV2/ZeroShotProxy/compute_az_nas_score.py`。
- MBV2 搜索主循环：`ImageNet_MBV2/evolution_search_az.py`。
- AutoFormer 代理实现：`ImageNet_AutoFormer/lib/training_free/indicators/az_nas.py`。
- 重要细节：AutoFormer 分支不计算 `sP`，与论文对 ViT 的脚注一致。
- 代码中的聚合实现为 `np.log(stats.rankdata(score)/l)` 跨代理求和，对齐 Eq. (12)。
- MBV2 代码中在打分前执行 Kaiming fan-in 初始化。

## 与相关方法关系
- 对比 TE-NAS：AZ-NAS 在保持低搜索成本的同时有更高排序一致性。
- 对比 ZiCo/SynFlow：AZ-NAS 的代理维度更全，聚合方式更强调均衡性。
- 主要优势：性能-成本折中优秀且解释性强。
- 主要代价：仍依赖基准与任务域中的 proxy 相关性。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 5
- 关键公式: Eq. (1)-(12)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2403.19232
- HTML: https://arxiv.org/html/2403.19232
- 代码: https://github.com/cvlab-yonsei/AZ-NAS
- 本地实现: D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search

