---
title: "ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION"
method_name: "Robust-ZCP"
authors: [Yuqi Feng, Yuwei Ou, Jiahao Fan, Yanan Sun]
year: 2025
venue: ICLR
tags: [NAS, adversarial-robustness, zero-cost-proxy, NTK]
zotero_collection: ""
image_source: online
arxiv_html: https://openreview.net/forum?id=zHf7hOfeer
local_pdf: D:/PRO/essays/papers/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION.pdf
local_code: D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION
created: 2026-03-15
---

# 论文笔记：Robust-ZCP

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION |
| 会议 | ICLR 2025 |
| OpenReview | https://openreview.net/forum?id=zHf7hOfeer |
| 代码 | https://github.com/fyqsama/Robust_ZCP |
| 本地 PDF | `D:/PRO/essays/papers/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION.pdf` |
| 本地代码 | `D:/PRO/essays/code_depots/ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION` |

## 一句话总结
> 本文提出一个用于 [[Adversarial Robustness]] 评估的 [[Zero-Cost Proxy]]，在不训练网络也不生成对抗样本的前提下，能高效筛选 [[Robust Neural Architecture Search]] 候选结构。

## 核心贡献
1. 给出一个面向鲁棒性的 zero-cost 评分函数 `R`，由初始化权重上的 NTK 项与输入损失地形项组成（Sec. 3.2）。
2. 从 [[Neural Tangent Kernel]] 与 [[Input Loss Landscape]] 两条理论线索解释 proxy 与鲁棒性之间的关系（Sec. 3.3-3.5, Appx A）。
3. 在 DARTS/WRN 搜索空间与 CIFAR-10/ImageNet 等设置上展示显著速度优势，同时保持较强鲁棒精度（Sec. 4.1）。
4. 构建 Tiny-RobustBench 数据集，用于评估 zero-cost proxy 与真实鲁棒精度的相关性（Sec. 4.2.1, Appx C.1）。

## 问题背景
### 要解决的问题
- 现有 robust NAS 为了评估每个架构的鲁棒性，通常需要完整训练甚至对抗训练，成本极高。
- 已有鲁棒 zero-cost proxy（如 CRoZe）仍需要生成对抗样本，速度和理论可解释性都有限。

### 现有方法局限
- 训练式评估慢，难扩展到大量候选架构。
- 需要对抗样本生成的代理在搜索环节仍然昂贵。
- 理论解释不足，难判断 proxy 何时可信。

### 本文动机
- 如果可以只在初始化点用一次性统计量近似鲁棒性，就能在搜索阶段显著降本。

## 方法详解
### 总体评分函数（Eq. 4）
论文将代理分数写为：

$$
R = - \exp\left(\frac{t}{MN^2}\sum_{m=1}^{M}\sum_{i=1}^{N}\sum_{j=1}^{N}
\left(\frac{\partial f_{\theta_0}(x_i)}{\partial \theta_0^m}\right)
\left(\frac{\partial f_{\theta_0}(x_j)}{\partial \theta_0^m}\right)^T
\right)
\cdot
\left\|
\frac{l(x + h z^*) - l(x)}{h}
\right\|_2^2
$$

其中：
- 第一项近似 NTK 最小特征值相关项（Eq. 8）。
- 第二项近似输入 Hessian 最大特征值相关项（Eq. 7）。
- $l(x)=\nabla_x L(\theta_0, x)$，$z^*=\frac{\mathrm{sign}(\nabla_x L(\theta_0,x))}{\|\mathrm{sign}(\nabla_x L(\theta_0,x))\|_2}$。

### 理论思路
1. 从训练误差上界（NTK 理论）出发：损失与 $\lambda_{\min}(\Theta)$ 相关（Eq. 1-3）。
2. 将输入替换为对抗样本，得到对抗损失上界（Eq. 5-6）。
3. 用可零成本近似替代“对抗样本相关项”：
   - 用 $\lambda_{\min}(\Theta_{\theta_0})$ 近似对抗 NTK 项（Eq. 8）。
   - 用输入 Hessian 最大特征值近似局部对抗损失项，并用有限差分近似（Eq. 7）。
4. 组合得到 Eq. 4，避免显式对抗样本生成。

### 复杂度
- 论文给出总体复杂度：$O(MN^2)$（Sec. 3.4）。

## 关键实验结果
### White-box（Table 1, CIFAR-10）
- Ours: Natural 85.60%, FGSM 60.20%, PGD20 52.75%, PGD100 52.51%, APGDCE 52.25%, AA 49.97%。
- 搜索成本 0.017 GPU days，显著低于多数 robust NAS 方法（文中称至少约 20x 提速）。

