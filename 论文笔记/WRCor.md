---
title: "Zero-Shot Neural Architecture Search with Weighted Response Correlation"
method_name: "WRCor"
authors: [Kun Jing, Luoyu Chen, Jungang Xu, Jianwei Tai, Yiyu Wang, Shuaimin Li]
year: 2025
venue: arXiv
tags: [NAS, zero-shot-nas, training-free-proxy, response-correlation]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/2507.08841v2
local_pdf: D:/PRO/essays/papers/Jing 等 - 2025 - Zero-Shot Neural Architecture Search with Weighted Response Correlation.pdf
local_code: D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation
created: 2026-03-14
---

# 论文笔记：WRCor

## 元信息

| 项目 | 内容 |
|---|---|
| 论文 | Zero-Shot Neural Architecture Search with Weighted Response Correlation |
| arXiv | https://arxiv.org/abs/2507.08841 |
| HTML | https://arxiv.org/html/2507.08841v2 |
| 代码 | https://github.com/kunjing96/ZSNAS-WRCor |
| 本地 PDF | `D:/PRO/essays/papers/Jing 等 - 2025 - Zero-Shot Neural Architecture Search with Weighted Response Correlation.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/Zero-Shot Neural Architecture Search with Weighted Response Correlation` |

## 一句话总结

> 论文提出 [[Weighted Response Correlation]]（WRCor）：在未训练网络上统计不同样本在多层激活与梯度响应的相关系数矩阵，并对高层响应做指数加权，以更稳健地做 zero-shot NAS 排序。

## 核心贡献

1. 提出基于“响应相关性”的统一代理框架：同时覆盖可表达性（activation）与泛化相关性（gradient）。
2. 提出按层指数加权的 WRCor（底层到顶层权重 `2^l`），强调高层语义区分能力（Sec. 3.3.2, Eq. (10)-(11)）。
3. 提出投票代理 SPW/SJW，在不同搜索空间和设置下提升稳健性（Sec. 3.3.3）。
4. 在 NAS-Bench-101/201 和 MobileNetV2 搜索空间给出 zero-shot NAS 结果；RE-SJW 在 ImageNet-1k 上以 0.17 GPU day 达到 21.9% top-1 error（Table 10）。

## 问题背景

### 要解决的问题

现有 zero-shot proxy 往往在“效果、稳定性、泛化性”三者之间顾此失彼，且并不总能稳定优于 Params/FLOPs 这类朴素基线。

### 现有方法局限

- 很多 proxy 只刻画单一侧面（仅表达性或仅可训练性）。
- 部分 proxy 对结构或激活函数有额外约束，通用性不足。
- 搜索空间变大时，相关性指标可能明显退化（如 NB101 相比 NB201）。

### 本文动机

作者认为架构质量可由“跨样本响应是否线性独立”刻画，并且高层响应更关键，因此构造 response-correlation + layer weighting 的 proxy。

## 方法详解

### 1) 响应定义

- 响应包括：激活（activations）和对隐藏特征图的梯度（gradients）。
- 核心统计对象：同一层中，不同输入样本之间的相关系数矩阵（Sec. 3.1, 3.2）。

### 2) ACor / GCor / RCor

- ACor：仅聚合激活相关矩阵，偏向表达性。
- GCor：仅聚合梯度相关矩阵，偏向训练动态/泛化能力。
- RCor：把激活与梯度相关矩阵统一到同一 log-det 评分形式（Eq. (8)-(9)）。

### 3) WRCor（核心）

- 观察：好模型更依赖高层特征做区分，顶层响应相关性更能反映最终可分性。
- 设计：对层级相关矩阵做指数加权（bottom-to-top），权重随层数几何增长（Eq. (10)-(11)）。
- 直觉：允许底层存在一定相关性，但更强调顶层“跨样本可区分性”。

### 4) 投票代理 SPW / SJW

- SPW: SynFlow + PNorm + WRCor。
- SJW: SynFlow + JacCor + WRCor。
- 使用多数投票整合多 proxy，缓解单一 proxy 的场景脆弱性（Sec. 3.3.3）。

