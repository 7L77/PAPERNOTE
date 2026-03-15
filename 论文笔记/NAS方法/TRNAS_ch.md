---
title: "TRNAS_ch"
type: method
language: zh-CN
source_method_note: "[[TRNAS]]"
source_paper: "TRNAS: A Training-Free Robust Neural Architecture Search"
source_note: "[[TRNAS]]"
authors: [Shudong Yang, Xiaoxing Wang, Jiawei Ding, Yanyi Zhang, En Wang]
year: 2025
venue: ICCV
tags: [nas-method, zh, robust-nas, training-free-nas, zero-cost-proxy]
created: 2026-03-15
updated: 2026-03-15
---

# TRNAS 中文条目

## 一句话总结

> TRNAS 用训练前鲁棒代理 `R-Score` 配合多目标进化选择，在不做大规模对抗训练的前提下先筛出高潜力鲁棒架构，再对最优候选做完整对抗训练。

## 来源

- 论文: [TRNAS: A Training-Free Robust Neural Architecture Search](https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html)
- HTML: https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html
- 补充材料: `D:/PRO/essays/papers/Yang_TRNAS_A_Training-Free_ICCV_2025_supplemental.pdf`
- 代码: 截至 2026-03-15 未发现官方仓库
- 英文方法笔记: [[TRNAS]]
- 论文笔记: [[TRNAS]]

## 适用场景

- 问题类型: 对抗鲁棒神经架构搜索。
- 前提假设: 初始化阶段可计算分数与最终鲁棒精度具相关性。
- 数据形态: 图像分类（CIFAR-10/100、Tiny-ImageNet）与 DARTS 搜索空间。
- 资源约束: 无法对大量候选都做完整对抗训练时。
- 为什么适合: 先做训练前粗筛，再把训练预算投入少量高潜力候选。

## 不适用或高风险场景

- 需要直接复现且强依赖官方开源代码。
- 搜索空间与 DARTS 结构差异很大，代理迁移性未知。
- 目标鲁棒威胁模型与 FGSM/PGD/AutoAttack 偏差较大。

## 输入、输出与目标

- 输入: DARTS 候选架构、用于打分的数据批次、资源约束指标（参数量/FLOPs）。
- 输出: 候选排序、Pareto 保留集、最终最优鲁棒架构。
- 目标: 在控制复杂度前提下提升对抗鲁棒精度。
- 核心假设: `R-Score` 高的架构在对抗训练后更可能鲁棒。

## 方法拆解

### 阶段 1: 计算 R-Score

- 对未训练架构计算线性激活能力与特征一致性，并加权合成鲁棒分数。
- Source: Sec. 3.1, Eq. (2)-(7)

### 阶段 2: 多目标选择（MOS）

- 基于聚类的 Pareto 选择保留多样性，抑制早熟。
- Source: Sec. 3.2, Fig. 3

### 阶段 3: 代理引导进化搜索

- 按 `R-Score` 引导父代/子代筛选，迭代更新候选池。
- Source: Sec. 4.1; Supplement Sec. 3.2

### 阶段 4: 对最优候选做完整对抗训练

- 使用 PGD 对抗训练得到最终模型，并在多攻击下测试。
- Source: Sec. 4.2; Supplement Sec. 3.2

## 伪代码

```text
Algorithm: TRNAS
Input: 搜索空间 S, 迭代轮数 T, 种群规模 N
Output: 最优鲁棒架构 a*

1. 从 S 初始化种群 P。
   Source: Sec. 4.1
2. 对每个架构 a 计算:
   R(a) = beta * LAM(a) + (1-beta) * FRM(a)。
   Source: Sec. 3.1, Eq. (2)-(7)
3. 执行基于聚类的多目标 Pareto 选择。
   Source: Sec. 3.2, Fig. 3
4. 生成子代并迭代 T 轮进化更新。
   Source: Sec. 4.1; Supplement Sec. 3.2
5. 选出 top 候选并进行 PGD 对抗训练。
   Source: Sec. 4.2; Supplement Sec. 3.2
6. 在 FGSM/PGD/AutoAttack 下评估并返回最优架构。
   Source: Sec. 4.2; Supplement Sec. 3.2
```

## 训练流程（方法使用视角）

1. 在搜索空间做训练前代理评估和进化筛选。
2. 补充材料提到先做一次“明显劣操作剪枝”再进入完整搜索。
3. 对最终候选执行 7-step PGD 对抗训练。
4. 使用既定学习率策略与 SGD 完成训练。

Sources:

- Sec. 4.1, Sec. 4.2
- Supplement Sec. 2.2, Sec. 3.2

## 推理流程

1. 采用搜索得到的架构与训练好权重。
2. 在 clean 与攻击场景下报告准确率。
3. 与鲁棒 NAS 基线进行同设定对比。

Sources:

- Sec. 4.2
- Supplement Sec. 3.2

## 复杂度与效率

- 闭式复杂度: 论文未显式给出。
- 运行特征: 补充材料报告有效 1000 次评估约 `0.02 GPU-days`，多进程优化后可到 `0.01 GPU-days` 级别。
- 规模说明: 搜索阶段成本低于权重共享鲁棒 NAS，但最终对抗训练仍是主要开销。

## 实现细节备注

- 搜索阶段 8 cells，最终训练 20 cells。
- 进化参数: 20 次更新，父代/子代均 50，聚类参数 `e=20`。
- 攻击参数: FGSM `8/255`；PGD 单步 `2/255`、20/100 步；总预算 `8/255`；另评 AutoAttack。
- 环境: 单卡 RTX 4090，PyTorch 2.0。
- 代码状态: 论文和补充中未发现官方仓库链接。

## 与相关方法对比

- 对比 ZCPRob: 补充材料中 TRNAS 在效率和有效评估率上更强。
- 对比 [[CRoZe]]: TRNAS 的分数区分能力更细，重复分值问题更少（补充 Fig. 1）。
- 对比标准 NAS（[[SWAP-NAS]]、PADA、DARTS）: TRNAS 对鲁棒目标更直接，攻击下表现更好。
- 主要优势: 低开销鲁棒排序 + 稳定搜索。
- 主要代价: 缺少官方代码导致复现风险上升。

## 证据与可溯源性

- 关键图: Fig. 2, Fig. 3（正文）；Fig. 1（补充）。
- 关键表: Table 2/3/4（正文）；Table 1/2/3/4（补充）。
- 关键公式: Eq. (2)-(7)（R-Score）。
- 关键算法流程: Sec. 3.2 + Sec. 4.1 的进化搜索框架。

## 参考链接

- OpenAccess: https://openaccess.thecvf.com/content/ICCV2025/html/Yang_TRNAS_A_Training-Free_Robust_Neural_Architecture_Search_ICCV_2025_paper.html
- 补充 PDF: D:/PRO/essays/papers/Yang_TRNAS_A_Training-Free_ICCV_2025_supplemental.pdf
- 代码: Not found
- 本地实现: Not archived
