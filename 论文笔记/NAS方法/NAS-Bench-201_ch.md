---
title: "NAS-Bench-201_ch"
type: method
language: zh-CN
source_method_note: "[[NAS-Bench-201]]"
source_paper: "NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search"
source_note: "[[NAS-Bench-201]]"
authors: [Xuanyi Dong, Yi Yang]
year: 2020
venue: ICLR
tags: [nas-method, zh, benchmark, reproducibility, cell-based-nas]
created: 2026-03-17
updated: 2026-03-17
---

# NAS-Bench-201 中文条目

## 一句话总结
> NAS-Bench-201 的核心是把 NAS 对比变成“统一协议下的查表问题”：先穷举并评测 `5^6=15625` 个 cell 架构，再通过 API 查询结果评估搜索算法。

## 来源
- 论文: [NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search](https://arxiv.org/abs/2001.00326)
- HTML: https://arxiv.org/html/2001.00326
- 代码: https://github.com/D-X-Y/NAS-Bench-201
- 英文方法笔记: [[NAS-Bench-201]]
- 论文笔记: [[NAS-Bench-201]]

## 适用场景
- 问题类型: 需要可复现、公平地比较 NAS 搜索算法。
- 前提假设: 方法可在离散 cell 搜索空间上运行。
- 数据形态: 离线 benchmark 查询，或基于查询的模拟搜索。
- 规模与约束: 15,625 候选架构，预先计算好性能与成本指标。
- 适用原因: 可把“算法优劣”与“重复训练成本”分离。

## 不适用或高风险场景
- 需要直接结论覆盖超大搜索空间且无法做迁移验证。
- 方法依赖 NAS-Bench-201 不包含的宏观搜索维度。
- 需求是重建全 benchmark，而不是使用现成 benchmark。

## 输入、输出与目标
- 输入: 架构字符串或 index、数据集、训练协议标识（12/200 epoch）。
- 输出: train/valid/test 指标、FLOPs、参数量、延迟、排名信息。
- 优化目标: 为 NAS 算法比较提供统一可复查的证据。
- 核心假设: 统一训练协议可作为稳定参考基线。

## 方法拆解

### 阶段 1：定义算法无关的 cell 搜索空间
- 4 节点 DAG cell，6 条有向边，每条边从 5 个操作中选 1 个。
- 穷举得到 `5^6=15625` 个候选。
- Source: Sec. 2.1, Fig. 1, Appendix A

### 阶段 2：全量统一评测
- 在 CIFAR-10 / CIFAR-100 / ImageNet16-120 上按统一协议训练全部候选。
- 记录逐 epoch 指标与计算成本。
- Source: Sec. 2.2-2.4, Table 1-2

### 阶段 3：API 与诊断信息发布
- 提供按架构查询指标、trial 详情和成本的 API。
- 发布可支持收敛分析/代理建模的细粒度训练信息。
- Source: Sec. 2.4, Appendix D, repository `nas_201_api`

### 阶段 4：统一基线评测
- 在同一 benchmark 协议下评测 10 类 NAS 算法。
- 分析参数共享方法、BN 统计策略与搜索速度收益。
- Source: Sec. 5, Table 4-5, Fig. 6-8, Table 7

## 伪代码
```text
Algorithm: NAS-Bench-201 构建与使用流程
Input: 操作集合 O (|O|=5), 节点数 V=4, 数据集 D={CIFAR-10, CIFAR-100, ImageNet16-120}
Output: 可查询 benchmark 表与 API

1. 构造 V=4 的有向 cell 图，共 6 条有序边。
   Source: Sec. 2.1, Fig. 1
2. 对每条边枚举 O 中操作，得到 5^6=15625 个候选。
   Source: Sec. 2.1, Appendix A
3. 对每个架构和每个数据集按统一协议训练（H†），并在 CIFAR-10 提供 H‡（12 epoch）短预算设置。
   Source: Sec. 2.3, Table 1, Appendix A
4. 记录逐 epoch train/valid/test 指标与 FLOPs/params/latency。
   Source: Sec. 2.3-2.4, Table 2
5. 打包为 API 可索引 benchmark 文件。
   Source: Appendix D, repository API (`NASBench201API`)
6. 搜索算法通过查询 benchmark 完成评估，而非重复训练每个候选。
   Source: Sec. 5, Table 4-5
```

## 训练流程
1. 固定宏观骨架与 cell 搜索空间。
2. 穷举全部架构编码。
3. 以统一超参训练（`H†`，以及用于短预算实验的 `H‡`）。
4. 保存指标与模型信息到 benchmark 文件。

Sources:
- Sec. 2.1-2.3
- Table 1-2
- Appendix A / Appendix D

## 推理流程
1. 用 benchmark 文件初始化 `NASBench201API`。
2. 按架构 index 或字符串查询。
3. 取回指标与成本并完成候选排序/比较。

Sources:
- Appendix D
- repository `README.md` and `nas_201_api/api_201.py`

## 复杂度与效率
- 时间复杂度: 基准构建阶段极重（15,625 架构全量训练）。
- 空间复杂度: benchmark 文件与可选权重归档体量大。
- 运行特征: 构建后查询成本极低，许多非参数共享方法可在秒级完成评估环节。
- 扩展性: 对更大搜索空间难以继续做全量枚举，论文将其列为限制。

## 实现备注
- API 主类: `nas_201_api/api_201.py` 的 `NASBench201API`。
- 常用文件版本: `NAS-Bench-201-v1_0-e61699.pth`、`NAS-Bench-201-v1_1-096897.pth`。
- 仓库已标注 deprecated，并推荐迁移至 NATS-Bench。
- 实践注意: 查询轻量，但完整复现实验资产下载成本较高。

## 与相关方法关系
- 对比 NAS-Bench-101: NAS-Bench-201 用 edge-op 编码并去掉 edge 数约束，对更多 NAS 算法更友好。
- 对比 [[Surrogate NAS Benchmark]]: NAS-Bench-201 在小空间里给“精确查表”，surrogate benchmark 在大空间里给“近似评估”。
- 主要优势: 可复现性强、横向比较更公平。
- 主要代价: 搜索空间表达力有限，外推需谨慎。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2-5, Fig. 6-8
- 关键表: Table 1-7
- 关键公式: 无核心新优化公式（贡献以 benchmark 设计与评测协议为主）
- 关键算法: Appendix D 的 API 查询流程与 Sec. 5 的基线评测流程

## 参考链接
- arXiv: https://arxiv.org/abs/2001.00326
- HTML: https://arxiv.org/html/2001.00326
- 代码: https://github.com/D-X-Y/NAS-Bench-201
- 本地实现: D:/PRO/essays/code_depots/NAS-Bench-201 extending the scope of reproducible neural architecture search
