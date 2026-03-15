---
title: "Anti-Bandit Neural Architecture Search for Model Defense"
method_name: "ABanditNAS"
authors: [Hanlin Chen, Baochang Zhang, Song Xue, Xuan Gong, Hong Liu, Rongrong Ji, David Doermann]
year: 2020
venue: arXiv
tags: [nas, robust-nas, adversarial-defense, bandit]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2008.00698v2
local_pdf: D:/PRO/essays/papers/Anti-Bandit Neural Architecture Search for Model Defense.pdf
local_code: D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense
created: 2026-03-15
---

# 论文笔记：ABanditNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Anti-Bandit Neural Architecture Search for Model Defense |
| arXiv | https://arxiv.org/abs/2008.00698 |
| 代码 | https://github.com/RunwenHu/ABanditNAS |
| 本地 PDF | `D:/PRO/essays/papers/Anti-Bandit Neural Architecture Search for Model Defense.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense` |

## 一句话总结
> ABanditNAS 把鲁棒 NAS 建模成“反 bandit”搜索：用 [[Lower Confidence Bound (LCB)]] 公平采样、用 [[Upper Confidence Bound (UCB)]] 逐步淘汰低潜力操作，在复杂搜索空间里更快找到抗攻击结构。

## 核心贡献
1. 提出 anti-bandit 搜索策略：不是用 UCB 直接选最优臂，而是结合 LCB 采样与 UCB 剪枝，兼顾公平性和效率（Sec. 3.3-3.4, Eq. 1-7, Algorithm 1）。
2. 在鲁棒 NAS 搜索空间中加入防御相关操作（[[Gabor Filter]]、[[Denoising Block]]），提升结构多样性（Sec. 3.1, Fig. 2）。
3. 给出复杂度从指数级候选组合到多项式级搜索迭代的分析（Sec. 3.4, Eq. 8）。
4. 在 MNIST/CIFAR-10 上，对白盒和黑盒攻击都取得更好鲁棒性与更低搜索成本（Table 1-3）。

## 问题背景
### 要解决的问题
- 如何在“对抗训练开销高 + 搜索空间大”的条件下，仍然高效地做 [[Robust Neural Architecture Search]]。

### 现有方法局限
- 常规 bandit/UCB 只偏向“当前均值高”操作，容易过早压制早期尚未训练充分的参数化操作。
- 直接扩大搜索空间（更多操作）会让鲁棒 NAS 成本飙升。

### 本文动机
- 早期表现差的操作不一定最终差，但长期表现持续差的操作应被及时淘汰；因此需要“先公平探索，再逐步放弃”的策略。

## 方法详解
### 1) 搜索空间（Sec. 3.1）
- 以 cell 为基本单元，cell 是全连接 DAG，`M=4` 个中间节点。
- 每条边从 `K=9` 个操作中选一个：max/avg pooling、skip、conv、sep-conv、[[Gabor Filter]]、[[Denoising Block]] 等。
- 论文给出示例设置 `v=6` 类 cell，候选规模可达 `9^(10×6)=9^60`。

### 2) 对抗训练目标（Sec. 3.2）
- 使用标准 min-max 对抗训练：
  - 内层在 `||δ||_∞ <= ε` 下生成扰动；
  - 外层优化模型参数。
- 搜索阶段使用带随机初始化的 [[FGSM]] 近似，以降低相对 [[PGD Attack]] 的开销。

### 3) Anti-bandit 采样与剪枝（Sec. 3.3-3.4）
- 先用 LCB 定义采样分数 `sL`，以 `exp(-sL)` softmax 得到每个操作的采样概率；
- 每轮对采样结构做一轮对抗训练，得到验证准确率 `a`，并用指数滑动更新操作历史性能；
- 每 `K*T` 次采样后，计算 UCB 分数 `sU`，在每条边上剪掉 `sU` 最小的操作；
- 重复直到每条边只剩一个操作。

### 4) 复杂度（Eq. 8）
- 论文声称候选组合是指数级；
- ABanditNAS 的搜索迭代复杂度为 `O(T * sum_{k=2..K} k) = O(TK^2)`。

## 关键公式（含解释）
### Eq. (1) UCB
\[
\hat{r}_k + \sqrt{\frac{2\log N}{n_k}}
\]
- 第一项偏向历史高回报，第二项鼓励少采样臂的探索。

