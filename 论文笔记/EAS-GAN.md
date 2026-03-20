---
title: "Evolutionary Architectural Search for Generative Adversarial Networks"
method_name: "EAS-GAN"
authors: [Qiuzhen Lin, Zhixiong Fang, Yi Chen, Kay Chen Tan, Yun Li]
year: 2022
venue: IEEE Transactions on Emerging Topics in Computational Intelligence
tags: [NAS, GAN, evolutionary-search, image-generation]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/Evolutionary Architectural Search for Generative Adversarial Networks.pdf
created: 2026-03-20
---

# 论文笔记：EAS-GAN

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Evolutionary Architectural Search for Generative Adversarial Networks |
| 方法名 | EAS-GAN |
| DOI | https://doi.org/10.1109/TETCI.2021.3137377 |
| 代码 | As of 2026-03-20, no official repository was located |
| 本地 PDF | `D:/PRO/essays/papers/Evolutionary Architectural Search for Generative Adversarial Networks.pdf` |

## 一句话总结
> EAS-GAN 把 [[Neural Architecture Search]] 和 E-GAN 式进化训练拼在一起，把生成器写成可微 [[Super-network]] 后在进化过程中同时搜索结构与权重，从而在 CIFAR-10、STL-10 和 LSUN 上显著降低 [[Frechet Inception Distance]]。

## 核心贡献
1. 提出一种面向 [[Generative Adversarial Network]] 的 evolutionary architecture search，把“结构搜索”和“权重优化”放进同一条进化流程里，而不是先定结构再训参数。
2. 用 DARTS 风格的连续松弛来表示生成器搜索空间，再用 E-GAN 风格的 mutation / evaluation / selection 机制筛选更好的超网个体。
3. 在 CIFAR-10、STL-10、LSUN bedroom 上都优于 E-GAN、AGAN、WGAN-GP、RealnessGAN 等基线，并给出从 LSUN 到 CelebA 的 transferability 观察。

## 问题背景
### 要解决的问题
- 传统 GAN 结构通常靠人工 trial-and-error 设计，费时而且容易卡在局部经验。
- 已有 evolutionary GAN（如 E-GAN）改善了训练稳定性，但生成器结构本身仍然是固定的。
- 已有 GAN-NAS（如 AutoGAN、AGAN）能搜结构，但代价高，而且依赖 [[Inception Score]] 这类不够稳健的搜索或评价信号。

### 本文的切入点
- 作者保留 E-GAN 里“多种生成器目标函数作为 mutation operator”的优点。
- 同时借用连续可微搜索，把生成器候选结构写进一个共享权重的超网中。
- 这样每次进化不只是换 loss，也会推动结构参数和网络参数一起变。

## 方法详解
### 1. 两阶段总体框架（Fig. 1）
- 第一阶段：维护一个由 `mu` 个生成器超网组成的 population，在固定判别器环境下进化，得到最佳超网 `G_best`。
- 第二阶段：从 `G_best` 中抽取离散架构，再和判别器做常规 adversarial training。
- 关键点在于：第一阶段的判别器负责“环境评价”，第二阶段的判别器负责“最终对抗训练”。

### 2. 生成器搜索空间（Sec. III-A, Fig. 2, Fig. 3）
- 生成器由一串 cell 组成，每个 cell 是一个 DAG。
- 边上放候选操作，节点表示 feature map；最终每条边只保留权重最大的操作。
- 输入到第一层的 upsampling 候选包括：
  - transposed convolution `3x3`
  - nearest-neighbor interpolation
  - bilinear interpolation
- 其他边的候选操作包括：
  - `1x1` / `3x3` / `5x5` convolution
  - dilation=`2` 的 `3x3` / `5x5` convolution
  - skip-connect
  - zero
- 这实际上是一个偏 DCGAN 风格、面向生成器 backbone 的紧凑搜索空间，而不是搜索完整的现代 GAN 训练技巧包。

