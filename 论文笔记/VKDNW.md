---
title: "Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights"
method_name: "VKDNW"
authors: [Ondrej Tybl, Lukas Neumann]
year: 2025
venue: arXiv
tags: [NAS, training-free-nas, zero-cost-proxy, fisher-information]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2502.04975v1
local_pdf: D:/PRO/essays/papers/Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights.pdf
created: 2026-03-14
---

# 论文笔记：VKDNW

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights |
| arXiv | https://arxiv.org/abs/2502.04975 |
| Code | https://github.com/ondratybl/VKDNW |
| 本地 PDF | `D:/PRO/essays/papers/Training-free Neural Architecture Search through Variance of Knowledge of Deep Network Weights.pdf` |
| 本地代码 | 未完成归档（2026-03-14 连接 GitHub 443 超时） |

## 一句话总结

> 本文提出基于 [[Fisher Information Matrix]] 的零训练 NAS 代理分数 VKDNW，用参数估计不确定性的“谱熵”来排序架构，并提出 [[Normalized Discounted Cumulative Gain]] 更贴近 NAS 目标的评测方式。

## 核心贡献

1. 提出可在大模型上稳定估计经验 FIM 谱的实现方案（Sec. II-B, Eq. (8)-(10)）。
2. 提出训练前可计算的代理分数 `VKDNW`，并证明其与模型大小信息相对正交（Sec. II-C, Fig. 3/4, Table IV）。
3. 提出 TF-NAS 评测指标 `nDCG`，强调“是否能把好模型排到前面”，补足 KT/SPR 的不足（Sec. III, Eq. (14), Fig. 2）。

## 问题背景

### 要解决的问题

传统 NAS 需要对海量候选架构训练后再评估，成本极高。TF-NAS 希望用 cheap proxy 替代完整训练。

### 现有方法局限

- 单一 proxy 常受模型规模偏置影响，可能只是“偏爱大模型”。
- 常用评测（Kendall tau、Spearman rho）对“头部架构识别”不敏感。

### 本文动机

作者从 [[Cramer-Rao Bound]] 出发，把“权重可估计性/不确定性结构”转成可计算统计量，并把 NAS 的评价重点放回“top 架构检索能力”。

## 方法详解

### 1) Fisher 信息建模

- 把分类网络训练视为最大似然估计，定义 FIM（Eq. (2)）。
- 用 Cramer-Rao 下界解释：FIM 谱反映参数估计难度与方向不平衡性（Sec. II-A, Eq. (3) 及后续讨论）。

### 2) 经验 FIM 的可计算实现

- 经验 FIM 定义见 Eq. (8)。
- 采用分解形式避免数值不稳定，得到 `F_hat = (1/N) sum A_n^T A_n`（Eq. (9)-(10)）。
- 只采样少量代表参数（每层少量权重）降低维度并提升稳定性。
- 使用模型预测分布而非真实标签构造经验 FIM，因此可用随机输入（Sec. II-B）。

### 3) VKDNW 分数

- 从 FIM 谱取 decile（去掉极小/极大边界特征值），归一化后做熵：Eq. (11)。
- 直觉：谱越均衡，说明不同参数方向的不确定性更均匀，训练可估计性更好。

### 4) 用于排序的 size-aware 形式

- 单分数排序：`VKDNWsingle(f) = N_layers(f) + VKDNW(f)`（Eq. (12)）。
- 作用：先按规模粗分组，再在组内用 VKDNW 精排。

### 5) 评测指标与聚合

- 新指标 `nDCG_P`（Eq. (14)）更关注 top-P 的检索质量。
- 非线性聚合：`rank_agg = log(prod_j rank_j)`（Eq. (15)），聚合 V/J/E/T/F 五类分数（Sec. V-A）。
- 还给出 model-driven 聚合（随机森林等）作为补充。

## 关键公式

### Eq. (2): Fisher Information Matrix

$$
F(\theta)=\mathbb{E}[\nabla_\theta \sigma_\theta(c|x)\,\nabla_\theta \sigma_\theta(c|x)^T]
$$

含义：衡量参数扰动对预测分布的敏感性与信息量。

### Eq. (11): VKDNW 熵分数

$$
\text{VKDNW}(f)=-\sum_{k=1}^{9} \tilde{\lambda}_k\log \tilde{\lambda}_k,
\quad \tilde{\lambda}_k=\frac{\lambda_k}{\sum_{j=1}^9 \lambda_j}
$$

含义：用归一化特征值熵刻画“权重不确定性分布的均衡性”。

### Eq. (12): 单代理排序

$$
\text{VKDNW}_{single}(f)=\mathcal{N}(f)+\text{VKDNW}(f)
$$

其中 `N(f)` 是可训练层数代理。

### Eq. (14): nDCG

$$
\text{nDCG}_P=\frac{1}{Z}\sum_{j=1}^{P}\frac{2^{acc_{k_j}}-1}{\log_2(1+j)}
$$

含义：更重视高排名位置上的高精度架构。

## 关键图表

### Figure 1

