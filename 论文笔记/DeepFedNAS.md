---
title: "Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training"
method_name: "DeepFedNAS"
authors: [Bostan Khan, Masoud Daneshtalab]
year: 2026
venue: arXiv
tags: [federated-learning, nas, hardware-aware-nas, predictor-free, supernet]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2601.15127v2
local_pdf: D:/PRO/essays/papers/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training.pdf
local_code: D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training
created: 2026-03-23
---

# 论文笔记：DeepFedNAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training |
| arXiv | https://arxiv.org/abs/2601.15127 |
| HTML | https://arxiv.org/html/2601.15127v2 |
| 发布版本 | arXiv v2, 2026-01-28 |
| 官方代码 | https://github.com/bostankhan6/DeepFedNAS |
| 本地 PDF | `D:/PRO/essays/papers/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training` |

## 一句话总结
> DeepFedNAS 用 [[Pareto-Guided Supernet Training]] 替换随机子网训练，并用结构 fitness 直接做 [[Predictor-Free Search]]，把 FedNAS 的后处理搜索从约 20.65 小时压到约 20.33 分钟（约 61x 加速）。

## 核心贡献
1. 提出统一多目标 fitness \(F(A)\)，把熵、effectiveness、深度均衡、通道单调性放在同一可搜索目标里（Sec. III-C, Eq. 5-9）。
2. 提出离线 Pareto 路径缓存 + 在线 curriculum 训练，替代 SuperFedNAS 的随机 sampling（Sec. III-D/E, Alg. 1, Eq. 11）。
3. 提出 predictor-free 部署搜索：不再训练 accuracy surrogate，直接优化 \(F(A)\)（Sec. III-F, Eq. 12）。
4. 支持硬件约束部署：参数上界 + 轻量延迟预测器（LPM）用于硬/软延迟约束（Sec. III-G, Eq. 13-17）。
5. 在 CIFAR-10/CIFAR-100/CINIC-10、不同 non-IID 强度与不同 client 参与率下均优于基线，并显著提速（Sec. IV）。

## 问题背景
### 要解决的问题
- [[Federated Neural Architecture Search]] 里，supernet 训练常靠随机子网采样，梯度噪声大、共享权重质量受限。
- 训练后子网搜索通常需要额外 accuracy predictor 数据采样和训练，流程成本很高。

### 现有方法局限
- SuperFedNAS 将训练和搜索解耦后，仍有两个瓶颈：
  1) 训练阶段随机采样不够“有信息”；
  2) 部署搜索还依赖昂贵 predictor pipeline。

### 本文动机
- 用可计算的结构 fitness 提供“训练前/训练中/部署时”一致信号：
  - 训练前构造高质量 Pareto cache；
  - 训练中按 cache 进行 guided sampling；
  - 部署时直接以 fitness 搜索子网。

## 方法详解
### Phase 1：离线 Pareto cache 生成
- 搜索空间基于 generic ResNet supernet，架构编码为 \(A=(d,e,w)\)（Eq. 3-4）。
- 在一组预算 \(B_1...B_N\) 上分别运行 GA，得到 \(N\) 个高 fitness 子网，形成 “Pareto path cache”（Sec. III-D, Eq. 10）。
- 文中默认 \(N=60\)，图 5 显示其在拟合质量与多样性上是稳定折中。

### Phase 2：Federated Pareto Optimal Supernet Training
- 客户端采样遵循“边界 + 路径随机”策略：
  - 少采样的客户端优先分配最小/最大边界子网；
  - 其他客户端从 cache 中抽样（Eq. 11, Alg. 1）。
- 服务器聚合使用 [[Overlap-Aware Aggregation]]（Eq. 2），按参数被激活频次做掩码加权，避免未参与参数被错误平均。

### Phase 3：Predictor-Free 部署搜索
- 假设：经过路径引导训练后，fitness 与精度排序强相关（Eq. 12）。
- 因此部署搜索可直接在约束下最大化 \(F(A)\)，无需单独 accuracy predictor。
- 硬件约束支持：
  - 参数硬约束 \(Params(A)\le M\)（Eq. 13）；
  - 延迟预算硬约束或软惩罚（Eq. 16-17）。

## 关键公式
### Eq. (1)：联邦 supernet 目标
\[
\min_W \mathbb{E}_{A\in S}\left[\sum_{k=1}^K \frac{|D_k|}{|D|}L_k(G(W,A))\right]
\]
含义：共享权重 \(W\) 要对搜索空间中大量子网都可用，并在各客户端数据上有效。

### Eq. (2)：Overlap-aware 聚合
\[
\Delta_\theta = \frac{\beta_t I_{max}(\theta)\Delta_{k_{max}}(\theta) + (1-\beta_t)\sum_{k\in K'} I_k(\theta)\Delta_k(\theta)}{\beta_t I_{max}(\theta) + (1-\beta_t)\sum_{k\in K'} I_k(\theta)+\epsilon}
\]
含义：只对被激活的参数统计贡献，缓解子网参数重叠不一致带来的聚合偏差。

### Eq. (5)：统一 fitness
\[
F(A)=\sum_{j=1}^S \alpha_j H_j(A) - \omega Q(A) + \lambda\rho(A) - \gamma V(A),\ \text{s.t.}\ \rho(A)\le \rho_0
\]
- \(H_j\)：stage 熵项（表达能力）；
- \(Q\)：深度方差惩罚；
- \(\rho\)：effectiveness；
- \(V\)：通道非单调惩罚。

