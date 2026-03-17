---
title: "NAS-RobBench-201_ch"
type: method
language: zh-CN
source_method_note: "[[NAS-RobBench-201]]"
source_paper: "Robust NAS benchmark under adversarial training: assessment, theory, and beyond"
source_note: "[[NAS-RobBench-201]]"
authors: [Yongtao Wu, Fanghui Liu, Carl-Johann Simon-Gabriel, Grigorios G. Chrysos, Volkan Cevher]
year: 2024
venue: ICLR
tags: [nas-method, zh, robust-nas, benchmark, adversarial-training, ntk]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-RobBench-201 中文条目

## 一句话总结
> NAS-RobBench-201 把 NAS-Bench-201 的 6466 个非同构架构在对抗训练下系统化评估，形成可查询的鲁棒 NAS 基准，并给出与 NTK 相关的理论解释。

## 来源
- 论文: [Robust NAS benchmark under adversarial training: assessment, theory, and beyond](https://openreview.net/forum?id=cdUpf6t6LZ)
- 项目页: https://tt2408.github.io/nasrobbench201hp/
- 代码: https://github.com/TT2408/nasrobbench201
- 英文方法笔记: [[NAS-RobBench-201]]
- 论文笔记: [[NAS-RobBench-201]]

## 适用场景
- 问题类型: 在固定 cell-based 搜索空间中做鲁棒架构评估与搜索。
- 前提假设: 接受 NAS-Bench-201 搜索空间与论文威胁模型设定。
- 数据形态: 监督视觉分类 + 对抗训练。
- 规模与约束: 适合“离线一次性构建，在线频繁查询”的流程。
- 适用原因: 可以把 NAS 算法比较从“重复重训”转为“同基准查表评估”。

## 不适用或高风险场景
- 目标搜索空间不是 NAS-Bench-201（如 Transformer/LLM 架构搜索）。
- 需要全新威胁模型或未覆盖攻击设定下的严格结论。
- 主要优化目标是硬件延迟/功耗而非鲁棒准确率。

## 输入、输出与目标
- 输入: 架构 ID、数据集、攻击/训练超参、随机种子。
- 输出: 每个架构在 clean 与多种 robust 指标下的结果。
- 优化目标: 构建可复现 robust NAS benchmark，并解释 robust 搜索与 NTK 的关系。
- 核心假设: multi-objective adversarial training 可由混合 NTK 视角分析。

## 方法拆解

### 阶段 1：枚举与训练
- 从 NAS-Bench-201 中枚举 6466 个非同构架构。
- 对每个架构做对抗训练，并跨数据集/种子重复。
- Source: Sec. 3.1 / Fig. 1

### 阶段 2：评估与入库
- 统一评估 clean、FGSM、PGD、APGD/AutoAttack。
- 结果写入可查询 benchmark 表。
- Source: Sec. 3.1-3.2 / Table 1-2

### 阶段 3：理论与 train-free 线索
- 使用 Eq. (3) 的 multi-objective 损失建模训练目标。
- 构建 Eq. (4)/(5) 的混合核，给出 Theorem 1 与 Corollary 1。
- 在 Fig. 5 中分析 NTK-score 与鲁棒指标相关性。
- Source: Sec. 4 / Eq. (3)-(6) / Theorem 1 / Corollary 1 / Fig. 5

## 伪代码
```text
Algorithm: Build-and-Use NAS-RobBench-201
Input: 搜索空间 S, 数据集 D, 对抗训练器 A_eps, 权重 beta, 种子集合 R
Output: 基准表 B

1. 从 NAS-Bench-201 枚举非同构架构集合 S'（|S'|=6466）。
   Source: Sec. 3.1
2. 对每个 a in S', d in D, r in R:
   用 L=(1-beta)L_clean + beta L_robust 进行对抗训练。
   Source: Sec. 3.1 / Eq. (3)
3. 在 clean + FGSM/PGD (+ APGD/AutoAttack) 上评估并记录指标。
   Source: Sec. 3.1
4. 将结果写入 benchmark 表 B，用于后续 NAS 查表搜索。
   Source: Sec. 3.2 / Table 2
5. 可选：计算 clean/robust/twice-perturbation NTK 分数做训练前筛选。
   Source: Sec. 4.2-4.3 / Eq. (4)-(5) / Fig. 5
```

## 训练流程
1. 数据预处理与增强。
2. 固定超参对抗训练（逐架构）。
3. 多种子重复。
4. 汇总多攻击指标。

Sources:
- Sec. 3.1
- Table 1-2

## 推理/使用流程
1. 给定候选架构或搜索策略。
2. 直接查询 benchmark 获取鲁棒指标。
3. 按目标指标（如 PGD 8/255）排序并选型。
4. 必要时再对 Top-K 做额外验证训练。

Sources:
- Sec. 3.2
- Table 2 / Table 7

## 复杂度与效率
- 构建成本: 约 107k GPU hours（一次性重投入）。
- 查询成本: 构建后接近 O(1) 查表。
- 运行特征: 离线重、在线轻。
- 扩展性: 攻击强度和数据集数增加会显著放大离线成本。

## 实现备注
- 搜索算子: 3x3 conv / 1x1 conv / zeroize / skip / 1x1 avg pool。
- 训练设置（文中）: PGD-7, eps=8/255, step=2/255, 50 epochs, batch=256。
- 评估设置: FGSM/PGD（eps in {3/255, 8/255}）+ AutoAttack。
- NTK 分析: 采用与最小特征值相关的近似分数用于相关性分析。

## 与相关方法关系
- 对比 [[NAS-Bench-201]]: 增加了“对抗训练后”的鲁棒指标维度。
- 对比 [[RobustBench]]: 面向 NAS 查表评估流程，而非通用模型榜单。
- 主要优势: 可复现 robust NAS 基准 + 理论支撑。
- 主要代价: 搜索空间限定、一次性构建成本高。

## 证据与可溯源
- 关键图: Fig. 1-5
- 关键表: Table 1, Table 2, Table 6, Table 7
- 关键公式: Eq. (3), Eq. (4), Eq. (5), Eq. (6)
- 关键算法: Algorithm 1

## 参考链接
- OpenReview: https://openreview.net/forum?id=cdUpf6t6LZ
- Project: https://tt2408.github.io/nasrobbench201hp/
- Code: https://github.com/TT2408/nasrobbench201
- 本地实现: D:/PRO/essays/code_depots/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond

