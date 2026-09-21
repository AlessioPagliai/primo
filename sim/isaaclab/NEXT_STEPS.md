# Next steps, with the traps already mapped

Concrete guidance for the work that follows, written while the context is fresh.

---

## 1. Hip-yaw torque gate — do this first, it blocks a purchase

The CAD uses RobStride **RS06 (36 Nm peak)** at hip yaw; the locked BOM specifies **RS03 (60 Nm)**.
The decision was deliberately deferred to measurement.

**Method** — during turning (nonzero `ang_vel_z` commands), log
`env.scene["robot"].data.applied_torque[:, hip_yaw_ids]` across a long rollout. Report peak, RMS,
95th/99th percentile, and the fraction of samples above 80/90/95/99% of the 36 Nm limit. If it
saturates for more than about 2-5% of steps at the target turn rates, RS03 is required.

`knee_probe.py` is the template — it already patches `play.py`'s `env.step` to sample robot state
during a rollout; swap the knee angles for `applied_torque` and the same structure works.

**Two cautions**:
- Compare against the **rated** (continuous) torque, not just peak. RS04 is 120 Nm peak but only
  40 Nm rated, and continuous rating is where a real motor overheats.
- The ankle is a 2x RS06 pushrod differential modelled as two virtual joints. Simulated virtual
  joint torque is **not** the torque of either physical motor — it must be mapped through the real
  linkage Jacobian before any ankle motor conclusion.

---

## 2. Adding pushes

Worth knowing before you start: **H1, G1 and Cassie all disable push randomisation** in their
official Isaac Lab configs (`self.events.push_robot = None`). Only Digit keeps it. Our own attempt
at a faithful Digit port — with pushes on and backward/lateral commands — stalled at ~18 episode
length from a cold start, and only worked once pushes were turned off.

**Recommendation**: do not train from scratch with pushes. Fine-tune the working KneeHard policy
with pushes introduced gradually. Unlike gait *shape* (which fine-tuning cannot fix — see
HANDOFF round 1.75), robustness is exactly the kind of thing fine-tuning does well.

```python
self.events.push_robot = EventTerm(
    func=mdp.push_by_setting_velocity,
    mode="interval",
    interval_range_s=(10.0, 15.0),                       # start sparse
    params={"velocity_range": {"x": (-0.3, 0.3), "y": (-0.3, 0.3)}},   # start small
)
```

Then ramp magnitude and frequency over successive fine-tunes. Check after each stage that knee
flexion has not collapsed back (`knee_probe.py`) — push recovery is a plausible reason for a
policy to re-discover stiff legs.

While you are there, the other domain randomisation worth adding before sim-to-real: base mass
(`add_base_mass`), CoM offset, ground friction, motor strength scaling, action latency, and
IMU/joint-observation noise. Introduce them one at a time, not as a block.

---

## 3. Unlocking more joints

Current action space is 12 leg joints + waist roll. Natural next additions, in order of value:

1. **Waist yaw** — helps turning, low risk.
2. **Shoulder pitch + roll** — arm swing. The single biggest visual gain toward natural walking.
3. **Elbows** — optional, small additional benefit.

Keep wrists, shoulder yaw and neck held.

**Three specific traps**:

- **`events.hold_default_joint_targets` must stay** for whatever remains outside the action space.
  Without it those joints drive to the URDF zero pose, not your configured pose. This silently
  affected every legs-only run for several rounds (LESSONS.md B2).
- **The arms have no collision geometry** in the current URDF export. Before enabling arm swing,
  add collision to the arm links — otherwise the policy can swing an arm through the torso and
  learn a gait that is impossible on hardware.
- **Changing the action dimension invalidates the policy head.** You cannot fine-tune KneeHard
  into a larger action space; that is a retrain. So decide the final action set *before* investing
  in a long curriculum.

A 15-degree outward shoulder-roll offset is already in the default pose specifically so the arms
clear the hips when the waist rolls. Keep it when arms become active, or re-check hip clearance.

---

## 4. The conservative "walk mode" (unfinished)

The goal — a precise, small-step mode for positioning, like the walk/run switch on a G1 remote —
is still open. Round 3 attempted it and failed: cutting the swing incentive and adding stand-still
bonuses made standing the reward optimum, so the robot simply stopped walking.

**Better approach**: keep the working KneeHard reward set unchanged and constrain only the
*command distribution* — train (or fine-tune) with a low-speed command range and a small nonzero
floor, so slow walking is required rather than standing being rewarded. Alternatively train one
policy on the full speed range and expose speed as the mode switch at deploy time, which is closer
to what the G1 remote actually does.

Whatever you try, judge it against the round-3 failure mode: check the robot still *moves* when
commanded slowly, rather than scoring well by standing still.

---

## 5. Standing discipline for the whole project

The two habits that would have saved the most time:

1. **Change one variable per run, and always keep an unchanged control in the batch.**
2. **Measure the property you are judging.** Build the probe before the second argument about what
   a video shows. `knee_probe.py` took ten minutes to write and settled a question that had
   consumed two rounds.
