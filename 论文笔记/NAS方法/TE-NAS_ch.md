---
title: "TE-NAS_ch"
type: method
language: zh-CN
source_method_note: "[[TE-NAS]]"
source_paper: "Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective"
source_note: "[[TE-NAS]]"
authors: [Wuyang Chen, Xinyu Gong, Zhangyang Wang]
year: 2021
venue: ICLR
tags: [nas-method, zh, nas, training-free, ntk, linear-regions]
created: 2026-03-26
updated: 2026-03-26
---

# TE-NAS 中文条目

## 一句话总结
> TE-NAS 通过“删掉某个算子后 NTK 条件数变化 + 线性区域变化”的双排序相加来做剪枝式 NAS，在不训练候选网络的前提下完成高效搜索。

## 来源
- 论文: [Neural Architecture Search on ImageNet in Four GPU Hours: A Theoretically Inspired Perspective](https://arxiv.org/abs/2102.11535)
- HTML: https://arxiv.org/html/2102.11535
- 代码: https://github.com/VITA-Group/TENAS
- 英文方法笔记: [[TE-NAS]]
- 论文笔记: [[TE-NAS]]

## 适用场景
- 问题类型: 训练自由（training-free）的 cell-based NAS 搜索。
- 前提假设: 初始化阶段的 proxy 与最终性能存在可用相关性。
- 数据形态: 以图像分类搜索空间为主（NAS-Bench-201、DARTS）。
- 规模与约束: 搜索预算紧，但允许多次计算 NTK/线性区域指标。
- 适用原因: 显式平衡可训练性与表达性，且组合规则可解释。

## 不适用或高风险场景
- 目标任务与图像分类搜索空间差异过大，proxy 相关性未知。
- 结构不适合 ReLU 线性区域统计。
- 模型规模过大，重复 proxy 评估成本过高。

## 输入、输出与目标
- 输入: 搜索空间（边与候选算子）、数据加载器、初始化方式、repeat 次数。
- 输出: 剪枝后的最终架构（single-path 或 DARTS 稀疏单元）。
- 优化目标: 在低搜索成本下挑出高质量架构。
- 核心假设: `\kappa_N` 低 + `\hat{R}_N` 高的架构更优。

## 方法拆解

### 阶段 1: 构建并初始化超网
- 从“所有算子都在”的超网出发。
- 每次代理评估前按 Kaiming 重新初始化。
- Source: Sec. 3.2, Algorithm 1; Appendix A.

### 阶段 2: 逐算子计算删除后的 proxy 变化
- 对每条边上的每个未删除算子，构造临时删除版本。
- 计算删除前后 NTK 条件数变化与线性区域变化。
- 重复多次后取均值降低随机初始化噪声。
- Source: Algorithm 1; `prune_tenas.py`、`lib/procedures/ntk.py`、`lib/procedures/linear_region_counter.py`.

### 阶段 3: 双排序求和并按边剪枝
- 分别按 NTK 与线性区域两项做排序。
- 计算 `s(o_j)=s_\kappa(o_j)+s_R(o_j)`。
- 每条边剪掉重要性最低的算子，迭代到终止。
- Source: Algorithm 1, Sec. 3.2.

## 伪代码
```text
Algorithm: TE-NAS
Input: 初始超网 N0（E 条边，每边 |O| 个算子），重复次数 r
Output: 最终架构 N*

1. 初始化超网 N <- N0。
   Source: Algorithm 1 (line 1)
2. 当 N 还不是 single-path 时循环：
   Source: Algorithm 1 (line 2)
3.   对每个可删算子 oj：
     3.1 构造 N\oj（屏蔽 oj）。
         Source: Algorithm 1 (line 3-5)
     3.2 估计 NTK 变化分数（repeat 后取均值）。
         Source: Algorithm 1 (line 4), Sec. 3.1.1
     3.3 估计线性区域变化分数（repeat 后取均值）。
         Source: Algorithm 1 (line 5), Sec. 3.1.2
4.   分别得到 NTK 排名 s_kappa(oj) 与区域排名 s_R(oj)。
     Source: Algorithm 1 (line 6-7)
5.   合并重要性 s(oj)=s_kappa(oj)+s_R(oj)。
     Source: Algorithm 1 (line 8)
6.   在每条边上剪去重要性最低的算子。
     Source: Algorithm 1 (line 10-12)
7. 返回最终架构 N*。
   Source: Algorithm 1 (line 14)
```

## 搜索与训练流程
1. 搜索阶段不对候选架构进行完整训练。
2. 每轮仅通过初始化 proxy（`\kappa_N` 与 `\hat{R}_N`）做决策。
3. 迭代剪枝得到目标架构。
4. 对目标架构按标准配方重训并报告最终精度。

Sources:
- Sec. 3, Sec. 4, Appendix A

## 推理流程
1. 固定搜索得到的最终拓扑。
2. 重训后按常规前向推理评估。
3. 按基准协议输出 test error / top-1 / top-5。

Sources:
- Sec. 4.2, Sec. 4.3
- Source: Inference from source

## 复杂度与效率
- 时间复杂度: 论文未给封闭表达式。
- 空间复杂度: 论文未给封闭表达式。
- 运行特征: 文中报告 NAS-Bench-201 约 0.5 GPU 小时，DARTS-ImageNet 约 4 GPU 小时。
- 扩展性说明: 逐轮删算子可显著压缩搜索分支，但每轮 proxy 评估仍有计算开销。

## 实现备注
- 启动脚本: `prune_launch.py`。
- 主循环: `prune_tenas.py::main`。
- NTK 条件数实现: `lib/procedures/ntk.py`（特征值比值）。
- 线性区域实现: `lib/procedures/linear_region_counter.py`（ReLU hook + 激活符号模式计数）。
- 代码细节: 实际是“删除后相对变化”再做排序求和，这是论文排序思想的工程实现。
- 关键超参数: `repeat`、`prune_number`、`batch_size`、`precision`、初始化模式。

## 与相关方法关系
- 对比 NAS w.o. Training（Mellor et al., 2020）: TE-NAS 用双指标而非单 Jacobian 信号，排序稳定性更好。
- 对比 [[Differentiable Architecture Search]] 系列: 搜索成本更低，但极限性能不总是最优。
- 主要优势: 训练自由、可解释、搜索快。
- 主要代价: 对 proxy-性能相关性的依赖较强。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 3, Fig. 4, Fig. 5, Fig. 8, Fig. 9, Fig. 10
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 5
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2102.11535
- HTML: https://arxiv.org/html/2102.11535
- 代码: https://github.com/VITA-Group/TENAS
- 本地实现: D:/PRO/essays/code_depots/Neural Architecture Search on ImageNet in Four GPU Hours A Theoretically Inspired Perspective
