# IDEA

## AZ-NAS

### 问题：
单一 proxy 覆盖的信息维度窄
	免训练在NAS架构排序上不够准确（SP，KT）
	现有 training-free NAS 虽然高效，但实用性受限。

**直接把现有 proxies 简单堆起来也不行**。
	简单线性聚合难以处理“某一维明显很差”的情况。

**一些方法计算代价高（例如依赖额外多次前后向或复杂核矩阵）**
	 - **TE-NAS**：因为要算 **NTK**，计算开销大。
	 - **GradSign**：因为做 **sample-wise analysis**
	 - 较高的：Grasp **395.9**、Snip **326.5**、ZiCo **372.8**



### 动机：

**要想在不训练网络的前提下更准确地判断架构优劣，必须从多个互补维度综合评估**。
	不再只靠单一 proxy，而是组合多个互补的 zero-cost proxies 来更可靠地预测架构优劣
	让不同视角的 proxy 互补，并通过聚合机制强化“全面强”而非“单项强”的架构。

### 设计
四个可在一次前后向中高效计算的 proxy
	表达性：layer_features 特征上做协方差分解，计算主成分归一化后熵值
非线性排名聚合 `sum(log(rank/m))`

### 衍生的问题：

很多 proxy 仍会天然偏好“更大/更深/更宽”的网络，或在某些搜索空间里出现系统性偏差
	**怎样同时刻画‘结构好不好’和‘容量够不够’**，目前还没有被优雅统一地解决；
	现有做法更像是“结构 proxy + size proxy”的拼接

在 AutoFormer 的 ViT 搜索空间里，他们**没有使用 progressivity proxy**，因为高斯随机输入下 attention 模块会产生相似的 token attention，导致“特征空间随深度扩展”这个假设不再可靠
	**开发更适合 ViT 的 zero-cost proxy 是未来工作**。

在DARTS内搜索空间会失去效果，性能只有其中的表达性会比较好，其他的几个反而拖后腿
	在实验中，你会发现在301搜索空间下，性能较为糟糕
	论文在 ViT 上也主动去掉了 sP，理由是该假设在那类结构上不稳；
	这和你在 DARTS 里观察到“某些子 proxy 失效”是同一类信号
	在 DARTS/NB301 这种 skip/多路径更复杂的空间里容易被某个局部层“卡住”，变成噪声项。

AZ-NAS 的进化算子仍是传统 top-k 变异范式，探索效率上有上限。
	LLMENAS 用 LLM 引导 crossover/mutation，并结合 one-shot/surrogate 降搜索样本与成本。

AZ-NAS 的复杂度项主要是 FLOPs，和真实部署约束（轻量+鲁棒）耦合不够。  
	后文补上：LRNAS 把参数预算和鲁棒目标一起放进搜索目标（Shapley + 预算约束）



## VKDNW

问题：只看“网络在初始化时的性质”，就估计它将来是否容易训练、是否可能达到更高分类精度？

动机：

“有理论基础、可解释”的 proxy

现有 proxy 评价指标也不够贴合 NAS 目标

​	NAS 真正关心的是：**能不能把“最好的那些网络”排到前面**，而不是低性能网络之间排得多精确。
​	于是他们提出引入 **nDCG** 作为更贴近实际 NAS 需求的评价指标。

idea：一个好架构，应该对应一个“更平衡、更稳定”的参数估计问题。



答案：

基于Fisher信息 神经网络预测对权重扰动的敏感性
​	特征值分布均匀（高VKDNW）→ 训练稳定，分类性能好。
​	特征值差异大 → 某些权重方向更新困难，需更多数据或调整架构

将FIM重写避免显式计算协方差矩阵
$$  \hat{F}(\theta) = \frac{1}{n} \sum_{n=1}^N A_n^T A_n $$

将FIM维度从p * p降至L * L,L 为层数，通常 L<<p。

