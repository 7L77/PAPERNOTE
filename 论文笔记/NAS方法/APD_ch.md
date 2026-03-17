---
title: "APD_ch"
type: method
language: zh-CN
source_method_note: "[[APD]]"
source_paper: "Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models"
source_note: "[[APD]]"
authors: [Haidong Kang, Lihong Lin, Hanling Wang]
year: 2025
venue: NeurIPS
tags: [nas-method, zh, training-free-nas, zero-cost-proxy, llm, actor-critic]
created: 2026-03-16
updated: 2026-03-16
---

# APD 中文条目

## 一句话总结
> APD 用 LLM 生成 zero-cost proxy，再用 actor-critic 学习“初始化/变异/交叉”提示策略，把训练免费 NAS 的代理设计从手工启发式升级为可学习的自动搜索。

## 来源
- 论文: [Revolutionizing Training-Free NAS: Towards Efficient Automatic Proxy Discovery via Large Language Models](https://openreview.net/forum?id=JJEiQmE5yA)
- PDF: https://openreview.net/pdf/4de84ad7c65b21c88fbadfd0dda141113b8c3017.pdf
- NeurIPS 页面: https://nips.cc/virtual/2025/poster/120003
- 代码: https://github.com/yohbii/APD
- 英文方法笔记: [[APD]]
- 论文笔记: [[APD]]

## 适用场景
- 问题类型: 训练免费 NAS 中的架构排序代理发现与优化。
- 前提假设: 有一小部分可用的真值性能样本用于相关性评估。
- 数据形态: 以视觉任务为主（分类/autoencoding/scene/jigsaw）。
- 规模与约束: 无法对大量候选架构完整训练，但需要较高排序质量时。
- 适用原因: 同时优化“proxy 本身”和“proxy 进化策略”，比固定启发式更灵活。

## 不适用或高风险场景
- 不能在安全沙箱中执行 LLM 生成代码。
- 没有可用真值子集，无法构建奖励信号。
- 需要严格确定性结果，不接受 LLM 生成随机性。

## 输入、输出与目标
- 输入: 提示操作集 `Π`、当前种群 `P_t`、上下文窗口 `C_t`、含真值性能的基准架构集合。
- 输出: 进化后的代理种群与最优代理 `f*`。
- 优化目标: 最大化代理评分排序与真实架构性能排序的一致性。
- 核心假设: 提示策略可被奖励学习；LLM 生成的 proxy 代码能表达有效排序启发。

## 方法拆解

### 阶段 1: 上下文感知的代理生成
- 每一步选择 `init/mut/cross` 操作，并把 prompt 与上下文喂给 LLM。
- 每个代理由 `(T, C)` 组成：`T` 是 thought 文本，`C` 是可执行代码。
- Source: Sec. 3.1, Eq. (2), Eq. (3), Fig. 4

### 阶段 2: 适应度评估
- 使用排序相关性评估 proxy，并加入运行代价惩罚。
- Source: Sec. 3.1, Eq. (4)

### 阶段 3: Actor-Critic 调度
- actor 根据历史状态选择下一步操作，critic 提供价值基线。
- 奖励取候选代理平均适应度。
- Source: Sec. 3.1, Eq. (5)

### 阶段 4: 种群更新
- 合并旧种群和新候选，保留 top-N，迭代直到预算耗尽。
- Source: Sec. 3.2, Algorithm 1

## 伪代码
```text
Algorithm: APD
Input: LLM L, 操作集 Π={init,mut,cross}, 基准集 B, 种群大小 N, 预算 T_max
Output: 最优 proxy f*

1. 用初始化 prompt 生成初始种群 P0
   Source: Sec. 3.2 Step 0, Algorithm 1
2. 对每一代 t=1..T_max:
   2.1 由历史策略和奖励构造状态 s_t
       Source: Sec. 3.1
   2.2 actor 从 πθ(a|s_t) 采样动作 a_t=(op, C_t)
       Source: Sec. 3.1, Eq. (5)
   2.3 通过 LLM 生成候选 P'_t = L(op, C_t)
       Source: Sec. 3.1 Eq. (2)(3), Sec. 3.2 Step 1
   2.4 计算候选适应度 ϕ（相关性与代价）
       Source: Sec. 3.1 Eq. (4), Sec. 3.2 Step 2
   2.5 计算奖励 r_t=E[ϕ(P'_t)] 并更新 actor/critic
       Source: Sec. 3.1 Eq. (5), Sec. 3.2 Step 3
   2.6 从 P_t ∪ P'_t 中选择下一代 P_{t+1}
       Source: Sec. 3.2 Step 4, Algorithm 1
3. 返回最高适应度 proxy
   Source: Algorithm 1
```

## 训练流程
1. 按 benchmark 准备 `init/mut/cross` prompt 模板。
2. 运行 APD 进化主循环，策略网络选择操作。
3. 在架构子集上评估候选 proxy 的排序能力。
4. 保留高分 proxy 并迭代更新。

Sources:
- Sec. 3.1, Sec. 3.2, Algorithm 1, Appendix B/C

## 推理流程
1. 固定搜索到的最优 proxy 函数。
2. 对新候选架构在初始化状态计算 proxy 分数。
3. 用分数排序后，仅训练头部候选架构。

Sources:
- Sec. 2, Sec. 4.2-4.5

## 复杂度与效率
- 时间复杂度: 论文未给闭式。
- 空间复杂度: 论文未给闭式。
- 运行特征: 文中报告约 30 代可达 Spearman > 0.80，单 RTX4090 约 1 小时。
- 扩展性说明: 成本主要受代数、种群规模、单次 proxy 评估耗时影响。

## 实现备注
- 主循环代码在 `main.py`：`get_new_pop -> evaluate -> A2C update -> topk`。
- `src/utils.py` 从 LLM markdown 响应中抽取 description+code。
- `src/env.py` 通过 `exec` 执行生成代码，失败样本记为 `0` 分。
- 论文默认超参（Table 8）：episodes=10、steps=100、history=5、gamma=0.9、hidden=256、batch=16、repeats=5。
- Paper/code 差异：
  - 论文定义 `ϕ = ρ - β cost`；当前代码路径主要处理单一 score。
  - 论文对不合法 proxy 记 `-∞`；代码实现是 `0`。
  - 当前 `ValueNet` 单输出后使用 `softmax`，critic 表达能力退化。
  - 仓库缺少 `evaluate_nas201.py / evaluate_nas101.py / evaluate_trans101.py` 与 `prompt/` 资源，需补齐后才能完整复现。

## 与相关方法关系
- 对比 [[Zero-Cost Proxy]] 手工设计：APD 把 proxy 设计自动化。
- 对比 [[AZ-NAS]] / [[SWAP-NAS]] 这类固定代理：APD 可按数据集和搜索空间自适应发现新 proxy。
- 主要优势: 自动化、可扩展、跨 benchmark 表现稳定。
- 主要代价: 依赖 LLM API 与代码执行安全；仍需真值子集做奖励。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- 关键表: Table 1, Table 2, Table 3, Table 4, Table 5, Table 6, Table 7, Table 8
- 关键公式: Eq. (1), Eq. (2), Eq. (3), Eq. (4), Eq. (5)
- 关键算法: Algorithm 1

## 参考链接
- OpenReview: https://openreview.net/forum?id=JJEiQmE5yA
- PDF: https://openreview.net/pdf/4de84ad7c65b21c88fbadfd0dda141113b8c3017.pdf
- NeurIPS 页面: https://nips.cc/virtual/2025/poster/120003
- 代码: https://github.com/yohbii/APD
- 本地实现: D:/PRO/essays/code_depots/Revolutionizing Training-Free NAS Towards Efficient Automatic Proxy Discovery via Large Language Models

