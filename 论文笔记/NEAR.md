---
title: "NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance"
method_name: "NEAR"
authors: [Raphael T. Husistein, Markus Reiher, Marco Eckhoff]
year: 2025
venue: ICLR
tags: [nas, training-free-nas, zero-cost-proxy, effective-rank, iclr]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2408.08776
local_pdf: D:/PRO/essays/papers/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance.pdf
local_code: D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance
created: 2026-03-14
---

# 论文笔记: NEAR

## 基本信息
| 项目 | 内容 |
|---|---|
| 论文 | NEAR: A Training-Free Pre-Estimator of Machine Learning Model Performance |
| arXiv | https://arxiv.org/abs/2408.08776 |
| 会议 | ICLR 2025 |
| 代码 | https://github.com/ReiherGroup/NEAR |
| 本地 PDF | `D:/PRO/essays/papers/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/NEAR A Training-Free Pre-Estimator of Machine Learning Model Performance` |

## 一句话总结
> NEAR 利用各层预激活/后激活矩阵的 [[Effective Rank]]，在不训练模型的前提下估计网络质量，是一个跨多个 NAS 搜索空间都较稳健的 [[Zero-Cost Proxy]]。

## 核心贡献
1. 提出 NEAR：基于激活几何结构（有效秩）的训练前代理指标。
2. 在 NATS-Bench-TSS/SSS 与 NAS-Bench-101 上验证了与最终精度的较强相关性。
3. 将应用扩展到架构排序之外，包括 MLP 层宽估计与激活函数/初始化方案选择。

## 问题背景与动机
- 许多已有代理方法依赖特定激活函数（尤其 ReLU）、标签信息，或只在局部搜索空间表现好。
- 部分代理方法甚至无法稳定超过 `#Params` 这种朴素基线。
- 该工作目标是提出一个对激活函数更通用、跨空间更稳健的代理分数。

## 方法细节
### 1) 将 Effective Rank 作为表达能力信号
对矩阵 `A`，NEAR 使用：
$$
\mathrm{erank}(A)=\exp(H(p_1,\dots,p_Q)),\quad
H=-\sum_{k=1}^{Q} p_k \log p_k,\quad
p_k=\frac{\sigma_k}{\sum_i \sigma_i}
$$
其中 `\sigma_k` 为奇异值。  
直观上，有效秩越高，表示特征几何越不易塌缩、越均衡。

### 2) NEAR 分数定义
对网络各层 `l=1..L`，定义预激活矩阵 `Z_l` 与后激活矩阵 `H_l`：
$$
s_{\mathrm{NEAR}}=\sum_{l=1}^{L}\left(\mathrm{erank}(Z_l)+\mathrm{erank}(H_l)\right)
$$
分数越高，通常代表预期性能越好。  
论文建议通过多次随机采样取平均（如 NAS 基准上使用 32 次）来降低波动。

### 3) 面向 CNN 的适配
- 卷积层输出先重排为矩阵，再进行秩相关计算。
- 使用子矩阵采样策略降低计算量，同时保持趋势一致性。

### 4) 层宽估计
- 经验上将相对 NEAR 分数与层宽做幂函数拟合。
- 在曲线斜率低于阈值处选取层宽，以取得参数量与性能的折中。

## 关键结果
### NAS 基准相关性
- NATS-Bench-TSS（Kendall/Spearman）：
1. CIFAR-10: `0.70 / 0.88`
2. CIFAR-100: `0.69 / 0.87`
3. ImageNet16-120: `0.66 / 0.84`
- NATS-Bench-SSS：
1. CIFAR-10: `0.74 / 0.91`
2. CIFAR-100: `0.62 / 0.82`
3. ImageNet16-120: `0.76 / 0.92`
- NAS-Bench-101：
1. CIFAR-10: `0.52 / 0.70`

### 全局排序表现
- 跨搜索空间/数据集平均 rank（越低越好）：
1. NEAR: `1.71`
2. MeCoopt: `2.57`
3. ZiCo: `3.57`

### 超参数选择信号
- 在论文给出的实验中，NEAR 能较好识别明显差的激活/初始化组合（如部分 Tanhshrink 组合）。
- 对性能非常接近的候选，NEAR 的细粒度排序不一定总与最终损失严格一致。

## 论文与代码对照
- `src/near_score/near_score.py` 用 SVD 奇异值 + 熵来计算 effective rank，对应论文 Eq. (4)-(5)。
- `__get_near_score(...)` 对各层激活求和得到总分，与论文分数定义一致。
- 代码中对卷积输出做重排与子采样，与 Sec. 3.3 的效率设计一致。
- `estimate_layer_size(...)` 使用幂函数拟合和 `slope_threshold`，与 Sec. 4.2 的思路一致。

## 批判性结论
### 优点
1. 不依赖标签，且对激活函数限制更少。
2. 跨搜索空间一致性较强，不是只在单一基准有效。
3. 可用于架构之外的决策（层宽、初始化、激活函数）。

