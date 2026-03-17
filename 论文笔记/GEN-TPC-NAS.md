---
title: "Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers"
method_name: "GEN-TPC-NAS"
authors: [Jun-Hua Ko, Tzi-Dar Chiueh]
year: 2025
venue: IJCNN
tags: [NAS, zero-shot-nas, self-supervised-learning, transformer]
zotero_collection: ""
image_source: online
arxiv_html: https://ieeexplore.ieee.org/document/11229357
local_pdf: D:/PRO/essays/papers/Generalization-Aware_Zero-Shot_Neural_Architecture_Search_for_Self-Supervised_Transformers.pdf
created: 2026-03-17
---

# 论文笔记：GEN-TPC-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Generalization-Aware Zero-Shot Neural Architecture Search for Self-Supervised Transformers |
| DOI | https://doi.org/10.1109/IJCNN64981.2025.11229357 |
| 会议 | IJCNN 2025 |
| 任务 | Transformer 架构搜索（CV + NLP） |
| 本地 PDF | `D:/PRO/essays/papers/Generalization-Aware_Zero-Shot_Neural_Architecture_Search_for_Self-Supervised_Transformers.pdf` |
| 官方代码 | 论文正文未提供公开仓库链接（截至 2026-03-17 未定位到明确官方仓库） |

## 一句话总结
> GEN-TPC-NAS 先用 [[Total Path Count]] 快速筛出高表达性候选，再切换到基于 [[Self-Supervised Learning]] 特征谱熵的泛化评分，实现“表达性-泛化性”平衡的 zero-shot Transformer 搜索。

## 核心贡献
1. 提出 Entropy score：基于特征矩阵谱熵评估网络在低标注设置下的泛化潜力（Sec. III-A, Eq. (1)-(2)）。
2. 提出 TPC + Entropy 的分阶段遗传搜索：前期按 TPC 排序，后期在 TPC 下界约束下按 Entropy 细排（Sec. III-C, Alg. 1）。
3. 在 ImageNet-1K / ADE20K / Wikitext-2 上验证：在标准和低标注设置都表现强，且标注需求显著下降（Sec. IV-B）。

## 问题背景
### 要解决的问题
- 现有 Transformer NAS 多依赖监督训练与标签，搜索代价高，且对低标注泛化考虑不足。
- 仅靠单一 zero-shot proxy 往往偏向某一属性（如表达性），难兼顾泛化能力。

### 现有方法局限
- One-shot NAS 有权重共享干扰问题。
- 传统 zero-shot NAS 大多面向监督范式，对 SSL 场景支持不足。
- 缺少显式“泛化能力”代理指标来指导搜索。

### 本文动机
- 用 [[Self-Supervised Learning]] 降低标注依赖；
- 在 zero-shot NAS 中同时引入表达性代理（TPC）与泛化代理（Entropy），获得更稳健架构。

## 方法详解
### 1) Entropy score：泛化能力代理
- 对第 p 层第 h 个 head 的特征矩阵做 SVD，得到特征值并归一化。
- 用归一化特征值熵衡量特征各向同性（更均匀分布通常泛化更好）。
- 逐层逐头累加得到整体 Entropy 分数。

公式（Sec. III-A）：

\[
E_h = \sum_{i=1}^{c} -\bar{\lambda}_i \log(\bar{\lambda}_i)
\]

\[
S_e = \sum_p \frac{1}{H}\sum_h E_h
\]

符号说明：
- \(c\): 通道数（特征值个数）
- \(H\): attention heads 数量
- \(\bar{\lambda}_i\): 归一化特征值
- \(S_e\): 架构的泛化代理分数

### 2) TPC score：表达性代理
- 基于 [[Total Path Count]] 衡量模型从输入到输出可形成的路径总量。
- 卷积层、线性层、Transformer 层分别定义路径计数，再取对数求和得到整体 TPC 分数。

公式（Sec. III-B, Eq. (3)-(6)）：

\[
O_p = C_{o,p}\cdot \frac{k_p^2}{s_p^2}\cdot g_p
\]
\[
O_p = C_{o,p}
\]
\[
O_p = (A \times 3)\times D \times (D \times r)\times D
\]
\[
S_t = \sum_p \log(O_p)
\]

符号说明：
- \(C_{o,p}\): 输出通道
- \(k_p,s_p,g_p\): kernel / stride / group
- \(A,D,r\): Q-K-V 维度、embedding 维度、MLP ratio
- \(S_t\): TPC 总分（对数域）

