---
title: "PO-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[PO-NAS]]"
source_paper: "Per-Architecture Training-Free Metric Optimization for Neural Architecture Search"
source_note: "[[PO-NAS]]"
authors: [Anonymous Author(s)]
year: 2025
venue: "NeurIPS 2025 (under review submission)"
tags: [nas-method, zh, nas, training-free, zero-cost-proxy, surrogate-model, evolutionary-search]
created: 2026-03-16
updated: 2026-03-16
---

# PO-NAS 中文条目

## 一句话总结
> PO-NAS 针对每个候选架构动态学习训练无关指标的组合权重，并将该代理模型与 BO + 进化搜索结合，在小真实训练预算下实现更有效的 NAS 搜索。

## 来源
- 英文方法笔记: [[PO-NAS]]
- 论文 PDF: `D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf`
- 匿名代码链接: https://anonymous.4open.science/r/PO-NAS-2953（2026-03-16 仍不可 clone）

## 适用场景
- 问题类型: 训练成本高、候选架构多的 NAS 搜索。
- 前提假设: 不同架构对各训练无关指标的敏感性不同。
- 数据形态: 大量低成本 proxy 评估 + 少量真实训练反馈。
- 规模与约束: 特别适合大搜索空间（例如 DARTS）。
- 适用原因: 使用“按架构自适应”的指标融合，而非全局固定权重。

## 不适用或高风险场景
- 没有任何真实训练反馈预算。
- 架构编码质量不足，导致代理模型难以区分结构差异。
- 任务极度不稳定，对代理排序误差容忍度低。

## 输入、输出与目标
- 输入: 架构图 \(G(A)\)、训练无关指标 \(Z(A)\)、少量真实性能 \(f(A)\)。
- 输出: 候选评分 \(\hat S(A)\) 与最终最优架构 \(A^*\)。
- 优化目标: 在有限真实训练下提高代理排序与真实性能排序的一致性。
- 核心假设: 架构级别的指标加权比全局加权更能跨任务泛化。

## 方法拆解
### 阶段 1: 初始化与预训练
- 随机生成候选池，计算训练无关指标。
- 训练少量架构得到初始真实标签集。
- 用节点 mask 重建损失 + 指标预测损失预训练编码器与预测器。
- Source: Sec. 3.2-3.3, Eq. (3)(4), Alg. 1 lines 1-10.

### 阶段 2: BO 代理搜索
- 每轮用当前真实标签集更新代理模型。
- 通过 cross-attention 生成“每个架构对应的指标权重”。
- 在候选池中选最优架构做真实训练并回流监督。
- Source: Sec. 3.4, Eq. (5)-(8), Alg. 1 lines 11-29.

### 阶段 3: 进化扩展（大搜索空间）
- 根据预测分数与操作代价选父代组合。
- 用最短操作路径交叉 + 邻域遍历变异生成子代。
- 子代再经代理筛选后回填候选池。
- Source: Sec. 3.5, Appendix A.2-A.4, Eq. (9), Alg. 2.

## 伪代码
```text
Algorithm: PO-NAS
Input: N_ini, N_t, T_p, T_s, T_e, metrics Z
Output: A*

1. 构建初始候选集 A0，并计算 Z(A0)
   Source: Alg. 1 lines 1-3
2. 训练 N_t 个架构得到 Q0={(A,f(A))}
   Source: Alg. 1 line 4
3. 预训练编码器 E 与指标预测器 Pz
   Source: Sec. 3.3 Eq. (3)(4)
4. for t=1..T_s:
   4.1 用 Qt-1 更新代理 M（L_align + L_corr + L_dir）
       Source: Sec. 3.4 Eq. (6)(7)(8)
   4.2 若 t>T_e，执行进化搜索并更新候选池
       Source: Sec. 3.5, Eq. (9), Alg. 2
   4.3 选当前最优 A_best 做真实训练，加入 Qt
       Source: Alg. 1 lines 23-28
5. 返回 Qt 中真实性能最优架构
   Source: Alg. 1 line 30
```

## 训练流程
1. 预计算训练无关指标。
2. 预训练 GAT 编码器与指标预测器。
3. BO 迭代中持续更新代理并引入真实训练反馈。
4. 大空间中加入进化子代，扩大探索覆盖面。

Sources:
- Sec. 3.2-3.5, Appendix B.2.

## 推理/使用流程
1. 搜索阶段用代理模型快速打分与筛选候选架构。
2. 选出的最终架构按标准训练配方完成训练后用于部署推理。

Sources:
- Sec. 3.4 与实验配置章节。
- Inference from source.

## 复杂度与效率
- 时间开销: 代理更新 + 少量真实训练 +（可选）进化子代评估。
- 空间开销: 与候选池规模、指标缓存、代理模型参数量相关。
- 运行特点: 大量廉价 proxy 评估，少量昂贵真实训练。
- 扩展性: 小空间可只用代理；大空间加入进化更有效。

## 实现备注
- 使用 6 个指标: grad_norm, snip, grasp, fisher, synflow, jacob_cov。
- 归一化公式见 Eq. (10)(11)（附录 B.2）。
- 评分函数显式保留正/负相关权重（Eq. 5）。
- 差异阈值 \(T_{th}\) 与损失阈值对稳定性影响明显。
- 当前匿名代码链接不可 clone，复现需等待公开仓库。

## 与相关方法关系
- 对比 HNAS: PO-NAS 更强调“按架构动态加权”。
- 对比 RoBoT: 同为混合范式，但 PO-NAS 加入进化扩展与更细粒度权重建模。
- 主要优势: 更好处理不同架构的指标敏感性差异。
- 主要代价: 系统组件更多，代理优化稳定性压力更大。

## 证据与可追溯性
- 关键图: Fig. 1, Fig. 2, Fig. 3。
- 关键表: Table 1, Table 2, Table 3。
- 关键公式: Eq. (1)-(9), Eq. (10)(11)。
- 关键算法: Algorithm 1, Algorithm 2。

## 参考链接
- 本地 PDF: `D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf`
- 匿名代码链接: https://anonymous.4open.science/r/PO-NAS-2953
- 本地实现: Not archived (repository not found on 2026-03-16)