AZ-NAS的表达性和VKDNW的vkdnw_entropy = -(temp * log(temp + 1e-10)).sum()都用到了香农熵，这里的香农熵是有什么作用吗，有什么论文说过香农熵可以表示神经网络或者神经架构的表达性吗？
- 香农熵本身不“直接等于表达性”；
- 它通过“谱是否均匀（有效维度是否高）”间接刻画表达性/可训练性，这在 NAS 和表示学习里很常见。

AZ-NAS
- 对特征协方差做特征分解，归一化后当概率，再算  $$ H=−∑p_ilog⁡p_i​。$$熵高 => 主成分更均匀（更各向同性），作者把这解释为更强表达性。
VKDNW
- 对 Fisher 信息矩阵谱（实现里是奇异值/分位值）归一化后算熵。
- 熵高 => 各方向信息更均衡，作者解释为“训练可估计性更平衡”，并与架构质量相关。




衍生的问题：

如何从理论上更严谨地解释 initialization-time proxy 为什么能预测 final accuracy
	​这些理论本来对应的是“接近最优参数点”的分析，而实际计算却是在**初始化权重**上做的
	proxy 中仍显式叠加了规模项 `N_layers`，在不同搜索空间的泛化边界仍需更多验证

**怎样同时刻画‘结构好不好’和‘容量够不够’**，目前还没有被优雅统一地解决；现有做法更像是“结构 proxy + size proxy”的拼接
	自己的核心分数与网络大小基本正交，而在真正做 NAS 排序时，又不得不把 **网络层数 ℵ** 加回去，因为跨不同大小的网络比较时，容量仍然重要

**不同 proxy 的权重、交互关系、适用场景，是否能被自适应学习，而不是手工固定**。
	AZ-NAS 用的是非线性 rank aggregation，核心思想是“某个 proxy 很差就要重罚”；
	VKDNW 也沿用了类似的非线性聚合，并进一步尝试 model-driven aggregation。
	加入更多特征做 model-driven aggregation 后，指标还能继续涨，这说明“如何学会更好的 proxy fusion”本身就是一个值得做的方向

VKDNW 强调理论可解释性，AZ-NAS 强调多视角互补。但两者现在都主要停留在“给分并排序”。
	还可以继续做的是：**把 proxy 分解为更细粒度的结构诊断信号**，
	​比如明确指出某个架构差是因为梯度传播差、表达冗余大、attention 退化，还是容量利用不足。

香农熵是不是泛用性不强？  答：是的。
	香农谱熵是一个有意义且计算便宜的**线性-谱**代理（衡量主成分能量分布/effective rank），在很多场景下能提供对“表示多样性/丰富度”的直观信号，但**它无法通用地、完备地表示神经网络或神经架构的全部表达性**，因为它忽略深层非线性、输入分布依赖、层间复合效应等。
	严重依赖输入分布 / 批次 /预处理。
		谱熵取决于你喂入的随机批（Gaussian input / real data）、batch size、归一化、是否做 centering、通道数和空间拆分方式。换一个输入分布或尺度，熵可以显著变化，从而不能作为架构本身的稳健不变标量。
	**对等效变换不敏感或过于敏感——不能区分“重要”的表征差异。**  
		许多对学习与泛化至关重要的结构（例如可逆变换、局部不变性、非线性低维流形结构）不会在协方差谱上留下明确区别；反之，噪声／微小扩展可能改变谱而不改变最终性能。
	单层或逐层的谱熵求和/汇总（AZ-NAS 做聚合）是启发式的，但层间的复合效应（深层网络把简单特征逐层组合成复杂表示）不总被谱熵捕获。



## MeCo

问题：
zero-shot / training-free NAS 里，如何在“不训练网络”的前提下，更快、更稳、更少依赖数据与标签地评估一个架构好不好
	​**大多数方法依赖梯度，至少要做一次反向传播**，这仍然有计算开销，不够高效
	**很多方法强依赖输入数据和标签**，这样评估到的更多是“数据/标签条件下的表现”，而不是架构本身的内在性质；如果标签有噪声，还会干扰排序。

