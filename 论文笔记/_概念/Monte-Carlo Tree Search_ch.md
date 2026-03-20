---
type: concept
language: zh-CN
source_concept_note: "[[Monte-Carlo Tree Search]]"
aliases: [蒙特卡洛树搜索, MCTS]
---

# Monte-Carlo Tree Search 中文条目

## 一句话直觉
MCTS 是“边试边学”的树搜索：既优先走看起来更好的分支，也会给不确定分支保留探索机会。

## 为什么重要
在离散组合空间里，它能避免全量穷举，常用来做高效搜索与规划。

## 小例子
在 NAS 里，很多架构分支初期都不确定；MCTS 会先广泛尝试，再逐步把预算集中到回报更高的分支。

## 定义
经典 MCTS 包含选择、扩展、模拟、回传四步。对于已完全展开的 NAS 树，扩展/模拟可被简化。

## 核心要点
1. 依赖访问次数与奖励统计来驱动搜索。
2. 树结构质量直接影响效率和最终结果。
3. 常与 UCB/UCT 类探索项结合。

## 在本文中的作用
- [[MCTS-Learned Hierarchy]] 在学习得到的层级树上执行 MCTS，并用 Eq.(2-4) 的奖励更新进行训练与搜索。

## 代表工作
- Kocsis and Szepesvari (2006)
- Wang et al. (2021a)
- Su et al. (2021a)

## 相关概念
- [[Upper Confidence Bound (UCB)]]
- [[Multi-Armed Bandit]]
- [[Neural Architecture Search]]
