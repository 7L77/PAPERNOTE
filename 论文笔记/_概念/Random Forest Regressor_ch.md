---
type: concept
language: zh-CN
source_concept_note: "[[Random Forest Regressor]]"
aliases: [随机森林回归, RF 回归器]
---

# Random Forest Regressor 中文条目

## 一句话直觉
随机森林回归器就是“很多决策树一起投票做回归”，每棵树各看一部分样本和特征，最后取平均，结果更稳。

## 它为什么重要
在 NAS 代理预测里，特征关系通常非线性且有噪声。随机森林对这类表格特征很友好，调参门槛也相对低。

## 一个小例子
我们要用 `jacov`、`snip`、`flops` 预测架构鲁棒精度。单棵树容易过拟合，森林把多棵树平均后，泛化通常更稳定。

## 更正式的定义
Random Forest Regressor 是一种集成回归模型：对多个 bootstrap 子样本训练决策树，并在节点分裂时随机采样特征，最终输出各树预测均值。

## 核心要点
1. 擅长处理非线性特征交互。
2. 对特征缩放不敏感，工程上较省心。
3. 特征重要性可解释，但 MDI 与 permutation 的解释口径不同，不能混用结论。

## 这篇论文里怎么用
- [[ZCP-Eval]]: 用随机森林将多代理特征映射到 clean/robust 目标，并分析训练规模对 `R^2` 的影响。

## 代表工作
- [[ZCP-Eval]]: 将随机森林用于鲁棒 NAS 代理预测评测。
- Breiman (2001): 随机森林经典论文。

## 相关概念
- [[Surrogate Predictor]]
- [[Permutation Feature Importance]]
- [[Neural Architecture Search]]