### 局限
1. NEAR 主要刻画表达能力，不直接刻画完整优化动力学。
2. 对头部模型的微小差异，区分能力可能有限。
3. 效果仍受任务与搜索空间分布影响。

## 复现状态
- [x] 官方代码已发布
- [x] 本地 PDF 已归档
- [x] 本地代码已归档
- [ ] 尚未在本机完整复跑所有基准

## 相关概念
- [[Zero-Cost Proxy]]
- [[Training-free NAS]]
- [[Neural Architecture Search]]
- [[Network Expressivity]]
- [[Effective Rank]]
- [[Kendall's Tau]]
- [[Spearman's Rank Correlation]]


## 代码
### 特征提取
```

def get_activation(layer_id):
        def hook(model, input, output):
            # pylint: disable-msg=redefined-builtin
            called.add(layer_id)
            if isinstance(output, tuple):
                output = output[0] # tuple 输出只取第一个（如某些模型返回多项）
            size = output.shape[-1]
            if output.dim() > 2:
                output = torch.transpose(output, 1, 3).flatten(0, 2)
                # 若是卷积特征图（dim>2），先 transpose(1,3) 再 flatten(0,2) 变成 2D 矩阵
            activations[layer_id] = torch.cat((activations[layer_id], output), dim=0)
            if activations[layer_id].shape[0] >= activations[layer_id].shape[1]:
                # 不断拼接样本后，当行数 >= 列数时,随机取一段连续行子矩阵,然后删除该层hook
                start = (
                    np.random.randint(0, activations[layer_id].shape[0] // size - 1) * size
                    if activations[layer_id].shape[0] // size - 1 > 0
                    else 0
                )
                end = start + activations[layer_id].shape[1]
                activations[layer_id] = activations[layer_id][start:end]
                hooks[layer_id].remove()
                finished.append(layer_id)

        return hook
```
### 选择要抓取的层
```
# 把“有 weight 的模块 + 激活函数模块”都放进 layer_stack。
# 这相当于同时覆盖 pre-activation / post-activation 信息来源。
    activation_functions = tuple(
        getattr(torch.nn, fct) for fct in torch.nn.modules.activation.__all__
    )
    layer_stack = [
        module
        for name, module in model.named_modules()
        if hasattr(module, "weight") or isinstance(module, activation_functions)
    ]
    if layer_index is not None:
        layer_stack = [layer_stack[layer_index]]
```

### 注册hook抓取输出
```
# 每层注册 forward_hook，前向时收集 output。
    for layer_id, layer in enumerate(layer_stack):
        activations.append(torch.tensor([]))
        hook = layer.register_forward_hook(get_activation(layer_id))
        hooks.append(hook)
```
### 只用输入，不用标签
核心输入是 dataloader 迭代出来的 X，不是在函数内部自己 torch.randn 生成的。
关键代码在这里
是否随机，取决于你给的 dataloader（数据本身 + shuffle）。
```
# 只前向 model(X)，不反传
    for X, _ in dataloader:  # pylint: disable=invalid-name
        model(X)
        if len(finished) == len(called):
            break
```

### 对提取的特征值矩阵计算有效秩并求和
```
# get_effective_rank 用 SVD 奇异值 + 熵计算
    score = 0.0
    for activation in activations:
        if len(activation) == 0:
            continue
        score += get_effective_rank(activation)


def get_effective_rank(matrix, return_singular_values=False):
    """
    Calculates the effective rank of a matrix.

    Args:
        matrix (torch.Tensor): Input matrix.
        return_singular_values (bool, optional): If True, also returns the singular values. Default is False.

    Returns:
        float or tuple: Effective rank of the matrix. If `return_singular_values` is True, returns a tuple
        containing the effective rank and the singular values.
    """
    s = torch.linalg.svdvals(matrix)  # pylint: disable-msg=not-callable
    if return_singular_values:
        singular_values = s.detach().clone()
    s /= torch.sum(s)
    erank = torch.e ** scipy.stats.entropy(s.detach())
    if return_singular_values:
        return np.nan_to_num(erank), singular_values
    return np.nan_to_num(erank)

```

### 香农熵，但是不太一样
Shannon 熵（香农熵）
NEAR 在代码里是这样算的：
先取奇异值：s = torch.linalg.svdvals(matrix)
归一化：s /= torch.sum(s)
熵后再取指数：erank = e ** entropy(s)

NEAR：对激活矩阵奇异值谱做熵（再指数化成 effective rank）。
AZ-NAS：sE 是对PCA 特征值谱做熵。
VKDNW：对**FIM 特征值谱（分位采样后）**做熵

### 激活前后的奇异值个数
NEAR 的奇异值个数是不是固定？
    不是全局固定。torch.linalg.svdvals(matrix) 返回个数是 min(m, n)
NEAR 会尽量把每层激活裁成近似方阵（行数裁到列数），所以单层里常见是 n 个奇异值；但不同层的 n 不同，所以整体仍不固定。
    调用 torch.linalg.svdvals(matrix)。 min(m,n) 这个规则是 svdvals 本身的数学/库行为，不是代码里手写常数。
    