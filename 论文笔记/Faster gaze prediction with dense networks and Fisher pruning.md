---
title: "Faster Gaze Prediction With Dense Networks and Fisher Pruning"
method_name: "Fisher Pruning for Gaze Prediction"
authors: [Lucas Theis, Iryna Korshunova, Alykhan Tejani, Ferenc Huszar]
year: 2018
venue: arXiv
tags: [saliency, gaze-prediction, pruning, distillation, efficient-inference]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/1801.05787
local_pdf: D:/PRO/essays/papers/Faster gaze prediction with dense networks and Fisher pruning.pdf
created: 2026-03-20
---

# 论文笔记：Faster Gaze Prediction With Dense Networks and Fisher Pruning

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Faster Gaze Prediction With Dense Networks and Fisher Pruning |
| arXiv | https://arxiv.org/abs/1801.05787 |
| 作者页 | https://theis.io/publications/23/ |
| 代码 | Not officially released in the paper / author page (checked 2026-03-20) |
| 本地 PDF | `D:/PRO/essays/papers/Faster gaze prediction with dense networks and Fisher pruning.pdf` |
| 方法笔记 | [[Fisher Pruning for Gaze Prediction]] |

## 一句话总结
> 论文把 [[Knowledge Distillation]]、[[Fisher Pruning]] 和 FLOPs 约束结合起来，把 DeepGaze II 这类高精度 [[Saliency Prediction]] 模型压缩成更快的 FastGaze / DenseGaze，并在 CAT2000 上实现同等 AUC 下约 10x 的推理加速。

## 核心贡献
1. 提出一套面向 gaze / saliency prediction 的高效建模流程：先蒸馏、再逐步剪枝、最后在速度和效果之间取 Pareto 最优。
2. 给出 Fisher pruning 的更有原则的推导：用经验 [[Fisher Information Matrix]] 近似移除参数或 feature map 后的损失增量，而不是只靠启发式幅值。
3. 把“剪哪个 feature”从只看精度损失，扩展为同时考虑计算代价的联合目标，从而直接优化速度-性能权衡。
4. 证明在 gaze prediction 里，大型 ImageNet backbone 明显过参数化，经过蒸馏和剪枝后仍能保持很强泛化。

## 问题背景
### 要解决的问题
- 当时最强的 gaze prediction 方法 DeepGaze II 依赖 VGG-19 深层特征，预测效果好，但 CPU 单张推理非常慢。
- 真实场景里常常需要大批量图片甚至视频级处理，因此仅追求 saliency 指标而不考虑吞吐量并不实用。

### 现有方法的局限
- 直接沿用分类网络作 backbone，参数量和 FLOPs 对 fixation prediction 任务来说偏大。
- 以往 pruning 工作多聚焦分类，不直接针对 saliency prediction 的输出形式和部署需求。
- 只按权重大小或激活大小剪枝，很容易错删“虽然数值小但对输出分布重要”的 feature。

### 本文的核心想法
- 用 DeepGaze II teacher 在更多数据上生成 soft saliency map，再通过 [[Knowledge Distillation]] 允许 student 网络端到端微调。
- 用 Fisher 近似估计“删掉某个参数 / feature map 会让交叉熵涨多少”，把这个量当成 pruning signal。
- 把损失增量和 FLOPs 降低量合并进一个拉格朗日目标里，显式搜索最优速度-精度折中。

## 方法详解
### 1. 从 DeepGaze II 到更快骨干网络
- 原始 DeepGaze II 采用 VGG-19 多层特征、1x1 readout、Gaussian blur 和 [[Center Bias]] 先验，最终用 softmax 输出 fixation probability。
- 本文重实现时先做 readout 再上采样，从而避免对高维 feature map 做昂贵的双线性插值。
- 还把 Gaussian blur 改成 separable filter，进一步减轻推理代价。
- 基于此构建两类 student：
  - `FastGaze`: 用 VGG-11，且只取最后一层卷积特征。
  - `DenseGaze`: 用 DenseNet-121，并取 dense block 3 输出作为 readout 输入。

### 2. 输出分布建模
论文把 saliency map 写成：

$$
Q(x, y \mid I) \propto \exp \left(R(U(F(I))) * G_\sigma + \log Q(x, y)\right)
$$

