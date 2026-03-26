---
title: "Training-Free Robust Neural Network Search Via Pruning"
method_name: "RTP-NAS"
authors: [Qiancheng Yang, Yong Luo, Bo Du]
year: 2024
venue: ICME
tags: [NAS, robust-nas, training-free-nas, pruning, adversarial-robustness, UAP]
zotero_collection: ""
image_source: online
arxiv_html: "https://doi.org/10.1109/ICME57554.2024.10687950"
local_pdf: "D:/PRO/essays/papers/Training-Free Robust Neural Network Search Via Pruning.pdf"
created: 2026-03-25
---

# 论文笔记：RTP-NAS

## 元信息
| 项目 | 内容 |
|---|---|
| 论文 | Training-Free Robust Neural Network Search Via Pruning |
| 会议 | ICME 2024 |
| DOI | https://doi.org/10.1109/ICME57554.2024.10687950 |
| 代码 | 论文 PDF 中未给出可访问链接（文中仅称会公开） |
| 本地 PDF | `D:/PRO/essays/papers/Training-Free Robust Neural Network Search Via Pruning.pdf` |

## 一句话总结

> RTP-NAS 先用 [[Universal Adversarial Perturbation]] 构造可迁移的 [[Adversarial Input Space]]，再用对抗空间中的 [[Neural Tangent Kernel]] 条件数和 [[Linear Regions]] 对候选算子做训练前剪枝，从而在不逐个候选做对抗训练的情况下搜索鲁棒架构。

## 核心贡献

1. 提出鲁棒 training-free NAS 框架 RTP-NAS，降低“架构质量”和“对抗训练细节”之间的耦合。
2. 在对抗输入空间中联合两个指标做评分：
   - 对抗 NTK 条件数（可训练性）；
   - 线性区域数量（表达能力）。
3. 搜索阶段使用 UAP，而不是逐样本 PGD，降低评估成本并提高跨架构可迁移性。
4. 在 CIFAR-10/100 上获得优于多种鲁棒 NAS 基线的 clean/robust 准确率，搜索约 1 小时。

## 问题背景

### 难点

- 鲁棒 NAS 通常需要反复对候选架构做对抗训练评估。
- 这会带来高成本，并把架构本身效果和训练策略/超参/优化器因素混在一起。

### RTP-NAS 的思路

- 把评估迁移到一个共享的对抗输入空间里进行。
- 先用训练前结构指标做筛选和剪枝，再进行最终昂贵训练。

## 方法细节

### 1) 基于 UAP 的对抗空间构造

给定干净数据集 \(D_S=\{(x_i,y_i)\}_{i=1}^N\)，构造通用扰动 \(v\)，使：

$$
\mathcal{C}(x_i+v)\neq y_i,\quad \|v\|_p \le \epsilon
$$

对多数 \(x_i\in D_S\) 成立。  
Source: Sec. 3.1, Eq. (6).

无目标 UAP 优化目标：

$$
L_U = \max\left(C_{gt}(x_i+v)-\max_{j\neq gt} C_j(x_i+v), -\kappa\right)
$$

Source: Sec. 3.1, Eq. (7).

构造对抗空间：

$$
D_A = \{(x_i+v, y_i)\}_{i=1}^N
$$

Source: Sec. 3.1, Eq. (8).

### 2) 对抗 NTK + 线性区域剪枝信号

标准 NTK：

$$
H(x,x') = J(x)J(x')^T
$$

Source: Sec. 2.1, Eq. (1).

对抗 NTK：

$$
H_A(x+v, x'+v)=J(x+v)J(x'+v)^T
$$

Source: Sec. 3.2, Eq. (9).

对每个候选算子 \(o_i\)，计算移除后的变化量：

$$
\Delta \kappa_{A,t,o_i} = \kappa_{N_t} - \kappa_{N_t\setminus o_i}
$$
$$
\Delta R_{t,o_i} = R_{N_t} - R_{N_t\setminus o_i}
$$

