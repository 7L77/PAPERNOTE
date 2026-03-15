---
type: concept
language: zh-CN
source_concept_note: "[[Flow of Solution Procedure Matrix]]"
aliases: [FSP 矩阵, FSP Matrix]
---

# Flow of Solution Procedure Matrix 中文条目

## 一句话直觉
FSP 矩阵描述“某层输入特征如何流向输出特征”；如果同一层在 clean 和 adversarial 输入下的 FSP 差异很大，通常表示该架构对攻击更敏感。

## 它为什么重要
它提供了按层分析鲁棒性的结构化指标，不必只盯最终分类精度。

## 一个小例子
对同一张图片分别输入 clean 与 adversarial 样本，比较深层 cell 的 FSP 距离；距离越大，往往对应更大的鲁棒性退化。

## 更正式的定义
对第 `l` 层，FSP 矩阵可写为输入与输出特征在空间维度上的归一化内积：
\[
G_l(x;\theta)=\frac{1}{h\times w}\sum_{s=1}^{h}\sum_{t=1}^{w}F^{in}_{l,s,t}(x;\theta)\cdot F^{out}_{l,s,t}(x;\theta)
\]
鲁棒分析中常用 clean/adv 的 FSP 距离：
\[
L_l^{FSP}=\frac{1}{N}\sum_x \|G_l(x;\theta)-G_l(x';\theta)\|_2^2
\]

## 核心要点
1. FSP 关注中间特征流一致性，不仅是输出层 logits。
2. 在 [[RobNet]] 中，深层 FSP 距离与鲁棒性缺口相关性更强。
3. 可作为候选架构预过滤信号，降低后续评估成本。

## 这篇论文里怎么用
- [[RobNet]]: 在 cell-free 搜索中用 FSP 距离先过滤非鲁棒候选。

## 代表工作
- [[RobNet]]: 将 FSP 距离用于鲁棒架构筛选。

## 相关概念
- [[Adversarial Robustness]]
- [[Cell-based Search Space]]
- [[Neural Architecture Search]]

