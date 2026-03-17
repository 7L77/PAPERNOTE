---
title: "Robust Principles_ch"
type: method
language: zh-CN
source_method_note: "[[Robust Principles]]"
source_paper: "Robust Principles: Architectural Design Principles for Adversarially Robust CNNs"
source_note: "[[Robust Principles]]"
authors: [ShengYun Peng, Weilin Xu, Cory Cornelius, Matthew Hull, Kevin Li, Rahul Duggal, Mansi Phute, Jason Martin, Duen Horng Chau]
year: 2023
venue: BMVC
tags: [nas-method, zh, adversarial-robustness, cnn-architecture]
created: 2026-03-17
updated: 2026-03-17
---

# Robust Principles 中文条目

## 一句话总结
> Robust Principles 通过三条可组合的结构原则（WD 比率、卷积 stem、SE+SiLU）系统提升 CNN 在对抗攻击下的鲁棒精度。

## 来源
- 论文: [Robust Principles: Architectural Design Principles for Adversarially Robust CNNs](https://arxiv.org/abs/2308.16258)
- HTML: https://arxiv.org/html/2308.16258
- 代码: https://github.com/poloclub/robust-principles
- 英文方法笔记: [[Robust Principles]]
- 论文笔记: [[Robust Principles]]

## 适用场景
- 问题类型: 图像分类模型的架构级对抗鲁棒增强。
- 前提假设: 可以运行对抗训练与对抗评估（PGD/AA）。
- 数据形态: CIFAR 到 ImageNet 的有监督图像任务。
- 规模与约束: 适合“允许改 backbone 结构”的项目。
- 适用原因: 提供可执行的结构参数修改路径，而非只改训练超参。

## 不适用或高风险场景
- 需要形式化认证鲁棒性保证的场景。
- 训练预算不足以支持对抗训练和多次攻击评估。
- 非 CNN 主体结构且难以映射 stage/stem/block 设计的场景。

## 输入、输出与目标
- 输入: 基线 CNN、攻击预算、训练配方、stage 的宽度/深度配置。
- 输出: 鲁棒化模型 `Ra*`（如 RaResNet、RaWRN）。
- 优化目标: 在可接受参数预算下提高 AA/PGD 鲁棒精度并保持 clean 精度。
- 核心假设: 宏观和微观结构组件可以稳定影响对抗鲁棒性。

## 方法拆解

### 阶段 1: 用 WD 比率做宏观重平衡
- 定义并计算 `WD ratio = (1/(n-1)) * sum_{i=1}^{n-1}(W_i/D_i)`。
- 调整各 stage 的宽深配置使 WD 比率落入 `[7.5, 13.5]`。
- Source: Sec. 4.1, Eq. (2), Fig. 2(a)

### 阶段 2: Stem 结构替换
- 采用卷积 stem + postponed downsampling，减少过激进下采样。
- 在预算允许时将 stem 宽度提升到 96。
- Source: Sec. 4.2, Fig. 2(b)

### 阶段 3: 残差块鲁棒化
- 在 `3x3` 卷积后插入 SE 模块，reduction ratio 取小值（推荐 `r=4`）。
- 将 ReLU 替换为非参数平滑激活（优先 SiLU）。
- Source: Sec. 4.3.1, Sec. 4.3.2, Table 1

### 阶段 4: 跨配方与跨规模验证
- 在 Fast-AT / SAT / TRADES / MART 等训练方案下复现实验。
- 在 CIFAR-10/100 与 ImageNet 上用 PGD + AutoAttack 评估增益稳定性。
- Source: Sec. 5, Table 2, Table 3

## 伪代码
```text
Algorithm: Robust Principles 架构鲁棒化流程
Input: 基线模型 A, 数据集 D, 攻击配置 B, 训练配方 T
Output: 鲁棒化模型 A_ra

1. 计算 A 的 WD 比率:
   WD = (1/(n-1)) * sum_{i=1}^{n-1}(W_i / D_i)
   Source: Eq. (2)
2. 调整各 stage 宽深参数，使 WD 落到 [7.5, 13.5]
   Source: Sec. 4.1, Fig. 2(a)
3. 将 stem 改为卷积 stem + postponed downsampling，并适当增大 stem 宽度
   Source: Sec. 4.2
4. 在残差块加入 SE（r=4），并将 ReLU 改为 SiLU
   Source: Sec. 4.3.1, Sec. 4.3.2
5. 用对抗训练配方 T 训练 A_ra
   Source: Sec. 3, Sec. 5
6. 用 PGD 与 AA 做鲁棒评估，和基线 A 对比
   Source: Sec. 3, Table 1/2/3
7. 若收益不足，回到步骤 2-4 继续调优
   Source: Inference from source
```

## 训练流程
1. 通过 Hydra 读取配置并构建模型。
2. 用 `LinfPGDAttack` 构造内层攻击样本。
3. 执行 FAT 或 SAT 训练循环。
4. 在 clean/PGD/AA 上统一评估。

Sources:
- Paper: Sec. 3, Sec. 5
- Code: `robustarch/main.py`, `robustarch/adv_train.py`, `MODEL.mk`

## 推理流程
1. 加载 checkpoint。
2. 跑自然样本精度与 PGD/AA 对抗精度。
3. 汇报不同预算下的鲁棒指标。

Sources:
- Paper: Sec. 3, Sec. 5
- Code: `test_natural`, `test_pgd`, `benchmark(...)`

## 复杂度与效率
- 时间复杂度主要由对抗训练与对抗评估主导。
- 空间开销相比基线略增（SE 与更宽 stem）。
- 论文中用 Fast-AT 作为大规模探索的效率方案。
- 在多参数规模和多网络族上都观察到稳定提升。

## 实现备注
- 本地代码: `D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs`。
- `MODEL.mk` 直接编码了鲁棒化覆盖参数（WD 配置、stem、SE、SiLU）。
- `robustarch/models/model.py` 负责 stage/block/SE/activation 的可配置组装。
- `robustarch/adv_train.py` 执行 PGD 内层最大化与测试阶段 PGD/AA。

## 与相关方法关系
- 对比 [[RobNet]]: 本文不是 NAS 搜索，而是给出可迁移的手工设计原则。
- 对比仅改训练策略的方法: 本文更强调“架构本身的鲁棒性归因”。
- 主要优势: 规则清晰、可组合、代码可定位。
- 主要代价: 对抗训练成本高，结论仍是经验鲁棒。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2
- 关键表: Table 1, Table 2, Table 3
- 关键公式: Eq. (1), Eq. (2)
- 关键算法: 论文未给单独算法框，流程来自 Sec. 4-5。

## 参考链接
- arXiv: https://arxiv.org/abs/2308.16258
- HTML: https://arxiv.org/html/2308.16258
- 代码: https://github.com/poloclub/robust-principles
- 本地实现: D:/PRO/essays/code_depots/Robust Principles Architectural Design Principles for Adversarially Robust CNNs

