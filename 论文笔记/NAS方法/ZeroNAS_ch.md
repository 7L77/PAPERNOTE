---
title: "ZeroNAS_ch"
type: method
language: zh-CN
source_method_note: "[[ZeroNAS]]"
source_paper: "ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning"
source_note: "[[ZeroNAS]]"
authors: [Caixia Yan, Xiaojun Chang, Zhihui Li, Weili Guan, Zongyuan Ge, Lei Zhu, Qinghua Zheng]
year: 2022
venue: TPAMI
tags: [nas-method, zh, zero-shot-learning, gan, differentiable-nas]
created: 2026-03-17
updated: 2026-03-17
---

# ZeroNAS 中文条目

## 一句话总结

> ZeroNAS 用可微对抗双层优化联合搜索生成器和判别器结构，再通过剪枝得到离散 GAN 架构，用于 ZSL/GZSL 特征生成并提升最终分类表现。

## 来源

- 论文: [ZeroNAS: Differentiable Generative Adversarial Networks Search for Zero-Shot Learning](https://doi.org/10.1109/TPAMI.2021.3127346)
- HTML: 论文未提供 arXiv HTML（IEEE 文章页）
- 代码: https://github.com/caixiay/ZeroNAS
- 英文方法笔记: [[ZeroNAS]]
- 论文笔记: [[ZeroNAS]]

## 适用场景

- 问题类型: 基于特征生成的 [[Zero-Shot Learning]] / [[Generalized Zero-Shot Learning]] 架构搜索。
- 前提假设: 类语义向量可用，且 GAN 生成特征可支持后续 softmax 分类器。
- 数据形态: 仅 seen 类有训练样本，unseen 类只在测试出现。
- 规模与约束: 不希望采用 RL 风格高成本 GAN NAS 时，更适合可微搜索。
- 适用原因: 搜索阶段显式建模 G/D 耦合，而不是只搜其中一侧。

## 不适用或高风险场景

- 你希望“跨数据集直接复用”同一架构而不重搜。
- 你的任务是像素级生成，不是特征级生成。
- 你无法承担对抗搜索中的交替更新与梯度惩罚训练。

## 输入、输出与目标

- 输入: seen 特征 `x`、语义向量 `c_y`、噪声 `z`、DAG 搜索空间、FC 候选操作集。
- 输出: `genotype_G`、`genotype_D`、训练后的 GAN、合成特征与最终 ZSL/GZSL 精度。
- 优化目标: 联合优化 G/D 的结构与参数，使 unseen 类特征分布拟合更好。
- 核心假设: 更匹配的 G/D 架构会提升特征合成质量和分类可分性。

## 方法拆解

### 阶段 1: 构建可微 MLP 超网

- G 和 D 都用 DAG + MixedLayer。
- 边权重与边内操作权重都通过 softmax 学习。
- Source: Sec. 3.2 / Eq. (2) / Eq. (3) / Fig. 2

### 阶段 2: 对抗双层架构搜索

- 下层在训练集上更新网络参数 `u_g/u_d`。
- 上层在验证集上更新结构参数 `v_g/v_d`。
- Source: Sec. 3.3 / Eq. (5) / Algorithm 1

### 阶段 3: 四步交替优化

- 每轮更新顺序：`v_d -> u_d -> v_g -> u_g`。
- Source: Algorithm 1 / Eq. (6)-(9)

### 阶段 4: 剪枝导出离散架构

- 每个中间节点保留权重最高的两条入边。
- 每条保留边只保留权重最高的一个操作。
- Source: Sec. 3.4；代码 `model.py:get_cur_genotype()`

### 阶段 5: 重训练与评估

- 用全训练集从头训练导出结构。
- 合成 unseen 特征并训练 softmax 分类器进行 ZSL/GZSL 评测。
- Source: Sec. 3.4 / Eq. (10)-(11) / Table 1-2

## 伪代码

```text
Algorithm: ZeroNAS
Input: Seen data D_tr, semantic embeddings C, noise prior p(z)
Output: genotype_G, genotype_D and final ZSL/GZSL predictor

1. 构建 G/D 的 MLP DAG 超网，并在边上放置 mixed operations。
   Source: Sec. 3.2, Fig. 2
2. 初始化网络参数 (u_g, u_d) 与结构参数 (v_g, v_d)。
   Source: Algorithm 1
3. 迭代直到收敛：
   3.1 在验证集更新 v_d。
       Source: Eq. (6), Algorithm 1
   3.2 在训练集更新 u_d。
       Source: Eq. (7), Algorithm 1
   3.3 在验证集更新 v_g。
       Source: Eq. (8), Algorithm 1
   3.4 在训练集更新 u_g。
       Source: Eq. (9), Algorithm 1
4. 对超网进行 top-2 边剪枝 + top-1 操作剪枝，得到离散结构。
   Source: Sec. 3.4
5. 从头重训练离散 G/D，生成 unseen 特征并训练 softmax 分类器。
   Source: Sec. 3.4, Eq. (10)-(11)
```

## 训练流程

1. 先训练 seen 类分类器 `C`，提供分类监督项。
2. 将 seen 训练集随机划分为 train/valid 做架构搜索。
3. 在 WGAN-GP + 分类损失下交替更新 G/D 的结构参数与网络参数。
4. 导出最优 genotype 后，用全训练集重训练。
5. 生成 unseen 特征并完成 ZSL/GZSL 分类评估。

Sources:

- Sec. 3.1-3.4, Algorithm 1
- 代码: `clswgan.py`, `clswgan_retrain.py`, `classifier.py`, `classifier2.py`

## 推理流程

1. 给定 unseen 类语义 `c_y`，采样 `z~N(0,1)` 生成特征 `x~=G(z,c_y)`。
2. 构建合成训练集（ZSL 仅 unseen，GZSL 为 seen+unseen）。
3. 用已训练 softmax 分类器预测查询样本标签。

Sources:

- Sec. 3.4 / Eq. (10)-(11)
- Source: Inference from source（论文未单独给部署式推理 API）

## 复杂度与效率

- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: 相比 RL-based GAN NAS 更省；文中报告 FLO/CUB 搜索约 1.5/2 GPU 小时。
- 扩展性说明: 架构对数据集依赖强，跨数据集迁移会明显退化。

## 实现备注

- 代码中的搜索维度：
  - Generator: `[128, 256, 512, 1024, 2048]`
  - Discriminator: `[1024, 512, 256, 128, 1]`
- 候选算子为 FC + 激活/BN/Dropout 的组合，和论文定义一致。
- G/D 各自分离“结构参数优化器”和“权重参数优化器”。
- `clswgan.py` 中 seen 训练集做随机 50/50 划分作为 train/valid。
- `clswgan_retrain.py` 需要手动填入 `genotype_G/genotype_D` 后重训。
- 官方环境较老：Python 3.6 + PyTorch 0.3.1。

## 与相关方法关系

- 对比 [[AutoGAN]] / AGAN：不依赖 RL controller，搜索成本更低。
- 对比 DEGAS：ZeroNAS 同时搜索 G 和 D，而不是只搜 G。
- 对比 [[f-CLSWGAN]]：保持特征生成范式，但把手工结构替换为自动搜索结构。
- 主要优势: 在多 GAN 基线和多数据集上有稳定增益。
- 主要代价: 架构迁移性不足，通常需要按数据集重搜。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5, Fig. 6
- 关键表: Table 1, Table 2, Table 3
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (5), Eq. (6)-(11)
- 关键算法: Algorithm 1

## 参考链接

- DOI: https://doi.org/10.1109/TPAMI.2021.3127346
- 代码: https://github.com/caixiay/ZeroNAS
- 本地实现: D:/PRO/essays/code_depots/ZeroNAS Differentiable Generative Adversarial Networks Search for Zero-Shot Learning

