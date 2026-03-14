---
title: "ROME_ch"
type: method
language: zh-CN
source_method_note: "[[ROME]]"
source_paper: "ROME: Robustifying Memory-Efficient NAS via Topology Disentanglement and Gradient Accumulation"
source_note: "[[ROME]]"
authors: [Xiaoxing Wang, Xiangxiang Chu, Yuda Fan, Zhexi Zhang, Bo Zhang, Xiaokang Yang, Junchi Yan]
year: 2023
venue: ICCV
tags: [nas-method, zh, differentiable-nas, single-path-nas, robustness]
created: 2026-03-14
updated: 2026-03-14
---

# ROME 中文条目

## 一句话总结
> ROME 的核心是把“拓扑选边”和“算子选择”拆开，并用两段 `K` 次采样的梯度累积来稳定双层优化，从而缓解单路径 DARTS 的 skip-collapse。

## 来源
- 论文: [ROME: Robustifying Memory-Efficient NAS via Topology Disentanglement and Gradient Accumulation](https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html)
- HTML: https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html
- 代码: 论文/CVF/arXiv 未提供可确认的官方仓库链接
- 英文方法笔记: [[ROME]]
- 论文笔记: [[ROME]]

## 适用场景
- 问题类型: cell-based 可微 NAS 中出现 parameter-free 操作（尤其 skip）聚集导致的 collapse。
- 前提假设: 目标结构满足每个中间节点入度为 2（DARTS 风格）。
- 数据形态: 需要 train/val 切分进行双层优化。
- 规模与约束: 显存受限，不适合 full-path DARTS 的场景。
- 适用原因: 单路径采样 + 拓扑一致性约束可同时改善稳定性与显存占用。

## 不适用或高风险场景
- 搜索空间不是 DAG/cell 结构，无法表达“每节点入度约束”。
- 项目不接受每轮多次子网采样带来的实现复杂度。
- 需要极简的一阶段搜索流程（无需双层优化）。

## 输入、输出与目标
- 输入: 超网权重 `omega`、算子架构参数 `alpha`、拓扑参数 `beta`、采样数 `K`、搜索空间定义。
- 输出: 离散架构 `z* = argmax_z p(z; alpha, beta)`。
- 优化目标: 在采样架构分布下最小化验证集期望损失，同时训练集更新超网权重。
- 核心假设: collapse 主要来自拓扑不一致与采样方差过大。

## 方法拆解

### 阶段 1: 拓扑-算子解耦
- 用 `B_{i,j}` 表示边是否被选，用 `A^o_{i,j}` 表示边上算子是否被选。
- 强制每个中间节点只保留两条入边。
- Source: Sec. 3.3, Eq. (1-3)

### 阶段 2: 可微拓扑采样
- ROME-v1: 在节点前驱边组合空间中采样。
- ROME-v2: 直接做 Gumbel-Top2 选边。
- Source: Sec. 3.4.1-3.4.2, Eq. (4-8), Sec. 3.5

### 阶段 3: 双重梯度累积
- 对架构参数 (`alpha`,`beta`)：在验证集上对 K 个子网梯度求均值。
- 对超网权重 (`omega`)：在训练集上对 K 个子网梯度累积更新。
- Source: Sec. 3.6, Eq. (9-12), Alg. 1

## 伪代码
```text
Algorithm: ROME (默认 v2)
Input: omega, alpha, beta, sampling count K, iterations T
Output: z*

1. 对每个迭代 t，采样两批数据 Ds(验证) 与 Dt(训练)。
   Source: Alg. 1 line 2
2. 重复 k=1..K：按 Eq. (7-8) 采样拓扑边、按 Eq. (3) 采样边上算子，得到 z_k。
   Source: Sec. 3.4.2, Eq. (7-8), Eq. (3), Alg. 1 line 3-6
3. 用 K 个 z_k 的验证损失梯度均值更新 alpha 与 beta。
   Source: Eq. (11), Alg. 1 line 7
4. 再重复 k=1..K：重新采样 z'_k。
   Source: Alg. 1 line 8-11
5. 用 K 个 z'_k 的训练损失梯度累积更新 omega。
   Source: Eq. (12), Alg. 1 line 12
6. 搜索结束后按 p(z; alpha, beta) 解码 z*。
   Source: Eq. (9), Alg. 1 line 14
```

## 训练流程
1. 构建 8-cell 搜索超网（初始通道 16）。
2. 默认 `K=7`，CIFAR-10 搜索 50 epochs。
3. 按“先更新架构参数，再更新超网权重”的双层循环执行。
4. 解码离散结构并按标准 protocol 重新训练评估。

Sources:
- Sec. 4.1
- Algorithm 1

## 推理流程
1. 使用搜索后离散架构 `z*`，而非超网。
2. 在目标数据集上按论文设定训练并评估最终模型。
3. ImageNet 可用“CIFAR 转移”或“直接搜索”两条路径。

Sources:
- Sec. 4.3
- Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给封闭表达式，单轮成本与 `K` 近似线性相关。
- 空间复杂度: 在报告设置中低于 GDAS 与 PC-DARTS。
- 运行特征: CIFAR 搜索约 0.3 GPU-days，直接 ImageNet 搜索可在低预算下进行。
- 扩展性说明: `K` 增大带来更稳结果，但收益会趋于饱和（Table 5）。

## 实现备注
- ROME-v2 是论文默认版本，兼顾效率与稳健性。
- 两段采样使用不同数据批（对应 val/train）。
- 关键超参: SGD(lr=0.05, momentum=0.9) 更新 `omega`，Adam(lr=3e-4) 更新架构参数，`K=7`。
- 代码状态: 论文称将公开代码，但当前可见页面未给出官方仓库 URL。

## 与相关方法关系
- 对比 [[GDAS]]: 增加拓扑一致性与双重梯度累积，显著缓解 collapse。
- 对比 [[DARTS]]: 单路径机制降低显存，且更稳定。
- 主要优势: 在多搜索空间、多数据集下鲁棒提升。
- 主要代价: 训练循环与实现逻辑更复杂。

## 证据与可溯源性
- 关键图: Fig. 1-5
- 关键表: Table 1-7
- 关键公式: Eq. (1-3), Eq. (7-8), Eq. (9-12)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: 论文页面未明确给出
- HTML: https://openaccess.thecvf.com/content/ICCV2023/html/Wang_ROME_Robustifying_Memory-Efficient_NAS_via_Topology_Disentanglement_and_Gradient_Accumulation_ICCV_2023_paper.html
- 代码: 未检索到官方链接
- 本地实现: Not archived

