---
type: concept
language: zh-CN
source_concept_note: "[[Upper Confidence Bound (UCB)]]"
aliases: [上置信界, UCB]
---

# Upper Confidence Bound (UCB) 中文条目

## 一句话直觉
UCB 给每个选项一个“乐观分数”：历史均值 + 不确定性奖励，试得少的选项会被额外鼓励。

## 它为什么重要
它在 bandit 中能稳定地实现探索与利用平衡，并有经典理论保证。

## 一个小例子
两个操作当前平均精度差不多，但其中一个只试过几次，UCB 会给它更高探索奖励，避免被过早忽略。

## 更正式的定义
常见形式：
\[
\hat{r}_k + \sqrt{\frac{2\log N}{n_k}}
\]
其中 `hat{r}_k` 是经验均值，`n_k` 是第 `k` 个臂被选择次数，`N` 是总轮次。

## 数学形式（如有必要）
当 `n_k` 增大时，探索项衰减；当 `N` 增大时，探索需求缓慢增长。

## 核心要点
1. 通过“乐观估计”实现探索。
2. 少样本臂会自动得到更多机会。
3. 常数项可按任务规模调节。

## 这篇论文里怎么用
- [[ABanditNAS]]: 用 UCB 做“淘汰判据”（剪掉最小 UCB 的操作），而不是传统的“选最大 UCB 操作”。

## 代表工作
- Auer et al. (2002): 经典 UCB。
- UCT/MCTS 系列工作中的 UCB 应用。

## 相关概念
- [[Multi-Armed Bandit]]
- [[Lower Confidence Bound (LCB)]]
- [[ABanditNAS]]

