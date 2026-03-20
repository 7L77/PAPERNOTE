---
title: "Group Fisher Pruning for Practical Network Compression"
method_name: "Group Fisher Pruning"
authors: [Liyang Liu, Shilong Zhang, Zhanghui Kuang, Aojun Zhou, Jing-Hao Xue, Xinjiang Wang, Yimin Chen, Wenming Yang, Qingmin Liao, Wayne Zhang]
year: 2021
venue: ICML
tags: [pruning, model-compression, structured-pruning, object-detection]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/Group Fisher Pruning for Practical Network Compression.pdf
local_code: D:/PRO/essays/code_depots/Group Fisher Pruning for Practical Network Compression
created: 2026-03-20
---

# 论文笔记：Group Fisher Pruning

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Group Fisher Pruning for Practical Network Compression |
| 会议 | ICML 2021 / PMLR 139 |
| PMLR | https://proceedings.mlr.press/v139/liu21ab.html |
| arXiv | https://arxiv.org/abs/2108.00708 |
| 代码 | https://github.com/jshilong/FisherPruning |
| 本地 PDF | `D:/PRO/essays/papers/Group Fisher Pruning for Practical Network Compression.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Group Fisher Pruning for Practical Network Compression` |

## 一句话总结
> Group Fisher Pruning 把结构化通道剪枝推广到残差、组卷积、深度卷积和 FPN 这类“跨层耦合通道”场景，用基于 [[Fisher Information Matrix|Fisher Information]] 的全局重要性和按 memory reduction 归一化的贪心剪枝来换取更真实的 GPU 加速。

## 核心贡献
1. 提出 layer grouping：沿计算图自动找出必须一起删的 [[Coupled Channels]]，而不是只剪“内部层”。
2. 用 Fisher 近似把单通道重要性写成 mask 梯度平方，并把共享 mask 的多层耦合通道重要性写成跨层梯度求和后的平方。
3. 指出实际 GPU 加速更接近 memory access 的下降而不是 FLOPs 的下降，因此用 memory reduction 而不是 FLOPs reduction 做重要性归一化。
4. 在 ResNet、ResNeXt、MobileNetV2、RegNet 以及带 [[Feature Pyramid Network]] 的检测器上验证了“准确率-速度”折中。

## 问题背景

### 要解决的问题
- 传统 [[Channel Pruning]] 多半默认网络是串行的，剪掉某层输入通道只影响它唯一的前驱层。
- 但现代 CNN 常见结构包含残差分支、[[Group Convolution]]、[[Depth-wise Convolution]]、[[Feature Pyramid Network]]，这些结构里多个层的通道是绑在一起的。
- 如果仍然按单层独立剪枝，FLOPs 看起来会下降，但真正可删掉的输出通道和访存并不多，实际推理速度提升有限。

### 现有方法的局限
- 局部重建误差类方法如 CP、ThiNet 主要是 layer-wise，通常要手工做 per-layer sensitivity analysis。
- 依赖 BN scale 的方法在检测场景不稳定，因为检测模型往往不能像分类一样广泛依赖 BN。
- 只考虑单层 importance、不处理耦合结构的方法，很容易在残差和 FPN 中“算上了 FLOPs，没拿到 speedup”。

### 本文动机
- 真正想要的是“删掉对 loss 影响小、同时能带来实际推理开销下降的通道组”。
- 所以作者同时回答两个问题：
  1. 哪些通道必须一起删？
  2. 用什么 proxy 才更接近真实 GPU speedup？

## 方法详解

### 1. 给每个输入通道加二值 mask
- 对每个 Conv/FC 层输入通道引入二值 mask `m`，初始全为 1。
- 将输入特征 `A` 变成 masked input `\tilde{A} = A \odot m`。
- 当某个通道的 mask 被置 0，就等价于把该输入通道剪掉；而对应父层的输出通道也应随之删除。

### 2. 用 Fisher 近似单通道的重要性
作者对“删掉第 `i` 个通道后 loss 变大多少”做二阶 Taylor 近似：

$$
s_i = L(m - e_i) - L(m) \approx -g_i + \frac{1}{2} H_{ii}
$$

- 这里 `g_i` 是 loss 对 mask `m_i` 的一阶梯度，`H_{ii}` 是 Hessian 的对角项。
- 当模型在收敛点附近时，`g_i \approx 0`，于是重要性主要由 `H_{ii}` 决定。
- 进一步作者用 [[Fisher Information Matrix|Fisher Information]] 把它近似成 sample-wise mask 梯度平方的均值：

$$
s_i \propto \frac{1}{N}\sum_{n=1}^{N}\left(\frac{\partial L_n}{\partial m_i}\right)^2
$$

### 3. 用 layer grouping 找到耦合通道
- 作者沿反向计算图做 DFS，只保留 Conv/FC 层，给每个层找最近的父 Conv。
- 如果两个层共享父层，它们的输入通道耦合，应该分到同一组。
- 如果某层或其父层是 [[Group Convolution]] / [[Depth-wise Convolution]]，则同组里还要同步考虑组内输入输出通道耦合。
- 在残差块里，这样可以把两个分支上“同索引”的通道绑在一起剪，而不是只剪 bottleneck 内部。

### 4. 共享 mask 后的组重要性
对一组共享同一个 mask 的通道集合 `X`，作者把组重要性写成跨层梯度求和后的平方：

