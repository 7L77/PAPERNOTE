---
title: "ZCP-Eval_ch"
type: method
language: zh-CN
source_method_note: "[[ZCP-Eval]]"
source_paper: "An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness"
source_note: "[[ZCP-Eval]]"
authors: [Jovita Lukasik, Michael Moeller, Margret Keuper]
year: 2025
venue: IJCV
tags: [nco-method, zh, nas, zero-cost-proxy, robustness]
created: 2026-03-13
updated: 2026-03-13
---

# ZCP-Eval 中文条目

## 一句话总结
> ZCP-Eval 评估“零训练代理信号”能否预测架构鲁棒性，核心结论是：预测 clean accuracy 常可依赖少量特征，但预测 robust accuracy 通常需要多代理联合。

## 来源
- 论文: [An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness](https://doi.org/10.1007/s11263-024-02265-7)
- HTML: https://link.springer.com/article/10.1007/s11263-024-02265-7
- 代码: https://github.com/jovitalukasik/zcp_eval
- 英文方法笔记: [[ZCP-Eval]]
- 论文笔记: [[ZCP-Eval]]

## 适用场景
- 问题类型: 不做全量训练时，预测候选架构的 clean/robust 表现。
- 前提假设: 有固定搜索空间（如 [[NAS-Bench-201]]）且可稳定计算 ZCP。
- 数据形态: 离线监督评估（benchmark-level）。
- 规模与约束: 架构数量大、对抗评估成本高时。
- 适用原因: 随机森林可将代理向量映射到鲁棒目标并取得较高 R2。

## 不适用或高风险场景
- 需要严格因果解释或理论保证的鲁棒性估计。
- 任务/搜索空间偏离 NAS-Bench-201 且缺少校准数据。
- 代理特征无法一致提取（工具链不统一或缺失）。

## 输入、输出与目标
- 输入: 每个架构的代理向量（如 `jacov`、`nwot`、`snip`、`flops`、`params`、`jacob_fro`，可加 GRAF）。
- 输出: clean 准确率与各攻击下 robust 准确率预测值。
- 优化目标: 单目标/多目标回归下提升测试 R2。
- 核心假设: 代理信号能携带足够的结构性能信息。

## 方法拆解

### 阶段 1：构建代理特征表
- 为 NAS-Bench-201 架构收集/对齐 ZCP 与鲁棒标签。
- 合并 Jung et al. 2023 与 Wu et al. 2024 的评估数据。
- Source: Sec. 3 / Sec. 4.1 / Sec. 4.2 / Sec. 4.3

### 阶段 2：训练预测器
- 在训练规模 32 / 128 / 1024 上训练随机森林。
- 同时做单目标与多目标回归。
- Source: Sec. 5.2 / Fig. 3 / Table 1-5

### 阶段 3：分析特征有效性
- 代理类别消融（Jacobian、Pruning、Baseline、Hessian、Piecewise-linear、GRAF）。
- Top-1 only 与去掉 Top-1 的对照实验。
- Source: Sec. 5.2.5 / Sec. 5.3 / Table 8-10 / Fig. 4-11

## 伪代码
```text
Algorithm: ZCP-Eval
Input: NAS-Bench-201 架构集合 A，代理集合 P，鲁棒标签 Y
Output: 预测性能与特征重要性分析

1. 对每个架构 a，提取代理向量 x_a。
   Source: Sec. 3 / Sec. 4.3
2. 构建数据集 D={(x_a, y_a)}，覆盖 clean 与 robust 目标。
   Source: Sec. 4.2 / Sec. 4.3
3. 对 n in {32, 128, 1024}，训练随机森林回归器。
   Source: Sec. 5.2
4. 在单目标/多目标设置下评估 R2。
   Source: Sec. 5.2 / Table 1-5
5. 执行类别消融、Top-1 only、Exclude Top-1 分析。
   Source: Sec. 5.2.5 / Sec. 5.3.1 / Table 8-10
6. 输出结论：鲁棒预测依赖多特征协同，而非单一代理。
   Source: Sec. 6
```

## 训练流程
1. 读取 benchmark 元数据与代理文件。
2. 将架构编码映射为 NAS-Bench-201 ID，并对齐标签。
3. 训练 `RandomForestRegressor`（开源代码默认 100 trees、bootstrap、OOB）。
4. 计算测试集 R2，分析特征贡献。

Sources:
- Sec. 5.2, Sec. 5.3
- 归档代码 `random_forest.py`

## 推理流程
1. 对新架构计算代理向量。
2. 输入已训练随机森林。
3. 输出 clean/robust 预测并据此排序。

Sources:
- Sec. 5.2
- Source: Inference from source（论文未单列部署流程）

## 复杂度与效率
- 时间复杂度: 论文未给解析式。
- 空间复杂度: 论文未给解析式。
- 运行特征: 相比“先训练再对抗评估”，显著省时。
- 扩展性: 训练样本增大时 R2 提升，但 robust 目标仍普遍比 clean 难。

## 实现备注
- 代码主入口：`random_forest.py`；数据接口：`robustness_dataset.py`。
- 需外部数据目录：`robustness-data`、`zcp_data`、`robustness_dataset_zcp`。
- 开源实现中可见的特征重要性是 MDI（`rf.feature_importances_`）。
- 论文主体强调 permutation importance，存在 paper-code 不完全对齐，需要复现时单独核对。

## 与相关方法关系
- 对比 [[Surrogate Predictor]]: 本文更偏“预定义代理 + 树模型解释”，不是端到端学习代理器。
- 对比 [[One-shot NAS]]: 本文不是搜索算法本体，而是搜索前/中期的性能预测评估器。
- 主要优势: 明确给出“哪些代理可迁移到鲁棒目标”的实证规律。
- 主要代价: 结论强依赖基准数据与可用代理集合。

## 证据与可溯源性
- 关键图: Fig. 1-2, Fig. 3, Fig. 4-11
- 关键表: Table 1-10
- 关键公式: 无新的核心优化公式（贡献主要在评估协议）
- 关键算法: 随机森林回归流程（Sec. 5.2）

## 参考链接
- arXiv: https://arxiv.org/abs/2307.09365
- HTML: https://link.springer.com/article/10.1007/s11263-024-02265-7
- 代码: https://github.com/jovitalukasik/zcp_eval
- 本地实现: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness

