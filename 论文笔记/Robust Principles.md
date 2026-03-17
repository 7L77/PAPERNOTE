---
title: "Robust Principles: Architectural Design Principles for Adversarially Robust CNNs"
method_name: "Robust Principles"
authors: [ShengYun Peng, Weilin Xu, Cory Cornelius, Matthew Hull, Kevin Li, Rahul Duggal, Mansi Phute, Jason Martin, Duen Horng Chau]
year: 2023
venue: BMVC
tags: [adversarial-robustness, cnn, architecture-design, adversarial-training]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2308.16258
local_pdf: D:/PRO/essays/papers/Robust Principles Architectural Design Principles for Adversarially Robust CNNs.pdf
local_code: D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs
created: 2026-03-17
---

# 论文笔记：Robust Principles

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Robust Principles: Architectural Design Principles for Adversarially Robust CNNs |
| arXiv | https://arxiv.org/abs/2308.16258 |
| 代码 | https://github.com/poloclub/robust-principles |
| 会议 | BMVC 2023 |
| 本地 PDF | `D:/PRO/essays/papers/Robust Principles Architectural Design Principles for Adversarially Robust CNNs.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs` |

## 一句话总结
> 这篇论文提出三条可组合的 CNN 鲁棒架构原则（WD 比例、conv stem、SE+SiLU），并在 CIFAR-10/100 与 ImageNet 上稳定提升 [[Adversarial Robustness]]。

## 核心贡献
1. 提出统一的宏观设计规则：将网络的 [[Width-Depth Ratio]] 控制在经验最优区间 `[7.5, 13.5]`，替代“只调某一层深度/宽度”的经验做法。
2. 证明 stem 设计会系统影响鲁棒性：[[Convolutional Stem]]（尤其 postponed downsampling）整体优于 [[Patchify Stem]]。
3. 在残差块内给出更稳健的组合：SE 模块采用较小 reduction ratio（推荐 `r=4`），激活函数采用非参数平滑激活（SiLU/GELU）而不是参数化变体。

## 问题背景
### 要解决的问题
- 过去关于“哪些结构组件能提升对抗鲁棒性”的结论相互矛盾，且很多只在 CIFAR 小规模设置上验证。
- 目标是提炼一套跨数据规模、跨训练配方、跨网络家族都能复用的结构原则。

### 现有方法的局限
- 很多结论局限于 WRN + CIFAR，外推到 ImageNet 时可能失效。
- 对 SE 和激活函数的结论在不同论文中存在冲突，缺乏统一视角。

## 方法详解
### 1) 对抗训练目标（论文 Eq. 1）
论文沿用标准 min-max 目标：

$$
\min_{\theta}\ \mathbb{E}_{(x,y)\sim \mathcal{D}}\left[\max_{x' \in \mathcal{B}(x,\epsilon)} \mathcal{L}(f_\theta(x'), y)\right]
$$

**含义**：内层找最坏扰动样本，外层更新参数使模型在最坏扰动下也尽量正确。  
**符号说明**：
- $\theta$: 模型参数。
- $(x,y)$: 数据样本与标签。
- $x'$: 对抗样本。
- $\mathcal{B}(x,\epsilon)$: 以 $x$ 为中心、扰动半径为 $\epsilon$ 的约束集合（文中主要是 $\ell_\infty$）。

### 2) 宽深比原则（论文 Eq. 2）
定义（排除最后一个 stage）：

$$
\text{WD ratio}=\frac{1}{n-1}\sum_{i=1}^{n-1}\frac{W_i}{D_i}
$$

**含义**：衡量“每个 stage 的宽度相对深度有多大”。  
**结论**：
- 论文随机采样大量结构后发现，WD ratio 与鲁棒精度总体负相关。
- 最优区间约为 `[7.5, 13.5]`，而标准 ResNet-50 大约是 `32`，偏宽偏浅。

### 3) Stem 原则
- 同等对比下，卷积 stem（含重叠卷积、较温和下采样）优于 patchify stem。
- 把 patch 变小并增加重叠会改善鲁棒性，支持“重叠 + 低侵略下采样”这个机制解释。
- 将 stem 输出宽度从 64 提升到 96 在参数几乎不变时也能带来收益。