​**已有代理的性能还可以进一步提升**，也就是和真实精度的相关性还不够高。







答案：

做出一个比现有 zero-cost proxies 更“轻量”、更“数据无关”、同时排序更准的 NAS 指标？

​	一个随机输入、单次前向传播、无需标签

​	分析**特征图的 Pearson 相关矩阵最小特征值**，

Convolutional Neural Network (CNN)的 minimum eigenvalue of correlation on feature maps

​	多通道卷积层可以转写成一种带约束的“多样本全连接层”

​	借助过参数化网络的理论结果说明，**相关矩阵最小特征值**与训练收敛速度和泛化上界有关。

衍生的问题：

MeCo 对**通道数敏感**，在 NATS-Bench-SSS 这类通道数变化大的空间里会出现负相关，因此他们又提出了 **MeCoopt** 来缓解这个问题；



另外在一些任务上相关性接近 0，说明方法还不是完全通用。





## NEAR

问题：

**如何在不训练模型的前提下，提前估计一个神经网络/机器学习模型最终性能** 

提出一个**更通用、更稳健、更少约束**的训练前性能估计指标

动机：

很多已有 zero-cost proxy 依赖梯度，因此需要标签；还有一些方法虽然不需要反向传播，但往往只适用于 **ReLU**

NEAR 不仅能用于选架构，还可以用于选择**激活函数**和**权重初始化方式**

突破“固定搜索空间”的限制，进一步做层宽估计

​	希望 proxy 不只是“在候选架构里打分”，还能够进一步帮助回答：**某一层应该设多宽？** 



不是只看激活后的特征，同时看：

- **pre-activation matrix**：激活函数之前的输出矩阵
- **post-activation matrix**：激活函数之后的输出矩阵

然后计算这两个矩阵的 **effective rank**，再对所有层求和，得到 **NEAR score**。



问题：

NEAR 本质上主要反映的是**网络表达能力**，而**不直接刻画训练过程本身**，所以它可以预测大趋势，

但对一些**很接近的方案之间的细微差别**，未必能分得很准。
比如在激活函数和初始化方法比较中，它能稳定识别差方案，但对几个性能非常接近的好方案，排序未必完全一致。



## SWAP

问题：

跨不同 search space 和任务的泛化能力弱

**天然偏向更大的模型**，因此在希望找到更小、更经济模型时不够理想。

标准 activation patterns 在高维输入下的饱和与不可区分问题

什么是sample-wise
	 **GradSign**：偏向看样本级的梯度/优化几何一致性
	 **SWAP**：看 ReLU 激活的二值模式去重计数，基本是前向 hook + sign + unique 统计

动机：

“基于表达能力”的方法还有明显缺陷

**标准 activation patterns 在高维输入下很容易饱和**：不同网络算出来的 pattern cardinality 会迅速接近输入样本数上限，导致架构之间变得难以区分。

​	 这正是作者提出 **sample-wise activation patterns** 的直接动机：要设计一个**区分能力更强**的 expressivity 度量

不仅“搜得准”，还要“能控模型大小”

​	很多 training-free metric 有“大模型偏好”，更大的网络往往得分更高，但这未必符合实际需求，因为很多场景希望得到更小、更省算力的模型。



答案：

通过正则化实现**模型尺寸控制**



问题：

靠 **ReLU / 分段线性激活后的二值 activation pattern** 来打分，所以它天然建立在这类激活函数假设上

​	把“扩展到 GELU 等其他激活函数”列为未来工作。

**随着卷积层数量增加，proxy 与真实性能的相关性会急剧下降，甚至变成负相关**。

​	网络越深、非线性越强时，像 SWAP 这种基于激活模式/激活统计的代理，可能会把真正更好的架构打成更差。



## NCD

