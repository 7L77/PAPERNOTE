---
title: "SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS"
method_name: "SWAP-NAS"
authors: [Yameng Peng, Andy Song, Haytham M. Fayek, Vic Ciesielski, Xiaojun Chang]
year: 2024
venue: ICLR
tags: [nas, training-free-nas, zero-cost-proxy, swap]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2403.04161
local_pdf: D:/PRO/essays/papers/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS.pdf
local_code: D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS
created: 2026-03-14
---

# 论文笔记：SWAP-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | SWAP-NAS: Sample-Wise Activation Patterns for Ultra-Fast NAS |
| arXiv | https://arxiv.org/abs/2403.04161 |
| OpenReview | https://openreview.net/forum?id=tveiUXU2aa |
| 代码 | https://github.com/pym1024/SWAP |
| 本地 PDF | `D:/PRO/essays/papers/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS` |

## 一句话总结
> SWAP-NAS 用“按神经元收集、按样本二值化”的激活模式基数来衡量未训练网络可表达性，在保持极低搜索成本的同时显著提升了 training-free NAS 的排序相关性。

## 核心贡献
1. 提出 [[Sample-Wise Activation Pattern]] 与 SWAP-Score，用集合基数刻画网络表达能力（Sec. 3.2, Def. 3.2/3.3）。
2. 给 SWAP-Score 加入参数量正则，实现模型尺寸可控搜索（Sec. 3.3, Def. 3.4/3.5）。
3. 在 NAS-Bench-101/201/301 与 TransNAS-Bench-101 上对比 15 个 training-free 指标，相关性更稳（Sec. 4.1）。
4. 将 regularized SWAP-Score 融入进化搜索得到 SWAP-NAS，CIFAR-10/Imagenet 直接搜索分别约 6/9 分钟（Sec. 4.2）。

## 问题背景
### 要解决的问题
- [[Training-free NAS]] 需要一个“无需训练但能可靠排序”的打分函数。

### 现有方法局限
- 许多 [[Zero-Cost Proxy]] 在不同搜索空间和任务上相关性不稳。
- 指标常偏向大模型，难以在给定尺寸预算下稳定控参。

### 本文动机
- 把激活模式从“按样本作为行”重排为“按神经元作为行”，放大可区分上界，提升排序分辨率。

## 方法详解
### Step 1: 标准激活模式（对比基线）
定义标准模式集合：
$$
A_{N,\theta}=\left\{p^{(s)}:p^{(s)}=\mathbf{1}(p^{(s)}_v)_{v=1}^{V},\ s\in\{1,\dots,S\}\right\}
$$
- 上界由样本数 \(S\) 限制，输入分辨率升高时容易“饱和”到接近 \(S\)（Sec. 3.1）。

### Step 2: Sample-wise Activation Pattern（核心）
定义 sample-wise 集合：
$$
\hat{A}_{N,\theta}=\left\{p^{(v)}:p^{(v)}=\mathbf{1}(p^{(v)}_s)_{s=1}^{S},\ v\in\{1,\dots,V\}\right\}
$$
- 每个中间激活单元给出一个跨样本二值向量，集合基数上界由 \(V\) 驱动（Sec. 3.2, Def. 3.2）。

### Step 3: SWAP-Score
$$
\Psi_{N,\theta}=|\hat{A}_{N,\theta}|
$$
- 直接用 unique pattern 数量作为得分（Sec. 3.2, Def. 3.3）。

### Step 4: 参数量正则（控尺寸）
$$
f(\Theta)=\exp\left(-\frac{(\Theta-\mu)^2}{\sigma}\right),\quad
\Psi'_{N,\theta}=\Psi_{N,\theta}\cdot f(\Theta)
$$
- \(\mu\) 控中心，\(\sigma\) 控曲线宽度，可把搜索推向目标模型大小区间（Sec. 3.3, Def. 3.4/3.5）。

### Step 5: 与进化搜索结合（SWAP-NAS）
- 使用种群搜索、交叉、变异与“删最差”更新（Algorithm 1；附录 C）。
- 打分发生在初始化种群、交叉候选、变异子代三个位置。

## 关键实验结论
### 相关性（主结论）
- 论文报告：在 NAS-Bench-201 的 CIFAR-100 上，regularized SWAP-Score 与验证精度的 Spearman 达到 0.90，显著高于 NWOT 的 0.80（摘要）。

