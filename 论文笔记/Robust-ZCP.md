---
title: "ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION"
method_name: "Robust-ZCP"
authors: [Yuqi Feng, Yuwei Ou, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICLR
tags: [NAS, adversarial-robustness, zero-cost-proxy, NTK]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=zHf7hOfeer
local_pdf: D:/PRO/essays/papers/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION.pdf
local_code: D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION
created: 2026-03-15
---

# 论文笔记：Robust-ZCP

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION |
| 会议 | ICLR 2025 |
| OpenReview | https://openreview.net/forum?id=zHf7hOfeer |
| 代码 | https://github.com/fyqsama/Robust_ZCP |
| 本地 PDF | `D:/PRO/essays/papers/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION` |

## 一句话总结
> 本文提出一个用于 [[Adversarial Robustness]] 评估的 [[Zero-Cost Proxy]]，在不训练网络也不生成对抗样本的前提下，能高效筛选 [[Robust Neural Architecture Search]] 候选结构。

## 核心贡献
1. 给出一个面向鲁棒性的 zero-cost 评分函数 `R`，由初始化权重上的 NTK 项与输入损失地形项组成（Sec. 3.2）。
2. 从 [[Neural Tangent Kernel]] 与 [[Input Loss Landscape]] 两条理论线索解释 proxy 与鲁棒性之间的关系（Sec. 3.3-3.5, Appx A）。
3. 在 DARTS/WRN 搜索空间与 CIFAR-10/ImageNet 等设置上展示显著速度优势，同时保持较强鲁棒精度（Sec. 4.1）。
4. 构建 Tiny-RobustBench 数据集，用于评估 zero-cost proxy 与真实鲁棒精度的相关性（Sec. 4.2.1, Appx C.1）。

## 问题背景
### 要解决的问题
- 现有 robust NAS 为了评估每个架构的鲁棒性，通常需要完整训练甚至对抗训练，成本极高。
- 已有鲁棒 zero-cost proxy（如 CRoZe）仍需要生成对抗样本，速度和理论可解释性都有限。

### 现有方法局限
- 训练式评估慢，难扩展到大量候选架构。
- 需要对抗样本生成的代理在搜索环节仍然昂贵。
- 理论解释不足，难判断 proxy 何时可信。

### 本文动机
- 如果可以只在初始化点用一次性统计量近似鲁棒性，就能在搜索阶段显著降本。

## 方法详解
### 总体评分函数（Eq. 4）
论文将代理分数写为：

$$
R = - \exp\left(\frac{t}{MN^2}\sum_{m=1}^{M}\sum_{i=1}^{N}\sum_{j=1}^{N}
\left(\frac{\partial f_{\theta_0}(x_i)}{\partial \theta_0^m}\right)
\left(\frac{\partial f_{\theta_0}(x_j)}{\partial \theta_0^m}\right)^T
\right)
\cdot
\left\|
\frac{l(x + h z^*) - l(x)}{h}
\right\|_2^2
$$

其中：
- 第一项近似 NTK 最小特征值相关项（Eq. 8）。
- 第二项近似输入 Hessian 最大特征值相关项（Eq. 7）。
- $l(x)=\nabla_x L(\theta_0, x)$，$z^*=\frac{\mathrm{sign}(\nabla_x L(\theta_0,x))}{\|\mathrm{sign}(\nabla_x L(\theta_0,x))\|_2}$。

### 理论思路
1. 从训练误差上界（NTK 理论）出发：损失与 $\lambda_{\min}(\Theta)$ 相关（Eq. 1-3）。
2. 将输入替换为对抗样本，得到对抗损失上界（Eq. 5-6）。
3. 用可零成本近似替代“对抗样本相关项”：
   - 用 $\lambda_{\min}(\Theta_{\theta_0})$ 近似对抗 NTK 项（Eq. 8）。
   - 用输入 Hessian 最大特征值近似局部对抗损失项，并用有限差分近似（Eq. 7）。
4. 组合得到 Eq. 4，避免显式对抗样本生成。

### 复杂度
- 论文给出总体复杂度：$O(MN^2)$（Sec. 3.4）。

## 关键实验结果
### White-box（Table 1, CIFAR-10）
- Ours: Natural 85.60%, FGSM 60.20%, PGD20 52.75%, PGD100 52.51%, APGDCE 52.25%, AA 49.97%。
- 搜索成本 0.017 GPU days，显著低于多数 robust NAS 方法（文中称至少约 20x 提速）。

### Black-box transfer（Table 2）
- 作为 source model 时，Ours 对其他模型产生更强迁移攻击；配对比较显示其目标模型鲁棒性仍有竞争力。

### 跨数据集迁移（Table 3）
- 在 SVHN 上优于 ResNet-18/PDARTS。
- 在 Tiny-ImageNet-200 上自然精度与 FGSM 指标提升明显，PGD20 相对 PDARTS 略弱。

### ImageNet（Table 4）
- Ours: Natural 52.71%, FGSM 19.88%, PGD20 11.96%，优于文中对比的 RACL/AdvRush/CRoZe。

### 相关性评估（Fig. 2-4）
- NAS-Bench-201-R 上：弱攻击时相关性较好，强攻击时相关性退化（作者归因于该数据未对抗训练，精度接近零）。
- Tiny-RobustBench 上：在对比代理中取得最高 Kendall's Tau（图中 Ours 约 0.33）。

## 与代码实现的对照
- 核心搜索脚本：`exps/Robust_ZCP/search_robust.py`
  - 随机采样种子区间 `3000..3999`。
  - 使用 `procedure(...)` 计算鲁棒 proxy 分数并选最大者。
- 核心评分实现：`exps/Robust_ZCP/functions.py`
  - 代码中分数形式为 `RF = -exp(conv * 5000000) * regularizer_average`，对应论文中的指数项乘曲率项。
- 输入曲率近似：`exps/Robust_ZCP/regularizer.py`
  - 通过 `loss_cure.regularizer` 用有限差分梯度差实现地形项近似。
- 实践细节与潜在坑：
  - `search_robust.py` 默认有 `count_normal_skip(genotype) == 1` 的筛选条件。
  - CIFAR 数据目录在脚本内出现硬编码路径（`/home/yuqi/data`），复现实验时需改。

## 批判性思考
### 优点
1. 把“鲁棒性 zero-cost 评估”做成了清晰的两项分解，并给出理论动机。
2. 在搜索成本上优势明显，且在多个攻击设置下精度有竞争力。
3. 提供 Tiny-RobustBench，补上强攻击下 proxy 评估数据缺口。

### 局限
1. 理论推导依赖近似条件（如 NTK 相关假设）；在有限宽网络上的精确性有限。
2. 代理只看初始化点，论文也承认对 skip connection 等结构因素可能有误判。
3. 结论主要基于特定搜索空间与训练设定，跨任务泛化仍需更多验证。

## 关联概念
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Neural Tangent Kernel]]
- [[Input Loss Landscape]]
- [[NAS-Bench-201]]
- [[Kendall's Tau]]