问题：

当网络卷积更多、非线性更强时，现有 activation-based proxy 的 score magnitude 会被高非线性严重压低，从而导致排名方向反了

为什么 activation-based zero-cost proxies 在卷积更深、非线性更强的架构上会失效，甚至出现与真实性能相反的负相关？以及，如何消除这种负相关，让 training-free NAS 重新变得可靠？

动机：

在深一些、卷积更多的网络上，现有 activation-based proxy **会系统性误判架构优劣**。

​	这些方法大多只依赖简单的二值 activation pattern，却**忽略了架构的非线性能力以及 FLOPs 等结构因素对 proxy score 的影响**。

​	**高非线性会显著压低 AZP score 的幅值**，从而诱发这种负相关。

**现有方法没有真正抓住“非线性”这个关键因素**。

​	其设计仍然没有正确处理**非线性对架构表示模式的影响**。



## W-PCA

现有轻量级语言模型 NAS 要么依赖昂贵的 supernet 训练，要么现有 zero-shot proxy 在语言模型上评价偏置大、效果不佳



究动机是想设计一个真正适合 NLU 场景、无需梯度、只靠单次前向传播就能有效评估架构优劣的 proxy，

​	于是提出了将参数量与 FFN 隐状态 PCA 结合起来的 W-PCA。







## WRCor

问题：

**有些 proxy 对网络结构有特定要求**，通用性不够，比如只适用于 CNN，或者要求 ReLU 等

答案：

pre-activation 特征（替换 ReLU 后激活）

衍生的问题：



## TRNAS





## 改造：

AZ-NAS 获得

- expressivity_hist（逐层熵）
- az_channel_list（逐层通道数）
- expressivity_norm（逐层 H_l/log(C_l) 的均值）

az_info["expressivity"] 放进 az_list

**做了层级归一化再融合**

compute_composite_scores 里先 az_normalize(...)

 做 H_l/log(C_l) 后再层均值，并 clip 到 [0,1]

这就是你之前说的“不是直接用原始 AZ，而是层级归一化”。

- H_l 就是每层的 entropy，来自 az_info["expressivity_hist"]（你常叫 az_hist）。
- C_l 就是每层通道数，来自 az_info["az_channel_list"]（你常叫 az_channel）。

在 az_normalize 里做的是：$\text{az\_norm} = \frac{1}{L} \sum_{t=1}^{L} \frac{H_t}{\log(C_t)}$ 然后再 clip 到 [0,1]。



MeCo

调用时固定了：

- meco_stat="min_eig"
- meco_agg_mode="sum"

MeCo 获得的信息来自pre-activation 特征（替换 ReLU 后激活）

​	现象：MeCo在NB301中随着架构数的增加，SP，KT下滑不严重

每层 MeCo 用 corrcoef 后取 min_eig，并做了原始 MeCo 的 b/k 缩放

进入 composite 时，你又对 MeCo 做了二次处理：

- meco_process = mean(max(hist_l,0)) [aggregated.py (line 310)]
- meco_residualize_by_depth=True（按 depth 做残差化，若 bucket>1 才生效）

最终你当前排序模式是 composite_swap_probe，不是 meco_single。

真正跑的是 pre-activation + min_eig(b/k) + sum(hist)，然后在 composite 里再做 mean(max(hist,0)) 和 depth residual，最后进入 composite_swap_probe。



SWAP

用 ReLU forward hook 收集中间激活，再做二值化模式计数（>0）

模式计数做了位打包优化（uint8 -> int64 -> bitpack -> unique），这是你提速版。

compute_nas_score 增加了 SAM 相关参数：

​	enable_sam / sam_alpha / sam_apply_from_ratio / sam_mask_target / sam_rescale。



SAMHook 改动[SAMHook.py]

- 支持只对后段卷积生效（apply_from_ratio）。
  [SAMHook.py (line 22)]
