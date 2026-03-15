---
type: concept
language: zh-CN
source_concept_note: "[[Input Loss Landscape]]"
aliases: [输入损失地形, 输入空间损失曲面]
---

# Input Loss Landscape 中文条目

## 一句话直觉
Input Loss Landscape 关注的是：参数固定时，输入 `x` 在附近轻微扰动会让损失 `L(θ,x)` 怎么变化。

## 它为什么重要
对抗鲁棒性本质上就是输入邻域稳定性问题。若很小扰动就让损失大幅上升，模型通常更脆弱。

## 一个小例子
给图像加上很小的符号扰动后，交叉熵突然显著增大，说明该点附近地形很陡；如果损失变化平缓，通常鲁棒性更好。

## 更正式的定义
在固定参数 `θ` 下，输入损失地形研究 `L(θ,x)` 在输入空间的局部几何性质，比如梯度范数与 Hessian 曲率。这些量常作为鲁棒性近似指标。

## 数学形式（如有必要）
常见近似形式之一是输入梯度的有限差分：
$$
\left\|
\frac{l(x + h z^*) - l(x)}{h}
\right\|_2^2,\quad l(x)=\nabla_x L(\theta, x)
$$

符号说明：
- `L(θ, x)`: 输入 `x` 上的损失。
- `l(x)`: 损失对输入的梯度。
- `h`: 扰动尺度。
- `z*`: 扰动方向（常取 sign-gradient 方向）。

## 核心要点
1. 它描述的是输入空间的局部几何，而不是参数空间几何。
2. 局部曲率大通常意味着更容易被对抗扰动击穿。
3. 有限差分可以在较低成本下估计相关曲率信息。

## 这篇论文里怎么用
- [[Robust-ZCP]]: 使用 Eq. (7) 的有限差分项近似输入 Hessian 相关项，并与 NTK 项组合成最终鲁棒代理分数。

## 代表工作
- [[Robust-ZCP]]: 将输入地形近似用于 zero-cost 鲁棒性排序。
- [[Adversarial Robustness]]: 大量工作都把局部损失地形与攻击成功率联系起来。

## 相关概念
- [[Neural Tangent Kernel]]
- [[Adversarial Robustness]]
- [[Zero-Cost Proxy]]

