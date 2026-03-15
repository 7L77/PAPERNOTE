---
title: "DSRNA: Differentiable Search of Robust Neural Architectures"
method_name: "DSRNA"
authors: [Ramtin Hosseini, Xingyi Yang, Pengtao Xie]
year: 2021
venue: CVPR
tags: [nas, robust-nas, adversarial-robustness, differentiable-nas]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2012.06122
local_pdf: D:/PRO/essays/papers/DSRNA Differentiable Search of Robust Neural Architectures.pdf
created: 2026-03-15
---

# 论文笔记：DSRNA

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | DSRNA: Differentiable Search of Robust Neural Architectures |
| arXiv | https://arxiv.org/abs/2012.06122 |
| CVPR 页面 | https://openaccess.thecvf.com/content/CVPR2021/html/Hosseini_DSRNA_Differentiable_Search_of_Robust_Neural_Architectures_CVPR_2021_paper.html |
| 代码 | Not found (paper/arXiv 未给官方链接) |
| 本地 PDF | `D:/PRO/essays/papers/DSRNA Differentiable Search of Robust Neural Architectures.pdf` |

## 一句话总结
> DSRNA 在可微 NAS 中直接优化鲁棒性指标（[[Certified Robustness Lower Bound]] 或 [[Jacobian Norm Bound]]），而不是只靠对抗训练隐式增强鲁棒性。

## 核心贡献
1. 提出两类可微鲁棒性度量，并把它们直接放入架构搜索目标函数中（Sec. 3.1, Eq. 12-16）。
2. 给出基于 certified bound 的 DSRNA-CB，以及基于 Jacobian bound 的 DSRNA-Jacobian，并可组合成 DSRNA-Combined（Sec. 3.2）。
3. 在 CIFAR-10 / ImageNet / MNIST 上，在多种攻击下整体鲁棒性优于 RobNet、SDARTS-ADV、PC-DARTS-ADV（Table 1,3,4）。
4. 在 verification-based 评估中，得到更高的 certifiable lower bounds（Table 5,6）。

## 问题背景
### 要解决的问题
- 现有 [[Differentiable Architecture Search]] 搜出来的结构在对抗扰动下容易失稳。
- 以往 robust NAS 多依赖“对抗训练/噪声注入”这类间接策略，缺乏直接鲁棒性目标。

### 现有方法局限
- 通过训练过程“间接”提升鲁棒性，并不保证架构本身更稳健。
- 只优化 clean accuracy 的搜索目标，可能偏向“高精度但脆弱”的结构。

### 本文动机
- 如果鲁棒性指标本身对架构变量可微，就可以在架构搜索阶段显式最大化鲁棒性。

## 方法详解
### 1) Certified-bound robustness（Sec. 3.1.1）
- 对 ReLU-Conv-BN、(dilated) separable conv、pooling 等 block 做线性上下界传播（Eq. 1-11）。
- 在 DARTS 风格 DAG 中，block 输出乘以 architecture variable 后递归组合局部界，得到整网的 global lower bound。
- 把该 lower bound 作为鲁棒性度量 \(R\)。

### 2) Jacobian-bound robustness（Sec. 3.1.2）
- 定义输出变化的负期望：
\[
S=-\mathbb{E}_{x}\mathbb{E}_{\delta}\left[\frac{1}{K}\sum_{k=1}^{K}\left|f_k(x+\delta)-f_k(x)\right|\right],\quad \|\delta\|_p\le \epsilon
\]
（Eq. 12）
- 利用一阶 Taylor + Holder 不等式，把输出变化上界到 Jacobian 行向量范数（Eq. 13-15）。
- 进而最大化一个关于 Jacobian norm 的可微下界。

### 3) 鲁棒 NAS 目标（Sec. 3.2）
\[
\min_{\alpha}\sum_{i=1}^{M} \mathcal{L}(w^*(\alpha),\alpha,x_i^{val})
-\gamma R(w^*(\alpha),\alpha,x_i^{val})
\]
\[
\text{s.t. }w^*(\alpha)=\arg\min_{w}\sum_{i=1}^{N}\mathcal{L}(w,\alpha,x_i^{tr})
\]
（Eq. 16，双层优化）

- \(R\) 取 certified-bound 时为 DSRNA-CB，取 Jacobian-bound 时为 DSRNA-Jacobian。
- 两者可相加，得到 DSRNA-Combined。
- 求解上沿用 DARTS 近似（用一步 weight update 近似 \(w^*(\alpha)\)）。

## 关键图表与结果
### Table 1（CIFAR-10 attacked）
- DSRNA-Combined 在 PGD/FGSM/C&W/AutoAttack 指标上整体最强。
- 例如 PGD(100): 60.71；FGSM: 70.32；C&W: 64.76；AutoAttack(l2): 64.51。

### Table 2（CIFAR-10 clean）
- DSRNA-Combined clean acc 97.51，与强 NAS baseline 基本持平。
- 说明“鲁棒优化”没有明显牺牲无攻击精度。

### Table 3（ImageNet transfer）
- CIFAR-10 搜到的 cell 迁移到 ImageNet 后，DSRNA 在 C&W / AutoAttack(l2) 上明显优于 SDARTS-ADV / PC-DARTS-ADV。

### Table 4（MNIST）
- DSRNA-Combined 在 C&W 与 AutoAttack 指标优势明显，同时 clean acc 维持高水平（99.40）。

### Table 5/6（verification-based）
- DSRNA-CB 与 DSRNA-Jacobian 在 MNIST/CIFAR-10 的 \(l_\infty\) 与 \(l_2\) certifiable lower bounds 都更高。
- 例：MNIST \(l_2\) bound 约 0.4288（DSRNA-CB）对比 0.1767（SDARTS-ADV）。

## 实验与实现细节
- 搜索空间与 PC-DARTS 相同（8 ops，3x3/5x5 sep conv、dilated sep conv、pooling、identity、zero）。
- 搜索网络：8 cells, 50 epochs, init channels=16。
- DSRNA-CB 搜索代价较高但更稳健；DSRNA-Jacobian 更快更省内存。
- 文中报告（单 GTX1080Ti）：
  - CIFAR-10: DSRNA-CB 4 GPU days, DSRNA-Jacobian 0.4 GPU days
  - MNIST: DSRNA-CB 1 GPU day, DSRNA-Jacobian 0.2 GPU day

## 批判性思考
### 优点
1. 把“鲁棒性目标”从隐式训练技巧提升为显式可微目标，逻辑清晰。
2. 同时给出高保真（CB）与高效率（Jacobian）两条路线，并可组合。
3. 除 game-based 攻击评估外，额外给出 verification-based 证据。

### 局限
1. DSRNA-CB 成本仍偏高，对大规模搜索不够友好。
2. Jacobian 版本基于一阶近似，鲁棒性略弱于 CB 版本。
3. 官方代码未公开，端到端复现门槛较高。

### 潜在改进方向
1. 结合更高效的 certifier 或更紧下界，降低 CB 版本计算代价。
2. 在更大搜索空间和更多任务上验证泛化。
3. 结合硬件感知约束，形成鲁棒 + 效率联合搜索。

## 关联概念
- [[Robust Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Certified Robustness Lower Bound]]
- [[Jacobian Norm Bound]]
- [[Differentiable Architecture Search]]
- [[FGSM]]
- [[PGD Attack]]