- 支持掩码目标是 input 或 output（你现在常用 output）。
  [SAMHook.py (line 23)]
- 支持 dropout-style rescale（除以 keep_prob）。
  [SAMHook.py (line 20)]
- 注册时按 conv 列表切后段：start_idx = int(len(convs)*ratio)。
  [SAMHook.py (line 111)]



每个架构会同时算 swap_raw（无 SAM）和 swap_sam（有 SAM）

- swap_raw_feat = log1p(raw)
- swap_robust_feat = -log1p(|raw-sam|)
- swap_sensitivity = |raw-sam|/(|raw|+eps)

- 最终分数不是直接替换 SWAP，而是
  composite + beta * z(swap_robust_feat)；当前 beta=0.10。
  [pred_main_11_az_ex_meco_swap.py (line 649)]
- 排序模式当前是 composite_swap_probe（所以这条注入在生效）。



聚合

1.计算分数

- AZ: az_info["expressivity"]
- MeCo: meco_info["meco"] + meco_hist
- SWAP: swap_raw（并且还会算 swap_sam）

2.层内操作

- AZ 先层归一化（H_l/log(C_l) 层均值）
- MeCo 先做 mean(max(hist_l,0))
- SWAP 做 log1p(swap_raw)

3.MeCo 分支还开了“按 depth 残差化”

- 当前是 meco_residualize_by_depth=True

然后三个分支各自 robust-zscore，再线性相加（权重现在是 (1,1,1)）

4.在 base composite 上加了 SWAP 的 SAM-robust 特征

先算 swap_robust_feat = -log1p(|swap_raw-swap_sam|)

然后 composite_swap_probe = composite + 0.10 * z(swap_robust_feat)



- logE = log(az_norm)
- logS = log(log1p(swap_raw))（swap_proc = log1p(swap_raw) 后再取 log）
- logM = log(meco_proc)（对应 sqrt(MeCo)）

把 0.5 改成 1.0，结果通常几乎一样（除非数值边界情况）。

​	z_logM 基本会被“缩放抵消”（中位数和 MAD/STD 同比例缩放）

做 robust-zscore 标准化，得到 z_logE, z_logS, z_logM

```

def _robust_zscore(arr: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    """Robust z-score using median and MAD.
    z = (x - median) / (MAD or fallback std)
    """
    arr = np.asarray(arr, dtype=float)
    med = np.median(arr)
    mad = np.median(np.abs(arr - med))
    if mad < eps:
        denom = np.std(arr) + eps
    else:
        # Optionally scale MAD to be std-consistent: 1.4826 * mad
        denom = mad * 1.4826 + eps
    return (arr - med) / denom

```



MeCo分箱机制

meco_residualize_by_depth=False,# MeCo的分箱机制

给 **quality_bias 分箱**用的；在你当前代码里 quality_bias 传的是 relu_count_arr，所以是：

- 对 relu_count 做 quantile 分箱（8桶），不是对 depth。

depth 的那条是另一套开关控制的（meco_residualize_by_depth / meco_bucket_rank_by_depth），和 BUCKET_NUM_BINS 不是同一件事。



**按样本量 N 设上界**：保证每箱平均样本数 ≳ `min_count`（建议 `min_count=30` 或至少 15）。
$$
K \le \left\lfloor \frac{N}{\text{min\_count}} \right\rfloor
$$
例：N=500 → K ≤ 16（所以 K=8 很合理）；N=10000 → K ≤ 333（通常取 8–50 更稳）。

**按唯一值设上界**：如果 `relu_count` 的唯一值数 `U` 小于 K，则改为 `K=U` 或合并：没必要把 K>U。

**优先用 quantile bins（等频）**：等频能保证每箱样本数相近，稳定性好（尤其对非均匀分布）。
 但：quantile 会把极端值分到边箱，需在后处理时检查箱大小。

**合并小箱**：如果某些箱样本数 < `min_count_small`（建议 8–15），把它与相邻箱合并（通常跟最近的箱合并）。不要让箱太碎。

