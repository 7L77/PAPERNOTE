---
title: "EAS-GAN"
type: method
language: zh-CN
source_method_note: "[[EAS-GAN]]"
source_paper: "Evolutionary Architectural Search for Generative Adversarial Networks"
authors: [Qiuzhen Lin, Zhixiong Fang, Yi Chen, Kay Chen Tan, Yun Li]
year: 2022
venue: IEEE Transactions on Emerging Topics in Computational Intelligence
tags: [nas-method, gan, evolutionary-search, image-generation, zh-CN]
created: 2026-03-20
updated: 2026-03-20
---

# EAS-GAN 中文方法笔记

## 一句话总结

> EAS-GAN 在固定判别器下，把生成器写成可微超网，再用 minimax / least-squares / hinge 三种 mutation objective 去进化不同 offspring，最后抽取最优离散结构并从头重训。

## 来源

- 论文: [Evolutionary Architectural Search for Generative Adversarial Networks](https://doi.org/10.1109/TETCI.2021.3137377)
- HTML: IEEE article page via DOI
- 代码: 截至 2026-03-20 未检索到官方仓库
- 论文笔记: [[EAS-GAN]]

## 适用场景

- 问题类型: 面向无监督图像生成任务的 generator architecture search。
- 前提假设: 可以接受固定 discriminator family，只重点优化 generator。
- 数据形态: CIFAR-10、STL-10、LSUN bedroom 这类中低分辨率图像数据。
- 规模与约束: 有单卡 V100 级别算力，能接受一次搜索约 24 小时的开销。
- 为什么适合: 它把 supernet 式权重共享和 E-GAN 式进化 mutation 统一起来，适合研究“GAN 结构怎么自动搜”。

## 不适合的场景

- 你希望同时搜索生成器和判别器。
- 你要直接面向现代高分辨率 GAN 工程落地。
- 你非常依赖官方实现和现成复现实验脚本。

## 输入、输出与目标

- 输入: 真实图像 `x`、噪声 `z`、基于 DAG cell 的生成器搜索空间、固定判别器、三种 mutation objective。
- 输出: 最终离散生成器结构、其训练后的权重、以及采样得到的图像。
- 目标: 在 GAN 对抗训练中，同时提升样本质量、训练稳定性和生成器结构适配性。
- 核心假设: 不同 generator loss 会暴露不同优化偏好，而 evolutionary selection 能保留表现更好的结构-权重组合。

## 方法拆解

### 阶段 1：构建可微生成器超网

- 把生成器写成若干 cell，每个 cell 是带候选算子的 DAG。
- 用 architecture parameter `alpha` 对边上的候选操作做 softmax 加权。
- Source: Sec. III-A / Fig. 2 / Fig. 3

### 阶段 2：按双层优化交替更新 `omega` 和 `alpha`

- 固定 `alpha` 更新生成器权重 `omega`。
- 固定 `omega` 用 one-step approximation 更新结构参数 `alpha`。
- 这是 DARTS 风格 bilevel optimization 在 GAN 场景中的改写。
- Source: Sec. III-B / Eq. (4)-(6)

### 阶段 3：对超网个体施加进化 mutation

- 每个 parent generator supernet 都会在三种 mutation objective 下产生 offspring。
- 三种 mutation 分别是 minimax、least-squares、hinge。
- 每个 offspring 都会继续更新结构参数和网络权重。
- Source: Sec. III-C / Eq. (7)-(10) / Algorithm 1

### 阶段 4：按 fitness 选择幸存个体

- fitness 由质量项和多样性项构成。
- 每轮只保留最优 `mu` 个 supernet 进入下一代。
- Source: Sec. III-C / Eq. (10) / Algorithm 1

### 阶段 5：抽取离散结构并重训

- 在每条边上取最大权重操作，得到最终 generator architecture。
- 然后从头做常规 adversarial training。
- Source: Algorithm 2 / Fig. 1

## 伪代码

```text
Algorithm: EAS-GAN
Input: 数据集 D, 噪声先验 p(z), parent 数 mu, mutation 数 n_m
Output: 最终生成器结构 G*

1. 用 DAG cell 和候选算子构建 generator supernet。
   Source: Sec. III-A / Fig. 2 / Fig. 3
2. 初始化生成器权重 omega、结构参数 alpha 和固定判别器 D。
   Source: Sec. III-B
3. 对每轮训练重复：
   3.1 先更新判别器 D 若干步。
       Source: Algorithm 1, lines 2-5
   3.2 对每个 parent supernet j 和每种 mutation M_h：
       a. 采样噪声并更新 alpha_j。
          Source: Algorithm 1, lines 8-9
       b. 在当前 mutation 下更新 omega_j。
          Source: Algorithm 1, line 10
       c. 计算 offspring fitness F_{j,h}。
          Source: Algorithm 1, line 11 / Eq. (10)
   3.3 按 fitness 从高到低保留 top-mu supernet。
       Source: Algorithm 1, line 14
4. 在保留边上取最大权重操作，得到离散 generator。
   Source: Algorithm 2, line 2
5. 用该离散 generator 从头做常规 GAN 训练。
   Source: Algorithm 2, lines 3-10
```

## 训练流程

1. 定义生成器搜索空间。
2. 初始化 generator supernet population。
3. 用真实样本和当前生成样本更新判别器。
4. 对每个 parent，在不同 mutation objective 下产生多个 offspring。
5. 计算每个 offspring 的 quality + diversity fitness。
6. 保留最优 parent 继续进化。
7. 进化结束后离散化结构并重训。

Sources:

- Sec. III-A to III-C
- Algorithm 1 / Algorithm 2

## 推理流程

1. 从 `p(z)` 采样噪声。
2. 输入最终重训后的生成器 `G*`。
3. 输出生成图像，用于随机采样、插值或可视化。

Sources:

- Algorithm 2
- Inference from source

## 复杂度与效率

- 时间复杂度: 论文未给闭式表达。
- 空间复杂度: 论文未给闭式表达。
- 运行特征: 搜索一个 `32x32` 生成器约需 24 小时，单卡 Nvidia Tesla V100。
- 扩展性说明: 论文展示到 `64x64`，但没有证明能顺畅扩展到现代高分辨率 GAN 设定。

## 实现细节

- upsampling 候选: transposed convolution `3x3`、nearest-neighbor interpolation、bilinear interpolation。
- 其余候选算子: `1x1` / `3x3` / `5x5` convolution、dilated `3x3` / `5x5`、skip-connect、zero。
- 激活函数: convolution 与 transposed convolution 使用 ReLU。
- 判别器: 固定 DCGAN 风格，并加 batch normalization。
- 搜索阶段优化器: Adam，`beta1=0.5`、`beta2=0.9`、`lr=0.004`。
- 进化设置: `mu=1`、三种 mutation、`gamma=0.01`。
- 评测设置: 每次生成 50000 个样本计算 IS / FID。
- 最终重训: hinge loss，Adam `lr=0.0002`。
- 实操风险: 没有官方代码，复现时需要自己补 supernet、mutation loop 和 fitness 计算细节。

## 与相关方法的比较

- 相比 WGAN-GP 这类 GAN baseline：EAS-GAN 主要改变的是 generator architecture search，而不是只改 loss 或正则。
- 相比 E-GAN：EAS-GAN 不再固定生成器结构，而是在进化中联合优化结构参数和网络参数。
- 相比 AutoGAN / AGAN：EAS-GAN 不靠 RL controller，而是用 differentiable supernet + evolutionary selection。
- 主要优势: 把 NAS 与 GAN 稳定训练统一到一个闭环里。
- 主要代价: 搜索空间较旧，只搜 generator，不搜 discriminator。

## 证据与可追溯性

- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 9, Fig. 10
- 关键表: Table I, Table II
- 关键公式: Eq. (1), Eq. (4)-(10)
- 关键算法: Algorithm 1, Algorithm 2

## 参考

- DOI: https://doi.org/10.1109/TETCI.2021.3137377
- HTML: IEEE article page via DOI
- 代码: 截至 2026-03-20 未检索到官方仓库
- 本地实现: Not archived

