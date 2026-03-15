---
type: concept
language: zh-CN
source_concept_note: "[[Gabor Filter]]"
aliases: [Gabor滤波器, Gabor Wavelet]
---

# Gabor Filter 中文条目

## 一句话直觉
Gabor 滤波器是“高斯包络 + 正弦波”，可以选择性提取特定方向和频率的纹理/边缘信息。

## 它为什么重要
它提供了有结构的视觉先验，常用于增强边缘与纹理特征的稳定提取。

## 一个小例子
一个偏水平朝向的 Gabor 核对水平边缘响应更强，对垂直边缘响应较弱。

## 更正式的定义
二维 Gabor 可写成旋转坐标系下的高斯函数与余弦函数乘积，参数控制方向、波长、相位和长宽比。

## 数学形式（如有必要）
常见参数包括 `sigma/gamma/lambda/psi/theta`，分别对应尺度、纵横比、波长、相位和旋转角。

## 核心要点
1. 对方向与频率敏感。
2. 可作为手工先验或可学习模块。
3. 在鲁棒视觉任务中常用于稳定特征提取。

## 这篇论文里怎么用
- [[ABanditNAS]]: 把 3x3 Gabor 作为搜索空间操作之一，用于鲁棒结构搜索。

## 代表工作
- Dennis Gabor 的早期通信理论工作（1946）。
- Robust Gabor Networks 等后续鲁棒视觉研究。

## 相关概念
- [[Denoising Block]]
- [[Adversarial Robustness]]
- [[Neural Architecture Search]]