**交叉验证 K**：在 200–1000 样本上用网格 `K ∈ {4, 6, 8, 10, 12, 16}` 做验证，挑使 `avg_bucket_corr`（桶内 Spearman 平均） 或 overall Spearman 最优的 K。

**当 N 很大时**（如 10k），K 可取更高（10–20），但仍按 `min_count` 限制。RB201（若 N=10000）可试 10–20。





## NB201，RB201

网络越不敏感，越鲁棒。

### RACL 这类方法的核心信念是：“Lipschitz / sensitivity”思路

**低敏感度**：输入变一点，输出最多会被放大多少倍。

如果存在常数 $L$，使得对任意两个输入 $x_1,x_2$ 都有
$$
\|f(x_1)-f(x_2)\| \le L \|x_1-x_2\|
$$
**$L$ 小**：输入扰动不容易被层层放大，鲁棒性往往更好

**$L$ 大**：一点小扰动就可能把输出推得很远，更容易被攻击	

### 已经用到的论文

Robust_ZCP：构造 **adversarial loss 的上界**

​	用 **NTK** 和 **input loss landscape** 来证明这个 zero-cost proxy 与 adversarial robustness 相关

**AdvRush**：input loss landscape smoothness

**DSRNA**：Jacobian norm bounds / certified bounds

### 替代Lipschitz的常用思路

**Jacobian norm**

**输入扰动前后 feature consistency**

**input loss landscape smoothness**

**adversarial loss upper bound**

谱范数乘积

局部 Lipschitz 上界

certified bound surrogate

### 可能有的思路

AZ-NAS：加一个**局部敏感度分支**：
$$
AZ_{\text{rob}} = AZ_{\text{expr}} - \lambda \|J_x\|
$$
MeCo：与其只看 clean 的 Pearson 相关矩阵，不如比较：
$$
C(x),\; C(x+\delta)
$$
看扰动前后相关结构是否稳定。

SWAP：不要再让 SWAP 直接承担鲁棒 proxy 的任务；更合理的是：

- `swap_raw` 继续做表达性/规模项
- 再单独补一个 consistency / Jacobian / upper-bound 分支



### AdvRush

输入 Hessian 的最大特征值 $\lambda_{\max}(H)$ 来度量这种曲率

算 Hessian 很贵，所以 AdvRush 用了两步近似

用 Hessian 的 Frobenius 范数近似曲率量：
$$
\|H^{std}\|_F = \mathbb{E}\big[\|H^{std} z\|_2\big],\quad z\sim\mathcal N(0,I)
$$
第二步，用**有限差分**近似 Hessian-vector product：
$$
H^{std} z \approx \frac{l(x^{std}+hz)-l(x^{std})}{h},
\quad l(x)=\nabla_x L(f_{super}(\omega^{std}),x)
$$

1. 先算输入梯度 $l(x)=\nabla_x L$
2. 再对输入加一个很小的随机方向扰动 $hz$
3. 比较扰动前后的输入梯度差
4. 用这个差来近似 $H z$
5. 再用它构造一个“曲率正则项”加到 NAS 搜索目标里。

所以从实现角度看，AdvRush 真正抓的量是：

> **输入梯度在小扰动下变化得有多快**

这已经非常接近你想要的“可代理化鲁棒量”了。

WRCor 论文综述里提到过 **NetSens**，就是把 Jacobian 的 $l_1$ 范数当 training-free proxy。AdvRush 比它更进一步：
 不是只看一阶导 $J=\nabla_x f$，而是看**输入梯度对输入的变化**，也就是二阶信息 $H=\nabla_x^2 L$。

TRNAS 的综述表把 **DSRNA** 概括成 “Jacobian Regularization”，把 **AdvRush** 概括成 “Input Loss Landscape Smoothness”。
这两者都属于“从局部几何/敏感度刻画鲁棒性”的路线，只是：

