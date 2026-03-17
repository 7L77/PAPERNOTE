---
type: concept
language: zh-CN
source_concept_note: "[[Moore-Penrose Pseudoinverse]]"
aliases: [Moore-Penrose 伪逆, Pseudoinverse]
---

# Moore-Penrose Pseudoinverse 中文条目

## 一句话直觉
当矩阵不能直接求逆时，Moore-Penrose 伪逆提供了一个“最合理的逆替代”，用于求最小二乘或最小范数解。

## 它为什么重要
机器学习里大量线性方程组是非方阵或奇异矩阵场景，普通逆失效，伪逆是标准工具。

## 一个小例子
若 `U` 是高矩阵（`T>W`），`UW=X` 往往无精确解，`U^+X` 给出让误差最小的近似解。

## 更正式的定义
对任意矩阵 `U`，`U^+` 是满足 Penrose 四条件的唯一矩阵，推广了逆矩阵概念。

## 数学形式（如有必要）
若 `U = V_1 \Sigma V_2^\top`（SVD），则
\[
U^+ = V_2 \Sigma^+ V_1^\top
\]
其中 `\Sigma^+` 对非零奇异值取倒数。

## 核心要点
1. 非方阵和奇异矩阵也可用。
2. 欠定系统可得最小范数解。
3. 超定系统可得最小二乘解。

## 这篇论文里怎么用
- [[TF-MAS]]: 在 `T<W` 与 `T>W` 情形下都通过伪逆/最小二乘来求 `W_X/W_B/W_C`。

## 代表工作
- [[TF-MAS]]: 把伪逆放进训练免费代理的矩阵估计流程。

## 相关概念
- [[Principal Component Analysis]]
- [[Rank Collapse]]
- [[Training-free NAS]]

