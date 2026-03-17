---
type: concept
aliases: [A2C, Actor-Critic RL]
---

# Actor-Critic Reinforcement Learning

## Intuition

Split decision making into two roles: the actor chooses actions, while the critic judges how good the current state/action is. The critic's feedback helps the actor improve faster and with lower variance than plain policy gradient.

## Why It Matters

Many search or control problems have noisy rewards. Actor-critic stabilizes learning by introducing a value baseline, so policy updates are less erratic.

## Tiny Example

In NAS strategy selection, the actor decides whether to do initialization, mutation, or crossover this step; the critic estimates whether the current search state is promising. If reward improves, actor increases probability of that action in similar states.

## Definition

Actor-critic is a class of RL algorithms that jointly learn:
- a policy `pi_theta(a|s)` (actor), and
- a value function `V_psi(s)` or `Q_psi(s,a)` (critic),
and update policy with advantage estimates derived from critic predictions.

## Math Form (if needed)

For advantage actor-critic:
\[
\theta \leftarrow \theta + \eta \nabla_\theta \log \pi_\theta(a_t|s_t)\,\hat A_t
\]
\[
\hat A_t = r_t + \gamma V_\psi(s_{t+1}) - V_\psi(s_t)
\]
- `theta`: actor parameters.
- `psi`: critic parameters.
- `r_t`: reward.
- `gamma`: discount factor.

## Key Points

1. Actor learns "what to do"; critic learns "how good it is".
2. Advantage baseline reduces gradient variance versus pure REINFORCE.
3. Critic quality strongly affects convergence speed and stability.

## How This Paper Uses It

- [[APD]]: Uses actor-critic to schedule proxy-evolution operations (`init/mut/cross`) based on reward feedback.

## Representative Papers

- [[Asynchronous Methods for Deep Reinforcement Learning]]: Early practical actor-critic scaling (A3C).
- [[Proximal Policy Optimization Algorithms]]: Widely used actor-critic-style policy optimization.

## Related Concepts

- [[LLM-guided Search]]
- [[Neural Architecture Search]]
- [[Training-free NAS]]