### Black-box transfer（Table 2）
- 作为 source model 时，Ours 对其他模型产生更强迁移攻击；配对比较显示其目标模型鲁棒性仍有竞争力。

### 跨数据集迁移（Table 3）
- 在 SVHN 上优于 ResNet-18/PDARTS。
- 在 Tiny-ImageNet-200 上自然精度与 FGSM 指标提升明显，PGD20 相对 PDARTS 略弱。

### ImageNet（Table 4）
- Ours: Natural 52.71%, FGSM 19.88%, PGD20 11.96%，优于文中对比的 RACL/AdvRush/CRoZe。

### 相关性评估（Fig. 2-4）
- NAS-Bench-201-R 上：弱攻击时相关性较好，强攻击时相关性退化（作者归因于该数据未对抗训练，精度接近零）。
- Tiny-RobustBench 上：在对比代理中取得最高 Kendall's Tau（图中 Ours 约 0.33）。

## 与代码实现的对照
- 核心搜索脚本：`exps/Robust_ZCP/search_robust.py`
  - 随机采样种子区间 `3000..3999`。
  - 使用 `procedure(...)` 计算鲁棒 proxy 分数并选最大者。
- 核心评分实现：`exps/Robust_ZCP/functions.py`
  - 代码中分数形式为 `RF = -exp(conv * 5000000) * regularizer_average`，对应论文中的指数项乘曲率项。
- 输入曲率近似：`exps/Robust_ZCP/regularizer.py`
  - 通过 `loss_cure.regularizer` 用有限差分梯度差实现地形项近似。
- 实践细节与潜在坑：
  - `search_robust.py` 默认有 `count_normal_skip(genotype) == 1` 的筛选条件。
  - CIFAR 数据目录在脚本内出现硬编码路径（`/home/yuqi/data`），复现实验时需改。

## 批判性思考
### 优点
1. 把“鲁棒性 zero-cost 评估”做成了清晰的两项分解，并给出理论动机。
2. 在搜索成本上优势明显，且在多个攻击设置下精度有竞争力。
3. 提供 Tiny-RobustBench，补上强攻击下 proxy 评估数据缺口。

### 局限
1. 理论推导依赖近似条件（如 NTK 相关假设）；在有限宽网络上的精确性有限。
2. 代理只看初始化点，论文也承认对 skip connection 等结构因素可能有误判。
3. 结论主要基于特定搜索空间与训练设定，跨任务泛化仍需更多验证。

