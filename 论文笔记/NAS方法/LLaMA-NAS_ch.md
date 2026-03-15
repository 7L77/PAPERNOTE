---
title: "LLaMA-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[LLaMA-NAS]]"
source_paper: "LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models"
source_note: "[[LLaMA-NAS]]"
authors: [Anthony Sarah, Sharath Nittur Sridhar, Maciej Szankin, Sairam Sundaresan]
year: 2024
venue: arXiv
tags: [nas-method, zh, llm, peft, lora, multi-objective]
created: 2026-03-14
updated: 2026-03-14
---

# LLaMA-NAS 中文条目

## 一句话总结
> LLaMA-NAS 先训练一个 mixed-rank adapter 的超网，再用 NSGA-II 搜索精度与参数量的 Pareto 解，从而替代手工设定 LoRA rank。

## 来源
- 论文: [LLaMA-NAS: Efficient Neural Architecture Search for Large Language Models](https://arxiv.org/abs/2405.18377)
- HTML: https://arxiv.org/html/2405.18377v1
- 项目页: https://llama-nas.github.io/
- 代码入口: https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning
- 英文方法笔记: [[LLaMA-NAS]]
- 论文笔记: [[LLaMA-NAS]]

## 适用场景
- 问题类型: LLM 适配器结构搜索与压缩部署。
- 前提假设: 可训练 one-shot 超网，且 adapter 搜索空间可离散化定义。
- 数据形态: 下游监督任务（论文中含 commonsense / math）。
- 规模与约束: 需要在有限参数预算下获得更高任务精度。
- 适用原因: 显式优化“性能-参数量”双目标，而非固定 rank。

## 不适用或高风险场景
- 不希望引入任何搜索过程，只接受固定规则。
- 任务目标不能被“精度 + 参数量”合理刻画。
- 必须要求官方代码路径与论文方法一一对应且可直接复现。

## 输入、输出与目标
- 输入: 基座 LLM、任务数据、每层 adapter rank 候选空间、搜索预算。
- 输出: Pareto 子网集合与可部署的子网选择。
- 优化目标: 提升任务性能并减少 adapter 参数。
- 核心假设: mixed-rank 超网的共享权重能近似反映候选结构优劣。

## 方法拆解

### 阶段 1: 构建并训练 mixed-rank 超网
- 每层放置多个 rank 候选 adapter，形成可弹性导出的超网。
- 通过 one-shot 训练共享参数。
- Source: Sec. 3.1

### 阶段 2: 使用 NSGA-II 做多目标搜索
- 目标 1: 任务指标最大化。
- 目标 2: adapter 参数最小化。
- Source: Sec. 3.2

### 阶段 3: 导出子网并评估
- 从 Pareto 集中选择满足预算的结构。
- 与 heuristic、LoRA、QLoRA、LoNAS 等进行对比。
- Source: Sec. 4, Table 2-5

## 伪代码
```text
Algorithm: LLaMA-NAS
Input: 基座模型 M, 数据集 D, 搜索空间 A, 搜索预算 B
Output: Pareto 子网集合 P 与部署候选

1. 构建 mixed-rank adapter 超网 S(M, A)。
   Source: Sec. 3.1
2. 在 D 上训练 S（one-shot 参数共享）。
   Source: Sec. 3.1
3. 在 A 中初始化一组候选结构种群。
   Source: Sec. 3.2
4. 计算每个候选的双目标适应度（性能、参数量）。
   Source: Sec. 3.2
5. 执行 NSGA-II 的选择/交叉/变异，迭代更新种群。
   Source: Sec. 3.2
6. 输出非支配解集合 P，并按预算选取部署子网。
   Source: Sec. 4, Table 2-5
```

## 训练流程
1. 准备任务数据并加载基座 LLM。
2. 训练 mixed-rank adapter 超网。
3. 在超网上执行 NSGA-II 搜索。
4. 导出并评估 Pareto 子网。

Sources:
- Sec. 3.1, Sec. 3.2, Sec. 4
- Table 2-5

## 推理流程
1. 从 Pareto 集按预算选子网。
2. 导出该子网 adapter。
3. 与基座模型组合后执行下游推理。

Sources:
- Sec. 4
- Source: Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给解析式。
- 空间复杂度: 论文未给解析式。
- 运行特征: one-shot 训练摊销了大量候选结构评估成本。
- 扩展性: 多数设置下比 heuristic 更优，但具体权衡仍依赖任务。

## 实现备注
- 方法主体（mixed-rank super-network + NSGA-II）在论文中较清晰。
- 截至 2026-03-14，项目页代码入口指向 IntelLabs 集合仓，未直接定位到同名 LLaMA-NAS 子目录。
- 因此当前条目以论文为主，代码链接作为官方入口保留。

## 与相关方法关系
- 对比 [[Low-Rank Adapter]]: 不再固定统一 rank，而是结构搜索 rank 组合。
- 对比 [[Parameter-Efficient Fine-Tuning]] 启发式: 输出 Pareto 解集，部署更灵活。
- 主要优势: 在精度-参数量上可显式权衡。
- 主要代价: 需要搜索预算，且复现受代码可得性影响。

## 证据与可溯源性
- 关键图: Fig. 1-3
- 关键表: Table 2-5
- 关键公式: 多目标优化描述（Sec. 3.2）
- 关键算法: NSGA-II（Sec. 3.2）

## 参考链接
- arXiv: https://arxiv.org/abs/2405.18377
- HTML: https://arxiv.org/html/2405.18377v1
- 项目页: https://llama-nas.github.io/
- 代码: https://github.com/IntelLabs/Hardware-Aware-Automated-Machine-Learning
- 本地实现: D:/PRO/essays/code_depots/LLaMA-NAS Efficient Neural Architecture Search for Large Language Models
