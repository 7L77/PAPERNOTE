---
type: concept
language: zh-CN
source_concept_note: "[[Extrinsic Curvature]]"
aliases: [外在曲率, 输出轨迹曲率]
---

# Extrinsic Curvature 中文条目

## 一句话直觉
外在曲率描述曲线在外部空间里“弯得有多厉害”；在神经网络里，它衡量输入轨迹经过网络后输出轨迹的弯曲程度。

## 它为什么重要
输出轨迹越弯，通常代表模型能表达更复杂函数形状，因此可作为表达性的几何代理。

## 一个小例子
同样给两个网络喂圆形输入轨迹：一个网络输出几乎直线（低曲率），另一个输出复杂弯曲轨迹（高曲率）。后者通常表达性更强。

## 更正式的定义
对输出轨迹 \(f(g(\theta))\)，通过对 \(\theta\) 求一阶和二阶导数，估计每个位置的曲率并进行聚合。

## 数学形式（如有必要）
典型形式可写为：
\[
\kappa \propto \|v\|^{-3}\sqrt{\|v\|^2\|a\|^2-(v^\top a)^2}
\]
其中 \(v=\frac{d f(g(\theta))}{d\theta}\)，\(a=\frac{d^2 f(g(\theta))}{d\theta^2}\)。

## 核心要点
1. 曲率关注的是输出几何形状，而非仅幅值。
2. 不依赖标签即可估计。
3. 需要高阶自动求导，计算成本通常高于普通前向 proxy。

## 这篇论文里怎么用
- [[Dextr]]: 把 \(\log(1+\kappa)\) 作为表达性分量，与逆条件数分量融合得到最终分数。

## 代表工作
- [[Dextr]]: 在 zero-shot NAS 里显式引入外在曲率。
- [[Network Expressivity]]: 表达性几何刻画相关概念族。

## 相关概念
- [[Network Expressivity]]
- [[Singular Value Decomposition]]
- [[Gram Matrix]]

