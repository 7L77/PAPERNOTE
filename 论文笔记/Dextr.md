---
title: "Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature"
method_name: "Dextr"
authors: [Rohan Asthana, Joschua Conrad, Maurits Ortmanns, Vasileios Belagiannis]
year: 2025
venue: TMLR
tags: [NAS, zero-cost-proxy, training-free-nas, svd, curvature]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=X0vPof5DVh
local_pdf: D:/PRO/essays/papers/Dextr Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature.pdf
local_code: D:/PRO/essays/code_depots/Dextr
created: 2026-03-16
---

# 论文笔记：Dextr

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature |
| Venue | TMLR (2025) |
| OpenReview | https://openreview.net/forum?id=X0vPof5DVh |
| Code | https://github.com/rohanasthana/Dextr |
| 本地 PDF | `D:/PRO/essays/papers/Dextr Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Dextr` |

## 一句话总结
> Dextr 用“各层特征图线性独立性（SVD 视角）+ 输出轨迹外在曲率（表达性）”构造无标签 zero-cost proxy，在多个 NAS 相关 benchmark 上获得更稳健的相关性与较低搜索成本。

## 核心贡献
1. 给出“[[Feature Map Collinearity|特征图共线性]] 与收敛/泛化负相关”的理论与实验证据（Sec. 3.2-3.3, Fig. 1）。
2. 将 [[Singular Value Decomposition]] 与 [[Extrinsic Curvature]] 组合成统一 proxy（Eq. 8），同时覆盖 convergence/generalization/expressivity。
3. 在 NB101/NB201/TransNASBench-101-micro 的相关性实验和 DARTS/AutoFormer 搜索实验中给出强竞争结果（Table 1-3）。

## 问题背景
### 要解决的问题
- 许多 zero-cost proxy 依赖标签，现实搜索场景常拿不到标签。
- 部分 proxy 只关注“好训练”或“高表达性”中的一侧，难以兼顾。

### 现有方法局限
- 只看收敛/泛化，容易偏向宽浅结构。
- 只看表达性，容易忽略训练稳定性与泛化。
- 论文沿用“固定参数预算下三者难同时最优”的观点（No Free Lunch for architecture attributes）。

## 方法详解
### 1) 收敛/泛化侧：特征条件数
- 对每层输出特征图做展开矩阵，计算其奇异值。
- 用奇异值比例（等价于逆条件数）刻画层内特征的线性独立程度。
- 直觉上：越不共线，收敛和泛化潜力越好。

### 2) 表达性侧：输出外在曲率
- 构造圆形输入轨迹 \(g(\theta)\)，看网络输出曲线弯曲程度。
- 曲率越高，表示函数形状变化能力越强，表达性更高。

### 3) 统一 Dextr 打分
论文给出的核心形式（Eq. 8）：

$$
\text{Dextr}
=
\frac{
\log\!\left(1+\sum_{l=1}^{L}\frac{1}{c_l(X_\phi)}\right)\cdot
\log(1+\kappa(\theta))
}{
\log\!\left(1+\sum_{l=1}^{L}\frac{1}{c_l(X_\phi)}\right)+
\log(1+\kappa(\theta))
}
$$

- \(c_l(X_\phi)\)：第 \(l\) 层特征图矩阵条件数。
- \(\kappa(\theta)\)：输出曲线外在曲率。
- 分子分母结构对应“简化调和平均”式融合；log 用于数值稳定与尺度压缩。

### 4) 对 ViT 的迁移
- 作者基于“注意力层在特定条件下可与卷积建立联系”+ GeLU 与 ReLU 的可比性，论证 Dextr 可迁移到 ViT 搜索（Sec. 3.3.4）。

## 关键结果（含数字）
### Table 1：相关性（Spearman）
- Dextr 在 NB101/NB201/TransNASBench-101-micro 多项任务领先或接近最优。
- 代表数值：
  - NB101: **0.65 ± 0.010**
  - NB201-cifar10: **0.90 ± 0.006**
  - NB201-cifar100: **0.91 ± 0.004**
  - NB201-ImageNet16-120: **0.87 ± 0.006**
  - NB301: 0.44 ± 0.007（非最优，但竞争力可接受）

### Table 2：DARTS 搜索（ImageNet 评估）
- Dextr（ZS）Top-1/Top-5 error = **24.6 / 7.4**, Params 6.6M, Search cost 0.07 GPU days。
- 比多数 one-shot 方法更快；与强 zero-shot baseline 相比精度与速度较均衡。

