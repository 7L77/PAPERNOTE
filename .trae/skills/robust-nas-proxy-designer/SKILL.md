---
name: "robust-nas-proxy-designer"
description: "Designs robust NAS workflows with train-free proxies and paper-grounded implementation plans. Invoke when user wants robust architecture search, zero-cost proxy design, or notes-to-skill conversion."
---

# Robust NAS Proxy Designer

目标：把用户关于“鲁棒性架构搜索”的想法，整理成一个可执行的 skill / 方法方案 / 实验计划，特别适用于以下路线：

- training-free robust NAS
- zero-cost proxy / zero-shot proxy
- robust proxy ensemble / proxy fusion
- 结合已有论文笔记，构建自己的鲁棒 NAS skill

## 何时调用

在以下场景调用：

- 用户说要做鲁棒 NAS、免训练鲁棒架构搜索、zero-cost robust proxy
- 用户提到 TRNAS、RTP-NAS、Robust_ZCP、CRoZe、RoBoT 等方法，并希望整理成实现方案
- 用户希望把论文笔记、代码仓库、方法草图整理成一个可复用的研究 skill
- 用户需要“问题分析 → 方法选择 → 代理设计 → 搜索流程 → 实验协议”的一体化输出

如果用户只是想读某篇论文本身，优先读论文；如果用户要“基于这些论文搭建自己的鲁棒 NAS 能力”，使用本 skill。

## 默认目标

默认把任务拆成五层：

1. 明确鲁棒 NAS 的目标定义
2. 选择最匹配的 proxy family
3. 设计搜索与筛选流程
4. 设计复现实验与消融
5. 输出成 skill / 方法卡 / 伪代码 / 代码实施清单

## 先收集的关键信息

若用户没有给全，先主动从上下文、仓库、笔记中补齐；仍缺失时再最小化追问。至少整理出：

- 搜索空间：NAS-Bench-201 / DARTS / NB301 / 自定义 supernet
- 目标任务：图像分类、鲁棒分类、分布外鲁棒、压缩约束下鲁棒
- 鲁棒目标：FGSM / PGD / AA / corruption / UAP / 混合威胁模型
- 预算约束：完全免训练、少量查询、可否最终 adversarial finetune
- 候选粒度：完整架构排序、算子剪枝、cell 搜索、top-k rerank
- 用户已有资产：论文笔记、代码仓库、已有 proxy、已有 benchmark

## 你应优先检索的本地笔记

当工作区中存在这些笔记时，优先把它们作为设计依据：

- `d:\PRO\essays\论文笔记\TRNAS.md`
- `d:\PRO\essays\论文笔记\RTP-NAS.md`
- `d:\PRO\essays\论文笔记\Robust-ZCP.md`
- `d:\PRO\essays\论文笔记\CRoZe.md`
- `d:\PRO\essays\论文笔记\RoBoT.md`
- `d:\PRO\essays\论文笔记\_概念\Robust Neural Architecture Search_ch.md`
- `d:\PRO\essays\综述\鲁棒性.md`

输出方案时，优先把这些笔记里的方法抽象成“可组合模块”，而不是逐篇复述。

## 方法家族选择规则

先判断用户更像哪一类任务，再决定 skill 的主线。

### A. 纯训练前评分型

适用：

- 用户强调极低搜索成本
- 不希望生成对抗样本
- 更关注快速排序与 top-k 筛选

优先参考：

- Robust-ZCP
- TRNAS

默认模块：

- NTK / 梯度相关信号
- 输入损失地形 / 局部曲率
- 线性激活能力 / 特征稳定性
- 多目标排序：robustness + FLOPs + Params

### B. 对抗空间剪枝型

适用：

- 用户接受“先构造共享扰动空间，再做免训练搜索”
- 搜索空间中算子级剪枝更自然

优先参考：

- RTP-NAS

默认模块：

- UAP 构造共享 adversarial input space
- adversarial NTK 条件数
- linear region / expressive power
- prune-by-score 的迭代剪枝流程

### C. 一致性代理型

适用：

- 用户希望代理能覆盖多种扰动
- 愿意用一次或少量 surrogate 更新

优先参考：

- CRoZe

默认模块：

- clean / perturbed 双分支
- feature consistency
- parameter consistency
- gradient alignment
- 乘积式或加权式融合

### D. 多代理集成与预算开发型

适用：

- 用户已有多个 proxy，但单个 proxy 不稳定
- 用户手上有有限 query budget，可做少量真实性能反馈

优先参考：

- RoBoT

默认模块：

- proxy pool 构建
- min-max 标准化
- 权重优化或 BO 融合
- top-T development / rerank / greedy exploitation

## 建 skill 时推荐的固定输出骨架

每次都尽量输出下面 8 个部分：

1. **任务定义**
   - 搜索空间
   - 鲁棒目标
   - 预算
   - 最终部署约束

2. **方法定位**
   - 属于 A / B / C / D 哪个主家族
   - 为什么不用另外几条路线