### 3) GEN-TPC-NAS 搜索流程
1. 初始化种群 \(P\)（size = N）。
2. 变异或交叉生成新个体，过滤不满足约束（FLOPs/Params/层数）者。
3. 初始阶段以 \(S_t\) 作为评价分数，保留 top-N。
4. 当种群内 \(S_t(F_{max}) - S_t(F_{min}) \le T_0\)（文中默认 \(T_0=0.5\)）时：
   - 记录 \(TPCThreshold = S_t(F_{min})\)
   - 切换到 Entropy 评价。
5. 切换后仅接受 \(S_t\) 不低于阈值的候选，再按 \(S_e\) 优选。
6. 迭代结束输出评分最高架构（Sec. III-C, Alg. 1）。

### 4) 搜索空间与约束
- 搜索维度：Embed dim、Q-K-V dim、Head dim、MLP ratio（Sec. III-D, Table III）。
- 约束：参数量、计算量、层数上限，避免“靠堆深度刷分”。

## 关键图表与结果
### Fig. 2 + Table I（Entropy 与低标注能力）
- 32 个 ViT 上，Entropy 分数与“可节省标注比例”呈强相关，Spearman = 0.93。
- 例：DeiT-T (Entropy 117.4, saving 40%)；DeiT-L (296.2, 98%)。

### Fig. 5 + Table II（TPC 与性能）
- TPC 与 ImageNet-100 (10% label) Top-1 准确率正相关。
- 例：DeiT-T (TPC 410.7, 64.2)；DeiT-L (1052.0, 85.6)。

### Table IV（ImageNet-1K SOTA 对比）
- GEN-TPC-NAS: 1.3G FLOPs, 5.4M Params, 77.5% Top-1, Search cost 0.02 GPU-days。
- 超过文中对比方法（如 T-Razor 75.5, MaskTAS 75.6）。

### Table V（ADE20K 迁移）
- GEN-TPC-Tiny mIoU = 41.2，高于 MaskTAS-Tiny 40.6、MAE-Tiny 37.6、DeiT-Tiny 38.0。

### Table VI（GPT2）
- GPT2: ppl 21.1
- TPC-GPT2: ppl 13.5
- GEN-TPC-GPT2: ppl 10.6（较 TPC-GPT2 再降 2.9）

### Table VII（ViT 架构对比）
- Small: GEN-TPC-Small 在 30% label 下 82.7，高于 TPC-Small 82.1。
- Tiny: GEN-TPC-Tiny 在 30% label 下 77.9，高于 TPC-Tiny 77.0。

### Table VIII/IX（阈值 T0 消融）
- \(T_0=0.5\) 效果最佳：在表达性与泛化性之间取得更好平衡。
- \(T_0=0\) 退化为偏 TPC 的搜索，\(T_0=1.0\) 则更偏 Entropy，易牺牲表达性。

## 实验设置速记
- 硬件：2x RTX 4090。
- 搜索：population=100，generations=1000，\(T_0=0.5\)。
- CV 预训练：MaskTAS 框架，100 epochs，batch 1024，lr 1.5e-4。
- CV 微调：ImageNet-1K 标准/低标注（20-40%）均 200 epochs。
- NLP：GPT2(12L, 110M)，pre-train 100k steps，seq len 1024，fine-tune 4 epochs。

## 批判性思考
### 优点
1. 代理设计互补：TPC 抓表达性，Entropy 抓泛化性，组合逻辑清晰。
2. 搜索效率高：zero-shot + 进化策略，报告搜索代价仅 0.02 GPU-days。
3. 跨模态验证：CV 与 NLP 都给出结果，不局限单任务。

### 局限
1. 代码与复现实验细节公开度不足（论文正文无官方仓库链接）。
2. Entropy 代理依赖特征谱统计，可能受初始化、输入采样策略影响。
3. 主要在作者定义搜索空间与基线下验证，跨搜索空间泛化仍需更多证据。

### 复现性评估
- [x] 核心算法流程清楚（Alg. 1 + Eq. (1)-(6)）
- [x] 主要超参给出（population, generation, T0 等）
- [ ] 官方代码仓库明确公开
- [ ] 一键复现实验脚本与数据处理全链路公开

## 关联概念
- [[Self-Supervised Learning]]
- [[Masked Image Modeling]]
- [[Total Path Count]]
- [[Feature Isotropy]]
- [[Network Expressivity]]
- [[Spearman's Rank Correlation]]
- [[Genetic Algorithm]]
- [[Evolutionary Neural Architecture Search]]
- [[Zero-Cost Proxy]]

