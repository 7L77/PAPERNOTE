---
type: concept
language: zh-CN
source_concept_note: "[[Hardware Performance Model]]"
aliases: ["硬件性能预测器", "Hardware Performance Model"]
---

# Hardware Performance Model 中文条目

## 一句话直觉

Hardware Performance Model 就是在真正跑到设备上之前，先预测一个网络在该设备上的 latency、energy 等表现。

## 它为什么重要

真实测量每个候选网络的硬件代价通常很慢，也不一定有足够多设备可用，所以需要一个替代模型。

## 一个小例子

对一堆候选网络，不去逐个上手机 GPU 跑，而是先用 latency predictor 根据结构估计每个网络的大概延迟。

## 更正式的定义

Hardware Performance Model 是用来估计候选神经网络在目标硬件上的设备侧指标的预测模型或查表系统。

## 核心要点

1. 它是 hardware-aware NAS 中和 accuracy proxy 对应的另一半。
2. 粒度可以是 layer-level，也可以是更细的 kernel-level。
3. 除了预测误差，跨设备迁移能力也很关键。

## 这篇论文里怎么用

- [[Zero-shot NAS Survey]]: 对比 BRP-NAS、HELP、NN-Meter，并强调硬件预测器对整个 NAS 流程同样关键。

## 代表工作

- [[Zero-shot NAS Survey]]: 总结主流硬件性能模型。
- [[NN-Meter]]: 常见 kernel-level latency predictor。

## 相关概念

- [[Hardware-aware NAS]]
- [[NAS Benchmark]]

