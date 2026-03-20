---
title: "On the Interplay of Convolutional Padding and Adversarial Robustness_ch"
method_name: "Padding-Robustness Interplay"
language: zh-CN
source_note: "[[Padding-Robustness Interplay]]"
authors: [Paul Gavrikov, Janis Keuper]
year: 2023
venue: ICCV Workshop
tags: [adversarial-robustness, cnn, padding, cifar-10, zh]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2308.06612
local_pdf: D:/PRO/essays/papers/On the Interplay of Convolutional Padding and Adversarial Robustness.pdf
created: 2026-03-18
---

# 论文笔记：Padding-Robustness Interplay（中文）

## 一句话总结
> 这篇工作系统分析了卷积 [[Convolutional Padding]] 与 [[Adversarial Robustness]] 的关系，指出 `zero padding` 在 AutoAttack 汇总指标上常占优，但分攻击结论并不总一致。

## 研究问题
作者关注两个核心问题：
1. 不同 padding 模式（`zeros` / `reflect` / `replicate` / `circular`）会如何影响鲁棒性？
2. 这种影响会不会随训练方式（普通训练 vs [[Adversarial Training]]）和攻击类型而改变？

## 实验设置
- 模型：ResNet-20
- 数据集：CIFAR-10
- 卷积核：k in {3, 5, 7, 9}，padding 大小使用 same 规则 floor(k/2)
- 攻击：APGD-CE、FAB、Square、AutoAttack
- 训练方式：
  - 普通训练（native）
  - FGSM 对抗训练（并用 PGD 指标早停）

## 关键结果
### 1) Clean 准确率（Table 1）
- 普通训练下，`zero padding` 基本最优。
- 对抗训练下，`reflect/replicate` 在部分设置可超过 `zero`。

### 2) 鲁棒准确率（Table 2 + Fig. 3）
- 只看 AutoAttack 汇总值时，`zero` 往往最好或接近最好。
- 但分攻击看，`reflect/replicate` 在某些 attack/kernel 组合上能更好。
- `circular` 在对抗训练场景下整体最差。

### 3) 扰动分布与边界异常（Fig. 4）
- 成功攻击的扰动在图像边缘存在明显异常，和 padding 区域强相关。
- 这种边界效应在不同攻击范数（Linf/L2）下表现不同。

### 4) 决策解释偏移（Fig. 5）
- 用 [[LayerCAM]] 观察到：攻击后关注区域会发生迁移，且迁移模式受 padding 影响。

### 5) 计算开销（Table 3）
- 仅看“padding 操作”时，zero 不是最快。
- 但看“padding + 卷积总体”时，zero 的前向时间最快。
- reflect/replicate 有额外开销，circular 开销最大。

### 6) 去掉 padding 是否更好（Table 4）
- 直接去掉 padding 会显著降低性能。
- upscaling/outpainting 虽可挽回部分 clean 指标，但鲁棒性仍明显下降。
- 结论：不建议把“去 padding”作为默认鲁棒策略。

## 实践建议
1. 不要只看 AutoAttack 汇总值，建议同时报告分攻击结果。
2. 对抗训练任务里可把 `reflect/replicate` 作为可选项一起试验。
3. 若追求推理效率，`zero padding` 的总体算子效率仍有优势。

## 局限性
1. 仅评测了 CIFAR-10。
2. 仅使用 ResNet-20。
3. 论文未提供官方代码仓库链接（截至 2026-03-18 检索未发现官方 repo）。

## 关联
- 英文原笔记：[[Padding-Robustness Interplay]]
- 方法笔记（英）：[[NAS方法/Padding-Robustness Interplay]]
- 方法笔记（中）：[[NAS方法/Padding-Robustness Interplay_ch]]

