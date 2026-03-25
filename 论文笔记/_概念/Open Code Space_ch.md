---
type: concept
language: zh-CN
source_concept_note: "[[Open Code Space]]"
aliases: [开放代码空间, Unconstrained Code Space]
---

# Open Code Space 中文条目

## 一句话直觉
Open Code Space 指的是“直接生成可执行代码作为候选架构”，而不是在固定 cell/算子清单里做组合。

## 它为什么重要
它给了 NAS 更高的结构表达自由度，能探索固定编码空间难以表示的网络形态。

## 一个小例子
在 cell-based 搜索里你只能从预设操作里选边；在开放代码空间里你可以直接写新的分支模块或非常规层次结构。

## 更正式的定义
候选架构以可执行程序形式表示，除运行合法性外不依赖严格预定义离散结构编码的搜索空间。

## 核心要点
1. 表达能力强于固定离散 cell 空间。
2. 搜索难度更高，错误代码比例通常更大。
3. 需要配套验证机制以过滤不可执行候选。

## 这篇论文里怎么用
- [[Iterative LLM-Based NAS with Feedback Memory]]: 用 LLM 直接生成 PyTorch 架构代码，并在闭环中持续改进。

## 代表工作
- [[Iterative LLM-Based NAS with Feedback Memory]]: 明确将方法定位为开放代码空间搜索。

## 相关概念
- [[Cell-based Search Space]]
- [[LLM-guided Search]]
- [[Neural Architecture Search]]
