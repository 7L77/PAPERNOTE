---
type: concept
language: zh-CN
source_concept_note: "[[Patchify Stem]]"
aliases: [切块 stem, Patch Stem]
---

# Patchify Stem 中文条目

## 一句话直觉
`Patchify Stem` 把图像先切成小块再送进主干，计算友好，但可能牺牲局部细节连续性。

## 它为什么重要
它是 ViT/ConvNeXt 类设计里常见入口层，和卷积 stem 的选择会直接影响鲁棒性。

## 一个小例子
`patch=4, stride=4` 的不重叠切块会更快降采样，但边缘/纹理细节可能丢失更多。

## 更正式的定义
采用 `kernel=p, stride=p` 的 patch 投影算子，把输入转成 patch token 或 patch feature map。

## 核心要点
1. patch 越大、重叠越少，信息压缩越强。
2. 在对抗场景中，过激进下采样可能不利。
3. 可通过减小步幅或增加重叠缓解问题。

## 这篇论文里怎么用
- [[Robust Principles]]: 与 convolutional stem 对比，发现其鲁棒表现通常更弱。

## 代表工作
- [[Robust Principles]]: 报告 patchify 与 conv stem 的鲁棒差异。

## 相关概念
- [[Convolutional Stem]]
- [[Adversarial Robustness]]