### Table 3：AutoFormer
- Tiny(6M)：Dextr Top-1 error **23.7**，优于 AZ-NAS 的 23.9，搜索成本同为 0.03 GPU days。
- Small(24M)：Dextr 18.0，接近 AZ-NAS 17.8，同时 FLOPs 更低（4.93G vs 5.13G）。

### Table 4：组件消融（NB201）
- `log(1+c(X))` 与 `log(1+κ)` 单独都比对应经典 proxy 更强。
- 直接“Zen 与 ZiCo 的朴素调和平均”显著弱于 Dextr，说明融合方式本身很关键。

## 代码对照（本地归档）
核心实现路径：
- `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`
- `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr_utils/no_free_lunch_architectures/length.py`
- `D:/PRO/essays/code_depots/Dextr/NASBench201/correlation/NAS_Bench_201.py`

实现观察：
1. 层侧分数用 `svd = min(s) / max(s)`，即逆条件数；随后跨层求和并取 `log(1+·)`。
2. 曲率由 `get_extrinsic_curvature(_opt)` 通过输出对轨迹参数 \(\theta\) 的一二阶导数估计。
3. 最终融合与论文 Eq. 8 一致：`dextr = results * curvature / (results + curvature)`。
4. 代码里对异常有回退（如 curvature NaN 时仅使用 SVD 侧项）。

## 局限与风险
1. Appendix 显示在 NATS-Bench-SSS 上原始 Dextr 可能出现负相关，需要额外优化版（Dextropt）修正。
2. 曲率估计涉及高阶自动求导，仍有算力开销，不是“零成本”意义上的免费。
3. 理论分析主要围绕 ReLU/GeLU，跨激活函数泛化仍待验证。

## 复现性评估
- [x] 论文公开（OpenReview）
- [x] 代码公开
- [x] 本地 PDF 已归档
- [x] 本地代码已归档
- [ ] 一键复现实验环境（需按 README 分别配置 NASLib/NB201/AutoFormer 环境）

## 关联概念
- [[Singular Value Decomposition]]
- [[Condition Number]]
- [[Extrinsic Curvature]]
- [[Gram Matrix]]
- [[Network Expressivity]]
- [[Neural Tangent Kernel]]

## Code Snippets and Operations

### A) Feature Extraction Path (layer activations -> SVD)
File: `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`

```python
def forward_hook(module, data_input, data_output):
    fea = data_output[0].clone().detach()
    n = torch.tensor(fea.shape[0])
    fea = fea.reshape(n, -1)
    s = torch.linalg.svdvals(fea)
    svd = torch.min(s) / torch.max(s)  # inverse condition signal
    svd[torch.isnan(svd)] = 0
    svd[torch.isinf(svd)] = 0
    result_list.append(svd)
```

### B) Curvature Path (curve input -> first/second derivatives)
File: `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr_utils/no_free_lunch_architectures/length.py`

```python
theta = torch.linspace(0, 2 * np.pi, n_interp).cuda(non_blocking=True)
curve_input = ...
output = network(curve_input[_idx:_idx+batch_size])
v = autograd.grad(output[:, index].sum(), theta, create_graph=True, retain_graph=True)[0]
a = autograd.grad(v.sum(), theta, create_graph=True, retain_graph=True)[0]
kappa += (vv**(-3/2) * (vv * aa - va ** 2).sqrt()).sum().item()
```

### C) Final Fusion (aligned with Eq. 8)
File: `D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`

```python
results = torch.log(1 + torch.sum(torch.tensor(result_list)))
curvature = torch.log(1 + torch.tensor(curvature))
dextr = results * curvature / (results + curvature)
```

### D) Practical Operations
1. NB201 correlation runs:
```bash
cd D:/PRO/essays/code_depots/Dextr/NASBench201/correlation
python NAS_Bench_201.py --start 0 --end 1000 --dataset cifar10 --measure dextr
python NAS_Bench_201.py --start 0 --end 1000 --dataset cifar100 --measure dextr
python NAS_Bench_201.py --start 0 --end 1000 --dataset ImageNet16-120 --measure dextr
```

2. NASLib benchmark entry scripts:
```bash
bash NASLib/scripts/cluster/benchmarks/run_nb101.sh correlation dextr
bash NASLib/scripts/cluster/benchmarks/run_nb301.sh correlation dextr
bash NASLib/scripts/cluster/benchmarks/run_tnb101.sh correlation dextr
```

3. DARTS search entry:
```bash
cd D:/PRO/essays/code_depots/Dextr/NASBench201
bash exp_scripts/zerocostpt_darts_pipeline.sh
```

## Dextr 用两路信号打分：
层特征的“逆条件数”表示收敛/泛化潜力；
  1/ntk
输出轨迹的外在曲率表示表达性；
  
最后做对数压缩后调和式融合。