- DSRNA 更偏一阶/界
- AdvRush 更偏二阶曲率

不要直接算全局 Lipschitz，而用这些更便宜的近似：

- 输入梯度范数
- 扰动前后输入梯度差
- Hessian-vector product 近似
- 输入小扰动下 feature / corr matrix 的变化

从 AdvRush 再走一步，就能变成 training-free proxy，例如：
$$
S_{rob} = - \frac{\|\nabla_x L(x+h z)-\nabla_x L(x)\|}{h}
$$
或者更轻量：
$$
S_{rob} = -\|f(x+\delta)-f(x)\|
$$
前者更贴 AdvRush，后者更贴你现在容易实现的 proxy。



### NADAR

从一个已经有不错标准精度的 backbone 出发，对它做“架构扩张 / dilation”，在尽量少增加开销的前提下提高对抗鲁棒性

#### **鲁棒性可以通过“架构扩张”获得，而不是只靠训练算法**

也就是说，某些结构增强本身就有利于 robustness。
这意味着在你设计 proxy 时，可以关注：

- 某个架构是否更“容易被扩张后提升鲁棒性”
- 或某些结构模式是否本身更接近 robust-friendly topology。

**鲁棒性和结构容量/非线性模式有关**

- RACL：减少扰动放大
- NADAR：增加对鲁棒任务更合适的结构容量

对MeCo

- 不要只把相关矩阵看成“线性分离度”
- 还要看这种表征是否具有**鲁棒扩张性**
   也就是更深/更多单元后，相关结构是否仍然健康

这意味着你可以考虑：

- 不同层不等权
- 更偏后层/更深层的 corr 结构
- 或对 deeper stage 的 corr 赋更高权重

SWAP

NADAR 对 SWAP 的启发最直接：

- SWAP 本身已经在吃“非线性/规模/模式容量”
- NADAR 告诉你：这种容量不一定是坏事，尤其对 robustness 可能是有用的
- 所以在 RB201 上，不应该机械地去掉规模，而要区分：
  - 有用的鲁棒容量
  - 纯粹的参数膨胀

### RobNet

When NAS Meets Robustness: In Search of Robust Architectures against Adversarial Attacks

三个核心观察是：**更密集的连接模式更鲁棒**、在计算预算下**把卷积放到直连边上比单纯 skip 更有利于鲁棒性**、以及 **FSP（flow of solution procedure）matrix** 可以作为网络鲁棒性的一个指示器

通过 one-shot/supernet 搜索来发现鲁棒结构，并把 **FSP matrix** 当成 robustness indicator

**dense connectivity / conv-on-direct-edge** 这种**结构模式**与鲁棒性相关；

直观上像：

- 稀疏连接：A → B → C
- 密连接：A → B → C，同时 A 也直接连到 C，甚至更多跨层连接

RobNet 的一个经验结论就是：**更 dense 的连接模式通常更鲁棒**。论文里把这作为搜索后总结出的结构规律之一。

为什么可能有帮助：

- 特征传递路径更多，不容易因为某一条路径被扰动就整体崩掉
- 浅层和深层信息能更充分融合
- 梯度和特征流更稳定

这和你前面看到的 WRCor/CRoZe 那类“一致性/相关结构”思路是相通的：**信息流越稳定、越不容易被单点扰动放大，鲁棒性往往越好。**



**FSP matrix** 这种“层间表征流动/一致性”可以作为 robustness indicator


# 理论

## ZCP-Eval

An Evaluation of Zero-Cost Proxies - from Neural Architecture Performance Prediction to Model Robustness
	“预测 clean accuracy 往往靠少数代理即可，而预测鲁棒性通常必须联合多种代理特征”。

仅用 GRAF 或 Jacobian 类可获得较好效果。
仅用 `zen`（piecewise-linear）或 `hessian` 时性能显著下降（部分任务出现负 R2）。