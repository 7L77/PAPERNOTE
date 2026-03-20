---
title: "VDAT_ch"
type: method
language: zh-CN
source_method_note: "[[VDAT]]"
source_paper: "Vulnerable Data-Aware Adversarial Training"
source_note: "[[VDAT]]"
authors: [Yuqi Feng, Jiahao Fan, Yanan Sun]
year: 2025
venue: NeurIPS
tags: [nas-method, zh, adversarial-training, data-filtering, robust-nas]
created: 2026-03-20
updated: 2026-03-20
---

# VDAT 中文条目

## 一句话总结
> VDAT 先估计每个样本的脆弱性，再按概率决定其是否进入对抗训练，从而把算力集中到更关键样本上。

## 来源
- 英文方法笔记: [[VDAT]]
- 论文本地文件: `D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf`
- 代码链接: https://github.com/fyqsama/VD-AT（归档时不可访问，返回 404）
- 论文笔记: [[VDAT]]

## 适用场景
- 问题类型: 需要兼顾鲁棒性与训练成本的对抗训练任务。
- 前提假设: 样本到决策边界的相对位置差异可由 margin 差异刻画。
- 数据形态: 监督学习分类任务，通常是图像分类。
- 规模与约束: 在 CIFAR 或 ImageNet 这类规模上都希望降低对抗训练 wall-clock。
- 适用原因: 把“是否做对抗训练”从统一规则改成样本级自适应分配。

## 不适用或高风险场景
- 训练流程必须完全确定性，不接受随机采样门控。
- 早期模型不稳定导致脆弱性估计噪声很大。
- 任务输出不是类别 logit，难以定义决策间隔。

## 输入、输出与目标
- 输入: 数据集 \(X\)、模型 \(f_\theta\)、用于脆弱性估计的攻击方式、周期 \(T\)、温度 \(\tau\)。
- 输出: 训练后的鲁棒模型 \(\theta^*\)。
- 目标: 在尽量少的额外计算下，提升自然精度和鲁棒精度。
- 核心假设: 更脆弱样本需要更高频率地接受对抗训练。

## 方法拆解
### 阶段 1：生成脆弱性评估所需的对抗样本
- 对当前样本生成 \(x_i'\)。
- Source: Sec. 4, Fig. 3

### 阶段 2：计算样本脆弱性
- 通过 clean/adv 样本的 margin 差定义 \(V_\theta(x_i)\)。
- 用 soft margin 替代 hard margin 以覆盖 targeted attack 场景。
- Source: Sec. 4.1, Eq. (2)-(5)

### 阶段 3：脆弱性到概率映射
- 归一化得到每个样本进入对抗训练的概率 \(P_\theta(x_i)\)。
- Source: Sec. 4.2, Eq. (6)

### 阶段 4：样本级过滤与联合训练
- 依据随机门控把样本分到 \(X_{\text{adv}}\) 或 \(X_{\text{nat}}\)。
- 优化联合损失 \(L_{\text{nat}}+L_{\text{adv}}\)。
- Source: Sec. 4.2, Eq. (7)-(8), Alg. 1

### 阶段 5：周期性刷新过滤结果
- 每隔 \(T\) 个 epoch 重新估计脆弱性并重分配样本。
- Source: Alg. 1

## 伪代码
```text
Algorithm: VDAT
Input: X={(x_i,y_i)}, 模型 f_theta, 总 epoch N, 刷新间隔 T, 温度 tau
Output: 训练后参数 theta*

1. for epoch = 0..N:
   Source: Alg. 1
2.   if epoch mod T == 0:
       2.1 为每个样本生成脆弱性评估用对抗样本 x_i'
           Source: Sec. 4, Fig. 3
       2.2 计算软间隔与脆弱性:
           V_theta(x_i) = -|S_theta^y(x_i)-S_theta^y(x_i')|
           Source: Eq. (3)-(5)
       2.3 归一化为概率 P_theta(x_i)
           Source: Eq. (6)
       2.4 采样 r~U(0,1):
           若 r<=P_theta(x_i) -> X_adv，否则 -> X_nat
           Source: Eq. (7)
3.   计算 L_train = L_nat(X_nat,theta) + L_adv(X_adv,theta)，更新 theta
     Source: Eq. (8), Alg. 1
4. return theta*
```

## 训练流程
1. 指定脆弱性估计攻击（默认 FGSM）。
2. 按周期更新样本脆弱性和训练子集分配。
3. 每个 epoch 用自然分支与对抗分支联合优化。
4. 使用 FGSM/PGD/C&W/AA 评估鲁棒性。

Sources:
- Sec. 5.1-5.2, Tab. 1-3

## 推理流程
1. 训练完成后按普通分类模型做前向推理。
2. 鲁棒评估阶段不再做筛选，只运行标准攻击评测协议。

Sources:
- Sec. 5.1-5.2

## 复杂度与效率
- 时间复杂度: 每次刷新筛选约 \(O(nk)\)。
- 空间复杂度: 与数据缓存和对抗样本缓存线性相关。
- 运行特征: 通过减少进入对抗训练的样本比例降低总体训练时间。
- 扩展性: 论文在 CIFAR 与 ImageNet-1K 上均报告正收益。

## 实现备注
- 默认超参: \(\tau=5\), \(T=10\)。
- \(T\) 越小通常精度更好但成本更高，需要按预算折中。
- 评估前攻击与训练内攻击强度会影响最终 clean/robust 平衡。
- 可插入 TRADES/AWP/robust NAS 等现有流程。
- 代码状态: 作者给出仓库链接，但归档时不可访问（404）。

## 与相关方法关系
- 对比 batch-wise 数据过滤方法: VDAT 是 sample-wise 过滤，更细粒度。
- 对比仅改进扰动生成的方法: VDAT 额外优化“哪些样本做对抗训练”。
- 主要优势: 以较小改动获得精度和效率双提升。
- 主要代价: 增加脆弱性估计与随机门控流程。

## 证据与可溯源性
- 关键图: Fig. 1, Fig. 2, Fig. 3, Fig. 4, Fig. 5
- 关键表: Tab. 1-4（主结果）, Tab. 5-10（参数与消融）
- 关键公式: Eq. (1)-(8)
- 关键算法: Alg. 1（VDAT）, Alg. 2（附录中与 robust NAS 结合流程）

## 参考链接
- 本地 PDF: `D:/PRO/essays/papers/Vulnerable Data-Aware Adversarial Training.pdf`
- 代码: https://github.com/fyqsama/VD-AT
- 本地实现: Not archived（仓库不可访问）

