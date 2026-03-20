---
title: "Vulnerable Data-Aware Adversarial Training"
method_name: "VDAT"
authors: [Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: NeurIPS
tags: [adversarial-training, fast-adversarial-training, data-filtering, robust-nas]
zotero_collection: ""
image_source: online
arxiv_html: ""
local_pdf: D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf
created: 2026-03-20
---

# 论文笔记：VDAT

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Vulnerable Data-Aware Adversarial Training |
| 会议 | NeurIPS 2025 |
| 本地 PDF | `D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf` |
| 代码链接（作者主页给出） | https://github.com/fyqsama/VD-AT |
| 本地代码归档 | 暂未归档（仓库地址当前返回 404） |

## 一句话总结
> VDAT 用“样本脆弱性”替代“批次代表性”做筛选，让更脆弱样本更高概率走对抗训练，在更低训练成本下同时提升自然精度和鲁棒精度。

## 核心贡献
1. 提出基于 [[Decision Margin]] 差异的样本脆弱性估计（Sec. 4.1），从样本级别刻画“离决策边界有多近”。
2. 提出 [[Vulnerability-aware Data Filtering]]（Sec. 4.2），按脆弱性概率化地将样本分配到自然训练或对抗训练。
3. 在 CIFAR-10/100 和 ImageNet-1K 上，相比强基线在精度和成本上同时改进（Sec. 5.2, Tab. 1-3）。
4. 验证该策略可插入 [[Robust Neural Architecture Search]] 流程并降低搜索成本（Sec. 5.3, Tab. 4）。

## 问题背景
### 要解决的问题
- 现有快速对抗训练（FAT）通常对所有样本“一视同仁”，或者做 batch-wise 过滤。
- 但不同样本到决策边界的距离不同，部分样本对鲁棒性提升贡献更大。

### 现有方法局限
- 只做 batch 级筛选会漏掉“弱批次里的脆弱样本”，同时保留“强批次里的非脆弱样本”。
- 单纯增强对抗样本生成效率（如 FGSM 变体）并不直接解决“该训练哪些样本”的问题。

### 本文动机
- 从 sample-wise 角度识别并优先学习脆弱样本，减少无效对抗训练样本的计算开销。

## 方法详解
### 1) 脆弱性计算：Margin-based Vulnerability Calculation（Sec. 4.1）
- 先生成每个样本对应的对抗样本，然后比较自然样本与对抗样本的 logit margin 差异。
- 直观上：margin 差异越小，样本越“脆弱”，越值得进入对抗训练子集。
- 作者将 hard margin 扩展到 soft margin（log-sum-exp 形式）以更好覆盖 targeted attack 情况。

### 2) 脆弱性驱动过滤：Vulnerability-aware Data Filtering（Sec. 4.2）
- 将每个样本脆弱性归一化为概率 \(P_\theta(x_i)\in[0,1]\)。
- 用随机门控判断样本是否加对抗扰动：
  - 若 `Rand(0,1) <= P_theta(x_i)`，该样本进入对抗训练；
  - 否则进入自然训练。
- 最终训练损失：
  - `L_train = L_nat(X_nat, theta) + L_adv(X_adv, theta)`。

### 3) 训练流程（Algorithm 1）
- 每隔 `T` 个 epoch 重新计算脆弱性并刷新筛选结果；
- 每个 epoch 都用当前 `X_nat` 与 `X_adv` 更新模型参数；
- `T` 用于在性能与开销之间折中。

## 关键公式
### Eq. (1) 决策间隔（Preliminaries）
\[
M_\theta^y(x)=\ell_\theta^y(x)-\max_{y' \neq y}\ell_\theta^{y'}(x)
\]
含义：真实类别 logit 与最强竞争类别 logit 的差。

### Eq. (2) 硬间隔脆弱性
\[
V_\theta(x_i)=-\left|M_\theta^y(x_i)-M_\theta^y(x_i')\right|
\]
含义：自然样本和对抗样本的 margin 差值绝对值越大，通常表示越不脆弱。

### Eq. (3)-(5) 软间隔与软脆弱性
\[
S_\theta^y(x)=\ell_\theta^y(x)-\frac{1}{\tau}\log\sum_{y' \neq y}\exp(\tau \ell_\theta^{y'}(x))
\]
\[
V_\theta(x_i)=-\left|S_\theta^y(x_i)-S_\theta^y(x_i')\right|
\]
含义：用温度参数 \(\tau\) 控制“软最大”，更稳定地覆盖 targeted 场景。

### Eq. (6) 样本进入对抗训练的概率
\[
P_\theta(x_i)=\frac{1}{2}\left(
\frac{V_\theta(x_i)-\overline{V_\theta}}{\max_k|V_\theta(x_i)-V_\theta(x_k)|}+1
\right)
\]
含义：把脆弱性线性映射到 \([0,1]\) 作为筛选概率。

### Eq. (7)-(8) 概率筛选与联合损失
\[
F(x_i)=
\begin{cases}
x_i+\delta,& R(0,1)\le P_\theta(x_i)\\
x_i,& R(0,1)>P_\theta(x_i)
\end{cases}
\]
\[
L_{\text{train}}=L_{\text{nat}}(X_{\text{nat}},\theta)+L_{\text{adv}}(X_{\text{adv}},\theta)
\]

## 关键图表与结论
### Figure 1
- 对比 batch-wise 筛选与 sample-wise 脆弱性筛选的核心差异。

### Figure 2（ImageNet-1K）
- 在自然精度、PGD50 与训练成本三者上，VDAT 显示出更优折中。

### Table 1（CIFAR-10/100）
- 在 ResNet18 与 WRN34-10 上，VDATFGSM/VDATPGD 在多数攻击设置下达到 SOTA 或接近 SOTA。
- 典型例子：CIFAR-10 + ResNet18，VDATFGSM 在 PGD50=56.23，训练开销 1.04 GPUh。

### Table 2（ImageNet-1K）
- ResNet50 上，VDATFGSM：Natural=67.47，PGD10=39.48，PGD50=38.69，成本 38.41 GPUh。

### Table 3（与数据过滤类 FAT 对比）
- 对 AdvGradMatch/DFEAT，VDAT 在三套数据集上精度更高且成本更低。

### Table 4（Robust NAS）
- 将 VDAT 注入 DSRNA/AdvRush/RNAS/ARNAS，搜索成本显著下降且鲁棒指标多数场景提升。

### Figure 4-5（可视化）
- 训练过程稳定收敛；
- 训练后 margin difference 分布整体右移，说明脆弱样本得到更有效学习。

## 复杂度与效率
- 理论时间复杂度：`O(nk)`（Sec. 4.3）。
  - `n`：样本数；
  - `k`：类别数。
- 直观瓶颈：
  - 脆弱性计算需遍历样本并处理所有类别 logit；
  - 但筛选后对抗训练样本规模变小，整体 wall-clock 可下降。

## 实验设置速记
- 数据集：CIFAR-10 / CIFAR-100 / ImageNet-1K。
- 基础模型：ResNet18、WRN34-10、ResNet50。
- 默认超参：\(\tau=5\), \(T=10\)。
- 脆弱性评估前扰动：默认 FGSM。
- 评估攻击：FGSM、PGD、C&W、[[AutoAttack]]。

## 批判性思考
### 优点
1. 把“算力花在哪些样本上”显式建模，属于 FAT 里非常实用的角度。
2. 方法结构简单，可插拔到不同对抗训练框架（TRADES/AWP）与 robust NAS 流程。
3. 在中小规模和大规模数据集上都给出了一致增益。

### 局限
1. 脆弱性定义依赖当前模型与当前扰动方式，存在训练阶段偏置风险。
2. 概率筛选引入随机性，复现时需严格控制随机种子和筛选周期。
3. 作者主页给出的代码仓库当前无法访问（404），工程复现细节受限。

### 对你当前方向（鲁棒 NAS / ZCP）的启发
1. 可把样本级脆弱性权重引入 supernet 训练样本采样，而不只在 loss 上加权。
2. 可尝试把 `P_theta(x)` 改为多目标版本（clean-robust-cost 联合概率）。
3. 可与已有 robust proxy 联动：优先在“高脆弱样本”上评估 proxy 稳定性。

## 关联概念
- [[Adversarial Training]]
- [[FGSM]]
- [[PGD Attack]]
- [[Decision Margin]]
- [[Vulnerability-aware Data Filtering]]
- [[Catastrophic Overfitting]]
- [[Robust Neural Architecture Search]]
- [[AutoAttack]]
- [[TRADES]]

## 速查卡片
> [!summary] VDAT
> - 核心问题: 现有 FAT 忽略样本脆弱性差异
> - 核心方法: margin 差异估计 + 概率化样本筛选
> - 关键收益: 同时提升自然/鲁棒精度并降低训练与搜索成本
> - 复杂度: 额外筛选代价约 `O(nk)`，但总体 wall-clock 可下降