### 3. 可微超网 + 进化搜索（Sec. III-B, Eq. (4)-(6), Algorithm 1）
- 作者给每条候选边上的操作分配 architecture parameter `alpha`，通过 softmax 把离散搜索空间松弛成连续空间。
- 在固定 `alpha` 时更新网络权重 `omega`；在固定 `omega` 时用 one-step approximation 更新 `alpha`。
- 这一步借了 DARTS 的 bilevel 思想，但目标函数换成了 GAN 的 min-max 对抗训练。
- 在此基础上，再把多个超网个体放进 evolutionary loop 里，通过 fitness 排序做 survival of the fittest。

### 4. 三种 mutation objective（Sec. III-C, Eq. (7)-(9)）
作者把三种生成器损失看作 mutation operator：

#### Eq. (7) Minimax mutation
$$
\frac{1}{2}\mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]
$$

含义：对应原始 GAN 的 minimax 生成器目标，理论上关联 Jensen-Shannon divergence，但在分布不重叠时容易梯度消失。

#### Eq. (8) Least-squares mutation
$$
\mathbb{E}_{z \sim p_z}[(D(G(z)) - 1)^2]
$$

含义：把“骗过判别器”写成 least-squares 回归目标，缓解 vanishing gradients，并对 [[Mode Collapse]] 更友好。

#### Eq. (9) Hinge mutation
$$
-\mathbb{E}_{z \sim p_z}[D(G(z))]
$$

含义：hinge 形式在判别器很强时仍能提供非饱和梯度，因此训练更稳。

### 5. 评价与选择（Sec. III-C, Eq. (10)）
- fitness 延续 E-GAN 的思路，由两部分组成：
  - quality fitness：生成样本在判别器中的得分
  - diversity fitness：基于判别器梯度信息的多样性项
- 文中用 `gamma = 0.01` 平衡二者。
- 每轮会从 `mu x n_m` 个 offspring 中保留 fitness 更高的 `mu` 个 parent 进入下一轮。

### 6. 结构抽取与最终训练（Algorithm 2）
- 进化结束后，对每条边保留最大权重操作，得到离散 generator architecture。
- 再固定该结构，从头做标准 adversarial training。
- 这一步很重要，因为搜索阶段的共享权重并不等于最终部署性能。

## 关键公式
### Eq. (1) 标准 GAN 目标
$$
\min_G \max_D V(G, D)
= \mathbb{E}_{x \sim p_{data}}[\log D(x)]
+ \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]
$$

含义：生成器想骗过判别器，判别器想区分真样本和假样本。

### Eq. (4)-(5) 面向 GAN 的双层优化
$$
\min_{\text{omega}}\max_D \;
\mathbb{E}_{x \sim p_{data}}[\log D(x)]
+ \mathbb{E}_{z \sim p_z}[\log(1-D(G(z \mid \text{omega}, \alpha^*(\text{omega}))))]
$$

$$
\text{s.t. } \alpha^*(\text{omega})
= \arg\min_{\text{alpha}}\max_D \;
\mathbb{E}_{x \sim p_{data}}[\log D(x)]
+ \mathbb{E}_{z \sim p_z}[\log(1-D(G(z \mid \text{omega}, \text{alpha})))]
$$

含义：
- `omega` 是生成器权重
- `alpha` 是结构参数
- 外层希望在当前最优结构下把 GAN 训练好
- 内层希望在当前权重下找到更好的结构

## 重要图表与结论
### Figure 1
- 展示了 EAS-GAN 的两阶段框架：先进化超网找结构，再抽取最终结构做常规 GAN 训练。

### Figure 2 / Figure 3
- Figure 2 给出 DAG 搜索空间。
- Figure 3 说明“一个超网包含完整搜索空间，最终从中抽出离散架构”的过程。

### Figure 4 / Figure 9 / Figure 10
- 观察到更深层的 cell 更偏好大感受野操作，如 `5x5` dilated convolution。
- 更浅层的 cell 更常出现 skip-connect 或 zero，说明深层特征承担了更多表示任务。
- 作者据此强调：更深不一定更好，某些 cell 最终会被“空掉”。