- 在 ImageNet16-120 上，VKDNW 系列在 nDCG 上领先，且 KT/SPR 也保持竞争力。

### Figure 2

- 用 toy 例子说明：KT/SPR 可能认为某排序“相关性更高”，但 nDCG 能识别其 top 排名损坏。

### Figure 3 / Figure 4

- 展示 VKDNW 与模型规模（可训练层数或参数量）相关性更低，支持“正交信息”论点。

### Table I (NAS-Bench-201)

- `VKDNWsingle` 在 ImageNet16-120 上 `KT/SPR/nDCG = 0.622/0.814/0.608`。
- `VKDNWagg` 进一步提升到 `0.743/0.906/0.664`，优于 AZ-NAS 的 `0.673/0.859/0.534`。

### Table II (MobileNetV2 search)

- 在约 450M FLOPs 约束下，`VKDNWagg` 得到 `78.8` Top-1，优于 AZ-NAS 的 `78.6`，搜索成本同为 `0.4 GPU days`（最终训练仍昂贵）。

### Table V / VII / VIII

- 随机输入与真实输入表现接近；批量大小变化影响小。
- FIM 维度和层内采样策略有一定鲁棒区间（作者默认用 128 层采样与 batch size 64）。

## 实验设置与实现细节

- 搜索空间：NAS-Bench-201、MobileNetV2（Sec. V）。
- NAS-Bench-201 使用 9,445 个 unique 结构作为主报告（另给全 15,625 结果于补充）。
- 分数计算常用 64 张随机输入图像。
- model-driven 聚合在 1024 个架构上训练随机森林。
- MobileNetV2 实验在进化搜索中跑 100,000 次评估，保留 top 1024，再训练最终模型（480 epoch, SGD + cosine）。

## 与代码实现的对照

- 论文给出官方仓库：https://github.com/ondratybl/VKDNW。
- 本次尝试本地归档时，环境对 GitHub 连接超时（2026-03-14），因此未能完成代码级核查。
- 当前方法与实现细节解读以论文正文/补充文本为主。

## 批判性思考

### 优点

1. 理论动机明确：从 FIM 与统计估计理论推导 proxy，而非纯经验组合。
2. 评测视角改进到“top 架构检索”，更贴近 NAS 实际使用。
3. 在多个数据集和两个搜索空间上给出一致改进。

### 局限

1. proxy 中仍显式叠加了规模项 `N_layers`，在不同搜索空间的泛化边界仍需更多验证。
2. model-driven 聚合需要已知精度样本训练，降低了“完全零成本”属性。
3. 关键结论依赖补充材料中的细节（如采样稳定性），主文中不够展开。

### 可复现性评估

- [x] 论文公开
- [x] 官方代码链接公开
- [ ] 本地代码归档完成（本次因网络阻塞失败）
- [x] 公式与实验流程可追踪

## 关联概念

- [[Neural Architecture Search]]
- [[Zero-Cost Proxy]]
- [[Fisher Information Matrix]]
- [[Cramer-Rao Bound]]
- [[Normalized Discounted Cumulative Gain]]
- [[NAS-Bench-201]]

## 代码分析（基于本地 `VKDNW-master`）

代码路径：
`D:/PRO/essays/code_depots/VKDNW-master/VKDNW-master/NB201/ZeroShotProxy/compute_vkdnw_score.py`

这份实现里，VKDNW 实际返回两个代理（两个字段）：

1. `vkdnw_dim`
2. `vkdnw_entropy`

### 1) `vkdnw_dim` 怎么算

对应代码（Ln 248）：

```python
info['vkdnw_dim'] = float(len(list(model.named_parameters())))
```

含义：
- 它统计的是 `model.named_parameters()` 的条目数量（参数张量个数），不是参数总数，也不是 FLOPs。
- 这在实现里充当“结构/规模维度”的 size proxy。

### 2) `vkdnw_entropy` 怎么算

`vkdnw_entropy` 的上游计算链路是：

#### Step A: 初始化 + 输入准备（Ln 229-236）

```python
init_model(model, init_method)

# 来自随机化 或 来自trainloader
input_ = torch.randn(...) 
input_ = next(iter(trainloader))[0].to(device)

fisher_prob = get_fisher(model, input_, use_logits=False,
                         params_grad_len=params_grad_len, p=p)
```

要点：
- 默认会重置模型初始化（`init_model`）。
- 可用随机输入（`trainloader=None`）或真实数据输入。
- 核心矩阵是 `fisher_prob`。

#### Step B: 构造 Fisher 近似（`get_fisher`, Ln 126-140）

```python
jacobian = get_jacobian_index(model, input, p, params_grad_len)
if not use_logits:
    jacobian = torch.matmul(cholesky_covariance(model(input)[1]), jacobian)
fisher = mean( J^T J )
```

要点：
- 先拿到关于“选中参数子集”的 Jacobian。
- `use_logits=False` 时会乘上 `cholesky_covariance(logits)`，把 softmax 概率协方差信息合进来。
- 最终 Fisher 近似是批平均的 `J^T J`。

