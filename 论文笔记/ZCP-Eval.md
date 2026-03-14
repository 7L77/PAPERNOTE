---
title: "An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness"
method_name: "ZCP-Eval"
authors: [Jovita Lukasik, Michael Moeller, Margret Keuper]
year: 2025
venue: IJCV
tags: [NAS, zero-cost-proxy, robustness, random-forest]
zotero_collection: ""
image_source: online
arxiv_html: https://link.springer.com/article/10.1007/s11263-024-02265-7
local_pdf: D:/PRO/essays/papers/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness.pdf
local_code: D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness
created: 2026-03-13
---

# 论文笔记：ZCP-Eval

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness |
| DOI | https://doi.org/10.1007/s11263-024-02265-7 |
| Code | https://github.com/jovitalukasik/zcp_eval |
| 额外版本 | https://arxiv.org/abs/2307.09365 |
| 本地 PDF | `D:/PRO/essays/papers/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness` |

## 一句话总结
> 本文系统评估 [[Zero-Cost Proxy]] 在 [[NAS-Bench-201]] 上预测鲁棒性的能力，结论是“预测 clean accuracy 往往靠少数代理即可，而预测鲁棒性通常必须联合多种代理特征”。

## 核心贡献
1. 将 15 种 ZCP 与 GRAF 拓扑特征放到统一框架下，评估其对 clean / robust accuracy 的可预测性（Sec. 3-5）。
2. 把问题从单目标扩展到多目标（clean + robustness），并在 Jung et al. 2023 与 Wu et al. 2024 两个数据集上验证（Sec. 4.2, 5.2）。
3. 用随机森林 + [[Permutation Feature Importance]] 分析“哪些代理真正有用”，并给出“仅保留 Top-1 特征”与“去掉 Top-1 特征”两组对照（Sec. 5.3.1, Table 9, Table 10）。

## 问题背景
### 要解决的问题
- 传统 ZCP 主要用于预测训练后 clean 性能，但 NAS 场景中 [[Adversarial Robustness]] 同样关键。
- 问题是：已有准确率导向的 ZCP，能否迁移为鲁棒性预测器？

### 现有方法局限
- 只看 clean accuracy 会忽略“高精度但脆弱”的架构。
- 鲁棒性评估通常要对已训练模型做对抗攻击，成本高，难用于大规模搜索。

### 本文动机
- 若能在未训练/低成本阶段，用 ZCP 近似预测鲁棒性，可显著降低鲁棒 NAS 的代价（Sec. 1, 5.2）。

## 方法详解
### 1) 特征空间（代理集合）
- 代理类别：Jacobian-based、Pruning-based、Piecewise-linear、Hessian-based、Baseline、Neural Graph Features（Sec. 3）。
- 代表特征：`jacov`, `nwot`, `snip`, `grasp`, `hessian`, `flops`, `params`, `jacob_fro` 等。

### 2) 数据与搜索空间
- 搜索空间：[[NAS-Bench-201]]，6466 个 unique/non-isomorphic 架构（Sec. 4.1）。
- 数据集：
  - Robustness dataset（Jung et al., 2023）：clean train 后评估 FGSM/PGD/APGD/Square（Sec. 4.2）。
  - NAS-RobBench-201（Wu et al., 2024）：adversarial train 后评估 FGSM/PGD/AutoAttack（Sec. 4.2）。

### 3) 预测模型
- 输入：每个架构的 ZCP 向量（可拼接 GRAF 191 维特征）。
- 目标：单目标（clean 或某攻击下鲁棒准确率）与多目标（clean + robust）回归。
- 模型：RandomForestRegressor，文中默认 100 trees（Sec. 5.2）。

### 4) 评估与解释
- 相关性：Kendall tau（Fig. 1, Fig. 2）。
- 预测性能：测试集 R2（Table 1-8）。
- 特征重要性：置换重要性（Sec. 5.3；Fig. 4-11）。

## 关键结果（带数字）
### Table 1（Robustness dataset, eps=1/255）
- 训练样本 1024 时，CIFAR-10:
  - clean 单目标 R2 = 0.93
  - FGSM 单目标 R2 = 0.84
  - PGD/APGD 单目标 R2 = 0.56/0.56
- 说明：鲁棒目标明显更难，尤其强攻击下回归更差。

### Table 2/3（NAS-RobBench-201）
- 对抗训练后的数据更“可预测”，R2 整体更高；例如 1024 样本下 CIFAR-10 多数目标约 0.96-0.97。
- 用扰动输入重新计算代理，对相关性/预测并无普遍收益，仅在少量场景有小幅改善（Sec. 5.2.2）。

### Table 8（只用某一类代理）
- 仅用 GRAF 或 Jacobian 类可获得较好效果。
- 仅用 `zen`（piecewise-linear）或 `hessian` 时性能显著下降（部分任务出现负 R2）。

### Table 9 / Table 10（Top-1 特征实验）
- 只用最重要单特征时：clean 可接受，但 robust 常明显退化甚至负值（Table 9）。
- 去掉最重要特征后：整体只小幅下降（Table 10）。
- 结论：鲁棒性预测依赖“多特征协同”，不是单一万能代理。

## 与代码实现的对照
- 归档代码仓为 `zcp_eval`，核心脚本 `random_forest.py`。
- 代码默认依赖外部数据目录：`robustness-data/`、`zcp_data/`、`robustness_dataset_zcp/`（README）。
- 代码中可见的特征重要性实现是 MDI（`rf.feature_importances_`），而论文主体强调 permutation importance。
- 因此代码可复现实验框架，但“图表与最终数值完全一致性”依赖完整数据和未公开的其余脚本流程。

## 批判性思考
### 优点
1. 覆盖面广：单目标/多目标、clean train/adversarial train、多种攻击全评估。
2. 结论可操作：为鲁棒 NAS 的代理组合提供经验（优先 Jacobian + baseline + 图特征组合）。
3. 解释性较强：不仅报告精度，还分析特征贡献。

### 局限
1. 评估集中在 NAS-Bench-201，跨搜索空间泛化仍待验证。
2. 关注对抗攻击，未覆盖更广 distribution shift（作者在 Conclusion 中明确了该限制）。
3. 开源仓库偏“实验入口 + 依赖数据”，复现实验仍有数据门槛。

### 复现性评估
- [x] 代码开源
- [ ] 一键复现实验脚本完整
- [x] 训练/评估思路清晰
- [ ] 无门槛数据下载（需外部链接）

## 关联概念
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[NAS-Bench-201]]
- [[Permutation Feature Importance]]
- [[Neural Architecture Search]]

