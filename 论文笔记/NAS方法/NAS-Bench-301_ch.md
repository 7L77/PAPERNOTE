---
title: "NAS-Bench-301_ch"
type: method
language: zh-CN
source_method_note: "[[NAS-Bench-301]]"
source_paper: "NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH"
source_note: "[[NAS-Bench-301]]"
authors: [Julien Siems, Lucas Zimmer, Arber Zela, Jovita Lukasik, Margret Keuper, Frank Hutter]
year: 2020
venue: arXiv
tags: [nas-method, zh, benchmark, surrogate-model, architecture-performance-prediction]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-Bench-301 中文条目

## 一句话总结

> NAS-Bench-301 用可学习的 surrogate 回归器替代昂贵的“真实训练评估”，把 DARTS 超大搜索空间上的 NAS 基准从“高成本单次对比”变成“低成本可重复统计对比”。

## 来源

- 论文: [NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH](https://arxiv.org/abs/2008.09777)
- HTML: https://arxiv.org/html/2008.09777
- 代码: https://github.com/automl/nasbench301
- 英文方法笔记: [[NAS-Bench-301]]
- 论文笔记: [[NAS-Bench-301]]

## 适用场景

- 问题类型: 在大规模架构空间中比较 NAS 优化器优劣。
- 前提假设: 搜索空间固定且可编码，并且有足够的架构评估样本训练 surrogate。
- 数据形态: 离线监督回归（架构 -> 性能/耗时）。
- 规模与约束: 无法穷举的超大空间（如 >10^18）。
- 适用原因: 保留优化器行为趋势的同时，把单次架构评估成本降到秒级。

## 不适用或高风险场景

- 需要每个架构“真实训练后”的精确最终指标，不接受近似误差。
- 目标任务分布与 surrogate 训练分布差异很大。
- 使用者可以读取 surrogate 内部并“反向刷榜”，而不是黑盒查询。

## 输入、输出与目标

- 输入: 架构编码（DARTS cell graph/config），以及可选的查询设置（如 ensemble 采样）。
- 输出: 预测的验证性能与预测运行时。
- 优化目标: 尽量逼近真实 benchmark 的排序和轨迹行为，同时显著降低计算成本。
- 核心假设: 架构之间存在可学习的性能规律，且采样数据对空间覆盖足够。

## 方法拆解

### 阶段 1: 构建架构评估数据集

- 从多类优化器轨迹中收集样本（RS/DE/RE/TPE/BANANAS/COMBO/DARTS/GDAS/RANDOM-WS/PC-DARTS）。
- 记录架构表示、验证误差、测试误差、运行时等标签。
- Source: Sec. 3, Table 2

### 阶段 2: 训练 surrogate 候选模型

- 训练 GIN、LGB、XGB、RF、SVR 等候选，配合 HPO。
- 用 R2 与 sparse Kendall tau 评估拟合质量与排序质量。
- Source: Sec. 4.1-4.2, Table 3, Table 6

### 阶段 3: 留一优化器外推评估

- 做 LOOO（leave-one-optimizer-out）：拿掉一种优化器轨迹再测试外推性能。
- 检查 surrogate 是否能泛化到“新优化器走到的区域”。
- Source: Sec. 4.3, Table 4

### 阶段 4: 噪声与分布建模

- 对表现最好的 surrogate 家族做深度集成（每类 10 个 base learners）。
- 与重复评估真值对比 MAE 与 KL divergence。
- Source: Sec. 4.6, Table 5

### 阶段 5: 作为 NAS 基准引擎

- 用 surrogate query 替代真实训练，得到 anytime trajectory。
- 将 surrogate 上的轨迹与真实 benchmark 轨迹比较，验证行为一致性。
- Source: Sec. 5, Fig. 9-10

## 伪代码

```text
Algorithm: NAS-Bench-301 Surrogate Benchmark
Input: 搜索空间 Lambda（DARTS）, 评估数据 D={(arch_i, y_i, t_i)}, 优化器 O
Output: surrogate 基准上的搜索轨迹与架构排序

1. 在 D 上训练多个性能 surrogate f_j，用于预测 y。
   Source: Sec. 4.1-4.2
2. 用 R2 + sKT + LOOO 选择/报告 surrogate 质量。
   Source: Table 3, Table 4
3. 训练运行时 surrogate g 预测 t。
   Source: Sec. 5, Appendix A.6.1
4. 在优化循环中以黑盒方式查询：
      query(arch) -> y_hat（来自 surrogate/ensemble） + t_hat（runtime surrogate）
   Source: Sec. 5.1
5. 重复多次运行，汇总 anytime best-so-far 轨迹，并与真实 benchmark 对比。
   Source: Fig. 9, Fig. 10
6. 禁止直接利用 surrogate embedding 做反向搜索，避免对基准过拟合。
   Source: Sec. 6
```

## 训练流程

1. 将 DARTS 架构编码为模型可用特征（GIN 图表示、树模型配置表示等）。
2. 构建 train/val/test 与优化器分层切分。
3. 对每个 surrogate 家族执行 BOHB 超参搜索。
4. 训练最终 surrogate 并评估 R2/sKT/LOOO/KL 等指标。
5. 单独训练 runtime surrogate（LGB）。

Sources:

- Sec. 4, Table 3-6
- Appendix A.2, A.6.1

## 推理流程

1. 把候选架构转为基准输入格式。
2. 查询性能 surrogate（可从 ensemble 采样预测分布）。
3. 查询 runtime surrogate。
4. 将预测值返回给 NAS 优化器继续迭代。

Sources:

- Sec. 5.1, Fig. 9
- Source: Inference from source（具体 API 以仓库实现为准）

## 复杂度与效率

- 时间复杂度: 论文未给封闭形式。
- 空间复杂度: 论文未给封闭形式。
- 运行特征: surrogate 单次查询 <1 秒；真实单架构训练约 1-2 小时。
- 扩展性: 真实 benchmark 单次轨迹成本可达 >10^7 秒（约 115 GPU 天），而 surrogate 支持多次重复统计。

## 实现备注

- 官方仓库提供 benchmark 包、示例查询与模型训练入口。
- README 给出了 v0.9/v1.0 模型与数据下载链接。
- runtime 预测模型与 accuracy surrogate 分开训练。
- 论文强调“黑盒使用准则”，避免被优化器利用 surrogate 内部结构而失真。
- 不同 surrogate 版本会影响结论可比性，论文对版本管理有明确建议。

## 与相关方法的关系

- 对比 [[NAS-Bench-201]]: NAS-Bench-301 用近似替代穷举，换来搜索空间规模与现实性。
- 对比 [[Surrogate Predictor]]: 本文把 surrogate 从“搜索辅助模块”提升为“基准设施”。
- 主要优势: 大空间、低成本、可重复、可统计比较。
- 主要代价: surrogate 近似误差与采样偏差可能影响某些优化器排序。

## 证据与可溯源性

- 关键图: Fig. 2, Fig. 7, Fig. 8, Fig. 9, Fig. 10
- 关键表: Table 2, Table 3, Table 4, Table 5, Table 6
- 关键公式: 无单一核心新公式（贡献主要是 benchmark 构建与评测协议）
- 关键算法: surrogate 训练与 benchmark 查询协议（Sec. 4-5）

## 参考链接

- arXiv: https://arxiv.org/abs/2008.09777
- HTML: https://arxiv.org/html/2008.09777
- 代码: https://github.com/automl/nasbench301
- 本地实现: D:/PRO/essays/code_depots/NAS-BENCH-301 AND THE CASE FOR SURROGATE BENCHMARKS FOR NEURAL ARCHITECTURE SEARCH