- `F(I)`：backbone 提取的 feature maps。
- `R`：readout network，用 1x1 conv 做逐像素非线性映射。
- `U`：双线性上采样。
- `G_\sigma`：Gaussian blur。
- `\log Q(x, y)`：数据集相关的 [[Center Bias]] 对数先验。

这说明本文不是直接回归热图，而是显式输出一个像素级概率分布。

### 3. Fisher pruning 的核心推导
对交叉熵损失

$$
L(\theta) = \mathbb{E}_P[-\log Q_\theta(z \mid I)]
$$

在当前参数附近做二阶近似：

$$
L(\theta + d) - L(\theta) \approx g^\top d + \frac{1}{2} d^\top H d
$$

若把第 `k` 个参数置零，且近似认为局部一阶项在数据平均后消失，则损失增量约为：

$$
\Delta_k = \frac{1}{2N}\theta_k^2 \sum_{n=1}^N g_{nk}^2
$$

其中 `g_{nk}` 是第 `n` 个样本对参数 `theta_k` 的梯度。作者再用经验 [[Fisher Information Matrix]] 的对角项近似 Hessian 对角项，因此这个 pruning score 可以看成“删去该参数后预计会损失多少任务性能”。

### 4. 从参数剪枝到 feature-map 剪枝
卷积网络里真正影响速度的是通道数而不是稀疏单个权重，因此论文引入 binary mask `m_k` 乘到第 `k` 个 feature map 上：

$$
\tilde{a}_{nijk} = m_k a_{nijk}
$$

对 mask 的梯度为：

$$
g_{nk} = - \sum_{ij} a_{nijk} \frac{\partial}{\partial a_{nijk}} \log Q(z_n \mid I_n)
$$

于是 feature-map 级别的 pruning signal 为：

$$
\Delta_k = \frac{1}{2N}\sum_n g_{nk}^2
$$

这一步很关键，因为它把“影响输出分布的重要性”直接落到了通道级结构选择上。

### 5. 显式把计算成本放进目标
作者不只关心损失，而是求解：

$$
\min_\theta L(\theta) \quad \text{s.t.} \quad C(\theta) < K
$$

其中 `C(\theta)` 用 FLOPs 近似。对卷积层，计算成本写为：

$$
H \cdot W \cdot C_{out} \cdot (2 \cdot C_{in} \cdot K^2 + 1)
$$

实际 pruning 时最小化拉格朗日目标：

$$
L(\theta) + \beta C(\theta)
$$

删除某个 feature map 的综合代价为：

$$
\Delta L_i + \beta \Delta C_i
$$

这里 `\Delta L_i > 0`，而 `\Delta C_i < 0`。所以一个 feature 只有在“损失涨得不多，但 FLOPs 降得足够多”时才应该被剪。

### 6. 自动选择 trade-off 权重
论文还给出一个无需手动 sweep `beta` 的阈值式信号：

$$
\beta_i = - \frac{\Delta L_i}{\Delta C_i}
$$

直觉上，`beta_i` 越小，说明这个 feature 是“低性能代价、高算力收益”的优先剪枝对象。作者把它作为超参数自由的备选 pruning signal，但实验表明它更适合轻度剪枝，强剪枝下不如显式调 `beta` 稳定。

### 7. 训练流程
1. 先训练 DeepGaze II teacher：SALICON 预训练，用 MIT1003 做验证和 early stopping。
2. 把 10 个 DeepGaze II 模型做 ensemble，为 SALICON 图像生成平均 saliency map。
3. 用 teacher map 做蒸馏，student 的损失为 MIT1003 真值交叉熵和 teacher saliency 交叉熵的加权和，权重分别是 `0.1` 和 `0.9`。
4. student 收敛后开始剪枝：
   - 持续训练 10 个 step 并累计 Fisher pruning signal。
   - 每次删除 1 个 feature map。
   - 选择使综合代价 `\Delta L_i + \beta \Delta C_i` 最小的 feature。
5. 剪枝阶段优化器换成 SGD，学习率 `0.0025`，momentum `0.9`。

## 关键图表与结果
### Figure 1: 剪枝信号比较
- 对 FastGaze 不做 retraining，只看 pruning 本身的选择质量。
- 结果显示简单基线 `L1 activation` 和 `L1 weight` 很差。
- 不加 FLOPs 正则的 Fisher pruning 和 Molchanov 等方法相近，但显式考虑计算成本后更优。
- 动态更新 feature cost 也很重要，因为邻层被剪后，某个通道的边际计算成本会改变。

