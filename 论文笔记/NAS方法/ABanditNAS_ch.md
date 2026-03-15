---
title: "ABanditNAS_ch"
type: method
language: zh-CN
source_method_note: "[[ABanditNAS]]"
source_paper: "Anti-Bandit Neural Architecture Search for Model Defense"
source_note: "[[ABanditNAS]]"
authors: [Hanlin Chen, Baochang Zhang, Song Xue, Xuan Gong, Hong Liu, Rongrong Ji, David Doermann]
year: 2020
venue: arXiv
tags: [nas-method, zh, robust-nas, adversarial-defense, bandit]
created: 2026-03-15
updated: 2026-03-15
---

# ABanditNAS 中文条目

## 一句话总结
> ABanditNAS 在鲁棒 NAS 中把“采样”和“淘汰”解耦：先用 LCB 公平探索，再用 UCB 淘汰低潜力操作，从而在超大操作空间里保持可接受的搜索效率。

## 来源
- 论文: [Anti-Bandit Neural Architecture Search for Model Defense](https://arxiv.org/abs/2008.00698)
- HTML: https://arxiv.org/html/2008.00698v2
- 代码: https://github.com/RunwenHu/ABanditNAS
- 英文方法笔记: [[ABanditNAS]]
- 论文笔记: [[ABanditNAS]]

## 适用场景
- 问题类型: 面向对抗鲁棒性的神经架构搜索（分类任务）。
- 前提假设: 短周期对抗训练后的验证精度可用于评估操作潜力。
- 数据形态: 监督学习图像数据（文中是 MNIST/CIFAR-10）。
- 规模与约束: 搜索空间很大，无法对每个候选做完整训练。
- 适用原因: anti-bandit 机制专门处理“大臂数 + 高成本”搜索场景。

## 不适用或高风险场景
- 需要理论最优解保证，而非启发式剪枝。
- 无法承受搜索期的对抗训练迭代开销。
- 任务域与图像分类差异很大，短周期精度信号不可靠。

## 输入、输出与目标
- 输入: 训练/验证数据、每条边的候选操作集、`eps`、`K/T/lambda` 等超参数。
- 输出: 每条边仅剩一个操作的最终 cell 结构。
- 优化目标: 在较低搜索成本下提升模型的对抗鲁棒性。
- 核心假设: 经过公平试验后长期表现差的操作可安全淘汰。

## 方法拆解

### 阶段 1: 构建防御导向搜索空间
- 每个 cell 是 DAG，`M=4` 个中间节点，边上 `K=9` 个候选操作。
- 除常规操作外，显式引入 Gabor 与 denoising 操作。
- Source: Sec. 3.1, Fig. 2

### 阶段 2: 基于 LCB 的采样
- 用置信下界得到 `sL`（Eq. 3）。
- 通过 `softmax(-sL)` 计算每个操作采样概率（Eq. 4）。
- Source: Sec. 3.3-3.4, Eq. (2)-(4)

### 阶段 3: 一轮对抗训练与性能更新
- 每条边采样一个操作，进行一轮对抗训练，得到验证精度 `a`。
- 用历史加权更新 `m`（Eq. 5）。
- Source: Algorithm 1 lines 8-17, Eq. (5)

### 阶段 4: 基于 UCB 的淘汰
- 每 `K*T` 次采样计算 `sU`（Eq. 6）。
- 每条边删除 `sU` 最小的操作（Eq. 7）。
- 重复直到每条边只剩一个操作。
- Source: Algorithm 1 lines 18-23, Eq. (6)-(7)

## 伪代码
```text
Algorithm: ABanditNAS
Input: Dtr, Dval, Omega(i,j), eps, K, T, lambda
Output: 最终鲁棒结构

1. 初始化每条边每个操作的性能 m_k,0^(i,j)。
   Source: Algorithm 1 line 2
2. while K > 1:
   2.1 计算 LCB 风格分数 sL(o_k^(i,j))。
       Source: Eq. (3)
   2.2 计算采样概率 p(o_k^(i,j)) = softmax(-sL)。
       Source: Eq. (4)
   2.3 在每条边采样一个操作，并进行一轮对抗训练。
       Source: Algorithm 1 lines 8-15
   2.4 获取验证精度 a，更新 m_k,t^(i,j)。
       Source: Algorithm 1 lines 16-17, Eq. (5)
   2.5 每 K*T 次采样后计算 sU，并在每条边剪掉 argmin sU。
       Source: Algorithm 1 lines 18-23, Eq. (6)-(7)
3. 输出保留下来的操作集合对应结构。
   Source: Algorithm 1 output description
```

## 训练流程
1. 搜索阶段按 anti-bandit 规则采样并进行对抗训练更新。
2. 逐步剪枝得到最终 cell 结构。
3. 用最终结构进行标准对抗训练并报告鲁棒指标。

Sources:
- Sec. 3.4, Algorithm 1, Sec. 4.1

## 推理流程
1. 固定搜索得到的结构。
2. 在白盒与黑盒攻击下评估鲁棒性。
3. 输出 clean 与 adversarial accuracy。

Sources:
- Sec. 4.1-4.2, Table 1-3

## 复杂度与效率
- 时间复杂度: `O(TK^2)`（论文 Eq. 8）。
- 空间复杂度: 论文未给出封闭表达式。
- 运行特征: 单 Titan V 上搜索约 1.93h（MNIST）/1.94h（CIFAR-10）。
- 扩展性: 初始空间极大（示例 `9^60`），通过逐轮淘汰收缩。

## 实现备注
- 本地代码路径: `D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense`。
- `models/darts_ops_1.py` 包含 Gabor 与 denoising 相关操作定义。
- 归档仓库以评估/权重/固定结构为主（`defenses/defense_all.py`, `utils/genotypes_all.py`）。
- 与论文 Algorithm 1 对应的完整搜索主循环未见单独公开脚本。
- 因此：论文方法可读性强，但“从仓库直接端到端复现搜索”仍有缺口。

## 与相关方法关系
- 对比 UCBNAS: ABanditNAS 增加 LCB 公平采样，减少“过早误杀”。
- 对比手工结构（LeNet/Wide-ResNet）: 在相近或更低搜索成本下取得更强鲁棒性。
- 主要优势: 兼顾搜索效率与鲁棒性能。
- 主要代价: 依赖置信界启发式与短周期验证信号质量。

## 证据与可追溯性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- 关键表: Table 1, Table 2, Table 3
- 关键公式: Eq. (1)-(8)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2008.00698
- HTML: https://arxiv.org/html/2008.00698v2
- 代码: https://github.com/RunwenHu/ABanditNAS
- 本地实现: D:/PRO/essays/code_depots/Anti-Bandit Neural Architecture Search for Model Defense