### 4) 残差块原则
- [[Squeeze-and-Excitation Block]] 在 ImageNet 上可显著提升鲁棒性；并且 reduction ratio 越小通常越好（文中 sweep: `r={2,4,8,16,32,64}`，推荐 `r=4`）。
- 激活函数方面，[[SiLU (Sigmoid Linear Unit)]] / [[GELU]] 这类非参数平滑激活整体优于 ReLU 和参数化平滑激活（PSiLU/PSSiLU）。

## 关键图表
### Figure 1: 三条鲁棒架构原则总览
- 图链接：https://raw.githubusercontent.com/poloclub/robust-principles/main/img/principles.png
- 说明：把原则拆成宏观（宽深配置、stem）与微观（SE、激活）两层。

### Figure 2: 组件分析实验
- 参考位置：https://arxiv.org/html/2308.16258#S4.F2
- 说明：展示 WD ratio 趋势、stem 对比、SE/激活组件对比。

### Table 1: ResNet-50 逐步改造成 RaResNet-50（ImageNet/Fast-AT）
| 配置 | Clean | PGD10-2 | PGD10-4 | PGD10-8 |
|---|---:|---:|---:|---:|
| ResNet-50 | 56.05 | 42.81 | 30.59 | 12.62 |
| +WD 配置 | 57.85 | 45.90 | 33.87 | 15.27 |
| +Conv Stem | 58.00 | 46.59 | 34.90 | 15.85 |
| +SE | 60.22 | 48.95 | 36.43 | 16.43 |
| +SiLU | 62.02 | 51.47 | 39.65 | 18.97 |

### Table 2: CIFAR-10/100 综合结果（节选）
- 文中结论：跨 SAT/TRADES/MART/Diffusion-AT、跨参数规模均有一致增益。
- 代表结果：RaWRN-70-16（Diff.1M）在 CIFAR-10 AA 从 `65.02` 提升到 `66.33`；在 CIFAR-100 AA 从 `37.77` 提升到 `38.73`。

### Table 3: ImageNet 结果（SAT）
| 模型 | 参数量 | AA | PGD100-4 |
|---|---:|---:|---:|
| ResNet-50 | 26M | 34.96 | 38.96 |
| RaResNet-50 | 26M | 44.14 | 47.77 |
| ResNet-101 | 45M | 39.78 | 43.17 |
| RaResNet-101 | 46M | 46.26 | 49.30 |
| WRN-101-2 | 127M | 42.00 | 45.27 |
| RaWRN-101-2 | 104M | 48.94 | 51.03 |

## 与代码实现的对照
- 本地代码使用 Hydra 配置系统统一切换模型、攻击、训练配方（`robustarch/main.py`）。
- 训练端在 `robustarch/adv_train.py` 中直接构造 `LinfPGDAttack` 执行内层最大化；支持 FAT/SAT。
- `MODEL.mk` 里显式给出 RaResNet50 的关键覆盖参数：
  - `depths=[5,8,13,1]`
  - `group_widths=[36,72,140,270]`（对应 WD 控制）
  - `stem_width=96`、postponed downsampling
  - `se_ratio=0.25`（约等于 reduction ratio `r=4`）
  - 全部激活切到 `SiLU`

## 批判性思考
### 优点
1. 不是单点 trick，而是“可组合规则集”，便于迁移到不同 backbone。
2. 同时覆盖 CIFAR 与 ImageNet，缓解“小数据集结论不稳”的问题。
3. 提供了比较可执行的配置路径（从 ResNet-50 到 RaResNet-50 的路线图）。

### 局限
1. 主要仍是经验性鲁棒评估，对攻击设定和训练配方敏感。
2. 很多细节在主文只给趋势，不同场景下最优 WD 区间可能需要重新标定。
3. 论文强调 CNN 族，迁移到 ViT/MLP-Mixer 这类架构还需额外验证。

### 可复现性评估
- [x] 代码开源
- [x] 关键配置可定位（`MODEL.mk` + `configs/`）
- [x] 提供预训练权重下载入口
- [ ] 复现实验需要较大算力（尤其 ImageNet + 对抗训练）

## 关联笔记
- [[RobNet]]: 关注“用 NAS 搜鲁棒结构”，而本工作是“给通用 CNN 设计规则”。
- [[Robust-ZCP]]: 前者偏代理评估，本文偏架构原理与实证。
- [[Adversarial Robustness]]
- [[PGD Attack]]
- [[RobustBench]]

