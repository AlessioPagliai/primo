# Measured results

All runs: RSL-RL PPO, 3000 iterations unless noted, 1024-2048 parallel envs, RTX PRO 6000 Blackwell.
"Episode length" is mean steps survived out of 1000. "% straight" is the fraction of time a knee is
flexed less than 5.7 degrees, from `knee_probe.py` over a 500-step rollout.

---

## Round 1 — flat terrain, whole body (28 actions)

| recipe | episode length | velocity error | gait by eye |
|---|---|---|---|
| G1-style | 983 | 0.03 | survives, visibly lame |
| TienKung-style (gait clock) | 1000 | 0.43 | survives, poor tracking |
| legs-only baseline | ~900 | - | hopping |

Conclusion: survival metrics saturate and stop discriminating. Gait quality must be judged
separately.

---

## Round 1.5 — the `base_height` termination bug

Same trained flat policy, evaluated/fine-tuned on rough terrain:

| condition | episode length |
|---|---|
| rough, `base_height` termination active | **1.23** |
| rough, termination removed (same policy, same checkpoint) | 11 → 43 → 96 → 142 → 479 → **872** |

A single flat-terrain-only termination had been invalidating every rough-terrain experiment.

---

## Round 2a — six-way reward bake-off (rough terrain, symmetry on)

Final episode lengths after 3000 iterations:

| recipe | episode length |
|---|---|
| Cassie (minimal reward set) | 908 |
| Hybrid | 908 |
| H1 | 890 |
| G1 | 881 |
| TienKung | 841 |
| Digit | 828 |

Trajectory note — early readings are misleading:

| recipe | iter ~250 | iter ~700 | final |
|---|---|---|---|
| G1 | 908 | 881 | 881 |
| Hybrid | 178 | ~850 | 908 |
| Digit | 66 | 828 | 828 |

Hybrid and Digit both looked broken early and finished at the top of the field.

---

## Round 2b — soft-landing variants (rough terrain)

First attempt, penalties at constraint strength — all six stalled:

| iteration | episode length (all six) |
|---|---|
| 250 | 50-60 |
| 400 | 63-78 |

After halving every new penalty weight:

| recipe | episode length | velocity error |
|---|---|---|
| SoftTiny | 946 | 0.457 |
| SoftImpact | 945 | 0.399 |
| Soft | 909 | 0.519 |
| SoftPend | 902 | **0.398** |
| SoftSlow | 885 | 0.423 |
| SoftClock (gait clock) | **86** | - (killed) |

User verdict: SoftPend and SoftImpact good, steps too big. SoftClock confirms the gait clock fails.

---

## Round 3 — WALK/RUN split (regression)

| recipe | terrain | episode length | gait by eye |
|---|---|---|---|
| WalkG1 | flat | 1000 | **stands still** |
| WalkH1 | flat | 993 | **stands still** |
| WalkTiny | flat | 999 | **stands still** |
| RunPend | rough | 861 | walks, **locked knees** |
| RunImpact | rough | 879 | walks, **locked knees** |
| RunG1 | rough | 864 | walks, **locked knees** |

Perfect episode lengths, unusable policies. The walks found standing as the reward optimum after
the swing incentive was cut to a quarter and stand-still bonuses were added.

---

## Round 5 — knee flexion, measured

`knee_probe.py`, 500-step rollout, 32 envs, model_2999 of each run:

| variant | mean knee | range | % straight | pelvis above feet | verdict |
|---|---|---|---|---|---|
| PendBase (round-4 ref) | -3.6 deg | -5.4 … 137.0 | 96.1% | 0.728 m | locked |
| ArmsFwd (hypothesis test) | -4.4 deg | -5.4 … 130.8 | 98.3% | 0.730 m | locked |
| KneeSoft (-0.5, min 0.15) | -3.0 deg | -5.4 … 165.0 | 95.6% | 0.725 m | no effect |
| Crouch (pelvis cap 0.70) | -3.3 deg | -5.4 … 165.0 | 94.5% | 0.729 m | no effect |
| KneeDefault (bent default) | 26.4 deg | -5.2 … 103.3 | 0.1% | 0.721 m | works |
| KneeTorque (-1.0 + no knee torque tax) | 35.1 deg | -5.2 … 130.5 | 0.9% | 0.702 m | works |
| **KneeHard (-2.0, min 0.25)** | **36.1 deg** | **-5.2 … 116.0** | **0.4%** | **0.700 m** | **chosen** |

Two independent readings of the same conclusion: the arm pose is irrelevant to knee flexion
(ArmsFwd is the *most* locked variant), and removing the knee torque tax alone fixes it
(KneeTorque), which identifies the torque penalty as the mechanism that made locking optimal.

---

## Chosen policy

`policy/kneehard_model_2999.pt`

- Task: `Isaac-Velocity-R5-KneeHard-v0`, rough terrain with 5-23 cm stairs, curriculum on
- Action space: 12 leg joints + waist roll; arms/wrists/neck PD-held
- Symmetry augmentation active
- Episode length ~870/1000, mean knee flexion 36.1 deg, 0.4% of time straight
- Training cost: 3000 iterations, roughly 4-5 h at 1024 envs sharing a GPU with five sibling runs
