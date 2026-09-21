# The Journey — how this policy was actually arrived at

Written at the end of the process, deliberately including the dead ends. The final recipe is
about twenty lines of reward config; getting there took five rounds and roughly thirty training
runs, and almost every round failed for a reason worth writing down.

---

## Round 0 — getting anything to run at all

Three environment problems, none of them RL:

1. **NVIDIA driver 595.71 crashed Isaac Sim 5.1** (access violations in `rtx.scenedb`, a known
   Blackwell bug). Downgraded to the validated **580.88**. Do not let Windows update it.
2. **tensordict 0.13 crashed inside Kit** (`_C.pyd` access violation with torch 2.7). Pinned to
   **0.8.3**. This — not the driver — is what kept killing URDF to USD conversion after the downgrade.
3. **Python buffers stdout when redirected to a file.** Several "the GUI is hung" and "the test
   produced nothing" episodes were just invisible print output. Set `PYTHONUNBUFFERED=1` always.

Asset prep: URDF to USD with `--merge-joints`. Foot collision replaced with a box primitive —
but see LESSONS.md, the first attempt used the full-mesh bounding box and was wrong twice
(48.9 mm tall instead of 11.9; 81.5 mm wide instead of 70 — a 16% oversized support polygon,
i.e. a policy flattered in sim that would not transfer to hardware).

Verified with forward kinematics that the mirrored URDF is exact: rotation from root to both feet
at zero pose is identity and symmetric. **The mirror pipeline was never the problem**, which saved
a lot of pointless geometry debugging later.

---

## Round 1 — first policies: it hops, then it limps

First baseline: flat terrain, 12 leg joints only. It learned to **hop** — a symmetric bounding
gait that satisfies forward-velocity tracking perfectly well.

Then two whole-body (28-action) recipes on flat, ported from the official Isaac Lab configs:

- **G1-style**: episode length 983/1000, velocity error 0.03 — excellent numbers.
- **TienKung-style** (periodic gait clock): episode length 1000/1000, velocity error 0.43.

Both survived. Both looked **lame** — one leg dragging, held nearly straight, doing little work.

The first real lesson: **episode length measures not-falling, not gait quality.** A policy can
max out survival and velocity tracking while walking in a way you would never accept on hardware.
From here on every judgement was made on video, and later on measured joint angles.

---

## Round 1.5 — the bug that silently invalidated every rough-terrain run

Every attempt to train on rough terrain collapsed: episode length pinned at **1-8 steps**, while
the identical policy scored 983 on flat. Several hours were spent blaming the foot collision box,
the arm pose, the leg crouch, and the action space — changing five variables at once and then
chasing the resulting noise.

The actual cause was one line:

```python
mdp.root_height_below_minimum   # termination "base_height", minimum 0.50 m
```

It compares against **absolute world z**, and Isaac Lab's own docstring says it is "currently
only supported for flat terrains". On generated terrain a robot spawned in a pit or on descending
stairs is already below the threshold at t=0 and terminates on frame one.

Proof: a trained flat policy loaded onto rough scored 1.23. With the termination removed, the same
policy immediately went 11, 43, 96, 142, 479, 872.

The evidence had been visible the whole time in `Episode_Termination/*`. **When episode length is
pathologically low, read the termination fractions before touching anything else.**

---

## Round 1.75 — can terrain fix a lame gait? No.

Hypothesis: varied foot placement on rough terrain might break the entrenched limp. Fine-tuned
the good flat policy onto rough terrain (height scanner disabled so the observation size still
matched, which is what makes a flat checkpoint loadable at all).

It reached 872 episode length and **stayed lame**. Fine-tuning refines an existing gait; it does
not restructure a broken one. Experiment closed, negatively but definitively.

---

## Round 2a — the six-way bake-off

Six reward philosophies under identical conditions, to find out whether the lameness was a reward
problem: **G1, TienKung, Digit, H1, Cassie, Hybrid**.

All six converged into a narrow 828-908 band. Two findings mattered more than the ranking:

