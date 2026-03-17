---
title: "NADR-Dataset_ch"
type: method
language: zh-CN
source_method_note: "[[NADR-Dataset]]"
source_paper: "Neural Architecture Design and Robustness: A Dataset"
source_note: "[[NADR-Dataset]]"
authors: [Steffen Jung, Jovita Lukasik, Margret Keuper]
year: 2023
venue: ICLR
tags: [nas-method, zh, robustness-dataset, benchmark, adversarial-robustness]
created: 2026-03-17
updated: 2026-03-17
---

# NADR-Dataset 中文条目

## 一句话总结

> NADR-Dataset 把 NAS-Bench-201 的完整非同构架构空间做了对抗攻击和常见腐蚀的全量评测，产出可查询的结构化鲁棒性基准数据。

## 来源

- 论文: [Neural Architecture Design and Robustness: A Dataset](https://openreview.net/forum?id=p8coElqiSDw)
- HTML: http://robustness.vision/
- 代码: https://github.com/steffen-jung/robustness-dataset
- 数据: http://data.robustness.vision/
- 英文方法笔记: [[NADR-Dataset]]
- 论文笔记: [[NADR-Dataset]]

## 适用场景

- 问题类型: robust NAS、鲁棒代理指标、架构鲁棒性相关性分析。
- 前提假设: 可以接受“固定搜索空间 + 离线全量评测”范式。
- 数据形态: 预训练架构 + 后处理攻击/腐蚀评估结果。
- 规模与约束: 适合需要大量架构-鲁棒标签对、但不想反复重训的场景。
- 适用原因: 将昂贵评测前置，后续算法迭代成本显著降低。

## 不适用或高风险场景

- 需要在新搜索空间实时训练与评估。
- 需要超出数据集已有攻击/腐蚀范围的鲁棒定义。
- 需要完整训练流水日志，而不仅是最终评测张量。

## 输入、输出与目标

- 输入: 架构集合 `A`、数据集集合 `D`、攻击/腐蚀集合 `C`、预训练权重。
- 输出: 按 `(dataset, key, architecture[, epsilon/severity])` 索引的 `accuracy/confidence/cm` JSON。
- 优化目标: 形成可复用、可比较的架构鲁棒基准。
- 核心假设: 统一协议下的全量评测能提供稳定的跨方法比较基础。

## 方法拆解

### 阶段 1: 枚举并规范化架构

- 从 NAS-Bench-201 枚举架构，并保留 6,466 个非同构架构。
- 维护同构映射，确保统计口径一致。
- Source: Sec. 3.1, Appx A.1, Fig. 8

### 阶段 2: 加载预训练权重

- 对每个架构和每个数据源加载对应 checkpoint。
- 评测数据源包括 CIFAR-10 / CIFAR-100 / ImageNet16-120。
- Source: Sec. 3.1, Alg. 1

### 阶段 3: 对抗评测

- 执行 FGSM、PGD、APGD-CE、Square 多 epsilon 评测。
- 记录准确率、置信度矩阵、混淆矩阵。
- Source: Sec. 3.2, Eq. (1)-(3), Table 2, Fig. 2-3

### 阶段 4: 腐蚀评测

- 在 CIFAR-10-C / CIFAR-100-C 上评测 15 类腐蚀 x 5 级强度。
- 记录与对抗评测一致的三类结果。
- Source: Sec. 3.3, Fig. 4-5

### 阶段 5: 数据落盘与元信息维护

- 文件命名采用 `{key}_{measurement}.json`。
- `meta.json` 维护架构字符串、同构映射、epsilon 网格。
- Source: Appx A.3-A.4, Table 3-4, Fig. 10-11

## 伪代码

```text
Algorithm: Robustness Dataset Gathering (NADR-Dataset)
Input: Architecture space A, datasets D, attacks/corruptions C, result store R
Output: Structured robustness benchmark files

1. For each architecture a in A:
   load pretrained weights for a on each dataset d.
   Source: Alg. 1, line 1-3; Sec. 3.1
2. For each dataset d in D:
   For each corruption/attack operator c in C:
      construct transformed evaluation data d_c from d.
      Source: Alg. 1, line 4-5; Sec. 3.2/3.3
3. Evaluate model a on d_c and collect:
   Accuracy, Confidence, ConfusionMatrix.
   Source: Alg. 1, line 6
4. Write outputs into nested result dictionary:
   R[d][c]["accuracy"][a], R[d][c]["confidence"][a], R[d][c]["cm"][a].
   Source: Alg. 1, line 7-9
5. Export JSON files by key and measurement; keep metadata for id/isomorph/eps.
   Source: Appx A.4, Table 3-4, Fig. 10-11
```

## 训练流程

1. 使用 NAS-Bench-201 既有训练协议得到预训练模型。
2. 固定权重后做攻击/腐蚀 sweep，避免训练变量干扰。
3. 聚合三类评测信号（accuracy/confidence/cm）。
4. 发布数据快照与查询接口供下游研究复用。

Sources:

- Sec. 3.1-3.3, Appx A.2-A.4.

## 推理流程

1. 初始化 `RobustnessDataset(path=...)`。
2. 通过 `query(data, key, measure)` 取目标子集。
3. 使用 `get_uid()` 映射到非同构 canonical id。
4. 把结果送入排序、相关性、NAS 搜索模拟等下游模块。

Sources:

- `robustness_dataset.py` (`query`, `get_uid`, `id_to_string`, `string_to_id`)
- Appx A.4

## 复杂度与效率

- 时间复杂度: 近似 `|A| x |D| x |C| x eval_cost`。
- 空间复杂度: 与全量评测张量存储规模线性相关。
- 运行特征: 数据构建期需要集群级算力；构建完成后下游实验非常快。
- 扩展性说明: 适合“高前置成本，低复用成本”的研究工作流。

## 实现备注

- helper 代码中攻击 key 含 `@Linf` 后缀，便于区分范数设定。
- `missing_ok=True` 可在缺文件场景下做鲁棒查询。
- `ImageNet16-120` 默认不含 common corruption 结果（在 helper 内显式跳过）。
- `meta.json` 的同构映射需要在分析时显式处理，否则会重复计数。
- 论文-代码差异: 公开仓库强调“数据读取”；完整采集流水线并未完整开源。

## 与相关方法关系

- 对比 [[NAS-Bench-201]]: 从 clean 扩展到鲁棒维度。
- 对比 [[RobustBench]]: 覆盖完整架构空间而非只做模型榜单对比。
- 主要优势: 不重训即可做可复现实验和公平比较。
- 主要代价: 基准边界受限于搜索空间和攻击设置。

## 证据与可溯源性

- 关键图: Fig. 1-7, Fig. 9-11
- 关键表: Table 1-4
- 关键公式: Eq. (1)-(4)
- 关键算法: Algorithm 1 (Appx A.2)

## 参考链接

- OpenReview: https://openreview.net/forum?id=p8coElqiSDw
- 项目页: http://robustness.vision/
- 代码: https://github.com/steffen-jung/robustness-dataset
- 数据: http://data.robustness.vision/
- 本地实现: D:/PRO/essays/code_depots/Neural architecture design and robustness a dataset