### Eq. (2) LCB
\[
\hat{r}_k - \sqrt{\frac{2\log N}{n_k}}
\]
- 置信下界更小的操作会得到更多再次采样机会。

### Eq. (3) 边级 LCB 分数
\[
s_L(o_k^{(i,j)})=m_{k,t}^{(i,j)}-\sqrt{\frac{2\log N}{n_{k,t}^{(i,j)}}}
\]

### Eq. (4) 采样概率
\[
p(o_k^{(i,j)})=\frac{\exp(-s_L(o_k^{(i,j)}))}{\sum_m \exp(-s_L(o_m^{(i,j)}))}
\]

### Eq. (5) 历史性能更新
\[
m_{k,t}^{(i,j)}=(1-\lambda)m_{k,t-1}^{(i,j)}+\lambda a
\]
- `λ` 用于平衡新观测和历史均值（实验里最优约为 `0.7`）。

### Eq. (6) UCB 分数
\[
s_U(o_k^{(i,j)})=m_{k,t}^{(i,j)}+\sqrt{\frac{2\log N}{n_{k,t}^{(i,j)}}}
\]

### Eq. (7) 剪枝
\[
\Omega^{(i,j)} \leftarrow \Omega^{(i,j)} - \left\{\arg\min_{o_k^{(i,j)}} s_U(o_k^{(i,j)})\right\}
\]

### Eq. (8) 复杂度
\[
O\!\left(T\sum_{k=2}^{K}k\right)=O(TK^2)
\]

## 关键实验结论
### MNIST（Table 1）
- `ABanditNAS-6`：Clean `99.52`，FGSM `98.94`，PGD-40 `97.01`，PGD-100 `95.70`。
- 搜索成本 `0.08 GPU days`，与剪枝版 UCBNAS 接近，但鲁棒性更强。

### 白盒/黑盒（Table 2）
- CIFAR-10 上 `ABanditNAS-10` 在白盒 PGD-7 下 `58.74`；
- 黑盒（ResNet-18 迁移）PGD 下达到 `81.26`，显示较强迁移鲁棒性。

### CIFAR-10（Table 3）
- `ABanditNAS-10`：PGD-7 `58.74`，PGD-20 `50.51`，明显高于 Wide-ResNet 的 `50.0/45.8`。
- 搜索成本仍约 `0.08 GPU days`。

### 消融（Sec. 4.3, Fig. 5）
- `λ=0.7` 时性能最好；论文也明确说明部分结果有不稳定性，需要多次试验。

## 与代码实现的对照
- 归档仓库 README 与论文标题、摘要描述一致：`README.md`。
- 操作定义可在 `models/darts_ops_1.py` 找到，包含 `gab_filt_3x3` 与 `dtp_blok_3x3`。
- 归档代码主要是“测试脚本 + 预训练权重 + 已搜索结构”（如 `defenses/defense_all.py`, `utils/genotypes_all.py`）。
- **未发现完整的 anti-bandit 搜索训练主循环**（与论文 Algorithm 1 的逐轮采样/剪枝流程不完全对齐）。

## 批判性思考
### 优点
1. 把“公平探索”和“早淘汰”合并到同一策略里，直观且可解释。
2. 在鲁棒性与搜索成本之间给出不错平衡。
3. 引入防御相关操作（Gabor/denoising）让搜索空间更贴近任务需求。

### 局限
1. 实验主要集中于 MNIST/CIFAR-10，小规模数据集上的结论外推有限。
2. 对鲁棒评估稳定性给出了提示，但重复试验统计仍不充分。
3. 公开代码更偏重评估复现，搜索端可复现实操门槛仍高。

### 潜在改进方向
1. 在更大规模数据集和现代 backbone 上复核 anti-bandit 优势。
2. 补齐完整搜索代码和日志，降低复现难度。
3. 将 UCB/LCB 策略与硬件约束（真实延迟）结合，而不仅是参数量/FLOPs。

## 关联概念
- [[Neural Architecture Search]]
- [[Robust Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Multi-Armed Bandit]]
- [[Upper Confidence Bound (UCB)]]
- [[Lower Confidence Bound (LCB)]]
- [[FGSM]]
- [[PGD Attack]]
- [[Gabor Filter]]
- [[Denoising Block]]