### Figure 2: 速度-性能 Pareto 曲线
- 在 CAT2000 上，FastGaze 更快，DenseGaze 精度更强。
- 就 log-likelihood、NSS、SIM 而言，两类 student 都能比论文重实现的 DeepGaze II 泛化得更好。
- AUC 上 DenseGaze 甚至略优于 DeepGaze II，而 FastGaze 稍弱但速度更极致。

### Table 1: LeNet-5 on MNIST 的 pruning sanity check
| Method | Error | Computational cost |
|---|---:|---:|
| LeCun et al. | 0.80% | 100% |
| Han et al. | 0.77% | 16% |
| Fisher (`beta = 0`) | 0.84% | 26% |
| Fisher (`beta > 0`) | 0.79% | 10% |
| Fisher (`beta*`) | 0.86% | 17% |

结论是：Fisher 信号本身有效，但如果目标是部署速度，必须把算力成本显式纳入优化。

### Table 2: MIT300 benchmark
| Model | AUC | KL | SIM | NSS | GFLOP |
|---|---:|---:|---:|---:|---:|
| DeepGaze II | 88% | 0.96 | 0.46 | 1.29 | 240.6 |
| FastGaze | 85% | 1.21 | 0.61 | 2.00 | 10.7 |
| DenseGaze | 86% | 1.20 | 0.63 | 2.16 | 12.8 |

这里最值得记的是量级变化：从 `240.6 GFLOP` 降到约 `11-13 GFLOP`，也就是一个数量级以上的压缩。

### 定性结果
- 即便在 39x speedup 下，模型仍能抓住 faces、people、objects、signs、text 等显著区域。
- 强剪枝后 saliency map 会更模糊，但关注目标基本一致。

## 实验设置
- 训练数据：SALICON, MIT1003。
- 泛化评估：CAT2000。
- Benchmark 提交：MIT300。
- CPU 速度测试：单核 Intel Xeon E5-2620 2.4GHz，输入大小 `384 x 512`，6 张图像取平均。
- 实现框架：PyTorch。
- 搜索范围：
  - FastGaze 总 feature maps：`2803`
  - DenseGaze 总 feature maps：`7219`
  - `beta` 采样范围：`3e-4` 到 `3e-1`

## 我对这篇论文的理解
### 为什么它有效
1. gaze prediction 的训练数据比 ImageNet 少得多，直接套大 backbone 很容易“表示过剩”，因此蒸馏 + 剪枝天然有空间。
2. Fisher score 不是看 feature 的绝对大小，而是看“它对输出分布的敏感度”，更接近任务本身。
3. 把 FLOPs 代价直接并入 pruning objective，使方法从“模型压缩”变成“结构-部署联合优化”。

### 优点
1. 方法很干净，几乎只依赖训练中已有的梯度信号，工程实现成本低。
2. 任务适配做得好，不只是把通用 pruning 套到 saliency 上，而是结合了输出分布、center bias 和蒸馏数据扩展。
3. 对 deployment 友好，直接报告 CPU runtime 而不只报参数量。

### 局限
1. 主要针对单图像 saliency，视频 saliency 只是动机，没有真正建模时序。
2. `beta` 仍需要随机搜索；自动 `beta*` 虽然优雅，但强剪枝场景不总是最优。
3. 论文没有提供官方代码，复现时 teacher 训练、蒸馏数据构造和 pruning schedule 都需要自己补齐。
4. 结果中不同指标并不完全一致，例如 AUC 与 NSS / SIM 的偏好不同，说明“最优模型”依赖部署指标。

## 对你现在笔记库的价值
- 这篇论文虽然不属于 NAS，但它很适合作为“任务驱动结构压缩”的代表案例。
- 它和很多 zero-cost / training-free proxy 思路不同，不是在搜索前估计架构质量，而是在训练后用近似二阶信息做结构删减。
- 如果你后面想整理 robustness / efficiency / NAS 之间的关系，这篇可以放在“Fisher 信息用于结构决策”的早期脉络里。

## 关联概念
- [[Fisher Pruning]]
- [[Fisher Information Matrix]]
- [[Knowledge Distillation]]
- [[Saliency Prediction]]
- [[Center Bias]]
- [[KL Divergence]]
- [[Pareto Front]]