### 5) 搜索策略

- 随机搜索（R）
- 强化学习（RL，policy gradient）
- 规则化进化（RE，tournament + mutation）
- 最终都从探索集合中选 proxy 评分最优架构（Sec. 3.4, Alg. 1-2）。

## WRCor 免训练代理设计流程（含代码定位）

代码地址：D:\PRO\essays\code_depots\Zero-Shot Neural Architecture Search with Weighted Response Correlation

下面按“实际执行链路”说明 WRCor 如何在**不训练完整网络**的前提下给出架构分数。

### Step 0: 注册并暴露 WRCor 指标

1. 指标注册：`@measure('act_grad_cor_weighted', bn=True, mode='param')`  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:6-7`
2. 全量加载到可用指标表：`load_all()` 导入 `act_grad_cor_weighted`  
   代码：`foresight/pruners/measures/__init__.py:63,67`
```
@measure('act_grad_cor_weighted', bn=True, mode='param')
def compute_act_grad_cor_weighted(net, device, inputs, targets, mode, loss_fn, split_data=1):

    def get_counting_forward_hook(weight):
        def counting_forward_hook(module, inp, out):
            try:
                if isinstance(inp, tuple):
                    inp = inp[0]
                inp = inp.view(inp.size(0), -1)
                act_corrs = np.corrcoef(inp.detach().cpu().numpy())
                if np.sum(np.isnan(act_corrs)) == 0:
                    net.K = net.K + weight * (np.abs(act_corrs))
                    #net.N = net.N + weight
            except Exception as e:
                print(e)
        return counting_forward_hook
```

### Step 1: 搜索器调用代理评分入口

1. 每个候选架构在 `eval_arch` 中调用 `predictive.find_measures(...)` 计算零训练代理  
   代码：`search.py:184-188`
```
        measures, _ = predictive.find_measures(net, 
                                               self.train_loader, 
                                               (self.dataload, self.dataload_info, get_num_classes(self.dataset)),
                                               self.device,
                                               measure_names=self.measures)
```
2. `find_measures_arrays` 遍历 `measure_names`，通过 `measures.calc_measure(...)` 分发到具体实现  
   代码：`foresight/pruners/predictive.py:54-58`，`foresight/pruners/measures/__init__.py:30-31`
3. 输入批次来自训练集小批量（`random`/`grasp`），不是完整训练过程  
   代码：`foresight/pruners/predictive.py:41-45`，`foresight/pruners/p_utils.py:8-17,19-39`
```
def get_some_data(train_dataloader, num_batches, device):
    traindata = []
    dataloader_iter = iter(train_dataloader)
    for _ in range(num_batches):
        traindata.append(next(dataloader_iter))
    inputs  = torch.cat([a for a,_ in traindata])
    targets = torch.cat([b for _,b in traindata])
    inputs = inputs.to(device)
    targets = targets.to(device)
    return inputs, targets


def get_some_data_grasp(train_dataloader, num_classes, samples_per_class, device):
    datas = [[] for _ in range(num_classes)]
    labels = [[] for _ in range(num_classes)]
    mark = dict()
    dataloader_iter = iter(train_dataloader)
    while True:
        inputs, targets = next(dataloader_iter)
        for idx in range(inputs.shape[0]):
            x, y = inputs[idx:idx+1], targets[idx:idx+1]
            category = y.item()
            if len(datas[category]) == samples_per_class:
                mark[category] = True
                continue
            datas[category].append(x)
            labels[category].append(y)
        if len(mark) == num_classes:
            break

    x = torch.cat([torch.cat(_, 0) for _ in datas]).to(device) 
    y = torch.cat([torch.cat(_) for _ in labels]).view(-1).to(device)
    return x, y

