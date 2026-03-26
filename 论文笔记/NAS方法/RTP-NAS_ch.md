---
title: "RTP-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[RTP-NAS]]"
source_paper: "Training-Free Robust Neural Network Search Via Pruning"
source_note: "[[RTP-NAS]]"
authors: [Qiancheng Yang, Yong Luo, Bo Du]
year: 2024
venue: ICME
tags: [nas-method, zh, robust-nas, training-free-nas, pruning]
created: 2026-03-25
updated: 2026-03-25
---

# RTP-NAS 中文条目

## 一句话总结

> RTP-NAS 先用 UAP 构造可迁移的对抗输入空间，再用“对抗 NTK 条件数 + 线性区域数”做无训练剪枝搜索，从而减少鲁棒 NAS 的搜索成本。

## 来源

- 论文: [Training-Free Robust Neural Network Search Via Pruning](https://doi.org/10.1109/ICME57554.2024.10687950)
- HTML: 论文 PDF 未提供
- 代码: 论文中未给出可访问链接（文中仅写“code will be released publicly”）
- 英文方法笔记: [[RTP-NAS]]
- 论文笔记: [[RTP-NAS]]

## 适用场景

- 问题类型: 图像分类下的鲁棒神经架构搜索。
- 前提假设: UAP 能在候选架构之间提供可迁移的对抗评估空间。
- 数据形态: 监督学习（文中为 CIFAR-10/100）。
- 规模约束: 适合“无法对每个候选都做完整对抗训练”的场景。
- 适用原因: 搜索阶段不需要逐个候选做重训练，主要依赖结构性指标筛选。

## 不适用或高风险场景

- 搜索空间与 DARTS 风格差异很大，代理指标相关性未知。
- 需要立刻可运行的官方代码复现。
- 目标鲁棒性超出常见 \(\ell_p\) 约束攻击设定。

## 输入、输出与目标

- 输入: 候选超网、用于生成 UAP 的源模型、训练集。
- 输出: 剪枝后得到的鲁棒架构。
- 优化目标: 在降低搜索成本的同时，提高最终对抗鲁棒精度。
- 核心假设:
  - 对抗空间中的 NTK 条件数越小，结构可训练性越好；
  - 线性区域数越多，模型表达能力越强。

## 方法拆解

### 阶段 1: 构造对抗输入空间

- 使用源模型生成通用扰动 \(v\)，满足 \(\|v\|_p \le \epsilon\)。
- 形成 \(D_A=\{(x_i+v, y_i)\}\)。
- Source: Sec. 3.1, Eq. (6)-(8)

### 阶段 2: 计算结构评分指标

- 定义对抗 NTK:
  \[
  H_A(x+v, x'+v)=J(x+v)J(x'+v)^T
  \]
- 在 \(D_A\) 上计算条件数 \(\kappa_A\)。
- 同时计算线性区域数 \(R_{N,\theta}\)。
- Source: Sec. 2.1, Sec. 2.2, Sec. 3.2, Eq. (9)

### 阶段 3: 排序并剪枝

- 对每个算子 \(o_i\)，计算去掉该算子后的变化量：
  - \(\Delta \kappa_{A,t,o_i}\)
  - \(\Delta R_{t,o_i}\)
- 排序并打分：
  \[
  \text{Score}(o_i)=R_d(\Delta\kappa_{A,t,o_i})+R_a(\Delta R_{t,o_i})
  \]
- 每轮按最小分数剪枝。
- Source: Sec. 3.2, Eq. (10)-(15), Fig. 1

### 阶段 4: 最终训练与评估

- 对搜索出的架构再进行完整对抗训练与评估（FGSM/PGD/AA）。
- Source: Sec. 4.1

## 伪代码

```text
Algorithm: RTP-NAS
Input: 搜索空间 S, 训练集 D_S, 源模型 C, 扰动预算 epsilon
Output: 鲁棒架构 a*

1. 用 C 在 D_S 上生成通用对抗扰动 v，满足 ||v||_p <= epsilon。
   Source: Sec. 3.1, Eq. (6)-(7)
2. 构造对抗输入空间 D_A = {(x_i + v, y_i)}。
   Source: Sec. 3.1, Eq. (8)
3. 用 Kaiming 初始化超网 N_0。
   Source: Sec. 3.2
4. 对 t = 0..T-1:
   4.1 对每个剩余算子 o_i，估计去掉后
       Delta kappa_A,t,o_i 与 Delta R_t,o_i。
       Source: Sec. 3.2, Eq. (10)-(11)
   4.2 计算 score(o_i)=R_d(Delta kappa_A,t,o_i)+R_a(Delta R_t,o_i)。
       Source: Sec. 3.2, Eq. (12)-(14)
   4.3 每条边剪掉最小分数算子，得到 N_{t+1}。
       Source: Sec. 3.2, Eq. (15)
5. 达到单路径结构后停止搜索。
   Source: Sec. 3.2
6. 对最终架构做对抗训练并报告鲁棒精度。
   Source: Sec. 4.1
```

## 训练流程

1. 训练源模型（用于 UAP 生成）。
2. 构造 UAP 对抗输入空间。
3. 在超网上迭代计算指标并剪枝搜索。
4. 对最终架构做完整对抗训练。
5. 用 FGSM/PGD/AA 评估。

Sources:

- Sec. 3.1-3.2, Sec. 4.1

## 推理流程

1. 使用搜索得到并训练完成的模型。
2. 在 clean 与攻击条件下评估精度。

Sources:

- Sec. 4.1, Table 1

## 复杂度与效率

- 时间复杂度: 论文未给封闭表达式。
- 空间复杂度: 论文未给封闭表达式。
- 运行特征: 文中报告搜索约 1 小时完成。
- 扩展性说明: 通过避免“每个候选都对抗训练”，显著降低搜索成本。

## 实现备注

- 搜索空间: DARTS 风格 cell-based。
- 初始化: Kaiming normal。
- 关键剪枝逻辑: 倾向删除“线性区域损失小、对抗条件数下降大”的算子。
- UAP 设计影响显著:
  - 源模型不同，搜索结果会变；
  - 扰动预算增大通常会提高最终鲁棒结果。
- 官方代码: 当前未在论文 PDF 中定位到可访问链接。

## 与相关方法的关系

- 对比 [[RACL]] / [[AdvRush]] / [[RNAS-CL]]:
  - RTP-NAS 在搜索时避免反复对抗训练评估。
- 对比一般 training-free proxy:
  - RTP-NAS 显式引入了对抗输入空间后再评分。
- 主要优势: 成本低且鲁棒精度有竞争力。
- 主要代价: 对 UAP 迁移性的依赖较强。

## 证据与可追溯性

- 关键图: Fig. 1, Fig. 2
- 关键表: Table 1, Table 2, Table 3
- 关键公式: Eq. (6)-(15)
- 关键算法: Sec. 3.2 的排序剪枝流程

## 参考链接

- DOI: https://doi.org/10.1109/ICME57554.2024.10687950
- 本地 PDF: D:/PRO/essays/papers/Training-Free Robust Neural Network Search Via Pruning.pdf
- 代码: Not found
- 本地实现: Not archived