- **Cassie — the deliberately minimal reward set — nearly matched the best.** Evidence against
  heavy reward shaping.
- **Digit and Hybrid started terribly** (66 and 178 at iteration ~250) and both recovered to ~850
  by iteration 700. Two runs were nearly killed early on that evidence. From then on, slow starts
  were judged against Hybrid's recovery curve rather than against the fast recipes.

User preference from video: **Hybrid**, then G1.

Separately, **symmetry augmentation** was added here. No official Isaac Lab biped uses it (only
ANYmal, a quadruped). Because the URDF already mirrors the joint axes, mirroring is a plain
left-right swap with no per-joint sign flips — simpler than ANYmal's version. It reached the same
episode length in about a third of the iterations and visibly reduced the limp. It is in the final
recipe.

A clarification worth recording, because it caused confusion: symmetry augmentation does **not**
force both legs to move in phase. It constrains the *policy function* — mirror the state, and the
policy must produce the mirrored action. The mirrored state of "left leg forward" is "right leg
forward", i.e. the same gait half a period later. Normal alternating walking satisfies it; a limp
does not.

---

## Round 2b — soft landings, and over-penalising

Feedback on the winners: good, but the foot "comes up, stays up, then goes down very fast and hits
the ground hard", and the steps are too big.

Added `foot_landing_velocity` (penalise fast descent near the ground), `foot_contact_impact`
(punish the strike itself), a hip-yaw penalty (feet were splaying outward), plus tighter clearance
and air-time targets.

**All six variants plateaued at ~65 episode length.** The penalties were stacked at constraint
strength and blocked early exploration. Halving every new weight fixed it — five of six then
reached 555-859.

> New gait-quality penalties belong at **nudge** strength (about -0.3 to -1.0), not as hard
> constraints. Over-penalising looks exactly like a broken recipe.

Also confirmed here for the fourth time: **the fixed periodic gait clock (TienKung-style) does not
work on this morphology.** Every variant using it failed. The alternating gait emerges fine from
`feet_air_time` plus `no_jumps` alone.

---

## Round 3 — the round that went backwards

Feedback: steps still too big; plus an observation that the official H1 takes small steps.

That observation was correct and led to a genuine root cause: **our "official" G1/H1 recipes were
not official.** A corrections layer had added a 10 cm foot-clearance reward and a 0.7 s air-time
target — both of which explicitly pay for lifting high and stepping long. Official H1 uses air-time
0.4 at weight 0.25 and **no clearance reward at all**. That is why real H1 policies step small.
It also explains why an early checkpoint (G1 at iteration 700) looked better than the same run at
3000: it had not yet fully maximised the big-step incentives.

The right response was to remove those two additions. Instead the whole thing was redesigned: a
WALK/RUN split, air-time weight cut to a quarter, clearance removed entirely from the walks, slow
commands plus stand-still incentives, flat terrain for the walks.

Result: **the walks learned to stand still** (standing became the reward optimum) and **the runs
walked with locked straight legs** (with the swing incentive starved, not lifting minimises every
remaining penalty). Worse than what it replaced.

> Refine a working recipe one variable at a time. A redesign discards the information contained in
> the thing that already worked.

---

## Round 4 — correct method, wrong target

Corrected the method: take the proven round-2 recipe **exactly**, vary **one knob per run**
(air-time threshold, clearance target, command speed, tracking weight), all on mixed terrain, with
an unchanged control run to confirm the baseline reproduces.

Methodologically right, and it would have isolated the step-size mechanism cleanly — except every
run still walked with **locked knees**. The knee problem predated round 3's redesign and had been
invisible while attention was on step size.

---

## Round 5 — measuring instead of guessing

The user's hypothesis: the arms-down fix caused the locked knees, since it was the only change
versus round 2, which bent its knees. Plausible — with arms held forward, about 4 kg of arm mass
sits ahead of the hips and knee flexion is how a policy balances that forward CoM.

Rather than argue it, the hypothesis and the alternatives were tested together in one round of six
runs, and the outcome was **measured** with a purpose-built tool (`knee_probe.py`) instead of being
judged by eye:

