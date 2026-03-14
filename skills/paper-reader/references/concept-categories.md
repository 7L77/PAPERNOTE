# 概念自动归类规则

概念库位置：`{CONCEPTS_PATH}`

先用 `ls {CONCEPTS_PATH}` 查看已有子目录，再按下表分类：

| 子目录 | 归类标准 | 示例 |
|--------|----------|------|
| `1-生成模型` | 扩散模型、GAN、VAE、Flow、生成相关方法 | DMD, DPM-Solver, SDE, NFE, Score Distillation |
| `2-强化学习` | RL 算法、策略优化、价值函数、reward | Actor-Critic, PPO, MBRL, CRL, DrQv2, DAPG |
| `3-机器人策略` | 操作策略、抓取、灵巧手、模仿学习、VLA | HOI, DexRep, UniDexGrasp, Diffusion Policy |
| `4-足式运动` | 四足、双足、locomotion | CPG, Raibert Controller |
| `5-导航与定位` | SLAM、路径规划、导航 | NAVSIM, VPR |
| `6-3D视觉` | NeRF、3DGS、点云、深度估计、立体视觉 | Epipolar Geometry, 4DGS |
| `7-规划与控制` | 控制理论、优化器、MPC、PID | PID, SMC, ILC, OSQP, CVXPY, SNOPT |
| `8-仿真器` | 仿真平台、物理引擎 | IsaacLab, MuJoCo |
| `9-无人机` | UAV、飞行控制 | PX4 |
| `10-数据集` | 数据集、benchmark | ImageNet, YCB, BridgeV2, FFHQ |
| `11-深度学习基础` | 通用 DL 技术、架构组件、训练技巧 | GMM, EMA, MoE, GAT, Transformer, Teacher Forcing |
| `12-物理仿真` | 物理模型、生物力学仿真 | OpenSim, SCONE, FEM |
| `13-机器人硬件` | 传感器、执行器、机器人平台 | Tendon Drive, Tactile Sensor |
| `14-安全与鲁棒性` | 对抗攻击、安全约束 | CBF, Adversarial |
| `15-网页智能体` | 网页操作、浏览器自动化 | WebAgent |
| `16-人体动作` | 人体姿态、动作生成、动捕 | ViTPose, SMPL, Motion Capture |
| `0-待分类` | 仅在完全无法判断时才用，应尽量避免 | - |

## 概念写法要求

1. 先讲直觉，再讲定义，最后再上公式。
2. 默认要带一个小例子、玩具场景或类比，帮助第一次接触的人理解。
3. 不要用概念解释概念，避免“X 就是一种做 X 的方法”这种循环表述。
4. 如果论文里具体用了这个概念，要补一句“这篇论文里怎么用”。
5. 公式是可选项，不是必选项。只有公式真能帮理解时才写。

## 概念笔记模板

```markdown
---
type: concept
aliases: [中文别名, 英文别名]
---

# 概念名称

## 一句话直觉
{先用人话解释它在干什么}

## 它为什么重要
{它解决了什么问题}

## 一个小例子
{给一个简单具体的例子}

## 更正式的定义
{再给出更准确的定义}

## 数学形式（如有必要）
$$公式$$

## 核心要点
1. ...
2. ...

## 这篇论文里怎么用
- [[Paper1]]: ...

## 代表工作
- [[Paper2]]: ...

## 相关概念
- [[相关概念1]]
- [[相关概念2]]
```
