---
title: "Per-Architecture Training-Free Metric Optimization for Neural Architecture Search"
method_name: "PO-NAS"
authors: [Anonymous Author(s)]
year: 2025
venue: "NeurIPS 2025 (under review submission)"
tags: [nas, training-free-nas, zero-cost-proxy, surrogate-model, evolutionary-search]
zotero_collection: ""
image_source: online
arxiv_html: ""
project_page: "https://anonymous.4open.science/r/PO-NAS-2953"
local_pdf: D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/PO-NAS/PO-NAS-2953
created: 2026-03-16
---

# 论文笔记：PO-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Per-Architecture Training-Free Metric Optimization for Neural Architecture Search |
| 状态 | 投稿 NeurIPS 2025（匿名投稿） |
| 代码链接 | https://anonymous.4open.science/r/PO-NAS-2953 |
| 本地 PDF | `D:/PRO/essays/papers/Per-Architecture Training-Free Metric Optimization for Neural Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/PO-NAS/PO-NAS-2953` |

## 一句话总结
> PO-NAS 通过代理模型学习**每个架构专属的多元免训练指标融合权重**，并结合贝叶斯优化 + 进化搜索，在有限真实训练预算下显著提升 NAS 排序质量。

## 核心贡献
1. 提出架构专属的指标融合方法（而非全局权重融合）：\(S(A;w_A)=\sum_i w_{A,i}\tilde Z_i(A)\)（Eq. 1）。
2. 构建编码器 + 指标预测器 + 交叉注意力权重生成器的代理结构，学习**架构条件化**的指标权重（Sec. 3.3-3.4）。
3. 引入基于成对排序损失的 BO 驱动循环，再耦合进化阶段进行更广泛探索（Sec. 3.2, 3.5）。
4. 在 NAS-Bench-201、DARTS/ImageNet、TransNAS-Bench-101 上给出强基准结果（Table 1-3）。

## 问题背景
### 目标问题
- 在直接训练式 NAS 成本过高时，如何提升免训练 NAS 的架构排序质量。

### 现有方法局限
- 单一零成本代理指标在不同任务间迁移效果不稳定。
- 现有混合方法通常优化**全局**指标组合，忽略架构级别的敏感性差异。

### 本文动机
- PO-NAS 利用有限真实反馈学习每个架构的指标权重，再用预测分数扩展搜索探索。

## 方法详解

### 1) 架构专属评分与优化目标
给定 K 个免训练指标：

$$
S(A; w_A) = \sum_{i=1}^{K} w_{A,i}\,\tilde Z_i(A)
$$

- \(\tilde Z_i\)：归一化指标值
- \(w_A\)：架构专属权重向量（L1 归一化）

