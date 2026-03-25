---
title: "Dextr_ch"
type: method
language: zh-CN
source_method_note: "[[Dextr]]"
source_paper: "Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature"
source_note: "[[Dextr]]"
authors: [Rohan Asthana, Joschua Conrad, Maurits Ortmanns, Vasileios Belagiannis]
year: 2025
venue: TMLR
tags: [nas-method, zh, zero-cost-proxy, training-free-nas, svd, curvature]
created: 2026-03-16
updated: 2026-03-25
---

# Dextr 中文条目

## 一句话总结
> Dextr 是一个无标签 zero-shot NAS 代理：用层特征的逆条件数刻画收敛/泛化，用输出外在曲率刻画表达性，再进行融合得到最终分数。

## 来源
- 论文: [Dextr: Zero-Shot Neural Architecture Search with Singular Value Decomposition and Extrinsic Curvature](https://openreview.net/forum?id=X0vPof5DVh)
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- 代码: https://github.com/rohanasthana/Dextr
- 英文方法笔记: [[Dextr]]
- 论文笔记: [[Dextr]]

## 适用场景
- 问题类型: 训练前架构排序与低成本 NAS 搜索。
- 前提假设: 可提取初始化网络的层特征，并能估计输出曲率。
- 数据形态: 无标签输入即可计算（论文强调单样本可行）。
- 规模与约束: 候选数量大、不能逐个完整训练时。
- 适用原因: 同时覆盖 C/G 与表达性，减少单侧偏置。

## 输入、输出与目标
- 输入: 初始化网络 `f`、无标签 batch `x`、轨迹参数 `theta`。
- 输出: Dextr 标量分数。
- 目标: 在低成本下逼近最终性能排序。

## 方法拆解

### 阶段 1: 层特征分数（SVD）
- 对每层输出特征做展平。
- 计算奇异值并取 `sigma_min/sigma_max`（逆条件数信号）。
- 跨层求和并做 `log(1+.)`。
- Source: Sec. 3.3.1-3.3.3, Eq. (8)

### 阶段 2: 曲率分数
- 构造轨迹输入 `g(theta)`。
- 计算输出对 `theta` 的一阶/二阶导并估计 `kappa(theta)`。
- 做 `log(1+kappa)`。
- Source: Sec. 3.2.2, Eq. (5), Appendix A.6

### 阶段 3: 融合
- 设
  - `a = log(1 + sum_l 1/c_l(X_phi))`
  - `b = log(1 + kappa(theta))`
- 最终 `Dextr = a*b/(a+b)`。
- Source: Sec. 3.3.3, Eq. (8)

## 代码对应与操作

### 1) 输入特征提取（层特征图 -> SVD）
文件：`D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`

```python
def forward_hook(module, data_input, data_output):
    fea = data_output[0].clone().detach()
    n = torch.tensor(fea.shape[0])
    fea = fea.reshape(n, -1)
    s = torch.linalg.svdvals(fea)
    svd = torch.min(s) / torch.max(s)
    svd[torch.isnan(svd)] = 0
    svd[torch.isinf(svd)] = 0
    result_list.append(svd)
```

### 2) 曲率特征提取（轨迹输入 -> 一阶/二阶导）
文件：`D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr_utils/no_free_lunch_architectures/length.py`

```python
theta = torch.linspace(0, 2 * np.pi, n_interp).cuda(non_blocking=True)
curve_input = ...
output = network(curve_input[_idx:_idx+batch_size])
v = autograd.grad(output[:, index].sum(), theta, create_graph=True, retain_graph=True)[0]
a = autograd.grad(v.sum(), theta, create_graph=True, retain_graph=True)[0]
kappa += (vv**(-3/2) * (vv * aa - va ** 2).sqrt()).sum().item()
```

### 3) 最终融合（Eq.8）
文件：`D:/PRO/essays/code_depots/Dextr/NASLib/naslib/predictors/pruners/measures/dextr.py`

```python
results = torch.log(1 + torch.sum(torch.tensor(result_list)))
curvature = torch.log(1 + torch.tensor(curvature))
dextr = results * curvature / (results + curvature)
```

### 4) 实操命令
1. NB201 相关性：
```bash
cd D:/PRO/essays/code_depots/Dextr/NASBench201/correlation
python NAS_Bench_201.py --start 0 --end 1000 --dataset cifar10 --measure dextr
python NAS_Bench_201.py --start 0 --end 1000 --dataset cifar100 --measure dextr
python NAS_Bench_201.py --start 0 --end 1000 --dataset ImageNet16-120 --measure dextr
```

2. NASLib benchmark 入口：
```bash
bash NASLib/scripts/cluster/benchmarks/run_nb101.sh correlation dextr
bash NASLib/scripts/cluster/benchmarks/run_nb301.sh correlation dextr
bash NASLib/scripts/cluster/benchmarks/run_tnb101.sh correlation dextr
```

3. DARTS 搜索入口：
```bash
cd D:/PRO/essays/code_depots/Dextr/NASBench201
bash exp_scripts/zerocostpt_darts_pipeline.sh
```

## 复杂度与效率
- 时间复杂度: 论文未给闭式。
- 空间复杂度: 论文未给闭式。
- 运行特征: 曲率估计是主要开销来源。

## 与相关方法关系
- 对比 [[MeCo]]: Dextr 增加了表达性曲率项。
- 对比 [[AZ-NAS]]: Dextr 是单代理融合，AZ-NAS 是多代理组装。
- 主要优势: 无标签、可解释、实现直接。
- 主要代价: 曲率计算偏重，部分空间可能不稳定。

## 参考链接
- HTML: https://openreview.net/forum?id=X0vPof5DVh
- 代码: https://github.com/rohanasthana/Dextr
- 本地实现: D:/PRO/essays/code_depots/Dextr


Dextr 的本质是把两类信号融合：  
    收敛/泛化项 a=$log(1 + Σ_l 1/c_l(X))$，表达性项b = $log(1 + κ)$，最终 $Dextr = a*b/(a+b)$（Eq. 8）。
    收敛/泛化项：给网络所有模块注册 forward_hook，再前向 net(x)
    用各层特征的 σ_min/σ_max（即逆条件数）来近似$∑_l 1/c_l(X_ϕ)$ 
        每层取输出特征 fea，展平后做 svdvals，
        计算层分数$s_l=σ_min/σ_max$（逆条件数信号）
        汇总成 result_list。
    曲率（表达性）：调用 get_extrinsic_curvature_opt(...) 估计曲率 κ
        在 length.py 中构造轨迹输入 g(θ)，
        计算输出对 θ 的一阶导 v 和二阶导 a，
        累加曲率项（基于 v,a 的经典曲率表达式）得到 κ