Source: Sec. 3.2, Eq. (10)-(11).

排序并融合打分：

$$
\text{Score}(o_i) = R_d(\Delta \kappa_{A,t,o_i}) + R_a(\Delta R_{t,o_i})
$$

Source: Sec. 3.2, Eq. (12)-(14).

每轮每条边剪掉分数最小的算子：

$$
N_{t+1}=N_t\setminus o_m
$$

Source: Sec. 3.2, Eq. (15).

### 3) 搜索流程

1. 在干净数据上预训练源模型（仅用于生成 UAP）。
2. 在 \(\epsilon\) 约束下生成 UAP。
3. 构造对抗输入空间 \(D_A\)。
4. 用 Kaiming 初始化超网。
5. 用“对抗 NTK 条件数 + 线性区域”迭代评分并剪枝。
6. 收敛到单路径风格架构后，再做标准对抗训练和评估。

Source: Sec. 3, Fig. 1.

## 关键实验结果

### 主结果（Table 1）

#### CIFAR-10（所有模型均经对抗训练）

| Model | Params | Clean | FGSM | PGD20 | PGD100 | AA |
|---|---:|---:|---:|---:|---:|---:|
| RNAS | 3.6M | 83.94 | 56.09 | 50.77 | 50.49 | 48.86 |
| AdvRush | 4.2M | 84.26 | 58.76 | 52.33 | 51.46 | 49.05 |
| DenseNet-121 | 7.0M | 84.88 | 59.69 | 51.76 | 51.33 | 49.96 |
| **RTP-NAS** | **3.7M** | **85.70** | **59.92** | **53.11** | **52.76** | **50.14** |

#### CIFAR-100

| Model | Clean | FGSM | PGD20 | PGD100 | AA |
|---|---:|---:|---:|---:|---:|
| DenseNet-121 | 61.44 | 32.86 | 28.51 | 27.99 | 25.38 |
| AdvRush | 59.68 | 33.13 | 28.98 | 28.76 | 26.46 |
| **RTP-NAS** | 60.71 | **34.92** | **31.04** | **30.92** | **27.15** |

解读：
- RTP-NAS 在保持参数量适中的同时，鲁棒精度整体更高。
- 从 CIFAR-10 搜索出的架构迁移到 CIFAR-100 仍表现稳定。

### 指标消融（Table 2）

| Metric | Clean | PGD20 |
|---|---:|---:|
| \(\kappa\) only | 79.68 | 48.11 |
| \(\kappa_A\) only | 81.41 | 49.72 |
| linear regions only | 78.88 | 49.40 |
| \(\kappa +\) linear regions | 79.99 | 50.21 |
| **RTP-NAS** | **85.70** | **53.11** |

结论：
- 在鲁棒搜索中，对抗版 \(\kappa_A\) 优于干净空间 \(\kappa\)。
- 可训练性与表达性两个信号联合最有效。

### UAP 来源与扰动预算消融（Table 3）

- 由 VGG 系列模型生成的 UAP，最终搜索到的鲁棒架构优于 ResNet56 来源（即使后者 fooling ratio 更高）。
- 扰动预算从 `10/255` 增加到 `20/255` 时，最终鲁棒指标进一步提升。

## 优点

1. 思路清晰：先评估架构内在鲁棒信号，再进行最终训练。
2. 搜索效率高：避免对每个候选做完整对抗训练。
3. 消融实验完整：指标设计和对抗空间构造都被验证。

## 局限

1. 最终鲁棒性仍依赖下游对抗训练配方，未完全脱离训练策略影响。
2. UAP 源模型选择会影响结果，引入额外设计自由度。
3. 主要验证在 CIFAR 规模和 DARTS 风格空间，大规模泛化仍待验证。
4. 论文 PDF 内未提供官方代码链接。

## 可复现性检查

- [x] 本地 PDF 已归档
- [ ] 官方代码已归档（未找到）
- [x] 关键公式已提取
- [x] 关键结果表已提取
- [x] 搜索/剪枝流程可追溯到章节与公式

