---
title: "RZ-NAS"
type: method
language: zh-CN
source_method_note: "[[RZ-NAS]]"
source_paper: "RZ-NAS: Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy"
authors: [Zipeng Ji, Guanghui Zhu, Chunfeng Yuan, Yihua Huang]
year: 2025
venue: ICML (PMLR 267)
tags: [nas-method, llm-guided-search, zero-cost-proxy, reflection]
created: 2026-03-17
updated: 2026-03-17
---

# RZ-NAS 中文方法笔记

## 一句话总结
> RZ-NAS 把 LLM 放到演化 NAS 的“变异器”位置，用 Zero-Cost Proxy 做快速打分，再用反思反馈指导下一轮变异，从而在低搜索成本下提升架构质量。

## 来源
- 论文：[[RZ-NAS]]
- 代码：https://github.com/PasaLab/RZ-NAS
- 本地代码：`D:/PRO/essays/code_depots/RZ-NAS Enhancing LLM-guided Neural Architecture Search via Reflective Zero-Cost Strategy`

## 适用场景
- 问题类型：需要低成本搜索神经网络结构的 NAS 任务。
- 前提假设：[[Zero-Cost Proxy]] 与最终性能有可用相关性。
- 数据形态：图像分类为主，也演示了检测任务迁移。
- 约束：希望兼容 micro/macro 搜索空间。

## 不适用场景
- 需要完全确定性、可重复且不依赖外部 LLM 服务。
- 搜索空间约束难以通过文本/代码描述清晰表达。
- 代理指标在目标任务中相关性弱。

## 输入/输出/目标
- 输入：任务、数据集、搜索空间、代理类型、迭代轮数、种群大小、预算约束。
- 输出：种群中 Zero-Cost 分数最高的结构。
- 目标：最大化代理分数（Source: Sec. 3.1, Eq. (1)）。

## 方法分解
### 阶段 1：种群初始化与候选采样
- 初始化种群并按迭代随机选一个结构做变异。
- Source: Sec. 3.2; Alg. 1 line 1-4.

### 阶段 2：LLM 结构化提示词变异
- 提示词同时提供搜索空间描述、网络构造代码、代理计算说明、in-context 示例。
- Source: Sec. 3.3; Fig. 2.

### 阶段 3：合法性检查与代理打分
- 对变异结构做约束校验，再调用 proxy 代码计算分数。
- Source: Sec. 3.2; Alg. 1 line 5-8.

### 阶段 4：反思反馈与种群更新
- 将前后结构、分数和异常输入反思模块，生成下一步建议。
- Source: Sec. 3.2; Alg. 1 line 9-17; Appendix A.2.

## 可追溯伪代码
```text
Algorithm: RZ-NAS
Input: S, D, zc, B, T, N, F0
Output: F*

1. P <- {F0}
   Source: Alg. 1 line 1
2. for t in 1..T:
   Source: Alg. 1 line 2
3.   从 P 随机选 Ft
   Source: Alg. 1 line 3
4.   用结构化 prompt 让 LLM 生成 F't
   Source: Sec. 3.2-3.3, Fig. 2
5.   校验 F't 合法性与预算约束
   Source: Alg. 1 line 5-7
6.   z <- zc(F't)，加入 P
   Source: Alg. 1 line 7-8
7.   若 |P|>N，删除最低分结构
   Source: Alg. 1 line 9-10
8.   基于 (Ft, F't, z, exception) 生成反思建议
   Source: Alg. 1 line 15; Appendix A.2
9. return P 中最高分结构
   Source: Alg. 1 line 17
```

## 训练与推理流程
- 搜索阶段：执行“LLM 变异 + proxy 打分 + 反思反馈”循环。
- 评估阶段：对最优结构进行标准训练/测试，报告分类精度或检测 mAP。
- Source: Sec. 4, Fig. 4, Table 2-7.

## 复杂度与效率
- 论文未给出闭式复杂度。
- 报告了低搜索成本（如 Table 1 的 0.03 GPU days）以及每代理约 $75 API 成本（Sec. 4）。

## 代码实现备注
- 主入口：`evolution_search.py`。
- Prompt 模板：`prompt/template.txt`。
- 注意 1：当前代码里 `generate_by_llm(structure_str)` 没把传入结构字符串真正注入 prompt。
- 注意 2：模板尾部是不完整 assistant JSON，依赖 completion continuation。
- 注意 3：代码默认超参与论文实验设置（迭代/种群）不一致。
- 结论：代码体现思路，但要复现实验数字需要进一步对齐脚本和配置。

## 对比方法
- 相比 [[GENIUS]] / [[EvoPrompting]]：强调 text+code 双视角约束和反思闭环。
- 主要优势：低成本下提升 proxy 引导的搜索质量。
- 主要代价：依赖 LLM 服务与 prompt 工程细节。

## 证据锚点
- Figure: 1, 2, 3, 4
- Table: 1, 2, 3, 4, 5, 6, 7, 9, 10
- Equation: (1), (2)-(7)
- Algorithm: 1
