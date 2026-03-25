---
title: "NARes_ch"
type: method
language: zh-CN
source_method_note: "[[NARes]]"
source_paper: "A Neural Architecture Dataset for Adversarial Robustness"
source_note: "[[NARes]]"
authors: [Bowen Zheng, Ran Cheng, Shihua Huang, Zhichao Lu, Vishnu Boddeti]
year: 2025
venue: ICLR 2025 (OpenReview submission)
tags: [nas-method, zh, robustness-dataset, adversarial-robustness, macro-search-space, wrn]
created: 2026-03-23
updated: 2026-03-23
---

# NARes 中文条目

## 一句话总结
> NARes 通过统一对抗训练协议穷举 WRN 宏观空间，把“训练很贵的鲁棒 NAS”变成“可查询的数据集问题”。

## 来源
- 论文: [A Neural Architecture Dataset for Adversarial Robustness](https://openreview.net/forum?id=AZVvTBxTdZ)
- PDF: https://openreview.net/pdf/adb9acc706c4b858a6448cb218e58621b71dd419.pdf
- 补充材料: https://openreview.net/attachment?id=AZVvTBxTdZ&name=supplementary_material
- 代码: 当前 OpenReview/PDF 版本未提供公开仓库链接（检查日期 2026-03-23）
- 英文方法笔记: [[NARes]]
- 论文笔记: [[NARes]]

## 适用场景
- 问题类型: 鲁棒 NAS 基准评测、架构规律验证、代理指标分析。
- 前提假设: 允许离线表格化查询；研究目标与 WRN 宏观深宽设计相关。
- 数据形态: CIFAR-10 下的对抗训练与评测结果。
- 规模与约束: 适合“无法反复全量对抗训练”的场景。
- 适用原因: 先一次性付出高算力构建成本，后续反复实验几乎零训练成本。

## 不适用或高风险场景
- 你需要在新搜索空间做在线训练搜索。
- 你关心的不是 WRN 家族，而是 Transformer/NAS cell 等异构结构。
- 你需要跨数据集（非 CIFAR-10）直接结论外推。

## 输入、输出与目标
- 输入: 架构向量 `[D1, W1, D2, W2, D3, W3]`、CIFAR-10 数据、AT 超参数、攻击配置。
- 输出: 每 epoch 日志、每架构多 checkpoint、完整鲁棒指标（clean/FGSM/PGD20/PGD-CW40/AA-Compact/腐蚀/Stable/LIP）。
- 目标: 构建可复用的鲁棒架构地形图，支持 NAS 算法与理论验证。
- 核心假设: 一致训练协议下的大规模密集采样能更可靠揭示架构-鲁棒关系。

## 方法拆解

### 阶段 1: 定义 WRN 宏观搜索空间
- 使用 pre-activation WRN 三阶段结构。
- 决策变量为 6 维向量 `[D1, W1, D2, W2, D3, W3]`。
- 总空间 `5^6 = 15,625`。
- Source: Sec. 3.1, Fig. 1

### 阶段 2: 对全部架构统一对抗训练
- 使用 PGD 对抗训练，100 epochs。
- 学习率在 75/90 epoch 衰减。
- 以验证集 PGD-CW40 做 early stopping 缓解 robust overfitting。
- 保留 4 个 checkpoint（74/89/99/best）。
- Source: Sec. 3.1, Table 1

### 阶段 3: 训练期记录诊断指标
- 记录每 epoch 的训练与验证鲁棒指标。
- 额外记录稳定准确率与经验 Lipschitz 常数。
- Source: Sec. 3.2, Eq. (1), Table 1

### 阶段 4: 最终鲁棒评测
- 在测试集上评测 FGSM、PGD20、PGD-CW40、AA-Compact。
- 同时评测 CIFAR-10-C 的 common corruptions。
- Source: Sec. 3.2, Sec. 4, Table 1

### 阶段 5: 作为 NAS 基准复用
- 以最多 500 次查询运行 Random/Local Search/RE/BANANAS。
- 统计最优架构指标并做多次重复平均。
- Source: Sec. 5, Table 2

## 伪代码
```text
Algorithm: NARes 构建与基准复用
Input:
  深度集合 D={4,5,7,9,11}
  宽度集合 W={8,10,12,14,16}
  训练集 CIFAR-10, 验证集 CIFAR-10.1, 攻击集合 A
Output:
  可查询鲁棒数据集 R, 可选 NAS 基准结果 B

1. 枚举 D^3 x W^3 上所有架构向量 v 并实例化 WRN(v)。
   Source: Sec. 3.1, Fig. 1
2. 对每个架构 a 用统一 PGD 对抗训练训练 100 epochs。
   Source: Sec. 3.1
3. 每个 epoch 在验证集评测 clean/PGD20/PGD-CW40，并计算 Stable/LIP。
   Source: Sec. 3.2, Eq. (1), Table 1
4. 以验证 PGD-CW40 选 best epoch，保存 {74,89,99,best} checkpoint。
   Source: Sec. 3.1, Table 1
5. 对 best checkpoint 做测试攻击与腐蚀评测并写入 R。
   Source: Sec. 3.2, Sec. 4, Table 1
6. (可选) 在 R 上运行 NAS 算法，查询预算 <= 500，统计 400 次重复结果。
   Source: Sec. 5, Table 2
```

## 训练流程
1. 枚举 WRN 宏观空间。
2. 统一 PGD 对抗训练。
3. 每 epoch 记录验证鲁棒指标。
4. 基于 PGD-CW40 early stop，并存储多时刻 checkpoint。
5. 聚合测试与腐蚀指标形成最终条目。

Sources:
- Sec. 3.1, Sec. 3.2, Table 1

## 推理/使用流程
1. 根据架构向量查询 NARes。
2. 读取目标指标（鲁棒精度、Stable、LIP、Corruption）。
3. 用于排序、相关性分析或黑盒 NAS 模拟。

Sources:
- Sec. 4, Sec. 5, Table 2

## 复杂度与效率
- 构建成本:
  - 训练约 13.1K GPU days（约 36 GPU years）
  - 评测约 2.9K GPU days（约 8 GPU years）
  - 合计约 44 GPU years
- 搜索空间大小: 15,625
- 论文 NAS 实验查询预算: 500（3.2% 空间）

## 实现备注
- 攻击常用 `epsilon=8/255`，PGD20 步长 `0.8/255`。
- 使用 CIFAR-10.1 做验证与模型选择。
- Stable Accuracy 与经验 LIP 是关键诊断量，不只是附加指标。
- 多 checkpoint 设计支持后续微调与轨迹分析。
- 论文文本写明“将开源训练与评测代码”，但当前公开版本未给出可访问仓库链接。

## 与相关方法关系
- 对比 [[NADR-Dataset]]: NARes 更强调 WRN 宏观空间与高容量模型。
- 对比 [[NAS-Bench-201]] 系鲁棒数据: 从 cell 级拓扑转向 stage 级深宽设计。
- 对比 [[RobustBench]]: NARes 更像“空间内穷举地形图”，而非榜单式模型集合。
- 主要优势: 高分辨率、可复用、可统计验证。
- 主要代价: 受限于 CIFAR-10 与 WRN 空间，且为单次全量 sweep。

## 证据与可溯源性
- 关键图: Fig. 1-7
- 关键表: Table 1-2
- 关键公式: Eq. (1)
- 关键算法: 主文未给独立算法名，流程由 Sec. 3 + Table 1 可追溯重建

## 参考链接
- OpenReview: https://openreview.net/forum?id=AZVvTBxTdZ
- PDF: https://openreview.net/pdf/adb9acc706c4b858a6448cb218e58621b71dd419.pdf
- Supplementary: https://openreview.net/attachment?id=AZVvTBxTdZ&name=supplementary_material
- 代码: Not publicly linked
- 本地实现: Not archived