权重学习通过最大化 [[Kendall's Tau]]**排序一致性**（score 排序 vs 真实性能）实现：

$$
w_A^{(t+1)} = \arg\max_{w_A} \tau\big(\{S(A;w_A^{(t)})\}_{A\in A_t},\{f(A)\}_{A\in A_t}\big)
$$

### 2) 编码器预训练
- 使用 2 层 [[Graph Attention Network]](d:\PRO\essays\论文笔记\_概念\Graph%20Attention%20Network.md) 将架构图编码为嵌入向量（Sec. 3.3, Fig. 2）。
- 节点掩码重建 + 指标预测联合预训练：

$$
\mathcal{L}_{recon} = \frac{1}{|V_m|}\sum_{v\in V_m}\|\hat x_v-x_v\|_2^2,
\quad
\mathcal{L}_{metric} = \frac{1}{K}\sum_{i=1}^{K}\|P_z^i(h_G)-Z_i(G)\|_2^2
$$

### 3) 带符号指标效应的代理评分
归一化后，PO-NAS 将权重拆分为正/负激活：

$$
\hat S = \sum_{i=1}^{K}\big(\hat w_i^+\hat Z_i + \hat w_i^-(1-\hat Z_i)\big)
$$

直觉：同时保留指标与性能之间的正/负相关行为。

代理优化使用三个损失函数：
1. **对齐损失**：成对 score/性能差距分布对齐（Eq. 6）
2. **相关损失**：\(\mathcal{L}_{corr}=1-\rho(\hat S,f)\)（Eq. 7）
3. **方向损失**：\(\mathcal{L}_{dir}=\mathbb{E}[\mathrm{ReLU}(-\Delta_{pred}\Delta_{true})]\)（Eq. 8）

### 4) 搜索循环与进化
- 主循环：初始化 → 预训练 → BO 阶段 → 可选进化阶段（Algorithm 1）
- 进化阶段：最短操作路径交叉 + 邻域遍历变异（Algorithm 2）
- 进化中的配对分数：

$$
S_{pair} = N\,\tilde S_{cost} + (1-N)\,\tilde S_{pre}
$$

- N 是探索权重：早期高探索，后期低探索

## 关键实验结果

### NAS-Bench-201（Table 1）
- PO-NAS：**94.12±0.22 / 73.51±0.00 / 46.71±0.12**（CIFAR-10 / CIFAR-100 / ImageNet-16-120）
- 搜索成本：3162 GPU 秒

### DARTS on ImageNet（Table 2）
- PO-NAS：**23.9 top-1 error / 7.1 top-5 error**，6.3M 参数，0.64 GPU days

### TransNAS-Bench-101（Table 3）
- Micro 和 Macro 设置均表现接近最佳

## 复现要点
1. 六个基础指标：grad_norm、snip、grasp、fisher、synflow、jacob_cov
2. 预训练包括架构掩码和 100 epoch 调度
3. BO 阶段使用损失阈值和差距阈值 \(T_{th}\)（默认约 0.1）
4. DARTS 设置使用 10k 初始架构，有限真实训练预算（CIFAR 25 个，ImageNet 10 个）

## 与代码实现的对照（本地 PO-NAS 仓库）
代码地址：
- 匿名仓库（论文给出的实现地址）：`https://anonymous.4open.science/r/PO-NAS-2953`
- 本地代码：`D:/PRO/essays/code_depots/PO-NAS/PO-NAS-2953`

本地代码路径：
`D:/PRO/essays/code_depots/PO-NAS/PO-NAS-2953`

关键文件（NAS-Bench-201 分支）：
- `NAS-Bench-201/genotype_to_pretrain_data_nb201.py`
- `NAS-Bench-201/pretrain_dataloader_nb201.py`
- `NAS-Bench-201/search_nb201.py`
- `NAS-Bench-201/att_network_nb201.py`

### 输入如何转化为特征（代码对照）
1. **架构字符串 -> 图特征（GNN 输入）**
   - 从架构字符串解析 `edges / edge_ops`；
   - 构造节点特征 `node_features`、边连接 `edge_index`、边特征 `edge_attr`；
   - 组装成 `torch_geometric.data.Data`。
```python
# NAS-Bench-201/genotype_to_pretrain_data_nb201.py
def parse_arch_to_graph(arch):
    ...
    node_features = torch.tensor(node_features, dtype=torch.float)
    edge_index = torch.tensor(edges, dtype=torch.long).t()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)
    data = Data(x=node_features, edge_index=edge_index, edge_attr=edge_attr)
    return data
```

2. **多 ZC 指标 -> 指标向量（metrics 输入）**
   - 对每个架构按 `metric_names` 取 `data_metrics[name][arch_id]`；
   - 叠成 `metrics_tensor`，和图特征一起保存为 dataset。
```python
# NAS-Bench-201/genotype_to_pretrain_data_nb201.py
metric_values = [data_metrics[name][int(item['i'])] for name in metric_names if name in item["logmeasures"]]
metrics_tensors.append(torch.tensor(metric_values, dtype=torch.float32))
...
dataset = {"arch": arch_graphs, "metrics": metrics_tensor, "arch_ids": ...}
```

3. **DataLoader 拼批次 -> 模型前向输入**
   - `arch` 用 `Batch.from_data_list` 组成图 batch；
   - `metrics` 用 `torch.stack` 组成矩阵；
   - 在线阶段额外构造 `metric_ids = torch.arange(len(metric_names))`。
```python
# NAS-Bench-201/pretrain_dataloader_nb201.py
def nas_collate_fn(batch):
    return {
        'arch': Batch.from_data_list([item['arch'] for item in batch]),
        'metrics': torch.stack([item['metrics'] for item in batch]),
        'arch_ids': torch.stack([item['arch_id'] for item in batch]),
    }
```
```python
# NAS-Bench-201/search_nb201.py
online_out = online_trainer.model(
    arch=arch_batch,
    metric_ids=metric_ids_batch,
    metrics=metrics_batch
)
```

4. **代理分数生成（架构专属权重）**
   - `arch_encoder` 把图编码成 `z_arch`；
   - `metric_embed(metric_ids)` + cross-attention + `weight_mlp` 产出每架构权重；
   - 正/负权重分别作用在 `metrics` 与 `(1-metrics)` 上得到最终 `score`。
```python
# NAS-Bench-201/att_network_nb201.py
weights = self.weight_mlp(fused_feat).squeeze(-1)
normalized_weights = weights / (weights.abs().sum(dim=1, keepdim=True) + 1e-8)
positive_weights = torch.relu(normalized_weights)
negative_weights = torch.relu(-normalized_weights)
metric_score = (positive_weights * metrics + negative_weights * (1.0 - metrics)).sum(dim=1, keepdim=True)
```

## 批判性思考

### 优点
1. 解决了指标融合的真实痛点：架构间异质性
2. 混合设计实用：廉价指标 + 稀疏真实训练 + 引导搜索
3. 进化模块为大搜索空间设计

### 局限
1. 代理稳定性仍是已知问题
2. 方法复杂度高于单代理流水线
3. 匿名代码链接目前无法公开访问

### 后续想法
1. 尝试簇级指标权重（论文自己提出的未来方向）
2. 测试对每个搜索空间/任务指标子集变化的鲁棒性

## 关联概念
- [Training-free NAS](d:\PRO\essays\论文笔记\_概念\Training-free%20NAS.md)
- [Zero-Cost Proxy](d:\PRO\essays\论文笔记\_概念\Zero-Cost%20Proxy.md)
- [Surrogate Predictor](d:\PRO\essays\论文笔记\_概念\Surrogate%20Predictor.md)
- [Kendall's Tau](d:\PRO\essays\论文笔记\_概念\Kendall's%20Tau.md)
- [Bayesian Optimization](d:\PRO\essays\论文笔记\_概念\Bayesian%20Optimization.md)
- [Evolutionary Neural Architecture Search](d:\PRO\essays\论文笔记\_概念\Evolutionary%20Neural%20Architecture%20Search.md)
- [Graph Attention Network](d:\PRO\essays\论文笔记\_概念\Graph%20Attention%20Network.md)
- [NAS-Bench-201](d:\PRO\essays\论文笔记\NAS-Bench-201.md)
