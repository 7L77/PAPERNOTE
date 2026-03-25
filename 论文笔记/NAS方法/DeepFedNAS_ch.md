---
title: "DeepFedNAS_ch"
type: method
language: zh-CN
source_method_note: "[[DeepFedNAS]]"
source_paper: "Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training"
source_note: "[[DeepFedNAS]]"
authors: [Bostan Khan, Masoud Daneshtalab]
year: 2026
venue: arXiv
tags: [nas-method, zh, federated-nas, predictor-free-search, hardware-aware]
created: 2026-03-23
updated: 2026-03-23
---

# DeepFedNAS 中文条目

## 一句话总结

> DeepFedNAS 用 Pareto 路径缓存引导联邦 supernet 训练，并在部署时直接最大化结构 fitness 来搜索子网，从而跳过高成本 accuracy predictor 流程。

## 来源

- 英文方法笔记: [[DeepFedNAS]]
- 论文: https://arxiv.org/abs/2601.15127
- HTML: https://arxiv.org/html/2601.15127v2
- 代码: https://github.com/bostankhan6/DeepFedNAS
- 本地代码: `D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training`

## 适用场景

- 问题类型: [[Federated Neural Architecture Search]]，需要一套 supernet 适配多客户端、多硬件目标。
- 前提假设: 路径引导训练后，fitness 与真实精度排名保持较强相关。
- 数据形态: 联邦 non-IID 图像分类（文中为 CIFAR-10/100、CINIC-10）。
- 规模与约束: 有通信限制且部署侧存在 MAC/参数/延迟预算。
- 适用原因: 在保持精度的同时显著降低后处理搜索成本。

## 不适用或高风险场景

- 仅 Transformer 搜索空间且尚未迁移此框架。
- 无法承担任何离线 cache 生成开销的超快迭代场景。
- supernet 训练后无法建立稳定的 fitness-accuracy 排序相关性。

## 输入、输出与目标

- 输入: 搜索空间 \(S\)、联邦客户端数据 \(\{D_k\}\)、架构编码 \(A=(d,e,w)\)、资源约束。
- 输出: 训练后的 supernet \(W^\*\) 与部署子网 \(A^\*_{deploy}\)。
- 优化目标: 用统一 fitness 同时提升 supernet 训练质量和部署搜索效率。
- 核心假设: 高质量 Pareto curriculum 能改善共享权重，使 \(F(A)\) 可作为部署搜索代理信号。

## 方法拆解

### 阶段 1：离线 Pareto 缓存生成

- 构建多目标 fitness \(F(A)\)：熵项 + effectiveness + 深度惩罚 + 通道单调惩罚。
- 在多个 MAC 预算上分别运行 GA，得到 Pareto 路径缓存。
- Source: Sec. III-C, Sec. III-D, Eq. (5)-(10), Fig. 2

### 阶段 2：联邦 Pareto 引导 supernet 训练

- 用缓存替代随机 sandwich 采样：
  - 边界客户端训练最小/最大子网；
  - 其他客户端从缓存中抽样。
- 服务器端用 overlap-aware 聚合处理稀疏参数更新。
- Source: Sec. III-E, Alg. 1, Eq. (2), Eq. (11)

### 阶段 3：Predictor-Free 部署搜索

- 不再训练 accuracy surrogate，直接在约束下优化 \(F(A)\) 搜索部署子网。
- 文中通过相关性分析验证可行性。
- Source: Sec. III-F, Eq. (12), Fig. 6, Table V

### 阶段 4：硬件约束扩展

- 参数上界可作为硬约束。
- 延迟可作为硬约束或软惩罚项（结合轻量 LPM）。
- Source: Sec. III-G, Eq. (13)-(17)