## 关联概念
- [[Zero-Cost Proxy]]
- [[Adversarial Robustness]]
- [[Robust Neural Architecture Search]]
- [[Neural Tangent Kernel]]
- [[Input Loss Landscape]]
- [[NAS-Bench-201]]
- [[Kendall's Tau]]

## 代码
Robust_ZCP

代码位置

- `D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\search_robust.py`
- `D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\functions.py`
- `D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\regularizer.py`
- `D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\lib\utils\utils.py`

核心观察

- `NTK` 项在实现中没有显式构造成标准 `N x N` NTK Gram 矩阵，而是通过多次单样本反传后收集参数梯度，拼出一个压缩的梯度相关性统计量 `conv`。
- `input` 也没有先提一个单独的 embedding 特征；它主要是直接对输入图像求 `loss` 对输入的梯度 `∂L/∂x`，再构造扰动方向 `z`，用有限差分近似输入损失地形项。
- 最终 robust score 在代码里写成 `RF = -exp(conv * 5000000) * regularizer_average`。

搜索入口：如何调用 proxy

```python
# exps/Robust_ZCP/search_robust.py
# D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\search_robust.py

train_transform, valid_transform = utils._data_transforms_cifar10_eval(args)
train_data = dset.CIFAR10(root='/home/yuqi/data', train=True, download=True, transform=valid_transform)

train_loader_1 = torch.utils.data.DataLoader(
    train_data, batch_size=args.batch_size_1, shuffle=True, pin_memory=True, num_workers=0)
train_loader_2 = torch.utils.data.DataLoader(
    train_data, batch_size=args.batch_size_2, shuffle=True, pin_memory=True, num_workers=0)

score_robust, _, _, _ = procedure(
    train_loader_1, train_loader_2, network, criterion, None, None, 'train', grad=False, h=args.h)
```

这里有两个关键点：

- `train_loader_1` 默认 `batch_size_1=1`，主要用于逐次收集梯度，近似 `NTK` 项。
- `train_loader_2` 默认 `batch_size_2=32`，主要用于计算 input-loss-landscape 项。

输入预处理：input 如何进入网络

```python
# lib/utils/utils.py
# D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\lib\utils\utils.py

def _data_transforms_cifar10_eval(args):
  train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
  ])

  valid_transform = transforms.Compose([
    transforms.ToTensor(),
  ])
  return train_transform, valid_transform
```

`search_robust.py` 里实际把 `valid_transform` 传给了 `CIFAR10`，所以这里进入 proxy 的输入基本就是原始图像经过 `ToTensor()` 后的张量，没有标准化。

NTK 相关项：代码里是怎么来的

```python
# exps/Robust_ZCP/functions.py
# D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\functions.py

for i, (inputs, targets) in enumerate(train_loader_1):
    inputs = inputs.cuda()
    targets = targets.cuda(non_blocking=True)
    logits = network(inputs)
    loss = criterion(logits, targets)

    if mode == 'train':
        loss.backward()
        for name, param in network.named_parameters():
            if param.grad is None:
                continue
            if index_name > 10:
                break
            if len(param.grad.view(-1).data[0:100]) < 50:
                continue
            if name in grads:
                grads[name].append(copy.copy(param.grad.view(-1).data[0:100]))
            else:
                grads[name] = [copy.copy(param.grad.view(-1).data[0:100])]

        if len(grads[index_grad]) == 50:
            conv = 0
            for name in grads:
                for i in range(50):
                    grad1 = torch.tensor([grads[name][k][i] for k in range(25)])
                    grad2 = torch.tensor([grads[name][k][i] for k in range(25, 50)])
                    conv += torch.dot(grad1, grad2) / 2500
            break

RF = -torch.exp(conv * 5000000) * regularizer_average
```

这段实现表示：

- 每次取一个样本做前向和反向。
- 遍历参数，只保留前面少数参数张量，并且每个参数张量只截前 `100` 个梯度坐标。
- 收集到 `50` 次梯度快照后，把前 `25` 次和后 `25` 次在同一坐标上的梯度组成两个长度为 `25` 的向量，做点积并累加得到 `conv`。

所以这里更像是“参数梯度相关性的压缩 proxy”，而不是严格把所有样本 Jacobian 拼成标准 NTK 矩阵再做谱分析。

另外一个实现细节是：

```python
# functions.py
# if mode == 'train': optimizer.zero_grad()
```

这一行被注释了，所以代码里收集到的是累计梯度，不是严格独立的逐样本梯度。

Input loss landscape 项：input 如何被“提特征”

```python
# exps/Robust_ZCP/regularizer.py
# D:\PRO\essays\code_depots\ZERO-COST PROXY FOR ADVERSARIAL ROBUSTNESS EVALUATION\exps\Robust_ZCP\regularizer.py

def _find_z(self, inputs, targets, h):
    inputs.requires_grad_()
    outputs = self.net.eval()(inputs)
    loss_z = self.criterion(outputs, targets)
    loss_z.backward()
    grad = inputs.grad.data + 0.0
    z = torch.sign(grad).detach() + 0.
    z = 1. * h * (z + 1e-7) / (
        z.reshape(z.size(0), -1).norm(dim=1)[:, None, None, None] + 1e-7)
    self.net.zero_grad()
    return z, norm_grad

def regularizer(self, inputs, targets, h=3., lambda_=4):
    z, norm_grad = self._find_z(inputs, targets, h)
    inputs.requires_grad_()
    outputs_pos = self.net.eval()(inputs + z)
    outputs_orig = self.net.eval()(inputs)
    loss_pos = self.criterion(outputs_pos, targets)
    loss_orig = self.criterion(outputs_orig, targets)
    grad_diff = torch.autograd.grad((loss_pos - loss_orig), inputs)[0]
    reg = grad_diff.reshape(grad_diff.size(0), -1).norm(dim=1)
    return torch.sum(self.lambda_ * reg) / float(inputs.size(0)), norm_grad
```

这里的 “input 特征提取” 其实是输入敏感性提取：

- 先求 `∂L/∂x`。
- 用 `sign(∂L/∂x)` 构造归一化方向 `z`。
- 再比较 `x + z` 和 `x` 两点的损失差。
- 对这个差再对 `input` 求梯度，得到 `grad_diff`。
- 把 `grad_diff` 的样本内向量范数作为输入地形项 `regularizer_average`。

因此，Robust_ZCP 的 input 侧 proxy 不是显式中间层 feature，而是“输入梯度 + 有限差分曲率近似”。