```



### Step 2: 在 ReLU 层挂钩，收集激活与梯度响应

1. 遍历网络层（`cells/layers/block_list`），对每个 ReLU 注册 forward/backward hook  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:41-47`
```

    modules = net.cells if hasattr(net, 'cells') else net.layers if hasattr(net, 'layers') else net.block_list if hasattr(net, 'block_list') else None
    for i, module in enumerate(modules):
        for name, m in module.named_modules():
            if 'ReLU' in str(type(m)):
            #if isinstance(m, torch.nn.ReLU):
                m.register_forward_hook(get_counting_forward_hook(2**i))
                m.register_backward_hook(get_counting_backward_hook(2**i))

```
2. NAS-Bench-201 的 `lastact` 也单独注册 hook  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:48-53`
```
    if hasattr(net, 'lastact'): # for nasbench201
        for name, m in net.lastact.named_modules():
            if 'ReLU' in str(type(m)):
            #if isinstance(m, torch.nn.ReLU):
                m.register_forward_hook(get_counting_forward_hook(2**len(modules)))
                m.register_backward_hook(get_counting_backward_hook(2**len(modules)))

```


3. 层权重用 `2**i`（越深层权重越大）实现 Eq. (11) 的指数加权  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:46-47,52-53`
```
m.register_forward_hook(get_counting_forward_hook(2**len(modules)))
m.register_backward_hook(get_counting_backward_hook(2**len(modules)))

```


### Step 3: 构建相关矩阵并加权累加到 K

1. Forward hook：把激活 reshape 成 `[batch, -1]`，计算 `np.corrcoef`，累加 `weight * |C^A|` 到 `net.K`  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:14-18`
2. Backward hook：对梯度做同样操作，累加 `weight * |C^G|` 到 `net.K`  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:28-31`
3. 对 NaN 相关矩阵进行跳过保护，避免污染评分  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:16,30`
```
    def get_counting_forward_hook(weight):
        def counting_forward_hook(module, inp, out):
            try:
                if isinstance(inp, tuple):
                    inp = inp[0]
                inp = inp.view(inp.size(0), -1)
                act_corrs = np.corrcoef(inp.detach().cpu().numpy())
                if np.sum(np.isnan(act_corrs)) == 0:
                    net.K = net.K + weight * (np.abs(act_corrs))
                    #net.N = net.N + weight
            except Exception as e:
                print(e)
        return counting_forward_hook

    def get_counting_backward_hook(weight):
        def counting_backward_hook(module, grad_input, grad_output):
            try:
                if isinstance(grad_input, tuple):
                    grad_input = grad_input[0]
                grad_input = grad_input.view(grad_input.size(0), -1)
                grad_corrs = np.corrcoef(grad_input.detach().cpu().numpy())
                if np.sum(np.isnan(grad_corrs)) == 0:
                    net.K = net.K + weight * (np.abs(grad_corrs))
                    #net.N = net.N + weight
            except Exception as e:
                print(e)
        return counting_backward_hook
```

### Step 4: 单次前后向触发 hooks（无完整训练）

1. 初始化 `K` 为零矩阵（按 batch 大小）  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:56-60`
2. 对小批次做一次 forward，计算 loss 后 `loss.backward()`，由 backward 自动触发梯度相关采样  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:65-67`
3. 可选 `split_data` 分块以缓解显存压力（OOM 时在外层自动增大分块数）  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:57-64`，`foresight/pruners/predictive.py:63-72`

```
    s = []
    N = inputs.shape[0]
    for sp in range(split_data):
        net.zero_grad()
        net.K = np.zeros((N//split_data, N//split_data))
        #net.N = 0

        st=sp*N//split_data
        en=(sp+1)*N//split_data

        outputs = net(inputs[st:en])
        loss = loss_fn(outputs, targets[st:en])
        loss.backward()
        #if net.N != 0:
        #    s.append(hooklogdet(net.K / net.N))
        s.append(hooklogdet(net.K))
    #act_grad_cor_weighted = np.mean(s)
    act_grad_cor_weighted = np.prod(s)


```


### Step 5: log-det 打分并返回 WRCor 分数

