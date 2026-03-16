---
title: "AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search"
method_name: "AZ-NAS"
authors: [Junghyup Lee, Bumsub Ham]
year: 2024
venue: CVPR
tags: [nas, training-free-nas, zero-cost-proxy, cvpr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2403.19232
local_pdf: D:/PRO/essays/papers/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search.pdf
local_code: D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search
created: 2026-03-14
---

# 论文笔记：AZ-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | AZ-NAS: Assembling Zero-Cost Proxies for Network Architecture Search |
| arXiv | https://arxiv.org/abs/2403.19232 |
| 项目页 | https://cvlab.yonsei.ac.kr/projects/AZNAS |
| 代码 | https://github.com/cvlab-yonsei/AZ-NAS |
| 本地 PDF | `D:/PRO/essays/papers/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/AZ-NAS Assembling Zero-Cost Proxies for Network Architecture Search` |

## 一句话总结
> AZ-NAS 通过组合四类互补 zero-cost proxies（表达性、渐进性、可训练性、复杂度）并用非线性排名聚合，显著提升了训练前 NAS 排名与真实性能的一致性。

## 核心贡献
1. 提出多代理协同的 training-free NAS 视角，不再依赖单一 proxy（Sec. 1, Sec. 3）。
2. 设计四个可在一次前后向中高效计算的 proxy：`sE/sP/sT/sC`（Sec. 3.1）。
3. 提出非线性排名聚合 `sum(log(rank/m))`，显式惩罚“短板代理”（Sec. 3.2, Eq. 12）。
4. 在 NAS-Bench-201、MobileNetV2、AutoFormer 三类空间上取得更好搜索质量与成本比（Sec. 4.2）。

## 问题背景
### 要解决的问题
- 训练自由 NAS 的核心是：不用完整训练也能把候选架构排对序。
- 现实中单 proxy 往往相关性不足，导致“挑出来的最优架构”并不优。

### 现有方法局限
- 单一 proxy 覆盖的信息维度窄。
- 一些方法计算代价高（例如依赖额外多次前后向或复杂核矩阵）。
- 简单线性聚合难以处理“某一维明显很差”的情况。

### 本文动机
- 让不同视角的 proxy 互补，并通过聚合机制强化“全面强”而非“单项强”的架构。

## 方法详解
### 1) `sE`：Expressivity（表达性）
- 在各主干 block 特征上做协方差分解，计算主成分归一化后熵值。
- 直观上：特征越各向同性，表达能力越强（Sec. 3.1, Eq. 1-4）。

### 2) `sP`：Progressivity（渐进性）
- 定义为相邻 block 表达性差值的最小值：`min_l (sE_l - sE_{l-1})`（Eq. 5）。
- 约束“深层特征空间应持续扩展”，不是只看某个局部峰值。

### 3) `sT`：Trainability（可训练性）
- 目标是衡量梯度传播稳定性（谱范数接近 1 更好）。
- 通过 Hutchinson 风格随机向量近似 block Jacobian，再构造训练性分数（Eq. 6-11）。

### 4) `sC`：Complexity（复杂度）
- 直接使用 FLOPs 作为复杂度 proxy，在预算内偏好更高算力利用架构（Sec. 3.1）。

### 5) 非线性排名聚合
- 最终分数：对每个 proxy 的排名做 `log(rank/m)` 后求和（Eq. 12）。
- 作用：某一 proxy 排名很差会被明显惩罚，避免被其他高分项“冲掉”。

### 6) 搜索流程
- 采用进化式搜索（Algorithm 1）：
1. 计算当前架构四类 proxy；
2. 用非线性聚合算 AZ-NAS 分；
3. 从 top-k 中选父代变异生成新架构；
4. 迭代至预算结束，输出最高分架构。

## 关键公式（含解释）
### Eq. (3) 表达性熵
\[
s_l^E=\sum_i -\tilde{\lambda}_l(i)\log \tilde{\lambda}_l(i)
\]
- `\tilde{\lambda}` 是主成分方差的 L1 归一化系数。
- 熵高意味着主成分贡献更均匀，特征不塌缩。

### Eq. (5) 渐进性
\[
s^P=\min_l (s_l^E-s_{l-1}^E)
\]
- 关注最差“层间增长幅度”，确保深度方向持续提升。

### Eq. (11) 可训练性
\[
s^T=\frac{1}{L-1}\sum_{l=2}^{L}\left(-\sigma_l-\frac{1}{\sigma_l}+2\right)
\]
- `\sigma_l` 为近似 Jacobian 的谱范数。
- 当 `\sigma_l=1` 时单层项最大，偏离 1 会受罚。

### Eq. (12) 聚合分数
\[
s_{AZ}(i)=\sum_{M\in\{E,P,T,C\}}\log \frac{\mathrm{Rank}(s_M(i))}{m}
\]
- `Rank` 是在候选集中的升序排名。
- 对低排名项的惩罚更强，鼓励均衡表现。

## 关键图示解读
### Figure 1
- 横轴是 Kendall's Tau，纵轴是选中架构精度，气泡大小/颜色反映运行时。
- 结论：AZ-NAS 在“排序一致性 + 最终精度 + 计算成本”三者之间给出更优平衡。

### Figure 2
- 展示 `sE` 的直观含义：特征分布越各向同性，主成分系数越均匀，熵越高。
- 说明 `sE` 能检测特征塌缩与表达冗余。

### Figure 3
- 展示各 proxy 间相关性：`sT` 与其余 proxy 相关性更低。
- 解释了为什么“低相关代理的组合”可带来更明显增益。

## 关键实验结果
### NAS-Bench-201（Table 1）
- AZ-NAS 在 Kendall's Tau 上显著领先：
1. CIFAR-10: `0.741`
2. CIFAR-100: `0.723`
3. ImageNet16-120: `0.710`
- 对比 ZiCo（`0.589/0.590/0.584`）和 GradSign（`0.618/0.594/0.575`）均有明显提升。
- 运行时 `42.7 ms/arch`，远低于 TE-NAS（`1311.8 ms/arch`）与 GradSign（`1823.9 ms/arch`）。

### MobileNetV2 搜索空间（Table 2）
- 在 450M/600M/1000M FLOPs 约束下分别达到：
1. `78.6 ± 0.2`
2. `79.9 ± 0.3`
3. `81.1 ± 0.1`
- 同时保持低搜索成本（约 `0.4~0.7` GPU days）。

### AutoFormer（Table 3）
- Tiny/Small/Base 大多数设置优于 AutoFormer 和 TF-TAS，且搜索成本更低。
- 论文脚注说明：ViT 场景不使用 `sP`（progressivity），仍能保持竞争力。

### 消融与扩展（Table 4/5）
- 多代理明显优于单代理。
- 非线性聚合优于线性聚合（例如全代理：`0.741/0.723/0.710` vs `0.697/0.681/0.663`）。
- 把 AZ-NAS 代理并入 SynFlow/ZiCo 也能持续提升 Kendall's Tau。

## 与代码实现的对照
- 官方仓库：`https://github.com/cvlab-yonsei/AZ-NAS`（已归档到本地）。
- MobileNetV2 分支中 `ZeroShotProxy/compute_az_nas_score.py` 与论文一致实现 `sE/sP/sT/sC`。
- `evolution_search_az.py` 使用 `np.log(rank/l)` 聚合，和 Eq. (12) 对齐。
- AutoFormer 分支 `lib/training_free/indicators/az_nas.py` 仅计算 `expressivity/trainability/complexity`，与论文脚注“ViT 不用 progressivity”一致。

## 批判性思考
### 优点
1. 方法简单直接，可插拔到已有 search loop。
2. 精度-效率折中好，尤其是排序一致性提升明显。
3. 代理设计与聚合机制有清晰可解释性。

### 局限
1. 仍依赖“proxy 与真实性能相关”这一经验前提，跨域泛化需更多验证。
2. 当前主要集中在图像分类搜索空间，其他任务（检测/分割/NLP）证据不足。
3. `sC=FLOPs` 在某些硬件目标上可能与真实 latency 不一致。

### 复现性评估
- [x] 代码开源
- [x] 算法流程清晰
- [ ] 一键复现实验门槛低（仍需准备较重数据与环境）
- [ ] 跨任务统一复现脚本完善

## 关联概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
- [[NAS-Bench-201]]
- [[Non-linear Ranking Aggregation]]
- [[Kendall's Tau]]
- [[Hutchinson Estimator]]
- [[Spectral Norm]]


## 代码分析

#### 特征提取
```
layer_features = model.extract_cell_features(input_)

def extract_cell_features(self, inputs):
	cell_features = []
	feature = self.stem(inputs)
	if feature.requires_grad:
		feature.retain_grad()
	cell_features.append(feature)
	for i, cell in enumerate(self.cells):
		feature = cell(feature)
		if feature.requires_grad:
			feature.retain_grad()
		cell_features.append(feature)
	return cell_features
	
- layer_features[i] 就是 fi​（第 i 个 cell/block 的输出特征）
```

#### 表达性：

输入[16,3,32,32]
转化[BHW,C]=[16384,3]
对每一列减去全体样本均值得到X`
协方差矩阵sigma = ${X^`}^T {X^`} / N$
通道维度上的协方差（更准确说是二阶矩/协方差，因为它用了 1/N 而不是无偏估计的 1/(N-1)
特征值s ， clamp转化负数为0，denom求和，p=s/denom
香农熵 = $-p(log(p+\theta))$

#### 进步性
就是表达性[i]-表达性[i-1]

```
    expressivity_scores = []
    for i in range(len(layer_features)):
        feat = layer_features[i].detach().clone()
        b,c,h,w = feat.size()
        feat = feat.permute(0,2,3,1).contiguous().view(b*h*w,c)
        m = feat.mean(dim=0, keepdim=True)
        feat = feat - m
        sigma = torch.mm(feat.transpose(1,0),feat) / (feat.size(0))
        s = torch.linalg.eigvalsh(sigma) # faster version for computing eignevalues, can be adopted since sigma is symmetric
        prob_s = s / s.sum()
        score = (-prob_s)*torch.log(prob_s+1e-8)
        score = score.sum().item()
        expressivity_scores.append(score)
    expressivity_scores = np.array(expressivity_scores)
    progressivity = np.min(expressivity_scores[1:] - expressivity_scores[:-1])
    expressivity = np.sum(expressivity_scores)
```

#### 可训练性

1. 从一次前向里拿到逐层特征 `f_0, f_1, ..., f_L`。
2. 对每个相邻层对 `(f_{l-1}, f_l)`（从后往前遍历）：
	1. 采样一个与 `f_l` 同形状的 **Rademacher 梯度** `g_l`（每个元素是 ±1）。
   3. 用自动求导算  
      \[
      g_{l-1}=\frac{\partial f_l}{\partial f_{l-1}}^\top g_l
      \]
   4. 把 `g_l, g_{l-1}` 展平到二维：  
      - CNN: `[B,H,W,C] -> [BHW, C]`  
      - ViT: `[B,N,C] -> [BN, C]`
   5. 构造 Jacobian 近似矩阵  
      \[
      A_l \approx \frac{g_{l-1}^\top g_l}{N}
      \]
      这里 \(N=BHW\)（或 \(BN\)）。
   6. 对 \(A_l\) 做 SVD，取最大奇异值 \(s_{\max}\)。
   7. 层分数：
      \[
      t_l=-s_{\max}-\frac{1}{s_{\max}+10^{-6}}+2
      \]
      （当 \(s_{\max}\approx 1\) 时分数最高，偏离 1 就降分）
8. 全局可训练性分数：
   \[
   s_T=\frac{1}{L-1}\sum_l t_l
   \]
```
    scores = []
    for i in reversed(range(1, len(layer_features))):
        f_out = layer_features[i]
        f_in = layer_features[i-1]
        if f_out.grad is not None:
            f_out.grad.zero_()
        if f_in.grad is not None:
            f_in.grad.zero_()
        g_out = torch.ones_like(f_out) * 0.5
        g_out = (torch.bernoulli(g_out) - 0.5) * 2


        g_in = torch.autograd.grad(outputs=f_out, inputs=f_in, grad_outputs=g_out, retain_graph=False)[0]
        if g_out.size()==g_in.size() and torch.all(g_in == g_out):
            scores.append(-np.inf)
        else:
            if g_out.size(2) != g_in.size(2) or g_out.size(3) != g_in.size(3):
                bo,co,ho,wo = g_out.size()
                bi,ci,hi,wi = g_in.size()
                stride = int(hi/ho)
                pixel_unshuffle = nn.PixelUnshuffle(stride)
                g_in = pixel_unshuffle(g_in)
            bo,co,ho,wo = g_out.size()
            bi,ci,hi,wi = g_in.size()
            
            ### straight-forward way
            # g_out = g_out.permute(0,2,3,1).contiguous().view(bo*ho*wo,1,co)
            # g_in = g_in.permute(0,2,3,1).contiguous().view(bi*hi*wi,ci,1)
            # mat = torch.bmm(g_in,g_out).mean(dim=0)
            
            ### efficient way # print(torch.allclose(mat, mat2, atol=1e-6))
            g_out = g_out.permute(0,2,3,1).contiguous().view(bo*ho*wo,co)
            g_in = g_in.permute(0,2,3,1).contiguous().view(bi*hi*wi,ci)
            mat = torch.mm(g_in.transpose(1,0),g_out) / (bo*ho*wo)

            ### make it faster
            if mat.size(0) < mat.size(1):
                mat = mat.transpose(0,1)
            ###
            s = torch.linalg.svdvals(mat)
            scores.append(-s.max().item() - 1/(s.max().item()+1e-6)+2)
    trainability = np.mean(scores)
```


代码里的实现细节你也可以顺带标注：
- CNN 分支若空间尺寸不一致，会先做 `PixelUnshuffle` 对齐。
- 某些实现里若出现“近似恒等传播”会直接强惩罚（如记 `-inf`）。  

现有做法更像是“结构 proxy + size proxy”的拼接
	“拼接”通常是：先用结构分数衡量拓扑好坏，再加一个规模项补容量信息。

结构proxy
	 评估“这个网络拓扑设计本身是否有效”的指标
	 关注连接方式、算子组合、信息流/梯度流是否顺畅，而不是单纯大不大。
	 NASWOT/NWOT、SynFlow、Jacov、Zen、GradSign、
	 以及 AZ-NAS 里基于层特征与梯度的 expressivity/progressivity/trainability 信号

size_proxy
	它能反映“模型有多大”，但不能单独回答“结构是否聪明”。
	本质是规模量：#Params、FLOPs/MACs、深度、宽度、通道数、时延等。

快速区分方法：
- 两个模型参数量几乎一样，但精度差很多：这是 结构 proxy 在起作用。
- 同一结构把通道数放大后性能提高：这是 size proxy 在起作用。