### Table I：CIFAR-10 / STL-10
- CIFAR-10：
  - EAS-GAN `FID = 22.1`
  - E-GAN (`mu=1`) `33.2`
  - E-GAN (`mu=4`) `29.8`
  - AGAN `30.5`
- 同时 EAS-GAN 的 `IS = 7.45 +- 0.08`，仅次于把 IS 当 reward 的 AGAN。
- STL-10：
  - EAS-GAN `FID = 38.84`
  - AGAN `52.7`
  - E-GAN (`mu=1`) `62.5`
  - E-GAN (`mu=4`) `60.72`

### Table II：LSUN bedroom
- EAS-GAN `FID = 8.30`
- LSGAN `39.08`
- WGAN-GP `24.90`
- RealnessGAN `32.08`
- E-GAN (`mu=1`) `15.44`
- E-GAN (`mu=4`) `19.27`

### CelebA transferability
- 作者把在 LSUN bedroom 搜到的结构迁移到 CelebA 上重新训练。
- 结果以定性图和 latent interpolation 为主，说明该结构不是简单记忆训练样本，具备一定迁移性。

## 实验设置
### 数据集
- CIFAR-10：`32x32`
- STL-10：`48x48`
- LSUN bedroom：约 300 万 bedroom 图像
- CelebA：用于检验 transferability

### 评价指标
- [[Inception Score]]
- [[Frechet Inception Distance]]

### 实现细节
- 判别器采用 DCGAN 风格结构。
- 只使用 batch normalization，不使用 spectral normalization、gradient penalty 等额外稳定技巧。
- 搜索阶段 Adam 参数：`beta1=0.5`、`beta2=0.9`、`lr=0.004`
- `gamma=0.01`
- `mu=1`
- mutation 数量为 3
- 每次实验随机生成 50000 个样本来计算 IS / FID
- 作者报告：搜索一个 `32x32` 生成器大约需要 24 小时，单卡 Nvidia Tesla V100
- 第二阶段训练使用 hinge loss，Adam 学习率 `0.0002`

## 我的判断
### 优点
1. 这篇论文最值得看的点，不是“又做了一个 GAN”，而是把 DARTS 式超网搜索和 E-GAN 式 mutation-selection 真正揉成了一个统一训练流程。
2. 相比只搜结构或只换 loss，它把“结构选择”和“训练稳定性”放在同一个框架里考虑，思路是顺的。
3. 在 2022 这个时间点上，FID 提升很扎实，尤其 LSUN bedroom 上 `8.30` 的结果很亮眼。

### 局限
1. 它只搜索生成器，不搜索判别器；作者自己也把这件事放进 future work，说明框架还没完全闭环。
2. 搜索空间明显偏早期卷积 GAN 范式，和更现代的 StyleGAN 系列、正则化和归一化技巧脱节。
3. transferability 的证据主要是定性图像，没有很强的跨域定量分析。
4. 没找到官方代码，复现门槛会明显高于那类已有成熟实现的 NAS / GAN 工作。

### 适合怎么读
- 如果你关心“GAN 结构搜索怎么做”，这篇比纯 RL controller 那类工作更值得看，因为搜索机制更清楚。
- 如果你关心“现代高分辨率 GAN”，它的直接参考价值没那么高，更多是方法论上的过渡作品。
- 如果你想把 evolutionary idea 引进别的 NAS 场景，它的 mutation / evaluation / selection 组合值得借鉴。

## 关联概念
- [[Generative Adversarial Network]]
- [[Neural Architecture Search]]
- [[Evolutionary Neural Architecture Search]]
- [[Super-network]]
- [[Frechet Inception Distance]]
- [[Inception Score]]
- [[Mode Collapse]]

## 关联笔记
- [[ZeroNAS]]: 也是 GAN 结构搜索，但走的是 differentiable adversarial bi-level 路线，任务是 ZSL feature generation，而不是像素级图像生成。
- [[NAS-Bench-201]]: 可作为“结构搜索评测基准”对照，帮助区分 benchmark-style NAS 与 GAN-style open-ended 搜索。

