---
title: "Robust-ZCP_ch"
type: method
language: zh-CN
source_method_note: "[[Robust-ZCP]]"
source_paper: "ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION"
source_note: "[[Robust-ZCP]]"
authors: [Yuqi Feng, Yuwei Ou, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICLR
tags: [nas-method, zh, robustness, zero-cost-proxy]
created: 2026-03-15
updated: 2026-03-15
---

# Robust-ZCP 中文条目

## 一句话总结
> Robust-ZCP 在网络初始化时直接计算鲁棒代理分数，用 NTK 相关项与输入损失地形项联合排序候选架构，从而大幅降低 robust NAS 搜索成本。

## 来源
- 论文: [ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION](https://openreview.net/forum?id=zHf7hOfeer)
- HTML: https://openreview.net/forum?id=zHf7hOfeer
- 代码: https://github.com/fyqsama/Robust_ZCP
- 英文方法笔记: [[Robust-ZCP]]
- 论文笔记: [[Robust-ZCP]]

## 适用场景
- 问题类型: 在大规模候选架构中快速预估对抗鲁棒性。
- 前提假设: 初始化阶段统计量与最终鲁棒精度有可用相关性。
- 数据形态: 图像分类监督学习（CIFAR/ImageNet 风格）。
- 规模与约束: 候选架构多、完整对抗训练成本高。
- 适用原因: 代理阶段不需要生成对抗样本，也不需要完整训练。

## 不适用或高风险场景
- 需要可认证鲁棒性保证，而非经验排序。
- 任务分布与论文实验搜索空间差异很大且无校准。
- 架构性能高度依赖训练动力学，初始化信号不足以区分。

## 输入、输出与目标
- 输入: 候选架构、小批量样本、初始化权重。
- 输出: 标量鲁棒代理分数 `R`。
- 优化目标: 以极低成本筛出潜在高鲁棒架构。
- 核心假设: 初始化点上的 NTK 与输入地形近似可反映鲁棒排序。

## 方法拆解

### 阶段 1：NTK 近似项
- 计算层/样本上的梯度内积平均量，近似 NTK 最小特征值相关部分。
- Source: Sec. 3.2-3.3, Eq. (4), Eq. (8)

### 阶段 2：输入地形近似项
- 通过有限差分近似输入 Hessian 最大特征值相关项：
  `|| (l(x + h z*) - l(x)) / h ||^2`。
- Source: Sec. 3.2-3.3, Eq. (4), Eq. (7)

### 阶段 3：组合打分与排序
- 用指数缩放与负号组合两项得到最终 `R`。
- 按 `R` 排序并选择高分架构。
- Source: Eq. (4), Sec. 4.1.2

### 阶段 4：对入选架构做完整评估
- 仅对筛出的架构执行对抗训练与攻击评估。
- Source: Sec. 4.1, Table 1-4

## 伪代码
```text
Algorithm: Robust-ZCP
Input: 候选架构 A，样本集合 X，初始化权重 θ0，超参数 M,N,h,t
Output: 按鲁棒代理分数排序后的架构

1. 对每个候选架构 a，随机初始化 θ0。
   Source: Sec. 3.2
2. 计算 NTK 近似项：
   S_ntk = (1 / (M N^2)) * Σ_m Σ_i Σ_j <∂fθ0(x_i)/∂θ0^m, ∂fθ0(x_j)/∂θ0^m>.
   Source: Eq. (8)
3. 计算地形近似项：
   S_land = || (l(x + h z*) - l(x)) / h ||_2^2，其中 l(x)=∇xL(θ0,x)。
   Source: Eq. (7)
4. 计算最终分数：
   R = -exp(t * S_ntk) * S_land。
   Source: Eq. (4)
5. 按 R 排序，选 Top-K 架构进入完整对抗训练与评估。
   Source: Sec. 4.1.2
6. （代码细节）可加入结构过滤规则（如 skip-connect 数量约束）。
   Source: Inference from source (`search_robust.py`)
```

## 训练流程
1. 从搜索空间采样候选架构（文中示例为 DARTS 空间随机 1000 个）。
2. 用 Robust-ZCP 计算每个候选的代理分数。
3. 选取高分架构。
4. 对选中架构做对抗训练并报告 FGSM/PGD/APGD/AA 指标。

Sources:
- Sec. 4.1.1-4.1.2
- `exps/Robust_ZCP/search_robust.py`

## 推理流程
1. 对新候选架构做初始化。
2. 计算 `R`（NTK 近似项 + 地形近似项）。
3. 用于排序与剪枝，减少后续训练预算。

Sources:
- Sec. 3.2-3.4
- Eq. (4), Eq. (7), Eq. (8)

## 复杂度与效率
- 时间复杂度: `O(MN^2)`（论文给出）。
- 空间复杂度: 论文未明确给解析式。
- 运行特征: 代理阶段无需生成对抗样本。
- 扩展性: 在更大搜索空间下搜索成本仍然很低（0.017 -> 0.019 GPU days）。

## 实现备注
- 核心实现:
  - `functions.py::procedure` 中 `RF = -exp(conv * 5000000) * regularizer_average`。
  - `regularizer.py::loss_cure.regularizer` 实现地形项近似。
- 关键超参数:
  - 论文相关性实验: `M=11`, `N=25`, `h=50`, `t=5×10^6`, batch size 8。
  - 搜索脚本默认: `batch_size_1=1`, `batch_size_2=32`。
- 实践注意:
  - 代码包含 skip-connect 数量筛选条件。
  - 部分数据路径是硬编码，复现前需改成本地路径。
- 风险点:
  - 初始化信号可能误判“难训练但初始分数高”的架构。

## 与相关方法关系
- 对比 CRoZe: Robust-ZCP 代理阶段不显式生成对抗样本。
- 对比传统 robust NAS（RACL/DSRNA 等）: 搜索阶段显著省算力，训练预算集中在少量候选上。
- 主要优势: 搜索成本低且鲁棒精度有竞争力。
- 主要代价: 对近似假设依赖更强。

## 证据与可溯源性
- 关键图: Fig. 1-4
- 关键表: Table 1-6
- 关键公式: Eq. (4), Eq. (7), Eq. (8)
- 关键算法: 基于 proxy 的排序搜索流程（Sec. 4.1.2）

## 参考链接
- arXiv/OpenReview: https://openreview.net/forum?id=zHf7hOfeer
- HTML: https://openreview.net/forum?id=zHf7hOfeer
- 代码: https://github.com/fyqsama/Robust_ZCP
- 本地实现: D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION
