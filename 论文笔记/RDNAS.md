---
title: "RDNAS: Robust Dual-Branch Neural Architecture Search"
method_name: "RDNAS"
authors: [Anonymous Authors]
year: 2025
venue: ICLR 2026 Submission (OpenReview)
tags: [NAS, robust-nas, adversarial-training, shapley, dual-branch]
zotero_collection: ""
image_source: online
arxiv_html: "https://openreview.net/forum?id=JWW1hhEJTF"
local_pdf: "D:/PRO/essays/papers/Robust Dual-Branch Neural Architecture Search.pdf"
local_code: "D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search"
created: 2026-03-26
---

# 论文笔记：RDNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | RDNAS: Robust Dual-Branch Neural Architecture Search |
| 会议信息 | ICLR 2026 submission（OpenReview） |
| PDF | https://openreview.net/pdf?id=JWW1hhEJTF |
| Forum | https://openreview.net/forum?id=JWW1hhEJTF |
| 本地 PDF | `D:/PRO/essays/papers/Robust Dual-Branch Neural Architecture Search.pdf` |
| 本地代码目录 | `D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search` |

## 一句话总结

> RDNAS 在 DARTS 风格鲁棒 NAS 中引入“正常分支+鲁棒分支”双分支 cell，并用 [[Shapley Value]] 的鲁棒估计器 ROSE（[[Median-of-Means]] + [[Interquartile Range]]）稳定搜索打分，在保持较低搜索成本的同时提升多种白盒攻击下的鲁棒性。

## 核心贡献

1. 双分支 cell 设计：将 clean/robust 表征学习显式解耦，再通过 [[Efficient Channel Attention]] 融合。
2. ROSE 打分器：在对抗训练噪声下，用 MoM + IQR 对 Shapley 边际增益做稳健估计。
3. 小样本对抗搜索：在 CIFAR-10 上仅用 1000/500 train/val 样本做搜索，报告约 0.2 GPU-days。
4. 多数据集验证：CIFAR-10/100、SVHN、Tiny-ImageNet，并补充 NAS-Bench-201 与 ImageNet-1k 附加实验。

## 方法细节

### 1) 双分支 cell

令输入为 \(s_0,s_1\)，正常分支和鲁棒分支分别为：

\[
H_{norm}=C(s_0,s_1;\alpha_{norm}),\quad
H_{rob}=C(s_0,s_1;\alpha_{rob})
\]

Source: Sec. 3.2, Eq. (6)

拼接后：

\[
H=[H_{norm};H_{rob}]
\]

Source: Sec. 3.2, Eq. (7)

随后用 1x1 conv + GAP + 1D conv + sigmoid 产生通道权重并融合：

\[
U=W_{1\times1}(\mathrm{ReLU}(H)),\;
z=\mathrm{GAP}(U),\;
w=\sigma(\mathrm{Conv1D}(z)),\;
F=w\odot U
\]

Source: Sec. 3.2, Eq. (8)-(11)

### 2) 对抗搜索与外层更新

内层用 [[PGD Attack]] 生成对抗样本：

\[
x^{adv}=\arg\max_{\|\delta\|_\infty\le \epsilon} L_{train}(f(x+\delta),y)
\]

Source: Sec. 3.3, Eq. (12)

外层目标（ROSE 加权）：

\[
L_{val}(w^*(\alpha),\alpha)=
-\sum_{b=1}^3\sum_{e=1}^E\sum_{o=1}^O p_{e,o}^{(b)}(\alpha)\,\mathrm{Score}_{e,o}^{(b)}
\]

Source: Sec. 3.3, Eq. (13)

离散化：

\[
o_e^*=\arg\max_{k\in O}\alpha_e[k]
\]

Source: Sec. 3.3, Eq. (14)

### 3) ROSE（鲁棒 Shapley 估计）

先计算 clean/adv 边际增益：

\[
\Delta^{(s,b)}_{e,o,std}=Acc^{(s,b)}_{std}-Acc^{(s,b)}_{std,-o},\;
\Delta^{(s,b)}_{e,o,adv}=Acc^{(s,b)}_{adv}-Acc^{(s,b)}_{adv,-o}
\]

Source: Sec. 3.4, Eq. (15)

标准化后，做 IQR 异常分数 \(v\) 与 MoM 分数 \(m\)，最后组合：

\[
\mathrm{Score}^{(b)}_{e,o}=(1-\beta)m^{(b)}_{e,o}+\beta v^{(b)}_{e,o}
\]

Source: Sec. 3.4, Eq. (16)-(19)

作者报告 \(\beta\in[0.3,0.5]\) 表现较稳。

## 关键实验结果

### CIFAR-10（Table 1）

- RDNAS: Clean 86.56, FGSM 60.44, PGD20 52.62, PGD100 52.24, APGD-CE 52.05, AA 49.98
- 与 RACL 比：白盒指标整体更高，AA 略低（49.98 vs 50.23）
- 搜索成本：0.2 GPU-days（文中报告）

### Ablation（Table 4）

- 单分支 20 cells + ECA + adv search：86.0 / 51.5（clean/PGD20）
- 双分支 10 cells + ECA + adv search：86.5 / 52.6
- 结论：双分支 + ECA + 搜索期对抗训练组合最优。

### NAS-Bench-201（Table 5）

- RDNAS: search 731s, val 91.13±0.36, test 93.97±0.35
- 在其给出的基线中取得较好效率-精度折中。

### 附录 ImageNet-1k（Table 10）

- Ours: Clean 57.09, FGSM 22.11, PGD-20 12.68
- 超过其列出的 DARTS/LRNAS/CRoZe/ZCPRob/TRNAS。

## 与 OpenReview 讨论的关系

这篇工作的方法主线成立，但讨论区显示评审争议主要集中在：

1. “双分支优于单分支+TRADES”的证据是否足够闭环。
2. 对更强攻击与更系统 A/B 消融的充分性。
3. 仍局限于 [[Cell-based Search Space]]（DARTS/CNN），对 Transformer 范式覆盖有限。
4. 方法组件较多，复现和公平比较（如 FLOPs 对齐）解释空间较大。

## 批判性思考

这篇论文很典型地体现了鲁棒 NAS 的核心矛盾：

- 其优势来自把 [[Adversarial Training]] 纳入搜索环节；
- 但这也让“架构贡献”和“训练配方贡献”更难解耦。

从综述写作角度，它可以作为“高性能但耦合度高”的代表案例：

1. 搜索期攻击强度、训练损失、样本预算都会影响最终结构排序；
2. ROSE 在做“估计稳健化”，但仍建立在对抗训练生成的高噪声边际增益上；
3. 因而它更像是“在耦合系统里提高稳定性”，而不是完全解耦评估。

## 相关概念

- [[Robust Neural Architecture Search]]
- [[Differentiable Architecture Search]]
- [[Shapley Value]]
- [[Median-of-Means]]
- [[Interquartile Range]]
- [[Efficient Channel Attention]]
- [[Adversarial Training]]
- [[PGD Attack]]
- [[AutoAttack]]
- [[TRADES]]
- [[NAS-Bench-201]]