### Table 3（消融：输入分辨率）
- 标准模式 \(|A_{N,\theta}|\)：3x3 时相关性 0.86，15x15/32x32 分别降到 0.45/0.34，且方差几乎归零。
- SWAP-Score \(\Psi\)：3x3/15x15/32x32 相关性 0.86/0.84/0.90。
- Regularized \(\Psi'\)：3x3/15x15/32x32 相关性 0.89/0.92/0.93。

### Table 1（CIFAR-10 搜索）
- SWAP-NAS-A/B/C（不同 \(\mu=\sigma\)）测试误差：2.65/2.54/2.48。
- 搜索开销约 0.004 GPU days（约 6 分钟）。

### Table 2（ImageNet 直接搜索）
- SWAP-NAS (\(\mu=\sigma=25\)) Top-1/Top-5 error: 24.0/7.6。
- 搜索开销约 0.006 GPU days（约 9 分钟）。

## 论文与代码对照
- 论文方法：包含 SWAP-Score + regularization + evolutionary SWAP-NAS（正文+附录）。
- 官方仓库现状：`src/metrics/swap.py` 重点提供 SWAP-Score 计算；`correlation.py` 提供相关性复现实验。
- 关键实现点：
1. 在 ReLU 上注册 forward hook 收集中间激活（`SWAP.register_hook`）。
2. 拼接所有 ReLU 输出后取 sign，转置为 `(neurons, samples)`。
3. `torch.unique(..., dim=0).size(0)` 作为基数打分。
4. 正则项实现为 `exp(-((params-mu)^2)/sigma)`。
- 差异说明：仓库未直接提供论文附录里的完整 SWAP-NAS 进化搜索脚本，更多是评分器与相关性评估代码。

## 批判性思考
### 优点
1. 指标定义非常直接，计算图清晰，工程上易嵌入 NAS 循环。
2. 在多搜索空间/多任务上给出了更稳定的相关性证据。
3. 正则项把“相关性提升”和“模型尺寸可控”统一到同一打分框架。

### 局限
1. 依赖 ReLU 二值化视角，对非分段线性激活的迁移需要额外验证。
2. \(\mu,\sigma\) 的选择仍需结合搜索空间尺寸分布做调参。
3. 公开代码与论文“完整 NAS 算法”之间存在落差，复现全流程需要补齐搜索实现。

### 复现性评估
- [x] 论文公开
- [x] 官方代码公开
- [x] 打分核心实现清晰
- [ ] 完整 SWAP-NAS 搜索脚本一键复现（仓库未直接提供）

## 关联概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
- [[Sample-Wise Activation Pattern]]
- [[Network Expressivity]]
- [[Spearman's Rank Correlation]]
- [[Cell-based Search Space]]



## 代码分析

### 特征提取
注册提取点
在 [swap.py](D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS/src/metrics/swap.py#L77) 里，register_hook 遍历 model.named_modules()，给所有 nn.ReLU 注册 forward_hook

收集中间特征
在 [swap.py](D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS/src/metrics/swap.py#L82) 的 hook_in_forward，把每个 ReLU 的 output.detach() 存进 self.interFeature（只收 4D 特征图，通常是卷积特征）。
```
    def register_hook(self, model):
        for n, m in model.named_modules():
            if isinstance(m, nn.ReLU):
                m.register_forward_hook(hook=self.hook_in_forward)

    def hook_in_forward(self, module, input, output):
        if isinstance(input, tuple) and len(input[0].size()) == 4:
            self.interFeature.append(output.detach()) 

```

### 拼接成一个大特征矩阵
在 [swap.py](D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS/src/metrics/swap.py#L86)，一次前向后把每层特征 f.view(B, -1) 展平，再 torch.cat(..., dim=1)，得到 (batch_size, total_neurons)。
```

    def forward(self):
        self.interFeature = []
        with torch.no_grad():
            self.model.forward(self.inputs.to(self.device))
            if len(self.interFeature) == 0: return
            activtions = torch.cat([f.view(self.inputs.size(0), -1) for f in self.interFeature], 1)         
            self.swap.collect_activations(activtions)
            
            return self.swap.calSWAP(self.regular_factor)
```


### 二值化后用于 SWAP 评分
在 [swap.py](D:/PRO/essays/code_depots/SWAP-NAS Sample-Wise Activation Patterns for Ultra-Fast NAS/src/metrics/swap.py#L21)，对激活做 torch.sign，再转置成 (neurons, samples) 去重计数（torch.unique）得到 SWAP 分数。
```

    @torch.no_grad()
    def collect_activations(self, activations):
        n_sample = activations.size()[0]
        n_neuron = activations.size()[1]

        if self.activations is None:
            self.activations = torch.zeros(n_sample, n_neuron).to(self.device)  

        self.activations = torch.sign(activations)

    @torch.no_grad()
    def calSWAP(self, regular_factor):
        
        self.activations = self.activations.T # transpose the activation matrix: (samples, neurons) to (neurons, samples)
        self.swap = torch.unique(self.activations, dim=0).size(0)
        
        del self.activations
        self.activations = None
        torch.cuda.empty_cache()

        return self.swap * regular_factor
```

### 描述
SWAP 打分实际用的是 hook 到的中间 ReLU 特征。
    SWAP 只取激活后的特征
        SWAP 只给 nn.ReLU 注册 hook，并保存 output，也就是 ReLU 后特征。
        后续还会 torch.sign 二值化。
    NEAR 会同时覆盖“激活前后”信息，但方式是“遍历模块输出”
        NEAR 对两类模块都挂 hook：hasattr(module, "weight")（如 Conv/Linear）和激活函数模块。
        hook 取的是每个模块的 output。对带权重层来说通常是激活前；对激活层来说是激活后。