---
type: concept
language: zh-CN
source_concept_note: "[[Surrogate NAS Benchmark]]"
aliases: [代理 NAS 基准, NAS 代理基准]
---

# Surrogate NAS Benchmark 中文条目

## 一句话直觉

Surrogate NAS Benchmark 就是用“学出来的评估器”替代“每个架构都真实训练”，让 NAS 基准测试在大搜索空间里也能快速反复跑。

## 它为什么重要

传统 tabular benchmark 要穷举评估，空间一大就不可行；代理基准可以把评估成本从小时级降到秒级，同时保留对优化器行为的比较能力。

## 一个小例子

同样是比较 RE、BANANAS、随机搜索：真实训练可能要几个月 GPU 时间；代理基准中只需持续调用 surrogate query，就能得到可重复的 anytime 曲线。

## 更正式的定义

Surrogate NAS Benchmark 指：在固定搜索空间内，使用训练得到的 surrogate 模型来近似架构性能（以及可选的运行时），从而替代逐架构完整训练评估的基准体系。

## 核心要点

1. 本质是“以近似换规模、换速度、换可重复性”。
2. 好坏取决于训练数据覆盖与 surrogate 外推能力。
3. 应按黑盒方式使用，避免优化器利用 surrogate 内部结构刷分。

## 这篇论文里怎么用

- [[NAS-Bench-301]]: 在 DARTS 超大空间上构建 surrogate benchmark，并验证它与真实 benchmark 的轨迹排序一致性。

## 代表工作

- [[NAS-Bench-301]]: 代理基准范式的代表性实现。
- [[Surrogate Predictor]]: 代理预测器是该范式的技术基础。

## 相关概念

- [[Surrogate Predictor]]
- [[Neural Architecture Search]]
- [[Sparse Kendall Tau]]

