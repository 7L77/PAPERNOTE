---
title: "AdvRush_ch"
type: method
language: zh-CN
source_method_note: "[[AdvRush]]"
source_paper: "AdvRush: Searching for Adversarially Robust Neural Architectures"
source_note: "[[AdvRush]]"
authors: [Jisoo Mok, ByungMin Kim, Jihoon Park, Sungroh Yoon]
year: 2021
venue: ICCV
tags: [nas-method, zh, robust-nas, differentiable-nas, adversarial-robustness]
created: 2026-03-15
updated: 2026-03-15
---

# AdvRush 中文条目

## 一句话总结
> AdvRush 在 DARTS 双层优化框架中，先 warm-up，再在架构参数更新里加入输入损失景观平滑项 `L_lambda`，从而搜索出更抗攻击的结构。

## 来源
- 论文: [AdvRush: Searching for Adversarially Robust Neural Architectures](https://arxiv.org/abs/2108.01289)
- HTML: https://arxiv.org/html/2108.01289
- CVF: https://openaccess.thecvf.com/content/ICCV2021/html/Mok_AdvRush_Searching_for_Adversarially_Robust_Neural_Architectures_ICCV_2021_paper.html
- 本地补充材料: `D:/PRO/essays/papers/AdvRush Searching for Adversarially Robust Neural Architectures Supplemental.pdf`
- 代码: 本次核查中未在 CVF/arXiv/supp 链接中找到官方仓库
- 英文方法笔记: [[AdvRush]]
- 论文笔记: [[AdvRush]]

## 适用场景
- 问题类型: 面向图像分类的鲁棒神经架构搜索。
- 前提假设: 搜索空间可微，且可使用 DARTS 风格双层优化。
- 数据形态: 监督学习 + 对抗训练/评估。
- 规模与约束: 希望在不大改 DARTS 管线的前提下提升鲁棒性。
- 适用原因: 把鲁棒性信号放到架构更新目标里，而不只放在最终训练阶段。

## 不适用或高风险场景
- 搜索空间完全离散、不可微。
- 任务要求必须依赖官方公开代码做严格复现。
- 搜索预算无法承担 Hessian 相关正则带来的额外开销。

## 输入、输出与目标
- 输入: 超网权重 `w`、架构参数 `alpha`、训练/验证划分、warm-up 轮数 `E_warmup`、权重系数 `gamma`。
- 输出: 从 `alpha` 离散化得到的最终鲁棒架构。
- 优化目标:
  - 权重更新: 最小化训练损失 `L_train`。
  - 架构更新( warm-up 后 ): 最小化 `L_val + gamma * L_lambda`。
- 核心假设: 输入损失景观曲率更小（`lambda_max` 更低）通常对应更强的对抗鲁棒性。

## 方法拆解

### 阶段 1: DARTS 风格 warm-up
- 按普通 DARTS 方式交替更新权重和架构参数。
- 该阶段不引入平滑正则。
- Source: Supplement App. A1 / Alg. 1 line 3-5

### 阶段 2: 架构更新加入平滑正则
- 权重更新保持不变。
- 架构更新目标改为 `L_val + gamma * L_lambda`。
- 其中 `L_lambda = E[lambda_max(H)]`，`H = ∇_x^2 l(f_A(x), y)`。
- Source: Main Sec. 3.2 Eq. (9)-(10); Supplement Alg. 1 line 8

### 阶段 3: 离散化并训练最终模型
- 将优化后的 `alpha` 按 DARTS 规则离散化成 normal/reduction cells。
- 组装最终网络并进行标准/对抗训练评估。
- Source: Supplement Alg. 1 line 11; main experiment sections

## 伪代码
```text
Algorithm: AdvRush Search
Input: 总轮数 E, warm-up 轮数 E_warmup, 正则系数 gamma
Output: 最终架构 A*

1. 初始化超网 f_super(w0, alpha0)。
   Source: Supplement Alg. 1 line 1
2. for i = 1..E:
   Source: Supplement Alg. 1 line 2
3.   用 L_train 的梯度更新 wi (SGD)。
     Source: Supplement Alg. 1 line 4/7
4.   if i <= E_warmup:
       用 L_val 更新 alpha_i (Adam)；
     else:
       用 [L_val + gamma * L_lambda] 更新 alpha_i (Adam)。
     Source: Supplement Alg. 1 line 5/8; Main Sec. 3.2 Eq. (9)-(10)
5. end for
6. 按 DARTS 离散化规则得到 A*。
   Source: Supplement Alg. 1 line 11
```

## 训练流程
1. 构建 DARTS 风格 8 算子搜索空间。
2. 先 warm-up（不加平滑项）进行搜索。
3. 再启用 `L_lambda` 正则进行架构更新。
4. 离散化结构并在目标数据集上训练最终模型。

Sources:
- Main Sec. 3-4
- Supplement App. A1, Table A1

## 推理流程
1. 使用最终训练好的架构进行常规推理。
2. 在 clean 与多种攻击设置（FGSM/PGD/C&W/AA）下评估鲁棒性。
3. 可进一步做跨数据集、不同 PGD 迭代步数的稳定性分析。

Sources:
- Main result sections
- Supplement Table A2/A5, Fig. A6

## 复杂度与效率
- 时间复杂度: 论文未给完整闭式表达。
- 空间复杂度: 论文未给完整闭式表达。
- 运行特征: 在 DARTS 流程上增加了 Hessian 平滑相关项，结构改动较小。
- 扩展性: `gamma` 越大鲁棒性通常更强，但可能牺牲 clean 精度。

## 实现备注
- 搜索算子: zero, skip-connect, avg/max pooling, sep conv 3x3/5x5, dil conv 3x3/5x5。
- 搜索更新: 权重用 SGD，架构参数用 Adam。
- 对抗训练超参（补充材料）:
  - momentum=0.9
  - weight decay=1e-4
  - CIFAR/SVHN 200 epochs, Tiny-ImageNet 90 epochs
- `L_lambda` 在 warm-up 后启用（示例图在约 50 epoch 激活）。
- 代码状态: 本次未定位到官方仓库链接。

## 与相关方法关系
- 对比 [[DARTS]]:
  AdvRush 在架构更新目标里显式加入平滑正则。
- 对比 [[PDARTS]]:
  在补充材料对比中 AdvRush 的鲁棒指标整体更好。
- 主要优势: 改动小、可插拔、鲁棒收益明显。
- 主要代价: 需要额外曲率近似计算，对近似质量敏感。

## 证据与可追溯性
- 关键图: Main Fig. 2; Supplement Fig. A1/A2/A3/A6
- 关键表: Main Table 2/3; Supplement Table A1/A2/A3/A5/A6
- 关键公式: Main Eq. (9)-(10) 与 Sec. 3.2 搜索目标
- 关键算法: Supplement Algorithm 1

## 参考链接
- arXiv: https://arxiv.org/abs/2108.01289
- HTML: https://arxiv.org/html/2108.01289
- CVF: https://openaccess.thecvf.com/content/ICCV2021/html/Mok_AdvRush_Searching_for_Adversarially_Robust_Neural_Architectures_ICCV_2021_paper.html
- 代码: Not found
- 本地实现: Not archived
