---
type: concept
language: zh-CN
source_concept_note: "[[Square Attack]]"
aliases: [Square Attack, 黑盒方块攻击]
---

# Square Attack 中文条目

## 一句话直觉
Square Attack 通过随机修改图像中的小方块区域来攻击模型，不需要梯度信息。

## 它为什么重要
它是黑盒攻击代表方法，可补充白盒攻击视角，避免只看梯度攻击导致的误判。

## 一个小例子
每次在一块方形区域内改像素，如果让模型更容易误判就保留该修改，反复迭代直到预算用完。

## 更正式的定义
Square Attack 是在给定范数约束下，基于查询和随机搜索优化分类 margin 的黑盒对抗攻击方法。

## 数学形式（如有必要）
\[
\min_{\tilde{x}} \left(f_{y,\theta}(\tilde{x}) - \max_{k\ne y} f_{k,\theta}(\tilde{x})\right),\quad \|\tilde{x}-x\|_\infty \le \epsilon.
\]

## 核心要点
1. 不依赖梯度，可用于黑盒场景。
2. 查询效率高于朴素随机黑盒攻击。
3. 常与 APGD 等方法组合使用。

## 这篇论文里怎么用
- [[NADR-Dataset]]: 将 Square Attack 纳入统一评测键，对所有架构做多 epsilon 鲁棒评估。

## 代表工作
- Andriushchenko et al., ECCV 2020.
- Croce and Hein, ICML 2020.

## 相关概念
- [[AutoAttack]]
- [[Adversarial Robustness]]
- [[PGD Attack]]