1. 对聚合矩阵 `K` 计算 `np.linalg.slogdet(K)` 的 log-det  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:37-39`
```
    def hooklogdet(K):
        s, ld = np.linalg.slogdet(K)
        return ld

```
2. 当前实现把每个 split 的得分收集到 `s` 后取 `np.prod(s)` 作为最终 `act_grad_cor_weighted`  
   代码：`foresight/pruners/measures/act_grad_cor_weighted.py:70-74`
```
        s.append(hooklogdet(net.K))
    #act_grad_cor_weighted = np.mean(s)
    act_grad_cor_weighted = np.prod(s)

```

### Step 6: 在搜索中作为单指标或投票指标使用

1. 直接作为排序分数参与 random / RL / evolution 搜索的 `best` 更新  
   代码：`search.py:226-233,386-393,520-537`
```
        for i in tqdm(range(self.N)):
            arch     = self.sample_arch()
            measures, eval_time = self.eval_arch(arch)
            total_eval_time += eval_time
            cur = (arch, measures)
            history.append(cur)
            best = cur if best is None else max([cur, best], key=cmp_to_key(self.cmp))
        return best, history, total_eval_time


        for i in tqdm(range(self.N)):
            log_prob, arch = self.select_generate()
            measures, eval_time = self.eval_arch(arch)
            total_eval_time += eval_time
            cur = (arch, measures)
            history.append(cur)
            best = cur if best is None else max([cur, best], key=cmp_to_key(self.cmp))

            reward = sum([(measures[k]-measures_mean[j])/measures_std[j] for j, k in enumerate(self.measures)])
            if not (np.isnan(reward) or np.isinf(reward)):
                self.baseline.update(reward)
                if self.search_space == 'nasbench101':
                    policy_loss = (-log_prob[0] * (reward - self.baseline.value())).sum() + (-log_prob[1] * (reward - self.baseline.value())).sum()
                elif self.search_space == 'nasbench201':
                    policy_loss = (-log_prob * (reward - self.baseline.value())).sum()
                elif self.search_space == 'MobileNetV2':
                    policy_loss = sum([(-x * (reward - self.baseline.value())).sum() for x in log_prob])
                else:
                    raise ValueError('There is no {:} search space.'.format(self.search_space))
                self.optimizer.zero_grad()
                policy_loss.backward()
                self.optimizer.step()
            else:
                print('No updating!')

        return best, history, total_eval_time

        for i in tqdm(range(self.N)):
            '''if i < self.N / 2:
                lambd = (self.N - 2*i) / self.N
                p = lambd + 0.1 * (1 - lambd)
            else:
                p = 0.1'''
            p = 1.0
            samples  = random.sample(population, self.tournament_size)
            parent   = max(samples, key=cmp_to_key(self.cmp))
            child    = self.mutate(parent[0], p)
            measures, eval_time = self.eval_arch(child)
            total_eval_time += eval_time
            cur = (child, measures)
            population.append(cur)
            history.append(cur)
            population.popleft()
            best = cur if best is None else max([cur, best], key=cmp_to_key(self.cmp))
        return best, history, total_eval_time


