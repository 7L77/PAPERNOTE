---
title: "RDNAS_ch"
type: method
language: zh-CN
source_method_note: "[[RDNAS]]"
source_paper: "RDNAS: Robust Dual-Branch Neural Architecture Search"
source_note: "[[RDNAS]]"
authors: [Anonymous Authors]
year: 2025
venue: ICLR 2026 Submission
tags: [nas-method, zh, robust-nas, darts, adversarial-training]
created: 2026-03-26
updated: 2026-03-26
---

# RDNAS 中文条目

## 一句话总结

> RDNAS 在 DARTS 风格鲁棒 NAS 里，把 cell 拆成 normal/robust 两条路径并用 ECA 融合，再用 ROSE（MoM+IQR）稳定 Shapley 打分，从而在小样本搜索下依然找到鲁棒结构。

## 来源

- 论文: [RDNAS: Robust Dual-Branch Neural Architecture Search](https://openreview.net/pdf?id=JWW1hhEJTF)
- HTML: https://openreview.net/forum?id=JWW1hhEJTF
- 代码: PDF 未给出官方仓库；OpenReview supplementary 链接当前环境返回 403。
- 英文方法笔记: [[RDNAS]]
- 论文笔记: [[RDNAS]]

## 适用场景

- 问题类型: 图像分类中的鲁棒 NAS。
- 前提假设: 对抗训练噪声下仍可通过稳健统计恢复操作相对排序。
- 数据形态: 监督学习 + 白盒攻击评估。
- 规模约束: 适合不能对每个候选做完整对抗训练的场景。
- 适用原因: 用小样本搜索 + ROSE 稳定评分降低成本。

## 不适用或高风险场景

- 需要 Transformer/Hybrid 搜索空间（本文仍是 cell-based CNN）。
- 需要完全解耦“架构因素”与“训练配方因素”。
- 需要现成官方代码直接复现。

## 输入、输出与目标

- 输入: 超网搜索空间、分支 logits、训练/验证集、PGD 设置。
- 输出: 离散化后的鲁棒架构（normal/reduce/robust 三类 cell）。
- 优化目标: 在有限搜索预算下兼顾 clean accuracy 与 adversarial robustness。
- 核心假设:
  - 双分支可减少 clean/robust 目标冲突；
  - ROSE 可降低对抗噪声导致的打分方差。

## 方法拆解

### 阶段 1: 双分支 cell 设计

- normal 分支偏向干净精度，robust 分支偏向抗扰动。
- 使用 ECA 做通道加权融合，而非固定平均融合。
- Source: Sec. 3.2, Eq. (6)-(11), Fig. 2

### 阶段 2: 对抗双层优化搜索

- 内层: PGD 训练网络参数。
- 外层: 用 ROSE 加权验证目标更新架构参数。
- Source: Sec. 3.3, Eq. (12)-(14), Algorithm 1

### 阶段 3: ROSE 稳健打分

- 先算 clean/adv 边际增益，再标准化。
- IQR 分数捕获“少见但关键”的操作贡献，MoM 抑制重尾噪声。
- 最终得分:
  \[
  \mathrm{Score}=(1-\beta)m+\beta v
  \]
- Source: Sec. 3.4, Eq. (15)-(19)

## 伪代码

```text
Algorithm: RDNAS Search
Input: S, Nw, Ns, Shapley 样本数 S_num, MoM 分组 G, IQR 灵敏度 gamma, D_train, D_val
Output: A*

1. 初始化三类分支的架构参数 alpha 与网络参数 omega。
   Source: Alg. 1
2. 迭代 epoch = 1..Nw+Ns:
   2.1 用 PGD 对抗训练更新 omega。
       Source: Sec. 3.3, Eq. (12)
   2.2 若 epoch > Nw:
       - 计算 clean/adv 边际增益。
         Source: Eq. (15)
       - 计算 ROSE 得分（标准化 + IQR + MoM）。
         Source: Eq. (16)-(19)
       - 用得分更新并归一化 alpha。
         Source: Alg. 1
3. 每条边取最大 logit 操作并离散化得到 A*。
   Source: Eq. (14)
```

## 训练流程

1. 搜索网络 10 cells，初始通道 32。
2. 搜索时 PGD-7，\(\epsilon=8/255\)，step \(2/255\)。
3. CIFAR-10 小样本搜索：1000 train / 500 val。
4. 最终架构再做 120 epoch 对抗训练。
5. 在 FGSM、PGD20/100、APGD-CE、AA 上评估。

Sources:

- Sec. 4.2, Table 1

## 推理流程

1. 使用离散化并完成鲁棒训练的模型。
2. 在 clean 与多攻击下报告精度。
3. 可直接迁移已搜索结构到其他数据集（不重新搜索）。

Sources:

- Sec. 4.3-4.5

## 复杂度与效率

- 时间复杂度: 论文未给封闭表达式。
- 空间复杂度: 论文未给封闭表达式。
- 运行特征: 搜索成本报告约 0.2 GPU-days。
- 扩展性: 双分支会提高 FLOPs（1.30G），但白盒鲁棒性提升明显。

## 实现备注

- normal/reduce/robust 的操作评分分别统计，避免混合评分掩盖分支差异。
- ECA 在附录注意力模块对比中优于 CBAM/ECAM。
- ROSE 默认启用；去掉后 run-to-run 波动更大。
- 本地代码归档状态:
  - `D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search/README.md`
  - 已记录 supplementary 链接与 403 下载问题。

## 与相关方法的关系

- 对比 [[RACL]] / [[AdvRush]]:
  - 白盒大多数指标更好，AA 略低于最佳基线。
- 对比 [[LRNAS]]:
  - 都是鲁棒 NAS，但 RDNAS 更强调“双分支结构 + 鲁棒 Shapley 打分”。
- 主要优势: 在噪声对抗训练里仍能稳定搜索。
- 主要代价: 评估结果依赖攻击与训练配方，解耦程度有限。

## 证据与可溯源性

- 关键图: Fig. 2, Fig. 4
- 关键表: Table 1, Table 4, Table 5, Table 10
- 关键公式: Eq. (6)-(14), Eq. (15)-(19)
- 关键算法: Algorithm 1

## 参考链接

- OpenReview PDF: https://openreview.net/pdf?id=JWW1hhEJTF
- OpenReview Forum: https://openreview.net/forum?id=JWW1hhEJTF
- Supplementary: https://openreview.net/attachment?id=JWW1hhEJTF&name=supplementary_material
- 本地实现目录: D:/PRO/essays/code_depots/Robust Dual-Branch Neural Architecture Search
