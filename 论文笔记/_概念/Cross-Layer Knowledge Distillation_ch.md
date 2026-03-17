---
type: concept
language: zh-CN
source_concept_note: "[[Cross-Layer Knowledge Distillation]]"
aliases: [跨层知识蒸馏, Cross-Layer KD]
---

# Cross-Layer Knowledge Distillation 中文条目

## 一句话直觉

跨层知识蒸馏不是只让学生学教师最后输出，而是让学生每一层去匹配更合适的教师层。

## 它为什么重要

教师不同层携带的语义粒度不同，跨层匹配能传递更细的中间知识，通常比只蒸馏 logits 更有效。

## 一个小例子

学生浅层可以学习教师浅层的边缘纹理，学生深层学习教师深层的语义结构。

## 更正式的定义

学习 student 层与 teacher 层之间的映射权重，再最小化对应层特征/注意力/分布差异。

## 数学形式（如有必要）

常见写法:
`L = sum_i sum_j g_ij * d(f_s_i, f_t_j)`，
其中 `g_ij` 是可学习匹配权重，`d` 是距离函数。

## 核心要点

1. 层映射可学习，而不是人工固定。
2. 能缓解 teacher/student 深度不一致问题。
3. 常用 soft-to-hard 机制（如 Gumbel-Softmax）。

## 这篇论文里怎么用
- [[RNAS-CL]]: 把 tutor 层选择纳入 NAS，一起优化鲁棒性与效率。

## 代表工作

- [[RNAS-CL]]: 在鲁棒 NAS 中显式搜索跨层 tutor 映射。

## 相关概念

- [[Knowledge Distillation]]
- [[Attention Map]]
- [[Gumbel-Softmax]]
