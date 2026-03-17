---
title: "ParZC_ch"
type: method
language: zh-CN
source_method_note: "[[ParZC]]"
source_paper: "ParZC: Parametric Zero-Cost Proxies for Efficient NAS"
source_note: "[[ParZC]]"
authors: [Peijie Dong, Lujun Li, Zhenheng Tang, Xiang Liu, Zimian Wei, Qiang Wang, Xiaowen Chu]
year: 2025
venue: AAAI
tags: [nas-method, zh, nas, zero-cost-proxy, predictor-based]
created: 2026-03-17
updated: 2026-03-17
---

# ParZC 中文条目

## 一句话总结
> ParZC 将节点级零成本统计从“同权求和”改为“可学习聚合 + 可微排序优化”，显著提升低样本 NAS 的排序能力。

## 来源
- 英文方法笔记: [[ParZC]]
- 论文: https://arxiv.org/abs/2402.02105
- HTML: https://arxiv.org/html/2402.02105
- 代码: 论文/arXiv 页面未明确给出官方仓库

## 适用场景
- 问题类型: NAS 中的大规模候选架构快速排序。
- 前提假设: 不同节点的 ZC 统计贡献不一致，且存在不确定性。
- 数据形态: 有少量架构-精度监督样本（例如 0.02%-10% 搜索空间）。
- 约束条件: 计算预算紧张，希望比传统 ZC 求和更稳。
- 适用原因: 训练开销低于完整训练式 predictor，同时保留可学习能力。

## 不适用或高风险场景
- 完全无标注预算（无法训练 ParZC 主分支）。
- 搜索空间迁移差异过大，历史排名模式不稳定。
- 强依赖“官方代码即复现”的项目管理要求。

## 输入、输出与目标
- 输入: 每个架构的节点级 ZC 统计向量（可来自 W/A/G/H 等统计）。
- 输出: 架构排序分数。
- 目标: 最大化预测排序与真实排序的一致性（KD/SP）。
- 核心假设: 节点异质性 + 不确定性建模能提升排序稳健性。

## 方法拆解
### 阶段 1：节点级统计与归一化
- 提取节点 proxy 统计并做 min-max 归一化。
- Source: Sec. 3.1, Fig. 5

### 阶段 2：MABN 不确定性建模
- Bayesian 层与 mixer 结构联合建模跨段交互与不确定性。
- Source: Sec. 3.2, Fig. 5

### 阶段 3：DiffKendall 排序训练
- 用可微 Kendall 近似直接优化排名一致性。
- Source: Sec. 3.3

### 阶段 4：ParZC† 训练自由增强
- 对现有 ZC proxy 使用非负正弦权重重加权。
- Source: Sec. 3.4, Eq. (1)

## 伪代码
```text
Algorithm: ParZC 排序器
Input: 架构集合 A, 节点 proxy 提取器 Z, 训练集 D={(a_i, y_i)}
Output: 评分函数 f_theta

1. 对每个 a in A:
   计算 v_a = Normalize(Z(a))
   Source: Sec. 3.1, Fig. 5
2. 在 D 上训练 MABN:
   s_i = f_theta(v_{a_i})
   优化 DiffKendall(s, y)
   Source: Sec. 3.2-3.3
3. 用 s 对 A 排序并选择 top 架构
   Source: Sec. 4
4. 可选: 使用 ParZC† 替代训练分支做训练自由打分
   Source: Sec. 3.4
```

## 训练流程
1. 从搜索空间抽取少量带标签架构。
2. 构建节点统计向量并归一化。
3. 用 Adam + DiffKendall 训练排序器。
4. 在验证集合上评估 KD/SP。

Sources:
- Sec. 4, Tab. 2/3/8

## 推理流程
1. 为候选架构计算节点统计向量。
2. 前向得到排序分数。
3. 选高分架构进入完整训练/评测。

Sources:
- Sec. 4, Tab. 4

## 复杂度与效率
- 时间开销: 主要在节点统计提取 + 小样本 predictor 训练。
- 空间开销: 节点特征缓存 + MABN 参数。
- 报告成本: NB201 约 3000 GPU sec（约 50 分钟）。
- 扩展特征: 在低样本设置下相对 predictor 基线更有样本效率。

## 实现备注
- 优化器: Adam, lr=1e-4, wd=1e-3。
- batch: 训练 10，评估 50。
- epoch: NB101=150, NB201=200, NDS=296。
- DiffKendall 系数: alpha=0.5。
- 代码状态: 目前未检索到论文官方仓库，细节以论文描述为准。

## 与相关方法关系
- 对比 [[EZNAS]]: 低样本下排序相关性更高。
- 对比 [[HNAS]]: 在同类预算下报告更优 KD。
- 主要优势: 节点异质性建模 + 直接排序优化。
- 主要代价: 需要少量监督样本（除 ParZC† 外）。

## 证据与可溯源性
- 关键图: Fig. 2/4/5/6
- 关键表: Tab. 1/2/3/4/8
- 关键公式: Sec. 3.1/3.2/3.3 + Eq. (1)
- 算法出处: 主文无独立算法框，流程由 Sec. 3-4 复原

## 参考链接
- arXiv: https://arxiv.org/abs/2402.02105
- HTML: https://arxiv.org/html/2402.02105
- 代码: 论文/arXiv 页面未明确给出
- 本地实现: Not archived
