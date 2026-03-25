---
title: "Resource-Efficient Iterative LLM-Based NAS with Feedback Memory"
method_name: "Iterative LLM-Based NAS with Feedback Memory"
authors: [Xiaojie Gu, Dmitry Ignatov, Radu Timofte]
year: 2026
venue: arXiv
tags: [NAS, llm-nas, iterative-search, resource-efficient]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2603.12091v1
local_pdf: D:/PRO/essays/papers/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory.pdf
local_code: D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory
created: 2026-03-23
---

# 论文笔记：Iterative LLM-Based NAS with Feedback Memory

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Resource-Efficient Iterative LLM-Based NAS with Feedback Memory |
| arXiv | https://arxiv.org/abs/2603.12091 |
| HTML | https://arxiv.org/html/2603.12091v1 |
| 官方匿名代码 | https://anonymous.4open.science/r/Iterative-LLM-Based-NAS-with-Feedback-Memory-E7D6/README.md |
| 本地代码归档 | `D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory` |
| 本地 PDF | `D:/PRO/essays/papers/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory.pdf` |

## 一句话总结
> 论文把 LLM 驱动 NAS 从一次性“写代码即结束”改成“生成-评估-诊断-再生成”的闭环，并用固定长度 `K=5` 的 [[Historical Feedback Memory]] 在单张 RTX 4090 上跑出稳定提升。

## 核心贡献
1. 提出闭环 LLM-NAS 管线：`Code Generator -> Evaluator -> Prompt Improver`（Sec. 3.1, Fig. 1）。
2. 引入 [[Historical Feedback Memory]]，使用固定窗口保留最近 5 次改进尝试，避免上下文无限增长（Sec. 3.4, Eq. 1/2）。
3. 将失败轨迹显式结构化为 [[Diagnostic Triple]]，把“报错样本”变成学习信号（Sec. 3.4, Eq. 3）。
4. 在 CIFAR-10 / CIFAR-100 / ImageNette 上展示低预算可行性：2000 iter 搜索约 18 GPU 小时（Sec. 4.3, Sec. 7）。

## 问题背景
### 要解决的问题
- 传统 NAS 计算成本极高（RL/evolution 常见千到万 GPU-days 级别）。
- 现有 LLM 造网工作常是 single-shot，缺少“从失败中持续学习”的机制。

### 现有方案局限
- 许多方法工作在预定义 cell 搜索空间，表达能力受限。
- 部分迭代式 LLM 优化依赖“保留高分样本”，会忽视失败样本中的结构性信息。

### 本文动机
- 用固定上下文长度实现可持续迭代，并把代码执行错误本身纳入反馈闭环。

## 方法详解
### 模块 1：Code Generator（Sec. 3.2）
- 输入：任务定义、当前 best code、上轮改进建议、当前轮代码与表现。
- 输出：可执行的 `Net(nn.Module)` 代码。
- 生成参数：temperature `0.7`、top-p `0.9`、max new tokens `2048`（Sec. 3.2, 4.1）。

### 模块 2：Evaluator（Sec. 3.3）
- 先做快速校验：dummy forward + 输出维度检查。
- 通过后训练 1 epoch，使用 Top-1 准确率作为代理排序信号。
- 训练协议：SGD(m=0.9, wd=5e-4), lr=0.01 + cosine annealing, batch=128。

### 模块 3：Prompt Improver（Sec. 3.4）
- 输入：best code + 当前结果 + 历史窗口 `H_t`。
- 输出：下一轮改进建议（含原因/灵感/可执行建议）。
- 历史条目按 `problem/suggestion/outcome` 组织，强调因果复盘。

## 关键公式
### 公式 1：有限历史窗口（Sec. 3.4, Eq. 1）
\[
H_t^{(K)}=\{(s_{t-K},a_{t-K}),\ldots,(s_{t-1},a_{t-1})\},\quad K=5
\]
含义：只保留最近 K 次改进尝试，控制上下文长度。

### 公式 2：K 阶 Markov 依赖（Sec. 3.4, Eq. 2）
\[
P(s_t \mid \mathcal{A}^*,H_t)=P(s_t \mid \mathcal{A}^*,H_t^{(K)})
\]
含义：下一步建议只依赖当前 best 和最近历史，不依赖全轨迹。

### 公式 3：诊断三元组（Sec. 3.4, Eq. 3）
\[
s_i=(problem_i,\ suggestion_i,\ outcome_i)
\]
含义：每条历史不仅有建议，还记录问题与结果，支持失败可学习化。

## 关键图表与结论
### Figure 1（流程图）
- 明确三模块闭环与数据流，核心是“评估信号回流到下一轮提示”。

### Figure 2（全过程轨迹）
- 三模型在三数据集总体呈上升趋势。
- Qwen 在 CIFAR-10 最终峰值最高（71.5%），但成功率较低。
- DeepSeek 在 CIFAR-100 成功率高（95.1%），但 ImageNette 成功率极低（0.7%）。

### Table 2（核心数值）
- CIFAR-10:
  - DeepSeek: 28.2% -> 69.2%（+41.0pp, rho=0.754）
  - Qwen: 50.0% -> 71.5%（+21.5pp, rho=0.561）
  - GLM-5: 43.2% -> 62.0%（+18.7pp, rho=0.422）
- CIFAR-100:
  - DeepSeek: 5.0% -> 29.2%
  - Qwen: 27.0% -> 29.6%
  - GLM-5: 19.1% -> 24.8%
- ImageNette:
  - Qwen: 23.0% -> 54.6%（rho=0.663）
  - GLM-5: 41.1% -> 58.3%（rho=0.631）

### Figure 3（消融）
- 去掉反馈记忆或参考架构后，轨迹明显退化，难以持续超越 single-shot。

## 代码对照（已归档仓库）
- 关键流程在 `pipeline.py`，包含 `best_code`、`improvement_history`、`history_size=5`。
- 快速校验 + 单 epoch 评估在 `evaluator.py` / `train_script.py`。
- 提示词模板和历史注入逻辑在 `code_generator.py` / `prompt_improver.py`。
- 复现脚本在 `run.sh` 与 `run_ablation.sh`，与论文迭代实验设置一致（2k/100 iter）。

## 批判性思考
### 优点
1. 把失败轨迹结构化纳入学习，优于“只保留高分样本”的迭代范式。
2. 资源预算清晰且可复验，具备工程可落地性。
3. 在开放代码空间内搜索，表达能力强于固定 cell 编码。

### 局限
1. 评价信号只用 1-epoch 精度，未证明与 fully-trained 最终性能的稳定一致性。
2. 各模型成功率差异大，鲁棒性受模型/任务组合影响显著。
3. 目前主要在中小数据集验证，尚缺更大规模任务的证据。

### 可复现性
- [x] 代码可访问（已本地归档）
- [x] 关键超参数明确
- [x] 消融实验给出
- [ ] 大规模数据集复现实验不足

## 关联概念
- [[Historical Feedback Memory]]
- [[Diagnostic Triple]]
- [[One-Epoch Proxy Evaluation]]
- [[Open Code Space]]
- [[Neural Architecture Search]]
- [[LLM-guided Search]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]

## 速查卡片
> [!summary] Iterative LLM-Based NAS with Feedback Memory
> - 核心机制: 固定窗口历史记忆 + 失败三元组反馈
> - 关键收益: 单卡低预算下可持续提升架构质量
> - 关键风险: 成功率波动大，1-epoch proxy 与最终性能仍有差距
> - 本地实现: `D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory`
