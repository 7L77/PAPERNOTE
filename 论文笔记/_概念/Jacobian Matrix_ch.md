---
type: concept
language: zh-CN
source_concept_note: "[[Jacobian Matrix]]"
aliases: [雅可比矩阵, Jacobian]
---

# Jacobian Matrix 中文条目

## 一句话直觉
Jacobian 矩阵描述的是“输出对输入或参数微小变化有多敏感”。

## 它为什么重要
它能刻画局部几何与可训练性，很多训练自由 NAS proxy 都依赖 Jacobian 统计量。

## 一个小例子
如果某个参数微调后某个 logit 变化很大，对应 Jacobian 元素就大，说明该方向很敏感。

## 更正式的定义
对向量函数 `f`，Jacobian 定义为 `J_ij = partial f_i / partial x_j`，也可对参数 `w` 求偏导。

## 数学形式（如有必要）
批量形式可写为 `J = [partial f(x_1)/partial w; ...; partial f(x_B)/partial w]`。

## 核心要点
1. Jacobian 反映局部梯度结构。
2. 谱信息（奇异值/特征值）常与表达性或稳定性相关。
3. 可用于构造 zero-cost 架构评分。

## 这篇论文里怎么用
- [[IBFS]]: 在初始化处构建 Jacobian，并用谱熵作为架构表达性分数。

## 代表工作
- [[IBFS]]: Jacobian 谱熵 proxy。
- [[NASWOT]]: Jacobian 相关零成本代理。

## 相关概念
- [[Neural Tangent Kernel]]
- [[Entropy]]
- [[Zero-Cost Proxy]]
