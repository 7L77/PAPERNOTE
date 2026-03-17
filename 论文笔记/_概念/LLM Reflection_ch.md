---
type: concept
language: zh-CN
source_concept_note: "[[LLM Reflection]]"
aliases: [LLM反思, LLM Self-Reflection]
---

# LLM Reflection 中文条目

## 一句话直觉
LLM Reflection 就是“做完一步先复盘，再给下一步建议”的机制。

## 为什么重要
在有约束的生成任务中（如 NAS 架构变异），它能把错误信息转成下一轮可执行改进，减少无效输出。

## 小例子
如果当前变异结构超过 `MAX_LAYERS`，反思模块会提示“减少层数或替换为更轻量操作”，下一轮更容易生成合法结构。

## 更正式定义
LLM Reflection 是一种把历史输出质量信号（分数、异常、约束冲突）反馈到后续生成中的迭代优化机制。

## 核心要点
1. 反思可显著降低结构化任务中的异常率。
2. 反思把“试错”变成“有记忆的搜索”。
3. 反馈信号质量直接决定反思效果。

## 这篇论文怎么用
- [[RZ-NAS]]：输入“变异前后结构 + proxy 分数 + 异常信息”，生成下一轮变异提示。

## 代表工作
- [[RZ-NAS]]
- [[Reflexion]]

## 相关概念
- [[LLM-guided Search]]
- [[In-context Learning]]
- [[Zero-Cost Proxy]]
