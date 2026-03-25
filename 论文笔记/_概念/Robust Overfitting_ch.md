---
type: concept
language: zh-CN
source_concept_note: "[[Robust Overfitting]]"
aliases: [鲁棒过拟合, Robust Overfitting]
---

# Robust Overfitting 中文条目

## 一句话直觉
Robust Overfitting 指的是：对抗训练继续进行时，训练鲁棒性还在涨，但验证/测试鲁棒性反而开始掉。

## 它为什么重要
它直接影响模型选择与实验公平性；如果只看最后一个 epoch，很容易误判某个架构“更鲁棒”。

## 一个小例子
某模型在第 70 轮验证 PGD 准确率最高，但第 100 轮更低。若只取最后 checkpoint，会低估真实可泛化鲁棒性。

## 更正式的定义
在对抗训练中，随着训练继续，模型在训练集上的鲁棒指标提升，而在验证/测试集上的鲁棒指标出现系统性下降的现象。

## 数学形式（如有必要）
它通常通过训练曲线观察与诊断，没有唯一标准闭式公式。

## 核心要点
1. 在标准 AT 设定下较常见。
2. 用鲁棒验证指标做 early stopping 是常见缓解方案。
3. 若不处理，会让架构比较结论产生偏差。

## 这篇论文里怎么用
- [[NARes]]: 使用独立验证集并以 PGD-CW40 最优 epoch 选模型，显式缓解该问题。

## 代表工作
- Rice et al. (2020): 系统讨论了鲁棒过拟合现象。
- [[NARes]]: 在大规模架构数据集构建中将其作为关键工程问题处理。

## 相关概念
- [[Adversarial Training]]
- [[Adversarial Robustness]]
- [[PGD Attack]]