$$
s_i^{(X)} \propto \sum_{n=1}^{N}\left(\sum_{x \in X}\frac{\partial L_n}{\partial m_i^x}\right)^2
$$

- 这不是 heuristic，而是共享参数下链式法则的直接结果。
- 因而可以自然处理层内耦合和跨层耦合。

### 5. 为什么用 memory reduction 归一化，而不是 FLOPs
- 原始 `s_i` 只看“删掉它损失会多大”，不看“删掉它能省多少计算”。
- 作者先试了 FLOPs reduction，但实验发现实际 GPU speedup 和 FLOPs 并不线性。
- 相比之下，输出激活/访存规模的减少更贴近 wall-clock speedup，于是最终采用：

$$
\text{score}_i = \frac{s_i}{\Delta M_i}
$$

### 6. 剪枝流程
1. 从已收敛的 dense 模型出发。
2. 先通过 layer grouping 找到所有耦合组。
3. 跑若干 batch，累积 mask 梯度对应的 Fisher importance。
4. 每隔 `d` 次迭代，剪掉当前 `s_i / \Delta M_i` 最小的通道或通道组。
5. 继续训练并重新累积重要性，直到达到目标 FLOPs。
6. 最后对裁剪后的结构做完整 fine-tune。

## 关键图表与结果

### Figure 3 / 4 / 5：结构约束是本文的关键
- Fig. 3 展示了残差块、group conv、FPN、RPN/R-CNN 这些“必须同步删通道”的典型结构。
- Fig. 4 用 DFS 找 parent layers，是 layer grouping 的核心可视化。
- Fig. 5 给出 GConv 和 Faster R-CNN 中如何把跨层梯度聚到同一个共享 mask 上。

### Figure 6：memory 比 FLOPs 更接近 speedup
- 文中明确展示，随着剪枝推进，reduced memory 与 relative speedup 关系更线性。

### Table 1：同样 50% FLOPs，剪 coupled channels 明显更快
- ResNet-50：
  - `Res50-I` 只剪内部层：Top-1 `76.23%`，`50.22 ms`，`1.30x`
  - `Res50-M` 剪 coupled channels 且用 memory normalization：Top-1 `76.42%`，`36.50 ms`，`1.79x`
  - `Res50-F` 用 FLOPs normalization：Top-1 `76.20%`，`47.07 ms`，`1.39x`

### Table 2 / 3：MobileNetV2 和 RegNet 也能受益
- 在 MobileNetV2 上，pruned model 在 matched FLOPs 下普遍更快、更准。
- 在 RegNetX 上，pruned model 甚至能超过 searched smaller RegNet，例如 `RegX-0.8G` 上 `76.39%` 对 `75.24%`。

### Table 5 / 6：检测场景是亮点
- RetinaNet：`36.5 AP -> 36.5 AP`，同时 `1.57x` speedup。
- Faster R-CNN：
  - 50% FLOPs 档：`37.8 AP`，`1.73x`
  - 25% FLOPs 档：`36.6 AP`，`3.07x`

## 代码与复现备注
- 官方仓库直接给出了公开代码链接：`https://github.com/jshilong/FisherPruning`。
- 公开实现主要是 detection 版本，`README` 明确写了 classification code 之后再放。
- 代码要求 `pytorch==1.3.0`，因为它强依赖旧版 autograd graph 接口来做 layer grouping。
- 代码里的 `delta='acts'` 本质上就是用 activation count 近似 paper 中讲的 memory reduction。
- 一个需要记住的 paper/code 差异：
  - 论文覆盖 one-stage 和 two-stage detection。
  - 公开代码在 `fisher_pruning.py` 里还有 `# TODO: support two stage model`，README 也只明确宣布了 one-stage detection models released。

## 批判性思考

### 优点
1. 问题抓得非常准：结构化剪枝真正的难点不是 importance 本身，而是 coupled channels。
2. 把“真实 speedup”显式拉进方法设计里，而不是只停留在 FLOPs。
3. 一套框架同时覆盖 backbone、mobile network、NAS backbone 和检测器，工程泛化性强。

### 局限
1. 方法依赖 iterative prune-and-finetune，训练成本并不低。
2. Fisher 近似默认模型在较好收敛点附近；若基模型质量差，importance 估计可能不稳。
3. memory proxy 对 GPU 很有效，但对 CPU、TPU 或不同 kernel 实现是否同样成立，文中没有系统展开。
4. 公开代码与论文覆盖范围并不完全一致，尤其分类和 two-stage detection 的可复现性弱一些。

## 关联概念
- [[Channel Pruning]]
- [[Fisher Information Matrix|Fisher Information]]
- [[Coupled Channels]]
- [[Group Convolution]]
- [[Depth-wise Convolution]]
- [[Feature Pyramid Network]]

## 关联笔记
- [[Group Fisher Pruning]]

## 速查卡片
> [!summary] Group Fisher Pruning
> - 核心：自动找耦合通道组，用 Fisher 梯度平方评估重要性，再按 memory reduction 归一化做全局贪心剪枝。
> - 关键区别：不是只剪单层，而是剪 coupled channels。
> - 关键结论：真实 GPU speedup 更贴近 memory reduction，而不是 FLOPs reduction。
> - 检测亮点：Faster R-CNN 在 25% FLOPs 档还能做到约 `3x` 加速、`0.8 AP` 左右损失。