| variant | mean knee | % of time straight | verdict |
|---|---|---|---|
| PendBase (round-4 reference) | -3.6 deg | 96.1% | locked |
| **ArmsFwd** (arms back to forward pose) | **-4.4 deg** | **98.3%** | **locked - hypothesis disproved** |
| KneeSoft (penalty -0.5, min 0.15) | -3.0 deg | 95.6% | too weak, no effect |
| Crouch (pelvis capped at 0.70 m) | -3.3 deg | 94.5% | ineffective alone |
| KneeDefault (bent resting pose) | 26.4 deg | 0.1% | works, shallower |
| **KneeTorque** (penalty + no torque tax on knees) | **35.1 deg** | 0.9% | **works** |
| **KneeHard** (penalty -2.0, min 0.25) | **36.1 deg** | **0.4%** | **works - chosen** |

**The arm pose was never the cause.** ArmsFwd is, if anything, *more* locked. Round 2's knee bend
was incidental, not designed.

The real cause is **reward economics**: a locked knee carries load through structure at near-zero
torque, while a flexed knee pays `dof_torques_l2` on every single step — and nothing in the reward
set ever *asked* for flexion. Two independent results confirm it. Simply removing the torque tax on
knees (KneeTorque) produces 35 degrees of flexion on its own. And capping pelvis height (Crouch)
fails completely, because the robot satisfies the cap by other means — a reminder that constraining
a *symptom* is not the same as changing the incentive.

---

## The decision: KneeHard over KneeTorque

Both measure the same (36.1 vs 35.1 degrees, both essentially never straight) and look the same on
video. KneeHard was chosen, and simplicity is the smaller half of the reason.

**KneeHard** adds one reward term and changes nothing else:

```python
cfg.rewards.knee_bend = RewTerm(
    func=gait_quality_rewards.knee_straightness,
    weight=-2.0,
    params={"asset_cfg": KNEES, "min_bend": 0.25},
)
```

**KneeTorque** adds a similar term *and* removes the knees from `dof_torques_l2`.

The stronger argument is hardware safety. `dof_torques_l2` is the main thing keeping commanded
torque civilised, and the knee is driven by the highest-load actuator in the machine (RobStride
RS04: 120 Nm peak but only **40 Nm rated**, and the continuous rating is where a real motor
overheats). Removing the torque regulariser on exactly that joint means nothing in the objective
discourages a torque-hungry gait; the bill arrives as heat on the real robot. KneeHard keeps the
tax on and simply makes locked knees more expensive than paying it.

Secondary reasons: one additive term is easier to port, explain and tune than a term plus a
silent removal; and KneeHard's penalty is self-limiting (it stops applying once the knee passes
0.25 rad), so it shapes the gait without competing with the swing.

Two things to do before hardware, either way:
- Log per-joint applied torque and compare against the **rated** (not peak) RobStride figures.
- Re-check knee flexion with `knee_probe.py` after any reward change. It is cheap, and this exact
  problem went unnoticed for two full rounds.

---

## What the final recipe is

Base: Isaac Lab velocity task, rough terrain generator with stairs (5-23 cm steps), curriculum on.

- **Action space**: 12 leg joints + waist roll. Arms/wrists/neck PD-held (see `events.py`).
- **Symmetry augmentation** on (`code/symmetry/humanoid_biped.py`).
- **Anti-hop**: `no_jumps` (penalise timesteps with no foot in contact) plus `lin_vel_z_l2`.
- **Soft landing**: `foot_landing_velocity` and `foot_contact_impact`, both at nudge strength.
- **Knee flexion**: `knee_straightness`, weight -2.0, min_bend 0.25 rad. This is the round-5 fix.
- **Posture**: `upright_torso`, `flat_orientation_l2`, hip-yaw deviation to keep the toes forward.
- **Terminations**: bad orientation beyond 0.7 rad, root/torso ground contact. **No `base_height`**
  — it is flat-terrain-only and silently kills rough-terrain training.

The exact values as trained are in `policy/params_as_trained/env.yaml`.
