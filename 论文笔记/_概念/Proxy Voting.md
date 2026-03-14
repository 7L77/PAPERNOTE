---
type: concept
aliases: [Voting Proxy, Ensemble of Proxies]
---

# Proxy Voting

## Intuition

单个 zero-shot proxy 往往在某些设置表现很好、在另一些设置失效。`Proxy Voting` 的想法是让多个 proxy “投票”，用组合判断替代单指标判断。

## Why It Matters

对于 NAS 这样的高噪声排序任务，proxy voting 往往比单 proxy 更稳健，尤其当搜索空间、初始化方式或数据分布变化时。

## Tiny Example

如果三个 proxy 对两个架构排序如下：

- Proxy A: A > B
- Proxy B: A > B
- Proxy C: B > A

多数投票结果仍为 A > B，从而减少单 proxy 偏差影响。

## Definition

Proxy voting 是把多个代理评分或排序通过某种聚合规则（多数票、rank aggregation、加权融合等）合并成最终排序的方法。

## Math Form (if needed)

常见形式是排名层面的聚合，而不是分数直接相加。具体规则可为：

- 多数投票（majority voting）
- Rank product / rank sum
- 学习型聚合器（如随机森林）

## Key Points

1. 目标是“稳健性”而非保证每个数据集都最优。
2. 代理之间差异越互补，投票收益通常越大。
3. 代价是实现更复杂、推理开销更高。

## How This Paper Uses It

- [[WRCor]]: 定义了 SPW（SynFlow+PNorm+WRCor）与 SJW（SynFlow+JacCor+WRCor）两个投票代理，提升多个实验设置下的稳定性。

## Representative Papers

- [[WRCor]]: 在 zero-shot NAS 中将 WRCor 与其他 proxy 组合并验证。
- [[ZCP-Eval]]: 系统评估 zero-cost proxy 在不同设置下表现差异，支撑“组合优于单一”的动机。

## Related Concepts

- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Non-linear Ranking Aggregation]]


