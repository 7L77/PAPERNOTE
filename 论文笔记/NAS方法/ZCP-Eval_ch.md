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
tags: [nas-method, zh, nas, zero-cost-proxy, robustness, random-forest]
created: 2026-03-13
updated: 2026-03-20
---

# ZCP-Eval 中文条目

## 一句话总结
> ZCP-Eval 研究了低成本代理信号能否预测架构鲁棒性，结论是：预测 clean 往往可以依赖少量强特征，但预测 robust 需要多代理联合。

## 来源
- 论文: [An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness](https://doi.org/10.1007/s11263-024-02265-7)
- arXiv: https://arxiv.org/abs/2307.09365
- 代码: https://github.com/jovitalukasik/zcp_eval
- 英文方法笔记: [[ZCP-Eval]]
- 论文笔记: [[ZCP-Eval]]

## 适用场景
- 问题类型: 在不做全量训练的前提下，快速预测候选架构的 clean/robust 精度。
- 前提假设: 架构来自固定可评估搜索空间（如 [[NAS-Bench-201]]），并能稳定提取代理特征。
- 数据形态: 离线监督回归（基准评测数据）。
- 资源约束: 对抗评测成本高，希望先做低成本筛选。
- 适用原因: 随机森林在低样本下也能给出较高 `R^2`。

## 不适用或高风险场景
- 需要严格因果解释或理论保证的鲁棒性估计。
- 任务/搜索空间偏离 NAS-Bench-201 且无校准数据。
- 代理特征提取流程不一致或不可得。

## 输入、输出与目标
- 输入: 每个架构的代理向量（15 个 ZCP，如 `jacov`、`nwot`、`snip`、`flops`、`params`、`jacob_fro`），可选拼接 191 维 [[Neural Graph Features (GRAF)]]。
- 输出: clean 准确率与攻击下 robust 准确率的预测值。
- 优化目标: 在单目标与多目标设置下提升测试 `R^2`。
- 核心假设: 代理统计量携带足够的结构信息来估计 clean/robust 表现。

## 方法拆解
### 阶段 1：构建特征-标签表
- 收集每个架构的 ZCP 特征并对齐鲁棒标签。
- 标签来自 Jung et al. 2023 与 Wu et al. 2024。
- Source: Sec. 3 / Sec. 4.1 / Sec. 4.2 / Sec. 4.3

### 阶段 2：训练随机森林预测器
- 训练规模使用 32 / 128 / 1024 三档。
- 同时做单目标回归与多目标回归。
- Source: Sec. 5.2 / Table 1-7

### 阶段 3：分析特征有效性
- 代理类别消融（Jacobian、Pruning、Piecewise-linear、Hessian、Baseline、GRAF）。
- Top-1 only 与 Excluding Top-1 对照实验。
- Source: Sec. 5.2.5 / Sec. 5.3.1 / Table 8-10 / Fig. 4-11

## 伪代码
```text
Algorithm: ZCP-Eval
Input: 架构集合 A，代理提取器 P，鲁棒标签 Y
Output: 预测性能指标与特征重要性结论

1. 对每个架构 a，计算或读取代理向量 x_a。
   Source: Sec. 3 / Sec. 4.3
2. 构建数据集 D={(x_a, y_a)}，其中 y_a 含 clean 与 robust 目标。
   Source: Sec. 4.2 / Sec. 4.3
3. 对 n in {32, 128, 1024}，训练 RandomForestRegressor。
   Source: Sec. 5.2
4. 评估单目标/多目标测试 R^2。
   Source: Sec. 5.2 / Table 1-7
5. 执行类别消融、Top-1 only、Excluding Top-1 分析。
   Source: Sec. 5.2.5 / Sec. 5.3.1 / Table 8-10
6. 输出结论：robust 预测是否依赖多特征协同。
   Source: Sec. 6
```

## 训练流程
1. 读取鲁棒基准标签与代理特征文件。
2. 将架构编码映射到 NAS-Bench-201 ID 并对齐标签。
3. 训练随机森林（公开代码默认 `n_estimators=100`、`bootstrap=True`、`oob_score=True`）。
4. 统计测试 `R^2` 并做特征重要性分析。

Sources:
- Sec. 5.2, Sec. 5.3
- 代码证据: `random_forest.py`, `robustness_dataset.py`

## 推理流程
1. 为新候选架构提取代理向量。
2. 输入训练好的随机森林模型。
3. 输出 clean/robust 预测分数并据此排序。

Sources:
- Sec. 5.2
- Source: Inference from source（论文未单列部署流程）

## 复杂度与效率
- 时间复杂度: 论文未给解析式。
- 空间复杂度: 论文未给解析式。
- 运行特征: 相比“逐架构对抗训练+攻击评估”显著更省算力。
- 扩展趋势: 训练样本增加时 `R^2` 普遍上升；在 Jung 数据集上 robust 目标仍普遍难于 clean。

## 实现备注
- 本地归档代码: `D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness`
- 默认依赖外部数据目录:
  - `robustness-data/`
  - `zcp_data/`
  - `robustness_dataset_zcp/`
- 论文主文强调 permutation importance；当前公开脚本主要使用 MDI（`rf.feature_importances_`）。
- 复现实验图表时需显式记录这一 paper-code 差异。

## 与相关方法关系
- 对比 [[Surrogate Predictor]]: 本文是“代理特征迁移到鲁棒目标”的系统评测框架。
- 对比 [[One-shot NAS]] 鲁棒搜索: 本文不是完整搜索算法，而是评估/预测器设计。
- 主要优势: 给出可执行的“代理组合优先级”经验规律。
- 主要代价: 结论依赖基准数据质量与覆盖范围。

## 证据与可溯源性
- 关键图: Fig. 1-2（相关性）、Fig. 3（流程）、Fig. 4-11（重要性）。
- 关键表: Table 1-10。
- 关键公式: 无新的核心优化公式，贡献在评测协议与分析框架。
- 关键代码证据: `random_forest.py` 中随机森林超参数与 MDI 实现。

## 参考链接
- DOI: https://doi.org/10.1007/s11263-024-02265-7
- arXiv: https://arxiv.org/abs/2307.09365
- 代码: https://github.com/jovitalukasik/zcp_eval
- 本地实现: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness
