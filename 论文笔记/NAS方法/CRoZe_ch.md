---
title: "CRoZe_ch"
type: method
language: zh-CN
source_method_note: "[[CRoZe]]"
source_paper: "Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations"
source_note: "[[CRoZe]]"
authors: [Hyeonjeong Ha, Minseon Kim, Sung Ju Hwang]
year: 2023
venue: NeurIPS
tags: [nas-method, zh, robust-nas, zero-cost-proxy, training-free]
created: 2026-03-15
updated: 2026-03-15
---

# CRoZe 中文条目

## 一句话总结

> CRoZe 用“clean/perturbed 双分支的一步更新一致性”来做鲁棒 NAS 打分，在几乎不训练架构的前提下筛出更抗多种扰动的网络。

## 来源

- 论文: [Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations](https://arxiv.org/abs/2306.05031)
- HTML: https://arxiv.org/html/2306.05031
- 代码: https://github.com/HyeonjeongHa/CRoZe
- 英文方法笔记: [[CRoZe]]
- 论文笔记: [[CRoZe]]

## 适用场景

- 问题类型: 面向鲁棒性的神经架构搜索与排序。
- 前提假设: 单步 surrogate 指标能较好近似最终鲁棒排序。
- 数据形态: 图像分类（论文中为 CIFAR / ImageNet16-120）。
- 规模与约束: 适合预算紧、无法做 adversarial supernet 训练的场景。
- 适用原因: 只需代理评估，不需对每个候选做完整训练。

## 不适用或高风险场景

- 需要“可证明鲁棒性”而非经验鲁棒性排名。
- 扰动类型与论文设定相差过大。
- 任务中单步梯度信息与最终收敛行为相关性较弱。

## 输入、输出与目标

- 输入: 架构 `A`、批数据 `(x, y)`、扰动输入 `x'`、clean 网络 `f_theta`、robust 网络 `f_theta^r`。
- 输出: 标量分数 `CRoZe(A)`。
- 优化目标: 让 proxy 排名尽量贴近最终 clean+robust 性能排名。
- 核心假设: 好架构在 clean 与 perturbed 任务间会体现更高的特征/参数/梯度对齐。

## 方法拆解

### 阶段 1: 构建 robust surrogate

- 从随机初始化的 `f_theta` 出发。
- 通过层级参数扰动得到 `f_theta^r`（Eq. 3）。
- 在 `f_theta^r` 上用 FGSM 生成 `x'`（Eq. 4）。
- Source: Sec. 3.2 / Eq. (3)(4)

### 阶段 2: 特征一致性

- 计算 clean 与 perturbed 分支的层级特征相似度 `Z_m`。
- Source: Sec. 3.3 / Eq. (5)

### 阶段 3: 参数与梯度一致性

- 先得梯度 `g, g^r`（Eq. 6），再做一步更新得 `theta_1, theta_1^r`（Eq. 7）。
- 计算 `P_m`（参数一致性, Eq. 8）和 `G_m`（梯度一致性, Eq. 9）。
- Source: Sec. 3.3 / Eq. (6)(7)(8)(9)

### 阶段 4: 代理聚合

- `CRoZe = sum_m Z_m * P_m * G_m`。
- Source: Eq. (10)

## 伪代码

```text
Algorithm: CRoZe
Input: 架构 A, 批数据 (x, y), 扰动预算 epsilon
Output: 代理分数 s

1. 初始化 clean surrogate f_theta。
   Source: Sec. 3.2
2. 通过层级参数扰动构造 robust surrogate f_theta^r。
   Source: Eq. (3)
3. 基于 f_theta^r 生成 FGSM 扰动输入 x'。
   Source: Eq. (4)
4. clean/robust 双分支前向，提取层特征。
   Source: Eq. (5)
5. 计算 g, g^r 与一步更新参数 theta_1, theta_1^r。
   Source: Eq. (6)(7)
6. 对每层计算 Z_m, P_m, G_m 并累加 s += Z_m * P_m * G_m。
   Source: Eq. (5)(8)(9)(10)
7. 返回 s 作为架构鲁棒性代理分数。
   Source: Eq. (10)
```

## 训练流程

1. 在搜索空间中采样候选架构（random/mutate/warmup+move）。
2. 对每个候选计算 CRoZe 分数。
3. 选出高分架构。
4. 对选出架构做标准训练或对抗训练并汇报最终指标。

Sources:

- Sec. 4.2/4.3
- `main.py`, `sampling.py`

## 推理流程

1. 使用 CRoZe 选出的架构并加载训练权重。
2. 在 clean 和多攻击/腐化集上评估。

Sources:

- Sec. 4
- Source: Inference from source

## 复杂度与效率

- 时间复杂度: 论文未给闭式；主要受候选采样数量影响。
- 空间复杂度: 双 surrogate + 特征/梯度缓存。
- 运行特征:
  - DARTS/CIFAR-10 搜索约 17,066 GPU sec。
  - 相比 robust one-shot NAS（25万+ GPU sec）明显更省。

## 实现备注

- 本地代码: `D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations`
- 核心文件:
  - `zero_cost_methods/pruners/measures/croze.py`
  - `zero_cost_methods/pruners/p_utils.py`
  - `main.py`
  - `sampling.py`
- `adj_weights` 对应 robust surrogate 的权重扰动；`fgsm_attack` 对应输入扰动。

## 与相关方法关系

- 对比 SynFlow/GradNorm: CRoZe 显式建模 clean/perturbed 对齐，而不是只看 clean 训练信号。
- 对比 RobNet/AdvRush: 不做 adversarial supernet 训练，搜索成本更低。
- 主要优势: 鲁棒性与搜索开销的折中更好。
- 主要代价: 仍依赖单步近似质量。

## 证据与可溯源

- 关键图: Fig. 1~6
- 关键表: Table 1~6
- 关键公式: Eq. (2)~(10)

## 参考链接

- arXiv: https://arxiv.org/abs/2306.05031
- HTML: https://arxiv.org/html/2306.05031
- 代码: https://github.com/HyeonjeongHa/CRoZe
- 本地实现: D:/PRO/essays/code_depots/Generalizable Lightweight Proxy for Robust NAS against Diverse Perturbations