## 相关概念

- [[Training-free NAS]]
- [[Robust Neural Architecture Search]]
- [[Adversarial Robustness]]
- [[Universal Adversarial Perturbation]]
- [[Adversarial Input Space]]
- [[Neural Tangent Kernel]]
- [[Condition Number]]
- [[Linear Regions]]
- [[Differentiable Architecture Search]]
- [[Cell-based Search Space]]
- [[FGSM]]
- [[PGD Attack]]
- [[AutoAttack]]


## 操作
“利用免训练代理的计算结果，来融合生成最终的边得分（Edge Score）”
### 🌟 RTP-NAS 核心架构：免训练鲁棒网络搜索 (三步走战略)

**核心思想**：彻底抛弃耗时的“对抗训练”，在网络**初始化阶段（免训练）**，利用**极速剪枝**做减法，找出天生最抗揍的网络架构。

#### 📍 第一步：构建“通用对抗试炼场” (UAP Generation)
* **具体操作**：利用一个已有的预训练模型，在数据集上提前算出一个**通用对抗扰动（UAP）**，并将其叠加到干净的图片上。
* **核心目的**：
  * **解耦训练配方**：为所有未经训练的候选架构提供一个统一、公平的“抗击打测试环境”。
  * **极大降低成本**：UAP 具有跨架构迁移性，不需要为超网里成千上万个网络单独生成攻击样本，攻击生成成本从 $O(N)$ 骤降为 $O(1)$。

#### 📍 第二步：计算两大免训练代理指标 (Training-Free Indicators)
* **具体操作**：将加了 UAP 的对抗数据喂给未经训练的候选网络，通过前向传播（不反向传播更新权重），测量网络天生的数学底子。
* **两个核心指标**：
  1. **对抗 NTK 条件数 ($\kappa_A$)**：衡量 **“可训练性”**。$\kappa_A$ 越小越好，代表网络损失函数的地形越平滑（像圆碗），在后续对抗训练中不容易发生梯度爆炸。
  2. **对抗线性区域数量 ($R_{\mathcal{N},\theta}$)**：衡量 **“表达能力”**。数量越大越好，代表网络能把空间切分得越细，内部表征冗余度极高，更有空间去化解和吸收对抗噪声。

#### 📍 第三步：基于排名的留一法极速剪枝 (LOO Pruning)
* **具体操作**：
  1. **逐个试探 (Masking)**：在满配的超网中，挨个“临时遮蔽”某一条边上的算子（比如拿掉 $3\times3$ 卷积），看看去掉它之后，整个网络的 $\kappa_A$ 和 $R_{\mathcal{N},\theta}$ 恶化了多少（计算差值 $\Delta$）。
  2. **双重排名打分 (Ranking)**：因为 $\kappa_A$ 和 $R_{\mathcal{N},\theta}$ 单位（量纲）不同不能直接相加，所以对所有算子的**恶化差值进行排名**。差值越大（拿掉它网络崩了），排名越高。
  3. **末位淘汰 (Pruning)**：把 $\kappa_A$ 排名和 $R$ 排名相加得到“综合得分”。把综合得分**最低**（即拿掉它对网络影响最小的“废件”）的算子**永久剪除**。
  4. **循环迭代**：不断重复“评估 $\rightarrow$ 排名 $\rightarrow$ 剪除”的过程，像剥洋葱一样，直到超网坍缩成唯一的“最优单路径架构”。

---

**💡 笔记附加高光点 (可用于对比或扩展)**：
* **vs. LRNAS (Shapley)**：RTP-NAS 选择留一法（LOO）放弃了 Shapley 的全局公平性，是对“免训练模糊代理”和“算力成本”最聪明的工程妥协，换来了极速（1小时内搜完）。
* **vs. TRNAS (进化算法)**：RTP-NAS 是在满配超网里**做减法（剪枝）**，而传统方法大多是独立采样**做加法/筛选（进化）**。