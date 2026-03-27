---
type: concept
language: zh-CN
source_concept_note: "[[Sample-Wise Activation Pattern]]"
aliases: [样本维激活模式, SWAP Pattern]
---

# Sample-Wise Activation Pattern 中文条目

## 一句话直觉
它不是“看一个样本在所有神经元上的激活”，而是“看一个神经元在一批样本上的激活轨迹”。

## 它为什么重要
这种重排会显著增加可区分模式空间，让 training-free NAS 的架构排序更有分辨率。

## 一个小例子
batch 大小为 4 时，某神经元可能是 `[1,0,1,1]`，另一个是 `[0,0,1,0]`；把所有神经元这样的向量去重计数就是 SWAP 分数核心。

## 更正式的定义
对网络 \(N\) 与参数 \(\theta\)，每个中间激活位置 \(v\) 构造跨样本二值向量 \(\mathbf{1}(p_s^{(v)})_{s=1}^{S}\)，所有向量构成集合，其基数用于 SWAP-Score。

## 核心要点
1. 向量按神经元索引，不按样本索引。
2. 上界与中间激活数量 \(V\) 相关，通常大于样本数 \(S\)。
3. 去重后的基数可作为表达能力 proxy。

## 这篇论文里怎么用
- [[SWAP-NAS]]: 直接把样本维激活模式集合基数定义为 SWAP-Score。
- [[L-SWAG]]: 使用同类的 sample-wise pattern 基数作为 `Psi`（Def. 1/2, Eq. 7/8），但论文正文未显式写“先转置矩阵再 unique”。
- [[SWAP-NAS]]: 论文与实现更明确地采用“激活矩阵转置为 `(neurons, samples)` 后做 unique 计数”的写法。

## 代表工作
- [[SWAP-NAS]]: 首次系统提出并用于 ultra-fast NAS。

## 相关概念
- [[Network Expressivity]]
- [[Zero-Cost Proxy]]