```
2. 实验命令中常与 `synflow`、`jacob_cor` 组合形成 SJW 风格投票  
   代码：`README.md:26-30`

## 关键公式

### Eq. (1): 相关矩阵聚合

$$
\mathbf{K}^{A/G}=\sum_{i=1}^{N_a}|\mathbf{C}^{A/G}_i|^{x}
$$

含义：对层内多个响应单元的相关矩阵做聚合，得到架构级统计矩阵。  
符号：
- \(\mathbf{C}^{A/G}_i\)：第 \(i\) 个激活/梯度响应的样本相关矩阵
- \(N_a\)：响应单元数
- \(x \in [0,1]\)：幂次系数

### Eq. (8)-(9): RCor

$$
S_{\text{RCor}}=\log(\det(\mathbf{K})),\quad
\mathbf{K}=\sum_i\left(|\mathbf{C}^{A}_i|+|\mathbf{C}^{G}_i|\right)
$$

含义：统一使用 log-det 将“跨样本线性独立性”映射为标量分数。  
分数越高，意味着非对角相关更小，样本响应更独立。

### Eq. (10)-(11): WRCor

$$
S_{\text{WRCor}}=\log(\det(\mathbf{K})),\quad
\mathbf{K}=\sum_{l=1}^{L}\sum_{i=1}^{N_a^l}2^l\cdot\left(|\mathbf{C}^{A}_{l,i}|+|\mathbf{C}^{G}_{l,i}|\right)
$$

含义：在 RCor 基础上对层级做指数加权，强化顶层响应贡献。  
符号：
- \(l\)：层索引（由浅到深）
- \(L\)：层数
- \(N_a^l\)：第 \(l\) 层非线性单元数

## 关键图表

### Figure 1（方法总览）

- 展示从前向/反向响应提取相关矩阵，再经加权聚合与 log-det 得到 WRCor 分数的流程。

### Figure 2（代理分数 vs 真实精度）

- WRCor 的散点分布更紧凑，和 test accuracy 呈现更好的单调关系（优于 SynFlow/JacCor，接近 ValAcc）。

### Table 2（CIFAR-10, NB201）

- WRCor real Spearman \(\rho=0.812\)，优于 NASWOT(0.780)、ZiCo(0.800)、RCor(0.803)。

### Table 3（加权策略消融）

- `expb2t`（WRCor）优于 no/linear/quad/expt2b；验证“高层更重要”假设。

### Table 4/5/6/7（跨数据集/批大小/初始化/搜索空间）

- WRCor 在 NB201 上整体稳定且强；NB101 上虽然下降，但仍优于多数基线。
- 使用随机噪声输入时 WRCor 仍有竞争力（Sec. 4.2）。

### Table 8/9（NAS-Bench 搜索）

- WRCor 与 SJW 在多搜索策略下显著优于 ZeroCost，且代价远低于 ValAcc-based 搜索。

### Table 10/11（MobileNetV2 + ImageNet-1k）

- RE-SJW: top-1 error 21.9%，FLOPs 592M，搜索代价 0.17 GPU day。
- 与 ZiCo/AZ-NAS 精度接近，但搜索代价更低或相当。

## 与代码实现的对照

- 关键实现位于 `foresight/pruners/measures/act_grad_cor_weighted.py`：
  - 在 ReLU 模块注册 forward/backward hook，分别收集输入激活和梯度相关矩阵。
  - 用 `weight = 2**i` 做层级指数加权，对应 Eq. (11)。
  - 用 `np.linalg.slogdet` 计算 log-det 分数。
- 未加权版本在 `act_grad_cor.py`，对应 RCor 思路。
- 搜索流程与论文 Alg. 1/2 对应代码在 `search.py`（`RL_NAS` / `Evolved_NAS` / `Random_NAS`）。
- 实现细节补充：代码默认 measure 名为 `act_grad_cor_weighted`，在 README 中与 `synflow + jacob_cor` 组合复现 SJW 风格搜索。

## 批判性思考

### 优点

1. 代理构造简洁，直接从统计矩阵出发，解释性强。
2. 在大量 setting 下结果稳定，且兼顾 proxy 质量与搜索效率。
3. 代码公开，关键模块与论文叙述一致，可追踪性好。

### 局限

1. 在更大搜索空间（NB101）上 WRCor/SJW 的相关性仍明显退化。
2. 论文也承认不存在“单一全场景最优 proxy”，因此仍依赖投票融合。
3. 相关矩阵与 log-det 对 batch 和数值稳定性仍有工程敏感性（虽然实验证明总体可控）。

### 可复现性评估

- [x] 论文公开
- [x] 官方代码公开
- [x] 本地代码已归档
- [x] 关键公式/算法/实验均可追踪

## 关联概念

- [[Neural Architecture Search]]
- [[Training-free NAS]]
- [[Zero-Cost Proxy]]
- [[Spearman's Rank Correlation]]
- [[Weighted Response Correlation]]
- [[Proxy Voting]]

