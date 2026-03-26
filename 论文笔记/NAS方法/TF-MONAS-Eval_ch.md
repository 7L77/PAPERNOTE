---
title: "TF-MONAS-Eval_ch"
type: method
language: zh-CN
source_method_note: "[[TF-MONAS-Eval]]"
source_paper: "Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training"
source_note: "[[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]"
authors: [Can Do, Ngoc Hoang Luong, Quan Minh Phan]
year: 2025
venue: RIVF
tags: [nas-method, zh, evolutionary-nas, training-free-metrics, adversarial-robustness]
created: 2026-03-25
updated: 2026-03-25
---

# TF-MONAS-Eval 中文条目

## 一句话总结
> 这是一个“评测流程方法”：在对抗训练基准下，比较训练式目标与训练自由目标在 GA/NSGA-II 中搜索鲁棒架构的效果与成本。

## 来源
- 论文: [Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks under Adversarial Training](https://doi.org/10.1109/RIVF68649.2025.11365115)
- PDF: `D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf`
- 代码: 论文未给出官方仓库
- 英文方法笔记: [[TF-MONAS-Eval]]
- 论文笔记: [[Empirical Evaluation of Evolutionary NAS with Training-Free Metrics for Discovering Robust Networks Under Adversarial Training]]

## 适用场景
- 问题类型: 在鲁棒 NAS 中比较“搜索目标设计”而非提出新搜索器。
- 前提假设: 可访问 NAS-Bench-201 / NAS-RobBench-201 / NAS-Bench-Suite-Zero 这类基准查询。
- 数据形态: 图像分类（CIFAR-10/100, ImageNet16-120）。
- 规模与约束: 适合算力有限但希望做可靠对比实验的场景。
- 适用原因: 通过 benchmark query 替代全量训练，快速比较 objective 的优劣。

## 不适用或高风险场景
- 你需要在全新搜索空间做在线训练式 NAS。
- 你需要的是新算法创新而不是实验评估框架。
- 你要研究非图像任务且缺少对应鲁棒基准。

## 输入、输出与目标
- 输入: 搜索目标（Val-Acc-12 或 SynFlow）、搜索器（GA 或 NSGA-II）、预算。
- 输出: 每个变体得到的代表架构及其 clean/robust 指标、成本对比结果。
- 优化目标: 找到在对抗训练评测条件下更优的 objective+optimizer 组合。
- 核心假设: NAS-RobBench-201 的指标能代表对抗训练后的模型排序趋势。

## 方法拆解

### 阶段 1: 在 NAS-Bench-201 上运行 4 个 ENAS 变体
- `GA (Val-Acc-12)`、`GA (SynFlow)`、`NSGA-II (Val-Acc-12)`、`NSGA-II (SynFlow)`。
- 统一超参: population=20, eval budget=3000, crossover=0.9, mutation=1/l。
- Source: Sec. III-A, Fig. 3

### 阶段 2: 查询对抗训练后的评测指标
- 从 NAS-RobBench-201 读取 clean 和多攻击下精度（FGSM/PGD/AutoAttack）。
- Source: Sec. III-A, Sec. III-B/C

### 阶段 3: 为 MONAS 选择代表解
- NSGA-II 返回解集，按多条件总排名选一个代表架构用于横向比较。
- Source: Sec. III-A（CEC 2024 ranking rule）

### 阶段 4: 统计比较与效率分析
- 31 次独立运行，t-test (`p<0.01`)。
- 比较效果和搜索成本。
- Source: Sec. III, Table I, Table II

## 伪代码
```text
Algorithm: TF-MONAS-Eval
Input: 搜索空间 A, 目标集合 O={Val-Acc-12, SynFlow}, 搜索器 E={GA, NSGA-II}, 预算 T
Output: 对比报告 R

1. 对每个 (e,o) in E x O 运行 ENAS 搜索，预算为 T。
   Source: Sec. III-A, Fig. 3
2. 收集每次运行得到的架构（或架构集合）。
   Source: Sec. III-A
3. 查询 NAS-RobBench-201 中 clean 与攻击精度。
   Source: Sec. III-A, Sec. III-B/C
4. 若 e=NSGA-II，则按多条件总排名选代表解。
   Source: Sec. III-A (CEC 2024 ranking rule)
5. 重复 31 次，统计 mean/std 并做显著性检验。
   Source: Sec. III-A
6. 输出 SONAS 与 MONAS 最优组合及成本差异。
   Source: Table I, Table II, Sec. III-B/C
```

## 训练流程
1. 基于 benchmark 提供的目标值/代理值打分。
2. 执行 GA/NSGA-II 进化搜索。
3. 收集候选架构。
4. 在鲁棒 benchmark 协议下读取 clean/attack 指标。

Sources:
- Sec. II-A, Sec. III-A

## 推理/使用流程
1. 选择目标与搜索器组合。
2. 跑 benchmark-based 搜索。
3. 读取候选架构鲁棒画像。
4. 按部署偏好选型（偏 clean 或偏 robust）。

Sources:
- Sec. III-A, Sec. III-B/C

## 复杂度与效率
- 每次运行评估预算: 3,000。
- 训练式目标显著更贵；文中报告 `GA (Val-Acc-12)` 成本超过 `GA (SynFlow)` 11 倍。
- 论文未给闭式复杂度公式。

## 实现备注
- 论文重点是“目标函数在鲁棒评测条件下的表现差异”，不是新网络结构。
- 在 AT 条件下，最高 SynFlow 不必然对应最高鲁棒精度。
- 多目标解集多样性是 `NSGA-II (SynFlow)` 关键优势来源。

## 与相关方法关系
- 对比单目标 TF 搜索: 仅凭单一 TF 指标可能不足以稳定命中最鲁棒架构。
- 对比训练式 MONAS: TF-MONAS 在该基准下可同时获得更好效果和更低成本。
- 主要优势: 给出可执行的 objective 选择建议。
- 主要代价: 结论依赖于当前 benchmark 设定与算法集合。

## 证据与可溯源性
- 关键图: Fig. 3, Fig. 4, Fig. 5
- 关键表: Table I, Table II
- 关键公式: Eq. (1)-(7)
- 关键算法: GA / NSGA-II（Sec. II-A）

## 参考链接
- DOI: https://doi.org/10.1109/RIVF68649.2025.11365115
- PDF: D:/PRO/essays/papers/Empirical_Evaluation_of_Evolutionary_NAS_with_Training-Free_Metrics_for_Discovering_Robust_Networks_Under_Adversarial_Training.pdf
- 代码: Not officially linked
- 本地实现: Not archived

