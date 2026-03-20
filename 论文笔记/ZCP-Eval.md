---
title: "An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness"
method_name: "ZCP-Eval"
authors: [Jovita Lukasik, Michael Moeller, Margret Keuper]
year: 2025
venue: IJCV
tags: [NAS, zero-cost-proxy, robustness, random-forest]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/abs/2307.09365
local_pdf: D:/PRO/essays/papers/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness.pdf
local_code: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness
created: 2026-03-13
updated: 2026-03-20
---

# 论文笔记：ZCP-Eval

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness |
| 期刊 | IJCV 2025 |
| DOI | https://doi.org/10.1007/s11263-024-02265-7 |
| 代码 | https://github.com/jovitalukasik/zcp_eval |
| arXiv | https://arxiv.org/abs/2307.09365 |
| 本地 PDF | `D:/PRO/essays/papers/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness` |

## 一句话总结
> 这篇工作系统评估了 15 种 [[Zero-Cost Proxy]]（含拓扑特征）对 clean 与鲁棒精度的预测能力，结论是 clean 预测可由少量强特征完成，但 robust 预测通常依赖多特征协同。

## 核心贡献
1. 在 [[NAS-Bench-201]] 上，把 ZCP 评估从 clean accuracy 扩展到 adversarial robustness（单目标与多目标）评估。
2. 统一使用 [[Random Forest Regressor]] 建立预测器，比较两套鲁棒数据源：Jung et al. 2023 与 Wu et al. 2024。
3. 用 [[Permutation Feature Importance]] 分析代理贡献，明确了“鲁棒预测难于 clean 预测”的特征层机制。
4. 给出直接可操作结论：做鲁棒 NAS 时，单代理往往不够，多代理组合更稳健。

## 问题背景
### 要解决的问题
- 以往 ZCP 主要预测 clean 表现，但鲁棒 NAS 里真正昂贵的是“训练后再做攻击评估”。
- 作者关心：面向 clean 的 ZCP 能否迁移到 robust accuracy 预测？

### 现有方法局限
- 只看 clean 的 proxy 可能选到“高精度但脆弱”的架构。
- 强攻击下鲁棒评估成本高，不利于大规模搜索。

### 本文动机
- 如果在未训练/低成本阶段就能粗估鲁棒性，就能显著降低鲁棒 NAS 的搜索开销。

## 方法详解
### 1) 输入特征
- 15 个常见 ZCP（Jacobian / Pruning / Piecewise-linear / Hessian / Baseline 等）。
- 可选拼接 [[Neural Graph Features (GRAF)]]（NAS-Bench-201 上 191 维拓扑特征）。

### 2) 数据与任务
- Robustness Dataset（Jung et al., 2023）：clean 训练架构，在 FGSM/PGD/APGD/Square 攻击下评估。
- NAS-RobBench-201（Wu et al., 2024）：adversarially trained 架构，在 FGSM/PGD/AutoAttack 下评估。
- 任务包括：
  - 单目标回归：clean 或某一攻击下 robust accuracy。
  - 多目标回归：clean + 攻击精度联合预测。

### 3) 预测器
- 论文使用随机森林回归。
- 本地代码 `random_forest.py` 中默认配置可见：`n_estimators=100`、`bootstrap=True`、`oob_score=True`。

### 4) 评估与解释
- 排序相关性：Kendall tau（图中展示）。
- 回归性能：测试集 `R^2`（Table 1-10）。
- 特征解释：Permutation feature importance（论文），并做 Top-1 与 Excluding-Top-1 对照。

## 关键结果（带数字）
### Table 1（Jung 数据集，eps=1/255）
- 1024 训练样本时，CIFAR-10：
  - clean 单目标 `R^2 = 0.93`
  - FGSM/PGD/APGD/Square 单目标 `R^2 = 0.84 / 0.56 / 0.56 / 0.63`
- 结论：clean 明显更易预测，强攻击目标更难。

### Table 2/3（NAS-RobBench-201）
- 1024 训练样本时，CIFAR-10/100 多项任务常见 `R^2` 约 `0.96-0.97`。
- 对抗训练后的目标在该基准上表现出更高可预测性。

### Table 6/7（加入 GRAF）
- 在 Jung 数据集上，多数目标有提升（如 CIFAR-10 的 PGD/APGD 从 0.36/0.24 提升到 0.59/0.62，对应 128 样本设置）。
- 在 NAS-RobBench-201 上总体已很高，提升有限，个别目标有轻微下降。

### Table 8（按代理类别）
- 仅用 GRAF 或 Jacobian 类通常还能保持较好预测。
- 仅用 piecewise-linear（`zen`）或 Hessian 类时，多项 robust 目标出现显著下降，甚至负 `R^2`。

### Table 9/10（Top-1 对照）
- 只用最重要单特征时，clean 还能维持中等水平，但 robust 常明显退化：
  - 例如 CIFAR-10 单目标 PGD：`R^2 = -0.37`（Table 9）。
- 去掉最重要特征后，全模型只小幅下降：
  - 例如 CIFAR-10 单目标 PGD：`0.56 -> 0.51`（Table 1 vs Table 10）。
- 结论：robust 预测依赖“多特征协同”，而不是单一万能代理。

## 与代码实现的对照
- 归档仓库主脚本为 `random_forest.py`，依赖外部数据目录：
  - `robustness-data/`
  - `zcp_data/`
  - `robustness_dataset_zcp/`
- 论文主文强调 permutation importance；但当前公开代码里主要使用的是 MDI（`rf.feature_importances_`）。
- 这意味着：代码足以复现实验流程骨架，但论文图表数值级一致性仍依赖完整数据与细节脚本。

## 批判性思考
### 优点
1. 评估范围完整：覆盖两套鲁棒基准、单目标与多目标设置。
2. 结论清晰可操作：鲁棒预测要优先考虑代理组合，而非单代理。
3. 有解释分析：不仅报性能，还给出特征重要性证据链。

### 局限
1. 结论主要基于 NAS-Bench-201，跨搜索空间泛化仍待验证。
2. 主要聚焦对抗攻击鲁棒性，未覆盖更广泛 distribution shift。
3. 公开代码与论文解释分析口径（permutation vs MDI）存在轻微不一致。

### 对当前 NAS 研究的启发
1. 在鲁棒目标上，建议先做多代理融合，再做架构筛选。
2. 如果算力受限，优先构建“低成本 proxy 集合 + 轻量回归器”，而不是直接全量对抗训练搜索。
3. 特征重要性分析应作为标准步骤，避免被单 proxy 的局部高相关误导。

## 关联概念
- [[Zero-Cost Proxy]]
- [[Random Forest Regressor]]
- [[Neural Graph Features (GRAF)]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[NAS-Bench-201]]
- [[Permutation Feature Importance]]
- [[Neural Architecture Search]]

## 速查卡片
> [!summary] ZCP-Eval
> - 核心问题: clean 导向 ZCP 能否迁移到 robust 预测
> - 核心方法: 多 ZCP/GRAF 特征 + 随机森林回归 + 重要性分析
> - 关键结论: clean 可由少量强特征预测；robust 依赖多特征协同
> - 实践建议: 鲁棒 NAS 场景下优先做代理融合，不要押单指标
