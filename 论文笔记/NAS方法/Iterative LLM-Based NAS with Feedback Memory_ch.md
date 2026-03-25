---
title: "Iterative LLM-Based NAS with Feedback Memory_ch"
type: method
language: zh-CN
source_method_note: "[[Iterative LLM-Based NAS with Feedback Memory]]"
source_paper: "Resource-Efficient Iterative LLM-Based NAS with Feedback Memory"
source_note: "[[Iterative LLM-Based NAS with Feedback Memory]]"
authors: [Xiaojie Gu, Dmitry Ignatov, Radu Timofte]
year: 2026
venue: arXiv
tags: [nas-method, zh, llm-nas, iterative-search, feedback-memory]
created: 2026-03-23
updated: 2026-03-23
---

# Iterative LLM-Based NAS with Feedback Memory 中文条目

## 一句话总结
> 该方法把 LLM 生成架构改造成闭环优化系统：每轮“生成-验证-评估-诊断”，并用固定长度历史记忆避免上下文膨胀。

## 来源
- 英文方法笔记: [[Iterative LLM-Based NAS with Feedback Memory]]
- 论文: https://arxiv.org/abs/2603.12091
- HTML: https://arxiv.org/html/2603.12091v1
- 代码: https://anonymous.4open.science/r/Iterative-LLM-Based-NAS-with-Feedback-Memory-E7D6/README.md
- 本地实现: `D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory`

## 适用场景
- 问题类型: 图像分类任务下的低成本 NAS。
- 前提假设: 1-epoch 精度可作为可用的排序代理信号。
- 数据形态: 监督学习，论文覆盖 CIFAR-10/100 和 ImageNette。
- 约束条件: 单卡资源、不可做 LLM 微调时尤为适用。
- 适用原因: 显式吸收失败轨迹，减少重复无效探索。

## 不适用或高风险场景
- 你必须直接获得 fully-trained 条件下的最优架构，且不能接受代理指标偏差。
- 当前 LLM 在目标任务上代码生成成功率过低。
- 任务对结构约束特别强，难以靠纯提示词稳定控制。

## 输入、输出与目标
- 输入: 数据集规格、当前 best code、当前轮评估结果、最近历史窗口。
- 输出: 新候选架构代码与更新后的 best 架构。
- 目标: 在迭代中最大化 one-epoch proxy accuracy。
- 核心假设: 最近 K 次上下文已足够支持有效改进决策。

## 方法拆解
### 阶段 1：候选架构生成
- Code Generator 根据 `best code + 上轮建议 + 当前结果` 生成 `Net` 代码。
- Source: Sec. 3.1 / Sec. 3.2 / Alg. 1

### 阶段 2：快速校验与代理评估
- 先做 forward shape 校验，再进行 1 epoch 训练得到代理精度。
- Source: Sec. 3.3 / Sec. 4.1

### 阶段 3：反馈诊断与建议生成
- Prompt Improver 读取当前结果与历史窗口，输出下一轮可执行建议。
- Source: Sec. 3.4 / Eq. (1)-(3)

### 阶段 4：历史更新并继续迭代
- 将 `(problem, suggestion, outcome)` 追加到历史并截断到 K=5。
- Source: Eq. (1), Eq. (3), Alg. 1

## 伪代码
```text
Algorithm: Iterative LLM-Based NAS with Feedback Memory
Input: LLM L, 最大迭代 T, 历史窗口 K=5, 数据集 D
Output: 最优架构 A*

1. 初始化 A*=None, a*=0, H=empty, s0=None
   Source: Alg. 1
2. 对 t=1..T:
   2.1 用 (A*, s_{t-1}, 当前代码/结果) 生成候选 A_t
       Source: Sec. 3.1/3.2
   2.2 快速校验 A_t（可实例化 + 输出维度）
       Source: Sec. 3.3
   2.3 若通过则训练 1 epoch 得到 a_t，否则记录错误
       Source: Sec. 3.3, Sec. 4.1
   2.4 若 a_t > a*，更新 A*=A_t
       Source: Alg. 1
   2.5 用 (A*, A_t, 结果, H) 生成下一轮建议 s_t
       Source: Sec. 3.4
   2.6 记录诊断三元组并将 H 截断到最近 K 条
       Source: Eq. (1), Eq. (3)
3. 输出 A*
   Source: Alg. 1
```

## 训练流程
1. 加载并增强数据（CIFAR 使用随机裁剪/翻转）。
2. 训练候选模型 1 epoch。
3. 优化器使用 SGD（`lr=0.01`, `momentum=0.9`, `wd=5e-4`）+ cosine 调度。
4. 以 Top-1 作为代理分数反馈回闭环。

Sources:
- Sec. 3.3, Sec. 4.1, Table 2

## 推理流程
1. 生成器根据上下文产出候选代码。
2. 评估器返回精度或错误信息。
3. 改进器输出下一轮建议。
4. 持续维护 best-so-far 架构直到迭代结束。

Sources:
- Sec. 3.1-3.4, Alg. 1

## 复杂度与效率
- 时间开销: 约为 `O(T * 单次一轮训练成本)`。
- 空间开销: 由 LLM 推理占用和候选模型训练占用主导。
- 报告成本: 2000 轮约 18 GPU 小时（RTX 4090）。
- 扩展特征: 分辨率提升可能显著降低生成成功率。

## 实现备注
- 主流程在 `pipeline.py`。
- 生成参数在 `llm_client.py`：`temperature=0.7`, `top_p=0.9`, `max_new_tokens=2048`。
- 历史机制：`improvement_history` + `history_size=5`。
- 快速校验逻辑在 `evaluator.py`；训练隔离在 `train_script.py`（30 分钟超时）。
- 统一随机种子 43，配合 deterministic 设置提升可复验性。

## 与相关方法关系
- 对比 [[LLMO]]: 本文是开放代码空间搜索，不是固定离散 cell 空间。
- 对比 [[EvoPrompting]]: 报告设置不依赖 LLM 微调。
- 对比 [[OPRO]]: 本文显式建模错误轨迹与诊断三元组。
- 主要优势: 低预算条件下的失败可学习化迭代。
- 主要代价: 代理指标不等价于最终 fully-trained 表现。

## 证据与可溯源性
- 关键图: Fig. 1 / Fig. 2 / Fig. 3
- 关键表: Table 1 / Table 2
- 关键公式: Eq. (1) / Eq. (2) / Eq. (3)
- 关键算法: Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2603.12091
- HTML: https://arxiv.org/html/2603.12091v1
- 代码: https://anonymous.4open.science/r/Iterative-LLM-Based-NAS-with-Feedback-Memory-E7D6/README.md
- 本地实现: D:/PRO/essays/code_depots/Resource-Efficient Iterative LLM-Based NAS with Feedback Memory
