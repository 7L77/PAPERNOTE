---
type: concept
language: zh-CN
source_concept_note: "[[Network Expressivity]]"
aliases: [网络表达能力, 表达性]
---

# Network Expressivity 中文条目

## 一句话直觉
网络表达能力是“这个网络最多能表示多复杂函数”的能力边界。

## 它为什么重要
在 NAS 里，表达能力太弱难以拟合复杂模式，但过强也可能带来成本和泛化问题。

## 一个小例子
线性模型只能给出简单边界；深层 ReLU 网络可以形成大量分段线性区域，函数形状更丰富。

## 更正式的定义
对分段线性网络，表达能力常由输入空间可划分的线性区域数量刻画；区域越多，理论上可表达函数族越丰富。

## 核心要点
1. 表达能力高不等于最终精度必然高。
2. 深度与宽度都会影响表达能力。
3. 激活模式类 proxy 可以在不训练时近似刻画它。

## 这篇论文里怎么用
- [[SWAP-NAS]]: 用样本维激活模式去重基数作为表达能力 proxy。

## 代表工作
- [[SWAP-NAS]]: 把表达能力 proxy 直接用于 training-free NAS 排序。

## 相关概念
- [[Sample-Wise Activation Pattern]]
- [[Zero-Cost Proxy]]

