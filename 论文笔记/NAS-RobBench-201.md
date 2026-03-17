---
title: "Robust NAS benchmark under adversarial training: assessment, theory, and beyond"
method_name: "NAS-RobBench-201"
authors: [Yongtao Wu, Fanghui Liu, Carl-Johann Simon-Gabriel, Grigorios G. Chrysos, Volkan Cevher]
year: 2024
venue: ICLR
tags: [nas, robust-nas, adversarial-training, benchmark, ntk-theory]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=cdUpf6t6LZ
local_pdf: D:/PRO/essays/papers/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond.pdf
local_code: D:/PRO/essays/code_depots/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond
created: 2026-03-17
---

# 论文笔记：NAS-RobBench-201

## 元信息
| Item | Value |
|---|---|
| Paper | Robust NAS benchmark under adversarial training: assessment, theory, and beyond |
| Venue | ICLR 2024 |
| OpenReview | https://openreview.net/forum?id=cdUpf6t6LZ |
| Project page | https://tt2408.github.io/nasrobbench201hp/ |
| Official code | https://github.com/TT2408/nasrobbench201 |
| Local PDF | `D:/PRO/essays/papers/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond.pdf` |
| Local code | `D:/PRO/essays/code_depots/Robust NAS under Adversarial Training Benchmark, Theory, and Beyond` |

## 一句话总结
> 这篇论文把 robust NAS 从“零散实验”推进到“可复现基准 + 理论解释”：发布 NAS-RobBench-201（6466 个非同构架构的对抗训练结果），并给出多目标对抗训练下与 NTK 相关的泛化界。

## 核心贡献
1. 发布首个面向对抗训练的 NAS-Bench-201 风格鲁棒基准 [[NAS-Rob-Bench-201]]，覆盖 clean/FGSM/PGD/APGD 等指标。  
Source: Sec. 3, Fig. 2-4, Table 1-2.
2. 从 [[Neural Tangent Kernel]] 出发，给出多目标（clean + robust）训练下的泛化理论，并引入混合核与 twice-perturbation 核。  
Source: Sec. 4, Eq. (3)-(6), Theorem 1, Corollary 1.
3. 用基准系统分析鲁棒 NAS：跨数据集排序相关性、不同 NAS 算法表现、分布外扰动相关性。  
Source: Sec. 3.2, Fig. 3(c), Table 2, Appendix F (Table 6/7).

## 问题背景
- 传统 NAS 基准多数只看标准训练下的 clean accuracy，难以直接支持“对抗训练下找架构”。  
  Source: Sec. 1-2.
- 现有 robust NAS 既缺统一 benchmark，也缺“为什么这种搜索目标有效”的理论桥梁。  
  Source: Sec. 1, Sec. 4 intro.

## 方法与技术细节

### 1) 基准构建（NAS-RobBench-201）
- 搜索空间：NAS-Bench-201 cell（6 edges, 5 ops），总 15625，去同构后 6466 个架构。  
  Source: Sec. 3.1, Fig. 1.
- 数据集：CIFAR-10 / CIFAR-100 / ImageNet-16-120。  
  Source: Sec. 3.1.
- 训练设置：对每个架构做对抗训练（PGD-7，eps=8/255，step=2/255），50 epochs，batch=256，3 seeds。  
  Source: Sec. 3.1.
- 评估：clean + FGSM/PGD（eps in {3/255, 8/255}）+ AutoAttack。  
  Source: Sec. 3.1.
- 计算代价：约 107k GPU hours（文中估算）。  
  Source: Sec. 3.1.

### 2) 多目标对抗训练目标
文中把训练目标写成 clean loss 与 robust loss 的加权和（`beta` 控制权衡）：

\[
\mathcal{L}(W) = (1-\beta)\mathcal{L}_{clean}(W) + \beta \mathcal{L}_{robust}(W)
\]

其中 `beta=0` 退化为标准训练，`beta=1` 对应纯对抗训练。  
Source: Eq. (3), Sec. 4.1.

### 3) 理论：混合 NTK 与泛化界
作者构造了 clean 任务对应的混合核 `K_all` 与 robust 任务对应的 `\tilde{K}_{all}`，核心由 clean NTK、cross NTK、robust NTK 与 twice-perturbation NTK 组合而成。  
Source: Eq. (4), Eq. (5), Sec. 4.2.

主要结论（FCNN）：
- clean / robust 的 0-1 泛化误差上界受对应混合核的最小特征值控制；
- 当 `beta=0` 可退化到标准训练情形；
- robust bound 还依赖 twice-perturbation 相关核。  
Source: Theorem 1, Eq. (6), Remarks.

CNN 情况给出对应 corollary。  
Source: Corollary 1.

## 关键图表与结论

### Table 1（与已有 benchmark 的相关性对比）
- NAS-RobBench-201 内部 clean/PGD/FGSM 相关性高（例如 PGD 与 FGSM 达到 0.998）。
- 但和“标准训练后再做鲁棒评测”的旧基准相比，相关性显著掉落（如 PGD vs PGD* 仅 0.382），说明“标准训练排名”不能替代“对抗训练排名”。  
Source: Table 1.

### Table 2（在新基准上跑 NAS）
- 在该基准上，按 robust 指标搜索通常比按 clean 指标搜索更容易找到更鲁棒架构。
- Local Search 在示例设置中优于随机/进化搜索。  
Source: Table 2, Sec. 3.2.

### Figure 3(c)（跨数据集迁移）
- CIFAR-10/100/ImageNet-16-120 的架构排名相关性较高，支持“小数据集先搜，再迁移”的思路。  
Source: Fig. 3(c), Sec. 3.2.

### Figure 5（NTK-score 相关性）
- robust NTK 相关分数与鲁棒指标的相关性强于 clean NTK；
- 更强扰动设定下相关性上升趋势更明显。  
Source: Fig. 5, Sec. 4.3.

## 批判性思考
### 优点
1. 基准规模大且可公开查询，显著降低 robust NAS 比较成本。
2. 理论不是“单纯搬运标准训练 NTK”，而是明确写出 multi-objective 下的核组合。
3. 附录还补了 gradient obfuscation 与 corruption robustness 分析，覆盖面较完整。

### 局限
1. 搜索空间仍是 NAS-Bench-201 cell 级空间，外推到更大/更新搜索空间仍需验证。
2. 理论条件依赖宽网络和若干假设，和实际有限宽度网络之间仍有距离。
3. benchmark 构建成本很高（一次性 107k GPU hours），社区复建门槛不低。

## 可复用点（给你当前工作的价值）
1. 如果你在做 robust NAS，对比实验可以直接接入该 benchmark，减少重复训练。
2. 你的 proxy 设计可优先考虑和 robust NTK / twice perturbation 相关的信号。
3. 做论文复现时可先用 repo 的 lookup 接口快速验证“搜索策略是否真的提高鲁棒排名”。

## 关联概念
- [[NAS-Rob-Bench-201]]
- [[Robust Neural Architecture Search]]
- [[Neural Tangent Kernel]]
- [[Robust Neural Tangent Kernel]]
- [[Twice Perturbation]]
- [[Multi-objective Adversarial Training]]
- [[Adversarial Robustness]]
- [[NAS-Bench-201]]

