---
title: "PWLNAS_ch"
type: method
language: zh-CN
source_method_note: "[[PWLNAS]]"
source_paper: "Loss Functions for Predictor-based Neural Architecture Search"
source_note: "[[PWLNAS]]"
authors: [Han Ji, Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICCV
tags: [nas-method, zh, predictor-based-nas, ranking-loss, weighted-loss]
created: 2026-03-20
updated: 2026-03-20
---

# PWLNAS 中文条目

## 一句话总结
> PWLNAS 用“分段损失”改造 predictor-guided NAS：前期用回归/排序损失做 warm-up，后期切到加权损失，提升找到 top 架构的概率。

## 来源
- 英文方法笔记: [[PWLNAS]]
- 论文: https://arxiv.org/abs/2506.05869
- HTML: https://arxiv.org/html/2506.05869v1
- 补充材料: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Ji_Loss_Functions_for_ICCV_2025_supplemental.pdf
- 代码: https://github.com/jihan4431/PWLNAS

## 适用场景
- 问题类型: 有查询预算约束的 predictor-based NAS。
- 前提假设: 不同 loss 在不同数据规模阶段各有优势。
- 数据形态: 迭代搜索中，已查询架构集合持续增长。
- 约束条件: 希望在不改 predictor 主体结构的前提下提升搜索质量。
- 适用原因: 仅改训练目标调度即可获得稳定收益，工程接入成本低。

## 不适用或高风险场景
- 搜索流程无法支持多轮 predictor 重训。
- 已有大规模完整监督，可直接训练高精度 predictor。
- 任务迁移跨度过大且无法可靠设定切换阈值。

## 输入、输出与目标
- 输入: 搜索空间 \(S\)、已查询样本集 \(D_t\)、predictor \(f_\theta\)、分段 loss 配置。
- 输出: 固定预算下找到的最优架构。
- 目标: 提升 predictor 的 top-ranking 能力，进而提升最终搜索结果。
- 核心假设: 低样本阶段排序损失更稳，高样本阶段加权损失更利于识别优质架构。

## 方法拆解
### 阶段 1：warm-up 训练
- 使用回归或排序损失先建立可靠的相对排序结构。
- 常见组合中 warm-up 多为 HR 或 ListMLE。
- Source: Sec. 4.3; Sec. 5; Supplementary Table 9

### 阶段 2：切换到加权损失
- 查询样本达到阈值后，切换到 MAPE / WARP / EW 等加权目标。
- 强化对高性能架构的区分能力。
- Source: Sec. 4.3; Sec. 5; Supplementary Table 9

### 阶段 3：predictor-guided 进化搜索
- predictor 打分 -> 选候选 -> 查询真实性能 -> 回流训练集 -> 重训 predictor。
- Source: Sec. 4.3

### 阶段 4：任务特定组合
- NAS-Bench-201: HR -> MAPE
- NAS-Bench-101: ListMLE -> WARP
- TransNAS-Bench-101 Micro: Jigsaw 用 MSE -> EW，其余任务 HR -> WARP
- DARTS: HR -> MAPE
- Source: Sec. 4.3; Supplementary Table 9

## 伪代码
```text
Algorithm: PWLNAS
Input: 搜索空间 S, predictor f_theta, 查询预算 B, warm-up 阈值 q_w, 损失对 (L_warm, L_focus)
Output: 最优架构 x_best

1. 随机初始化少量已查询样本集 D
   Source: Sec. 4.3
2. while |D| < B:
   2.1 训练 predictor:
       若 |D| <= q_w, 用 L_warm
       否则用 L_focus
       Source: Sec. 4.3; Supplementary Table 9
   2.2 用 predictor 给候选集打分并挑选高分候选
       Source: Sec. 4.3
   2.3 执行 predictor-guided evolutionary 采样生成新候选
       Source: Sec. 4.3
   2.4 查询新候选真实性能并加入 D
       Source: Sec. 4.3
3. 返回 D 中最优架构
   Source: Sec. 4.3
```

Source: Inference from source
- 论文明确了“分段 loss + predictor-guided evolutionary”主流程，但公开代码尚未完整给出搜索脚本参数细节，上述伪代码按论文描述复原。

## 训练流程
1. 选择 predictor 骨干（主实验常用 GCN）。
2. 在 warm-up 阶段用回归/排序损失训练 predictor。
3. 达到阈值后切换到加权损失继续训练。
4. 在迭代查询过程中反复更新 predictor。
5. 用 top-ranking 指标和最终搜索精度评估。

Sources:
- Sec. 4.1-4.3, Sec. 5, Supplementary Table 9

## 推理流程
1. 编码候选架构并输入 predictor。
2. 依据预测分数排序候选。
3. 选择高分候选做高成本真实性能评估。
4. 更新当前最佳架构并继续迭代。

Sources:
- Sec. 4.3

## 复杂度与效率
- 时间开销: 多轮 predictor 训练 + 多次真实性能查询。
- 空间开销: predictor 参数与查询样本缓存。
- 报告成本: DARTS 场景下 PWLNAS 设置约 0.2 GPU-days（Table 5）。
- 扩展特征: 在有限查询预算下，收益主要来自 top 架构命中率提升。

## 实现备注
- 官方仓库已公开 predictor 与 loss 相关实现（`model.py`, `utils.py`）。
- `utils.py` 包含 ListMLE、LR 风格 pair loss、WARP、EW、MAPE 等实现。
- README 标注完整 ranking/search 实验代码“将后续发布”。
- 因此当前可确认“损失函数实现细节”，完整搜索工程流程仍以论文描述为主。

## 与相关方法关系
- 相比固定单一损失（如只用 MSE）：PWLNAS 增加阶段自适应。
- 相比仅排序损失（HR/ListMLE）：保留前期排序优势，同时提升后期头部识别。
- 主要优势: 兼顾全局排序与头部命中。
- 主要代价: 需要手工设定 loss 组合与 warm-up 阈值。

## 证据与可溯源性
- 关键图: Fig. 2, Fig. 3, Fig. 7
- 关键表: Table 2/3/4/5（主文）, Table 9（补充材料）
- 关键公式: Sec. 3 + Supplementary A.1-A.7
- 算法出处: Sec. 4.3

## 参考链接
- arXiv: https://arxiv.org/abs/2506.05869
- HTML: https://arxiv.org/html/2506.05869v1
- Supplementary: https://openaccess.thecvf.com/content/ICCV2025/supplemental/Ji_Loss_Functions_for_ICCV_2025_supplemental.pdf
- 代码: https://github.com/jihan4431/PWLNAS
- 本地实现: D:/PRO/essays/code_depots/Loss Functions for Predictor-based Neural Architecture Search
