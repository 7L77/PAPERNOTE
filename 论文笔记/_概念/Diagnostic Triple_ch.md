---
type: concept
language: zh-CN
source_concept_note: "[[Diagnostic Triple]]"
aliases: [诊断三元组, Problem-Suggestion-Outcome]
---

# Diagnostic Triple 中文条目

## 一句话直觉
Diagnostic Triple 把每次迭代写成“问题-建议-结果”三段式，让系统不仅知道分数，还知道因果。

## 它为什么重要
只有准确率曲线很难回答“为什么这次失败”。三元组能把失败原因和修复动作绑定，减少重复无效搜索。

## 一个小例子
`problem=输出类别维度错误, suggestion=重写分类头, outcome=通过校验但精度提升有限`。

## 更正式的定义
每个条目都是
\[
(problem_i,\ suggestion_i,\ outcome_i)
\]
用于描述一次改进尝试及其反馈。

## 核心要点
1. 不只记“分数”，还记“原因和动作”。
2. 失败案例可复用，避免被当作噪声直接丢弃。
3. 便于人工审计和后续可解释分析。

## 这篇论文里怎么用
- [[Iterative LLM-Based NAS with Feedback Memory]]: 在 Eq. (3) 中显式定义并作为历史记忆的基本单元。

## 代表工作
- [[Iterative LLM-Based NAS with Feedback Memory]]: 将诊断三元组用于 LLM-NAS 闭环反馈。

## 相关概念
- [[Historical Feedback Memory]]
- [[LLM Reflection]]
- [[One-Epoch Proxy Evaluation]]
