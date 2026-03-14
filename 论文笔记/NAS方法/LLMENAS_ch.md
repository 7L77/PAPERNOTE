---
title: "LLMENAS_ch"
type: method
language: zh-CN
source_method_note: "[[LLMENAS]]"
source_paper: "LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance"
source_note: "[[LLMENAS]]"
authors: [Xu Zhai, Xiaoyan Sun, Huan Zhao, Shengcai Liu, Rongrong Ji]
year: 2025
venue: arXiv
tags: [nco-method, zh, nas, llm, evolutionary-search]
created: 2026-03-13
updated: 2026-03-13
---

# LLMENAS 中文条目

## 一句话总结
> LLMENAS 把传统进化 NAS 的交叉和变异替换为 LLM 引导的结构编辑，并结合 one-shot 与代理预测器，在更低搜索成本下找到更优架构。

## 来源
- 论文: [LLMENAS: Evolutionary Neural Architecture Search via Large Language Model Guidance](https://arxiv.org/abs/2501.13154)
- HTML: https://arxiv.org/html/2501.13154v2
- 代码: https://github.com/LLMENAS/LLMENAS
- 英文方法笔记: [[LLMENAS]]
- 论文笔记: [[LLMENAS]]

## 适用场景
- 问题类型: 图像分类任务上的 cell-based NAS。
- 前提假设: 架构可被编码为可编辑的离散 token/结构描述。
- 数据形态: 监督学习（文中主要为 CIFAR-10 与 ImageNet-16-120）。
- 规模与约束: 搜索预算有限、无法对大量候选做完整训练时。
- 适用原因: LLM 提升候选生成质量，one-shot/代理评估降低评估开销。

## 不适用或高风险场景
- 不能接入外部 LLM（成本、延迟或安全限制）。
- 搜索空间无法被稳定序列化到 prompt。
- 任务对严格确定性复现要求极高，不能接受 LLM 采样波动。

## 输入、输出与目标
- 输入: 种群架构、交叉概率 `p_c`、变异率 `p_m`、历史统计 `H=[f_best,f_avg,f_min]`。
- 输出: 最优架构 genotype/cell。
- 优化目标: 在给定预算下最大化目标精度。
- 核心假设: LLM 生成的结构编辑有意义，代理评分与最终精度相关。

## 方法拆解

### 阶段 1: 种群初始化
- 在 cell-based 搜索空间构造初始种群。
- Source: Sec. 4.1, Eq. (1)

### 阶段 2: LLM 引导交叉
- 用 prompt 约束 LLM 融合父代优点，生成后代。
- Source: Sec. 4.2, Eq. (3), Fig. 2

### 阶段 3: LLM 引导变异
- 将历史统计 `H` 输入 prompt，对后代架构做定向变异。
- Source: Sec. 4.2, Eq. (4), Eq. (5)

### 阶段 4: 快速评估
- 使用 one-shot 与代理预测器快速估计候选性能。
- Source: Sec. 4.3, Sec. 4.4, Eq. (6)

### 阶段 5: 选择与迭代
- 按评分/验证结果更新种群并循环搜索。
- Source: Sec. 4.5, Algorithm 1

## 伪代码
```text
Algorithm: LLMENAS
Input: 初始种群 P, 交叉率 p_c, 变异率 p_m, 最大代数 G_max
Output: 最优架构 P*

1. 在 NAS 搜索空间中初始化种群 P
   Source: Sec. 4.1, Eq. (1)
2. 对每一代 g=1..G_max:
   2.1 选择父代架构 P^A, P^B
       Source: Sec. 4.2
   2.2 执行 LLM 交叉: G^C = LLM_Crossover(P^A, P^B, p_c)
       Source: Eq. (3), Fig. 2
   2.3 构造历史上下文 H=[f_best,f_avg,f_min]，执行 LLM 变异:
       G^M = LLM_Mutation(G^C, p_m, H)
       Source: Eq. (4), Eq. (5)
   2.4 用 one-shot/代理模型快速评估: s = g_phi(E(P))
       Source: Sec. 4.3-4.4, Eq. (6)
   2.5 根据适应度选择下一代种群
       Source: Sec. 4.5, Algorithm 1
3. 输出最终最优架构
   Source: Eq. (7)
```

## 训练流程
1. 搜索阶段: LLM 引导进化 + 快速评估循环。
2. 导出最优 genotype。
3. 对最终架构做标准训练/评测。
4. 汇报常规精度与鲁棒性指标。

Sources:
- Sec. 4, Sec. 5, Tab. 1/2/4/5

## 推理流程
1. 固定最终搜索得到的架构。
2. 对输入图像执行标准前向推理。
3. 鲁棒性测试时按 PGD 协议生成对抗样本后评估。

Sources:
- Sec. 5.1-5.2, Tab. 4

## 复杂度与效率
- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: 报告约 340 样本、0.6 GPU days 搜索成本。
- 扩展性说明: 相比 direct-search 基线，样本与成本显著下降。

## 实现备注
- 架构与算子代码: `model_search.py`, `operations.py`, `genotypes.py`。
- 评估脚本: `train.py`, `test.py`。
- 公开代码关键配置: `epochs=600`, `init_channels=36`, `layers=20`, SGD + cosine LR。
- 注意: 当前公开仓主要是评估链路，LLM 搜索主流程并未完整公开（README 已注明）。
- Paper/code 差异: LLM 操作细节主要依据论文文本整理。

## 与相关方法关系
- 对比 [[Evolutionary Neural Architecture Search]]: 用 LLM 替代人工交叉/变异规则。
- 对比 [[One-shot NAS]]: 保留权重共享效率，同时增强候选生成质量。
- 主要优势: 更优搜索质量-成本折中。
- 主要代价: 依赖 LLM 质量与调用成本。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 4
- 关键表: Tab. 1, Tab. 2, Tab. 4, Tab. 5
- 关键公式: Eq. (1)-(7)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2501.13154
- HTML: https://arxiv.org/html/2501.13154v2
- 代码: https://github.com/LLMENAS/LLMENAS
- 本地实现: D:/PRO/essays/code_depots/LLMENAS Evolutionary Neural Architecture Search via Large Language Model Guidance

