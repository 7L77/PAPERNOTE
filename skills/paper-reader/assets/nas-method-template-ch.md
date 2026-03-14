---
title: "{MethodName}_ch"
type: method
language: zh-CN
source_method_note: "[[{MethodName}]]"
source_paper: "{PaperTitle}"
source_note: "[[{PaperNoteName}]]"
authors: [{Authors}]
year: {Year}
venue: {Venue}
tags: [nas-method, zh, {tag1}, {tag2}]
created: {Date}
updated: {Date}
---

# {MethodName} 中文条目

## 一句话总结

> {一句话说清楚：它在解决什么问题，核心设计是什么，为什么这样设计。}

## 来源

- 论文: [{PaperTitle}]({ArxivUrl})
- HTML: {ArxivHtmlUrl}
- 代码: {CodeUrl}
- 英文方法笔记: [[{MethodName}]]
- 论文笔记: [[{PaperNoteName}]]

## 适用场景

- 问题类型: {该方法解决什么问题}
- 前提假设: {关键假设}
- 数据形态: {离线/在线/监督/RL/合成数据等}
- 规模与约束: {节点规模、时延、内存或结构约束}
- 适用原因: {结合方法结构说明它为什么适合，而不是泛泛地说“效果更好”}

## 不适用或高风险场景

- {场景 1}
- {场景 2}
- {场景 3}

## 输入、输出与目标

- 输入: {结构化输入}
- 输出: {结构化输出}
- 优化目标: {核心目标}
- 核心假设: {必须成立的条件}

## 方法拆解

### 阶段 1: {StageName}

- {这一阶段做什么}
- Source: {Sec/Fig/Alg/Eq citations}

### 阶段 2: {StageName}

- {这一阶段做什么}
- Source: {Sec/Fig/Alg/Eq citations}

## 伪代码

```text
Algorithm: {MethodName}
Input: {Inputs}
Output: {Outputs}

1. {步骤 1}
   Source: {Sec/Fig/Alg/Eq}
2. {步骤 2}
   Source: {Sec/Fig/Alg/Eq}
3. {步骤 3}
   Source: {Sec/Fig/Alg/Eq}
4. {如果某步是根据论文推断得到，明确标注}
   Source: Inference from source
```

<!-- 伪代码要和上面的阶段拆解一一对应，优先复用论文里的模块名、状态量、优化步骤。 -->

## 训练流程

1. {数据生成/预处理}
2. {前向过程}
3. {损失与监督}
4. {优化细节}

Sources:

- {Sec/Fig/Alg/Eq citations}

## 推理流程

1. {推理步骤 1}
2. {推理步骤 2}
3. {后处理 / 优化步骤}

Sources:

- {Sec/Fig/Alg/Eq citations}

## 复杂度与效率

- 时间复杂度: {若论文提供}
- 空间复杂度: {若论文提供}
- 运行特征: {论文报告的 wall-clock / 瓶颈}
- 扩展性说明: {随规模变化的行为}

## 实现备注

- 架构: {编码器/解码器/主干/模块}
- 超参数: {最重要的超参数}
- 约束 / masking: {可行性逻辑}
- 技巧: {损失平衡、搜索、奖励 shaping 等}
- 注意事项: {实现坑点}

## 与相关方法的关系

- 对比 [[{Baseline1}]]: {关键差异}
- 对比 [[{Baseline2}]]: {关键差异}
- 主要优势: {方法价值}
- 主要代价: {权衡}

## 证据与可溯源性

- 关键图: {Figure references}
- 关键表: {Table references}
- 关键公式: {Equation references}
- 关键算法: {Algorithm references}

## 参考链接

- arXiv: {ArxivUrl}
- HTML: {ArxivHtmlUrl}
- 代码: {CodeUrl}
- 本地实现: {LocalCodePath or "Not archived"}