#### Step C: Jacobian 子集怎么取（`get_jacobian_index`, Ln 175-212）

```python
indices = [linspace(..., steps=int(p_count)) for each parameter tensor]
params_grad = {k: v.flatten()[param_idx] ...}
params_grad = first params_grad_len entries
jacobian_dict = vmap(jacrev(compute_prediction))(input)
ret = cat(flatten(each jacobian block), dim=2)
```

要点：
- 不是对全部参数求 Jacobian，而是每个参数张量采样 `p_count` 个索引后再拼接。
- 再用 `params_grad_len` 截断参与 Jacobian 的参数块数量，控制开销。
- `compute_prediction` 用 `functional_call` 把“被采样的参数值”写回模型，再取 `model(...)[1]`（logits）作为输出。

#### Step D: 从 Fisher 到谱熵（Ln 239-253）

```python
lambdas = torch.svd(fisher_prob).S
quantiles = torch.quantile(lambdas, torch.arange(0.1, 1., 0.1))
temp = quantiles / (L1_norm(quantiles) + 1e-10)
vkdnw_entropy = -(temp * log(temp + 1e-10)).sum()
```

要点：
- 用 `SVD` 的奇异值 `S` 作为谱值（对称半正定矩阵下与特征值一致）。
- 取 0.1~0.9 的分位数（9 个代表值），做 L1 归一化后计算 Shannon entropy。
- 这就是实现中的 `vkdnw_entropy`。

### 3) 两个代理在这份代码里的关系

- `compute_nas_score` 最后只返回：

```python
{
  'vkdnw_dim': ...,
  'vkdnw_entropy': ...
}
```

- 也就是说：此文件只负责“算两个原始 proxy”，不在文件内做最终聚合。
- 在 `NB201/tss_supernet(gradsign).ipynb` 的评测单元里，会把 `results` 里的每个 key 当作一个可排序指标单独评估；AZ-NAS 的 `log-rank` 聚合只在 `az_nas` 分支里显式写出。

### 4) 和论文中 `VKDNWsingle = size + entropy` 的对齐

论文表达是“size proxy + VKDNW entropy”。
本地实现对应为：

- size proxy: `vkdnw_dim`
- entropy proxy: `vkdnw_entropy`

如果你要在实验脚本里显式构造 `VKDNWsingle`，可在收集完 `results` 后加一条组合逻辑（例如按 rank 相加或按原值相加，取决于你的复现实验设定）。


#### 细节
model.named_parameters()
每一项是 (name, tensor)，name 形如：
- stem.0.weight
- cells.0.edges.1<-0.2.op.1.weight
- cells.0.edges.1<-0.2.op.2.weight
- cells.0.edges.1<-0.2.op.2.bias
- cells.3.conv_a.op.1.weight
- classifier.weight
vkdnw_dim 统计的是**条目数**，不是参数总量。

ReLUConvBN 里 op 是 nn.Sequential(ReLU, Conv2d, BN)，所以常见：
    .op.1.weight = Conv2d 权重
    .op.2.weight/.bias = BN 参数（仅 affine=True 时有）  
	定义在 cell_operations.py

**NB201 supernet**（NAS201SearchCell）中，参数名里会有：
    edges.{i<-j}.{op_idx}....  
        因为每条边存了一个 ModuleList 候选 op，op_idx 是候选序号。  
        定义在 [search_cells.py:27](https://file+.vscode-resource.vscode-cdn.net/c%3A/Users/kknd/.trae/extensions/openai.chatgpt-26.311.21342-win32-x64/webview/) 和 [search_cells.py:44](https://file+.vscode-resource.vscode-cdn.net/c%3A/Users/kknd/.trae/extensions/openai.chatgpt-26.311.21342-win32-x64/webview/)


NB201 候选 op 顺序通常是：[none, skip_connect, nor_conv_1x1, nor_conv_3x3, avg_pool_3x3]，所以例如 .2 常对应 nor_conv_1x1
```
stem.0.weight
stem.1.weight
stem.1.bias

cells.0.edges.1<-0.2.op.1.weight
cells.0.edges.1<-0.2.op.1.bias
cells.0.edges.1<-0.3.op.1.weight
cells.0.edges.1<-0.3.op.1.bias

cells.0.edges.2<-1.2.op.1.weight
cells.0.edges.2<-1.2.op.1.bias
cells.0.edges.3<-2.3.op.1.weight
cells.0.edges.3<-2.3.op.1.bias

cells.5.conv_a.op.1.weight
cells.5.conv_a.op.2.weight
cells.5.conv_a.op.2.bias
cells.5.conv_b.op.1.weight
cells.5.conv_b.op.2.weight
cells.5.conv_b.op.2.bias
cells.5.downsample.1.weight

lastact.0.weight
lastact.0.bias
classifier.weight
classifier.bias
```
notebook 里 affine=bool(xargs.affine)，
	默认 --affine 0，所以 search-cell 里很多 BN 不带 weight/bias；
	如果改成 --affine 1，会额外出现不少 ...op.2.weight/.bias。

