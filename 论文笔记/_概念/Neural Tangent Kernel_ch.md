---
type: concept
language: zh-CN
source_concept_note: "[[Neural Tangent Kernel]]"
aliases: [神经切线核, NTK]
---

# Neural Tangent Kernel 中文条目

## 一句话直觉
Neural Tangent Kernel（NTK）衡量的是：两个输入在当前参数点上对网络参数产生的“梯度作用方向”有多相似。

## 它为什么重要
NTK 能把神经网络训练过程中的一些行为（如收敛速度、损失上界相关性）转成可分析的核矩阵问题，因此常被用于训练免费代理设计与理论解释。

## 一个小例子
如果两个样本 `x1` 和 `x2` 的参数梯度 `∇θ f(x1)`、`∇θ f(x2)` 几乎同向，那么更新 `x1` 时通常也会帮助 `x2`，此时二者的 NTK 值较大。

## 更正式的定义
对模型 `fθ`，输入 `x` 与 `x'` 的 NTK 定义为参数梯度内积：
`Θθ(x, x') = <∇θ fθ(x), ∇θ fθ(x')>`。
在批量上形成核矩阵后，其特征值常用于分析训练与泛化性质。

## 数学形式（如有必要）
$$
\Theta_{\theta}(x, x') = \left\langle \nabla_{\theta} f_{\theta}(x), \nabla_{\theta} f_{\theta}(x') \right\rangle
$$

符号说明：
- `fθ(x)`: 输入 `x` 的模型输出。
- `∇θ fθ(x)`: 输出对参数的梯度。
- `Θθ`: 由梯度内积构成的核矩阵。

## 核心要点
1. NTK 本质是参数空间里的梯度几何量。
2. NTK 特征值常被用在损失上界与收敛分析中。
3. 在 training-free NAS 中，初始化 NTK 常被当作廉价信号。

## 这篇论文里怎么用
- [[Robust-ZCP]]: 用 NTK 相关近似项（Eq. 8）作为鲁棒代理分数的一部分。

## 代表工作
- [[Robust-ZCP]]: 将 NTK 近似用于对抗鲁棒性 zero-cost 评估。
- [[ZCP-Eval]]: 讨论了梯度类代理在鲁棒预测中的作用边界。

## 相关概念
- [[Zero-Cost Proxy]]
- [[Input Loss Landscape]]
- [[Adversarial Robustness]]