## 伪代码
```text
Algorithm: DeepFedNAS
Input: 搜索空间 S, 客户端 K, 通信轮次 T, 预算集合 B={B1...BN}, 硬件约束 C_hw
Output: 训练后 supernet W*, 部署子网 A*_deploy

1. 对每个预算 Bi 执行 GA:
   A*i = argmax_A F(A) s.t. MACs(A) <= Bi
   形成缓存 C={A*1...A*N}
   Source: Sec. III-D, Eq. (10)

2. 每一轮联邦训练:
   2.1 选取参与客户端 Kt
       Source: Alg. 1
   2.2 按缓存规则分配子网 Ak:
       - 边界客户端分配 A_min / A_max
       - 其他客户端从 C 抽样
       Source: Eq. (11), Alg. 1
   2.3 客户端本地训练并回传更新
       Source: Alg. 1
   2.4 服务器执行 overlap-aware 聚合
       Source: Eq. (2), Alg. 1

3. 训练后部署搜索:
   A*_deploy = argmax_A F_deploy(A)
   s.t. MAC/Params/Latency 约束
   Source: Sec. III-F/G, Eq. (12), Eq. (16)-(17)
```

## 训练流程

1. 定义 supernet 配置（`configs/supernets/4-stage-supernet-deepfednas.json`）。
2. 运行缓存生成脚本（`scripts/cache_generation/run_subnet_cache_generation.sh`）。
3. 训练时使用 `--subnet_dist_type TS_optimal_path` 并指定 `--subnet_cache_path`。
4. 采样逻辑在 `src/deepfednas/Server/base_server_model.py`。
5. 聚合阶段使用 overlap-aware 参数掩码加权。

Sources:

- Sec. III-B to III-E, Alg. 1
- Code: `scripts/cache_generation/run_subnet_cache_generation.sh`, `experiments/02_deepfednas/cifar10.sh`, `src/deepfednas/Server/base_server_model.py`

## 推理/部署流程

1. 指定部署预算（MAC 必需，参数/延迟可选）。
2. 运行 `scripts/evaluation/find_subnet_for_macs.py` 做 GA 搜索。
3. 若需要延迟约束，加载 LPM 并加入硬/软约束。
4. 输出最优架构配置并导出子网部署。

Sources:

- Sec. III-F/G, Eq. (12)-(17)
- Code: `scripts/evaluation/find_subnet_for_macs.py`, `src/deepfednas/nas/deepfednas_fitness_maximizer.py`

## 复杂度与效率

- 时间开销: 主要是联邦训练与 GA；后处理搜索不再受 accuracy predictor 数据构造主导。
- 空间开销: supernet 参数 + 缓存子网 + 可选 LPM。
- 论文报告:
  - cache 生成约 20 分钟（60 子网）；
  - 单目标搜索约 20 秒；
  - 总后处理流程约 20.33 分钟，对比基线约 20.65 小时。
- 扩展性: 在需要频繁按预算重部署的场景收益更大。

## 实现备注

- fitness 实现在 `src/deepfednas/nas/deepfednas_fitness_maximizer.py`。
- cache 采样器在 `src/deepfednas/Server/base_server_model.py`（`TS_optimal_path`）。
- 部署 GA 入口在 `scripts/evaluation/find_subnet_for_macs.py`。
- 训练超参入口在 `experiments/02_deepfednas/*.sh`。
- 代码层面关键细节:
  1. cache 先按 MAC 排序，首尾自动作为边界子网；
  2. 中间客户端是从 cache 随机采样；
  3. fitness 可选叠加延迟软目标。

## 与相关方法关系

- 对比 [[SuperFedNAS]]: 保留 supernet 思路，但把随机采样替换为 Pareto curriculum。
- 对比 predictor-based 搜索管线: 去掉高成本 subnet-accuracy 数据集构造与 predictor 训练。
- 主要优势: 搜索效率提升显著，同时保持准确率增益。
- 主要代价: 依赖 fitness 设计和训练后相关性成立。

## 证据与可溯源性

- 关键图: Fig. 1, Fig. 2, Fig. 3/4, Fig. 6
- 关键表: Table II/III/IV, Table V, Table VI
- 关键公式: Eq. (2), Eq. (5)-(12), Eq. (16)-(17)
- 关键算法: Algorithm 1

## 参考链接

- arXiv: https://arxiv.org/abs/2601.15127
- HTML: https://arxiv.org/html/2601.15127v2
- 代码: https://github.com/bostankhan6/DeepFedNAS
- 本地实现: D:/PRO/essays/code_depots/Predictor-Free and Hardware-Aware Federated Neural Architecture Search via Pareto-Guided Supernet Training