### Eq. (10)：预算条件下的离线搜索
\[
A_i^* = \arg\max_{A\in S} F(A),\ \text{s.t.}\ MACs(A)\le B_i
\]

### Eq. (11)：客户端子网分配
\[
A_k = S(k,C)=
\begin{cases}
A_{min}, & k\in K_{t,min}\\
A_{max}, & k\in K_{t,max}\\
\text{Uniform}(C), & \text{otherwise}
\end{cases}
\]

### Eq. (12)：predictor-free 假设
\[
\arg\max_{A\in S}\mathbb{E}[Acc(A,W^*)]\approx \arg\max_{A\in S}F(A)
\]

### Eq. (16)-(17)：延迟感知部署
\[
F_{deploy}(A)=F(A)-\delta\cdot L_{pred}(A,\text{Device})
\]
\[
A_{deploy}^*=\arg\max_{A\in S}F_{deploy}(A)\ \text{s.t.}\ MACs/Params/Latency\ \text{constraints}
\]

## 关键图表与结论
### Figure 1（总体流程）
- 三段式：离线 cache 搜索 -> 联邦 supernet 训练 -> predictor-free 部署搜索。

### Figure 2（cache vs random）
- Pareto path 在同等 MACs 下能找到更高 fitness 子网，支持“训练 curriculum 要有质量”这一动机。

### Table I（搜索空间）
- DeepFedNAS 搜索空间覆盖更宽：最小 MACs 7.55M（基线约 458.97M），最大 3403.37M。
- 为公平对比，主实验报告集中在与基线重叠区间。

### Table II（主结果）
- 在 CIFAR-10/100/CINIC-10 各 MAC 档位均优于 SuperFedNAS。
- 典型结果：CIFAR-100 在 0.95-1.45B MACs 档位提升约 +1.21%（62.87 vs 61.66）。

### Table III/IV（鲁棒性与通信效率）
- non-IID 更强（\(\alpha\) 更小）时，优势更明显；
- client 参与率降低时仍保持领先，说明更适配受限通信场景。

### Table V（搜索成本）
- 基线：构造 predictor 数据约 20.65h；
- DeepFedNAS：cache 约 20 分钟 + 单次搜索约 20 秒，总流程约 20.33 分钟；
- 报告约 61x 加速。

### Table VI + Figure 6（机制验证）
- 加入 \(\rho,Q,V\) 后精度与稳定性均提升（方差显著下降）。
- fitness 与真实精度相关性较强（Spearman 0.764, Kendall 0.591），支撑 predictor-free 假设。

## 代码对齐（Code-first）
### 与论文一致的关键实现
- `src/deepfednas/nas/deepfednas_fitness_maximizer.py`
  - 实现 fitness 各项、\(\rho\) 约束、GA 搜索、可选 latency 软/硬约束。
- `src/deepfednas/Server/base_server_model.py`
  - `TS_optimal_path` 采样器：边界子网 + cache 抽样。
- `scripts/cache_generation/run_subnet_cache_generation.sh`
  - 直接生成 60 子网缓存。
- `scripts/evaluation/find_subnet_for_macs.py`
  - 部署阶段按 MAC 预算做 predictor-free GA 搜索。

### 读代码得到的实现细节
1. cache 在加载后会按 MACs 排序，最小/最大子网自动由首尾项给定。
2. 中间客户端是从 cache 随机抽样，而不是固定轮换路径。
3. latency predictor 是可选组件；不用时就是纯 predictor-free（针对 accuracy surrogate）。

## 批判性思考
### 优点
1. 把“训练策略”和“部署搜索策略”统一到同一 fitness，方法闭环完整。
2. 对比设置透明，尤其是非 IID 与 client participation 两组结果很有说服力。
3. 工程可落地性强，官方仓库给出 cache 生成、训练与搜索的可运行流程。

### 局限
1. 主要验证在 ResNet 风格 CNN 空间；Transformer/FM 场景仍待验证（论文也明确承认）。
2. fitness 权重仍依赖调参，跨任务迁移时可能需要重新标定。
3. predictor-free 依赖“fitness-accuracy 相关性成立”，在极端噪声或超低数据时可能不稳。

### 对你当前方向的启发（NAS / ZCP）
1. 可以先把“采样策略”从随机改成由 proxy 生成的 curriculum，即使不改主训练框架也会有收益。
2. 对需要频繁重部署的场景，优先优化“后处理搜索总时长”，收益可能大于追求 predictor 的微小精度提升。
3. 若你已有硬件约束任务，可把 latency 作为软目标并保留硬约束，避免只优化单一 MACs。

## 关联概念
- [[Federated Neural Architecture Search]]
- [[Pareto-Guided Supernet Training]]
- [[Predictor-Free Search]]
- [[Overlap-Aware Aggregation]]
- [[Super-network]]
- [[Entropy]]
- [[Genetic Algorithm]]
- [[Hardware-aware NAS]]
- [[Pareto Front]]
- [[Spearman's Rank Correlation]]
- [[Kendall's Tau]]

## 速查卡片
> [!summary] DeepFedNAS
> - 核心问题: FedNAS 训练随机采样低效 + 部署前 predictor pipeline 太贵
> - 核心方法: Pareto path curriculum + predictor-free fitness search
> - 关键结果: CIFAR-100 最高档到 63.20%，并将搜索流程加速约 61x
> - 工程结论: 对多硬件部署和非 IID 联邦场景，实用价值很高