3. **代理设计**
   - 核心分数公式
   - 每一项对应什么归纳偏置
   - 哪些项是 robust-specific，哪些项是通用 NAS proxy

4. **搜索流程**
   - sample / evaluate / prune / evolve / rerank / finalize
   - 是否需要最终 adversarial training 验证

5. **实验协议**
   - benchmark
   - 攻击设置
   - clean/robust 多目标指标
   - 相关性指标：Spearman / Kendall / Precision@T

6. **消融设计**
   - 单 proxy vs 融合 proxy
   - clean proxy vs robust proxy
   - 是否使用 UAP / perturbation branch / BO

7. **失败模式**
   - 代理分数塌缩
   - 强攻击下相关性下降
   - skip-heavy 结构误判
   - 数据增强与 proxy 不一致

8. **落地资产**
   - 要新增哪些脚本
   - 要复用哪些仓库/笔记
   - 最小可运行 baseline 是什么

## 从已有笔记提炼出的组合模板

### 模板 1：TRNAS 风格

适合“先筛再训”的鲁棒 NAS。

- robust proxy：`R-Score = β * LAM + (1-β) * FRM`
- search：evolutionary search 或 Pareto-aware selection
- objectives：robust proxy + FLOPs + Params
- finalize：top-1 / top-k 架构做 PGD adversarial training

### 模板 2：RTP-NAS 风格

适合“对抗输入空间 + 算子剪枝”。

- 先构造共享 UAP
- 在 adversarial space 上测 NTK conditioning
- 同时加入 linear regions
- 每轮删最弱操作，直至单路径架构收敛

### 模板 3：Robust-ZCP 风格

适合“完全 zero-cost，尽量不碰显式对抗样本”。

- NTK 相关项近似鲁棒可训练性
- input-loss-landscape 相关项近似局部脆弱性
- 对候选做快速 ranking
- 用 tabular benchmark 或少量最终训练验证 top-k

### 模板 4：CRoZe 风格

适合“跨扰动泛化”。

- 构造 clean / perturbed surrogate
- 计算 feature / parameter / gradient consistency
- 用乘积式或分层汇总分数筛架构
- 关注多扰动平均表现，而不只看单一 PGD

### 模板 5：RoBoT 风格

适合“已有很多 proxy，不知道怎么稳健融合”。

- 先构建 proxy pool：如 SynFlow、NASWOT、GradNorm、Robust-ZCP、CRoZe-style term
- 再做权重学习或 BO
- 最后用 development budget 在 top-ranked 架构中贪心开发

## 推荐你给用户的 skill 目录结构

如果用户要真正落地一个研究型 skill，优先建议如下结构：

```text
.trae/skills/robust-nas-proxy-designer/
  SKILL.md

可选配套代码目录：
robust_nas_skill/
  __init__.py
  search_spaces/
  proxies/
    ntk_proxy.py
    curvature_proxy.py
    consistency_proxy.py
    fusion_proxy.py
  search/
    rank_search.py
    prune_search.py
    evolution_search.py
  benchmarks/
    nb201.py
    darts.py
  eval/
    attacks.py
    rank_metrics.py
  scripts/
    smoke_rank.py
    run_nb201_rank_corr.py
    run_topk_finalize.py
```

但如果用户当前只想先定义 skill，本次只创建 `SKILL.md` 即可，不主动扩写整套代码。

## 输出风格要求

输出内容时遵循：

- 先给“问题定位 + 方法选择结论”
- 再给“为什么选这条路线”
- 再给“可执行 skill 草案 / 伪代码 / 文件骨架”
- 每个创新点都绑定一个验证方式
- 避免只写空泛词，如“更鲁棒”“更高效”；要落到 proxy、budget、benchmark、attack

## 默认实验建议

若用户没有给实验协议，默认建议：

- 搜索空间：NAS-Bench-201 或 DARTS
- 数据：CIFAR-10 起步
- 攻击：FGSM + PGD20 + AutoAttack
- 排序评估：Spearman / Kendall tau / Precision@T
- 最终验证：top-5 架构做标准训练或对抗训练
- 报告：clean accuracy、robust accuracy、search cost、rank correlation、top-k hit rate

## 默认回答模板

当用户说“帮我构建一个鲁棒 NAS skill”时，按以下顺序回答：

1. 用一句话定义其研究目标
2. 判断它更接近 TRNAS / RTP-NAS / Robust-ZCP / CRoZe / RoBoT 中哪几类
3. 给出一个最小可行 skill 说明
4. 给出后续代码模块与实验计划
5. 明确哪些部分来自笔记，哪些部分是新的组合设计

## 禁止事项

- 不要把 clean NAS 代理直接当作 robust proxy，除非明确说明只是 baseline
- 不要省略 threat model 与 attack budget
- 不要把“排序相关性高”直接等同于“最终鲁棒精度一定高”
- 不要只报单一攻击结果
- 不要默认所有搜索空间都适合同一种 proxy
