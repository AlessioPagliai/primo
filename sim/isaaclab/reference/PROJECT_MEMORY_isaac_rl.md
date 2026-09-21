# MEMORY — Isaac Sim / Isaac Lab RL work log

Scope: everything done on the Windows workstation from the first "install isaac sim and isaac lab"
prompt (2026-07-18) through 2026-07-19. Written by AI. The project-wide source of truth remains
`../MEMORY.md` and `../AI_HANDOFF.md`; this file is the Isaac/RL-specific history, including the
mistakes, because several of them cost hours and must not be repeated.

---

## 1. Environment (all working, do not "upgrade" casually)

| Piece | Value |
|---|---|
| Python | 3.11.9 (winget, user scope, NOT on PATH) |
| Venv | `C:\Users\WKS\isaac\env_isaaclab` |
| Isaac Sim | 5.1.0 (pip, `isaacsim[all,extscache]`, pypi.nvidia.com) |
| Isaac Lab | 2.3.2 source, `C:\Users\WKS\isaac\IsaacLab` (editable installs → edits are live) |
| PyTorch | 2.7.0+cu128 (+ torchaudio; pinned by isaacsim-core) |
| tensordict | **0.8.3** (pinned — see 3.2) |
| NVIDIA driver | **580.88** (downgraded — see 3.1) |
| GPU | RTX PRO 6000 Blackwell Max-Q, 96 GB, sm_120 |

### Standard launch command

```
cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& call C:\Users\WKS\isaac\env_isaaclab\Scripts\activate.bat && cd /d C:\Users\WKS\isaac\IsaacLab && call C:\Users\WKS\isaac\IsaacLab\isaaclab.bat -p <script> [--headless] > <UNIQUE_log> 2>&1"
```

Every element matters:
- full path to `isaaclab.bat` (bare name fails after `cd` in cmd)
- `PYTHONUNBUFFERED=1` — without it Python `print()` is buffered and diagnostics vanish (see 3.3)
- `OMNI_CRASHREPORTER_ENABLED=0` — crash-dump uploads stall startup
- **unique log file per launch** — reusing a log path while a previous shell tears down causes a
  sharing violation that silently wedges the new process (this was misdiagnosed for a long time as
  "two Isaac instances kill each other"; they do not — two trainings ran fine in parallel)

---

## 2. Assets and code

### URDF → USD
- Training URDF: `rl_full/urdf/rl_full.urdf` (from the CAD Mac's `mirror_urdf.py`; do NOT use the raw
  half-robot `rl/rl.urdf`). Backup of the pre-edit file: `rl_full.urdf.bak`.
- Convert: `scripts/tools/convert_urdf.py <urdf> usd/rl_full.usd --merge-joints --headless`
- Merged body names that configs depend on: root = `root`, torso = `waist_yaw_link`
  (battery+Thor merged in), feet = `left/right_ankle_roll_link`.
- AI separately built `humanoid_articulated_hands/` (TienKung-donor articulated hands, 24 finger
  DOFs, 0.540 kg/hand preserved). Used by the G1-whole-body tasks. It did **not** receive the foot
  collision fix below.

### Verified geometry facts
- `scripts/foot_zero_check.py`: chain rotation root→both feet at zero pose is exactly identity and
  symmetric. **The mirror pipeline is correct** — the "lame leg" is not a mirroring bug.
- Joint jog (`scripts/joint_jog.py`) confirmed by the user: all joints move correctly, left/right
  match in direction and value at equal commands.
- Standing root height ≈ 0.78 m with straight legs (user-measured 0.76891).

### Collision
- Feet: mesh → **box, sole plate only, 199.9 × 70.0 × 11.9 mm**
  (`scripts/simplify_foot_collision.py`). First attempt used the full-mesh AABB and was wrong twice:
  48.9 mm tall (a brick up to the ankle bracket, whose side faces catch on stair edges) and 81.5 mm
  wide (that is the *bracket* width, not the sole → a 16 % oversized support polygon, i.e. a policy
  flattered in sim that would not transfer). Audited with `scripts/audit_collisions.py`.
- Remaining 13 bodies still use full visual meshes as collision (~77 k triangles). Acceptable while
  self-collision is off; the ankle-gimbal cluster is the one that jitters when it is enabled.
- Self-collision OFF in the jog tool. With it ON the un-simplified ankle meshes overlap at rest and
  vibrate — that was the "left ankle vibrates" report, not a joint bug.

### Registered tasks (`.../locomotion/velocity/config/robstride/`)
| Task id | Notes |
|---|---|
| `Isaac-Velocity-Flat-Robstride-v0` / `-Rough-` / `-Play` | base tasks, G1-derived rewards |
| `Isaac-Velocity-Flat-Humanoid-G1WholeBody-v0` (+Play) | AI: 28 whole-body actions, articulated hands, 15° shoulder-roll clamp |
| `Isaac-Velocity-Flat-Humanoid-TienKungPeriodic-v0` (+Play) | AI: TienKung 0.85 s gait clock |
| `Isaac-Velocity-Rough-Humanoid-G1WholeBody-v0` (+Play) | fine-tune target, height scan disabled so a flat checkpoint loads |

Robot cfg: `isaaclab_assets/robots/robstride.py` → `ROBSTRIDE_HUMANOID_CFG`
(PD and effort limits from the real RobStride motors: RS04 120 Nm, RS06 36 Nm, ankle pitch 72 Nm
differential, RS00 14 Nm, RS05 5.5 Nm).

---

## 3. Bugs found and fixed (the expensive ones)

### 3.1 NVIDIA driver 595.71 crashed Isaac Sim 5.1
GUI and URDF conversion died with access violations in `rtx.scenedb`. Known NVIDIA bug affecting
Blackwell. Downgraded to the validated **580.88** (user-approved via UAC; restore point
"Pre NVIDIA 580.88 downgrade" exists). **Do not let Windows update this driver.**

### 3.2 tensordict 0.13 crashed inside Kit
`_C.pyd` access violation in `PyInit__C` with torch 2.7. This — not the driver — was what kept
killing URDF conversion after the downgrade. Fix: `pip install tensordict==0.8.3 --no-deps`.

### 3.3 Buffered stdout made working things look hung
Python buffers `print()` when stdout is redirected to a file. Several "the GUI won't load" and
"the test produced nothing" episodes were just invisible output. Always `PYTHONUNBUFFERED=1`.

### 3.4 THE BIG ONE — `base_height` termination is flat-terrain-only
`mdp.root_height_below_minimum` (used as termination `base_height`, minimum 0.50 m) compares against
**absolute world z**. Isaac Lab's own docstring: *"currently only supported for flat terrains"*.

On generated terrain, any robot spawned in a pit or on descending stairs is already below the
threshold at t=0 and terminates on frame one.

- Symptom: episode length pinned at **1–8** on every rough run, while the identical policy scored
  **983** on flat.
- Proof: a trained flat policy loaded onto rough scored **1.23**; with the termination removed the
  same policy immediately scored 11 → 43 → 96 → 142 → 479 → 872.
- Fix: `self.terminations.base_height = None` in `RobstrideRoughEnvCfg`; the flat config re-adds it
  (where it is valid and useful).

**This single line invalidated a whole afternoon of "fixes".** Foot box, arm pose, leg crouch,
legs-only vs whole-body actions — none of them were ever the cause. The termination-fraction
readout showed the answer early and was not read.

### 3.5 Method lessons (the real cost driver)
1. When episode length is pathologically low, **read `Episode_Termination/*` first**. It says exactly
   why robots die.
2. **Change one variable at a time.** Five simultaneous changes made the result uninterpretable and
   led to chasing self-created noise.
3. A robot that cannot stand passively with fixed PD is **normal** for humanoids — `stand_test.py`
   returning FALLS is not a valid asset gate. Do not over-conclude from it.
4. `play.py --checkpoint` wants a **full path**; `train.py --resume` wants `--load_run` + filename.
   `--resume True` is invalid (it is a flag).
5. Flat→rough fine-tuning requires matching observation size: disable the height scanner
   (blind locomotion) or the checkpoint will not load.

---

## 4. Training runs and results

Checkpoints: `C:\Users\WKS\isaac\IsaacLab\logs\rsl_rl\<experiment>\<timestamp>\`
Copies of the finished ones: `rl_full_isaac/training_runs/`.

| Experiment | Terrain | Actions | Result |
|---|---|---|---|
| `robstride_flat` | flat | 12 legs | first baseline; learned to **hop**, not walk |
| `humanoid_flat_g1_whole_body` | flat | 28 whole-body | 1500 iters, ep. len **983**, vel err 0.03 — but visibly **lame** gait |
| `humanoid_flat_tienkung_periodic` | flat | 28 + gait clock | 1500 iters, ep. len **1000**, vel err 0.43 |
| `humanoid_rough_g1_whole_body_finetune` | rough (blind) | 28 | resumed from flat model_1499; 1.23 → **872**. **Killed by user: lameness persisted** — left leg still straight/back, barely moving. Fine-tuning refines a gait, it does not restructure a broken one. |
| `robstride_rough` (current) | rough + stairs | whole-body | from scratch, new arms-down pose, corrected sole boxes; iter ~394 → ep. len **914**. Most promising; no inherited lameness. |

### Poses
- Straight legs (all zeros) are singular — the knee has no moment arm and buckles.
- Arms-down walking pose settled with the user: `shoulder_pitch 0`, `shoulder_roll +0.2618` (15°
  outward, clears the hip), `elbow +1.5708` (90°). Spawn z 0.78 (0.797 with sole-box clearance).
- G1 neutral (hip −0.20, knee 0.42, ankle −0.23) is what the two successful flat runs used.

### Open quality issue
The lame/asymmetric gait is **not** geometric (mirror verified) and **not** curable by terrain
fine-tuning (tested). Most likely the reward set: no biped baseline in Isaac Lab (H1, G1, Cassie,
Digit) includes a symmetry term. Options not yet tried:
- rsl_rl's `RslRlSymmetryCfg` data augmentation (only ANYmal uses it; needs a biped mirror function)
- Digit's `no_jumps` (`mdp.desired_contacts`) + stronger `flat_orientation_l2` / `lin_vel_z_l2`
- simply more iterations (official G1/H1 rough budgets are 3000+, ours were 1500)

---

## 4b. Session 2 (2026-07-19 afternoon): symmetry, gait quality

### Symmetry augmentation — WORKS, and is the fix for the lame gait
`mdp/symmetry/humanoid_biped.py` implements left-right augmentation for this robot and is wired
in via `RslRlSymmetryCfg` (`humanoid_rough_symmetry` experiment). **Verified genuinely active**
by `scripts/verify_symmetry.py` — batch doubles, all 13 left/right joint pairs swap correctly,
base y-quantities negate, height scan flips, actions mirror. Run that check after any change:
the function has dimension-mismatch fallbacks that would otherwise silently no-op.

Because `mirror_urdf.py` already mirrors the joint *axes*, mirroring joint data here is a plain
left↔right SWAP with **no per-joint sign flips** (ANYmal needs them; we do not). Central joints:
roll/yaw negate, pitch does not.

Result: symmetry reached ~940 episode length in ~1/3 the iterations of the baseline, and the user
judged its gait visibly better. Symmetry does **not** force both legs to move in phase — it
constrains the policy to be equivariant, which permits (and is satisfied by) normal alternating
walking; the mirrored state is simply the same gait half a period later.

### What did NOT work
- **Rough-terrain fine-tuning of a flat policy**: lameness persisted after 500 iterations. A
  mature policy's gait cannot be restructured by terrain; it only gets refined. Killed by user.
- **Digit-style faithful port** (`digit_style_env_cfg.py`, all 18 reward terms): episode length
  stuck ~18 and declining at iteration 106. Digit keeps **pushes enabled** and trains backward +
  lateral commands — both punishing from a cold start. H1/G1/Cassie all disable pushes.
- **TienKung gait clock + gait-quality corrections**: episode length ~90 vs G1's ~860 at the same
  iteration. The fixed 0.85 s clock over-constrains the problem when combined with foot-clearance,
  longer-airtime and a reduced action space. Killed.

### Gait-quality reward terms (`gait_quality_rewards.py`)
- `feet_swing_clearance`: penalises a swing foot lower than 10 cm **above the stance foot**.
  Measured foot-to-foot, never against world z — world height is what broke `base_height` (3.4).
- `upright_torso`: isolates fore/aft lean via base-frame gravity x (the robot was leaning back).
- Air-time threshold 0.4 → 0.7 s rewards longer, fewer steps.
- **Trap found**: raising the air-time threshold rewards *being airborne*, so a hop maximises it.
  It MUST be paired with Digit's `no_jumps` (`mdp.desired_contacts`, penalises timesteps with no
  foot in contact) or the policy learns to jump. This is what happened in the first G1Corrected run.

### Twitching is a reward-tuning issue, not symmetry
`action_rate_l2` penalty was ~identical in both runs (−0.393 symmetry vs −0.383 baseline), so
symmetry does not cause it. We inherited G1's `action_rate_l2 = −0.005`, the weakest of the
baselines; Digit uses −0.008, TienKung-Lab −0.01. Raise it before hardware — a twitchy policy is
hard on real actuators.

### Video/recording gotchas (cost several confusing rounds)
- **Play videos: the camera does not follow the robot by default.** On rough terrain the robots
  spawn across a large tile grid and end up off-frame — the video looks empty. Fixed in
  `RobstrideRoughEnvCfg_PLAY` with `viewer.origin_type = "asset_root"`, `asset_name = "robot"`.
- `viewer.eye`/`lookat` are **offsets from the robot root** (pelvis, ~0.78 m), not world coords.
  `lookat` z must be NEGATIVE (~−0.5) to see the feet; a positive value aims at the chest and
  crops the feet out.
- **ffmpeg finishes writing asynchronously.** Copying the mp4 immediately after `play.py` returns
  yields a truncated file that renders as an empty scene. Poll the file size until it is stable
  before copying. This wasted a full round of "there are no robots in the video".
- `play.py --checkpoint` needs a **full path**; `train.py` uses `--load_run` + `--checkpoint` name.

### Launching many runs at once: stagger by 90 s, not 12 s
Six runs launched 12 s apart ALL crashed ("Failed to set root link transforms in backend", then
`forrtl: error (200): program aborting due to window-CLOSE event`). Isaac takes ~90 s to boot, so
all six were initialising simultaneously and starved each other. Relaunched in two batches of
three with **90 s between launches** and all six came up cleanly at 1024 envs. Verify each batch
is actually iterating before starting the next.

### The six-way comparison (`six_ways_env_cfg.py`, tasks `Isaac-Velocity-Way-*-v0`)
G1 / TienKung / Digit / H1 / Cassie / Hybrid reward recipes, all sharing: legs + waist_roll action
space only (no arm swing, per user), symmetry augmentation, foot-clearance, longer air time,
upright torso, and `no_jumps`. Experiment names `way_<name>`. TienKung is loosened (clock weights
halved, air-time kept) and Digit has pushes off + forward-only commands, since the faithful
versions of both collapsed.

### The fixed gait clock (TienKung-style) does NOT work on this robot — CONFIRMED 3x
Every variant using the periodic 0.85 s swing/stance clock failed: standalone TienKung flat
(vel err 0.43), TienKung-corrected (~90 ep len), round-1 TienKung (weakest), and round-2 SoftClock
(stuck at 86 while its five siblings reached 555-859). The fixed timing over-constrains when
combined with any other gait shaping. Stop trying gait-clock recipes on this morphology; the
alternating gait emerges fine from `feet_air_time` + `no_jumps` alone.

### Round-2 "soft gait" recipes (video feedback: softer landing, smaller steps, arms down)
User's round-1 pick was Hybrid. Round-2 (`soft_ways_env_cfg.py`, tasks `Isaac-Velocity-Soft-*`)
adds, on the Hybrid base: `foot_landing_velocity` (decelerate into contact = pendulum landing),
`foot_contact_impact` (punish hard strikes), `hip_yaw_forward` (feet forward, no ballerina splay),
smaller clearance/air-time (less lift, shorter steps). **First attempt over-penalised** (upright
-3.0, no_jumps -1.5, landing -1.0, etc.) and all six plateaued at ~65 by iter 400. Halving every
new penalty fixed it: five of six then reached 555-859 by iter ~430. LESSON (again): new gait-
quality penalties belong at NUDGE strength (~-0.3 to -1.0), not as hard constraints; over-
penalising silently blocks early exploration and looks like a broken recipe.

### Judging "slow start vs broken": anchor to Hybrid, not the fast round-1 recipes
Round-1 G1/H1/Cassie hit 900 by iter ~340; Hybrid started at 178 (iter 240) and only recovered to
850 by iter 700. Recipes with heavy penalties legitimately start slow. Do not kill on a low early
reading — compare to Hybrid's curve and give it to ~iter 500-600 before judging.

### THE HELD-POSE BUG (2026-07-21, root cause of every "arms still forward" complaint)
Isaac Lab action terms write PD targets ONLY for action-space joints. Joints outside the action
space never receive a target → their drives pull to ZERO = the CAD zero pose (hands forward at
chest height). `init_state.joint_pos` sets the spawn STATE and action offsets, NOT the held
target — so in every legs-only run the arms drove back to hands-forward within a step, regardless
of configured pose. Isaac Lab's `reset_scene_to_default(reset_joint_targets=False)` docstring
acknowledges this. FIX: `events.hold_default_joint_targets` (reset-mode event writing default
targets for all joints), registered in `RobstrideRoughEnvCfg` → inherited everywhere. Verified by
extracting a video frame (ffmpeg via imageio_ffmpeg) and comparing with direct-Articulation
renders, which always looked right because the preview loop wrote all targets each step.

### Arm pose FINAL (user-confirmed + visually verified): elbow +1.5708, sp 0, roll +0.2618
Elbow exactly 90° from CAD zero = hands straight down along the body (user was right all along).
My earlier "needs 136°" FK was WRONG — the forearm vector I used included the wrist joint's
lateral offset. Values beyond ~90° bend the elbow unnaturally backward (user: "a movement a human
could not do"). LOOK AT RENDERS MYSELF (Read the PNG) before claiming a pose is correct.

### Round 3 (2026-07-21): WALK/RUN split (`round3_env_cfg.py`, tasks Isaac-Velocity-R3-*)
User insight: round-1/2 big steps came from MY corrections layer (10 cm clearance reward +
air-time 0.7) — official H1/G1 use air-time 0.4/weight 0.25 and NO clearance reward, which is why
real H1 steps small. G1-700 looked best because it hadn't yet maximised the big-step incentives.
Split mirrors Unitree's remote modes: 3 WALK variants (flat, slow, lateral+backward commands,
stand_still term, official stepping values, no clearance term) for precise positioning; 3 RUN
variants (rough+stairs, 5 cm clearance, pendulum/impact shaping) for speed and stairs.
Experiments `r3_*`.

### LOCKED-KNEE GAIT: cause found and fixed (2026-08-03, round 5) — MEASURED, not eyeballed
Symptom: every round-3/4 policy walked with straight legs. User hypothesised the arms-down fix
caused it. **Measured answer: NO.** `scripts/knee_probe.py` (patches play.py's env.step to sample
joint state; use this instead of rebuilding the RSL-RL runner, which needs nested `class_name`
keys) over 500 steps, mean knee angle / % time straight:

| variant | mean knee | % straight | verdict |
|---|---|---|---|
| PendBase (r4 ref) | −3.6° | 96.1% | locked |
| **ArmsFwd** (arms back to forward) | **−4.4°** | **98.3%** | **locked → hypothesis DISPROVED** |
| KneeSoft (−0.5, min 0.15) | −3.0° | 95.6% | too weak, no effect |
| Crouch (pelvis ≤0.70 m) | −3.3° | 94.5% | ineffective alone |
| **KneeHard** (−2.0, min 0.25) | **36.1°** | **0.4%** | **WORKS** |
| **KneeTorque** (knee straightness −1.0 + no torque tax on knees) | **35.1°** | **0.9%** | **WORKS** |
| KneeDefault (0.42 rad default + deviation −0.3) | 26.4° | 0.1% | works, shallower |

Real cause = reward economics, as suspected: a locked knee carries load through structure at
near-zero torque while flexion pays `dof_torques_l2` every step, and nothing in the reward set
ever *asked* for flexion. Fix must be an explicit penalty on straightness at sufficient strength
(−2.0/min 0.25) or removing the torque tax on knees. Weak versions (−0.5) do nothing.
Note the crouch/pelvis-height cap alone does NOT work — the robot satisfies it by other means.

### PC reset under combined load (2026-07-21→26) + the reliable launch pattern
The machine hard-reset while 6 RL runs AND an OpenPI VLA training ran together — the RL alone
uses only ~26 GB GPU / 126 W / 63 °C at 6×1024 envs, so the VLA stacked on top was the trigger.
Coordinate with the user before combining heavy workloads. ALSO: fixed 90 s launch staggers are
not reliable (4/6 launches wedged mid-boot once); the robust pattern is
`scripts/launch_sequential.ps1` / `launch_r3_loadaware.ps1` — launch one, WAIT for its first
"Learning iteration" line, then launch the next, with a load gate (GPU mem/temp/RAM) between
batches and a health watchdog (temp ≥83 °C, power ≥280 W, stalls >15 min) during training.

### Arm pose history (superseded): elbow can't reach fully vertical within joint limit
CAD-zero elbow is ~90 deg flexed (hands forward). +1.5708 reads as forward in walking video;
straight-down needs ~136 deg but the limit is 2.09 (119.7 deg) and even that looks slightly
backward. Closest natural hang within limit ~1.95 (112 deg). Arms are PD-held (not in the legs+
waist_roll action space), so pose is COSMETIC for the gait and changeable without retraining.
`preview_pose.py --elbow a,b,c` renders a sweep. Real-hardware elbow range should be checked before
trusting the sim limit.

### Arm pose history (superseded)
The CAD zero already has the elbow flexed ~90° with hands forward, so "arms along the body" is NOT
elbow=90°. Values tried and rejected by the user: +2.09 (arms backward), −1.05 (hands on
shoulders), +1.5708 (still visibly bent). `scripts/preview_pose.py` now renders a comma-separated
sweep of candidates in one run (`--elbow 0.0,0.6,1.0,1.5708,2.09`) — use that instead of guessing.

## 5. Reference-robot audit (what the official Isaac Lab bipeds actually do)

- **Symmetry rewards/augmentation:** only **ANYmal** (quadruped). No biped uses any.
- **Pushes during training:** H1, G1, Cassie all **disable** them. Only Digit keeps them.
- **Terrain:** the rough configs put every env on generated terrain (incl. pyramid stairs, 5–23 cm
  steps) from iteration 1, with per-env difficulty curriculum, `max_init_terrain_level=5`.
- **Actions:** the base `ActionsCfg` is `joint_names=[".*"]` — **whole body**. G1 never overrides it,
  so "G1 does legs only" is false.
- **H1 vs G1:** structurally near-identical, differing only in weight tuning. Neither is "more
  complete". **Digit** is the most engineered biped config (~18 reward terms, explicit `no_jumps`).
- **AMP:** not used by any official Isaac Lab biped locomotion task. TienKung-Lab mentions it
  optionally for style. We have neither retargeted reference motions nor discriminator support in
  rsl_rl, so AMP is a real project, not a quick win.

---

## 6. Utility scripts (`rl_full_isaac/scripts/`)

| Script | Purpose |
|---|---|
| `joint_jog.py` | GUI slider per joint, robot fixed, gravity off — CAD-style joint inspection |
| `stand_test.py` | headless: can the robot hold its pose? prints height/tilt over 5 s (see 3.5.3) |
| `foot_zero_check.py` | FK proof that both feet are identity-rotation at zero pose |
| `audit_collisions.py` | box-vs-mesh fidelity, lists every collision body and triangle count |
| `simplify_foot_collision.py` | rewrites the two foot links' collision to the sole-plate box |
| `preview_pose.py` | headless PNG renders of a given arm pose (two camera angles) |
| `preview_terrain.py` | headless video of the rough-terrain scene |
| `acceptance_test.py` | the four ISAAC_HANDOFF gates |
| `smoke_both_tasks.py` | 8-env sanity check of the two whole-body tasks |

Note: headless rendering (`--video`, or the preview scripts) has been far more reliable than the
interactive GUI on this machine. When the GUI stalls, render instead of fighting it.

---

## 7. Next steps

1. Let `robstride_rough` finish (3000 iters); record a Play video and judge the gait.
2. If still lame, add a symmetry mechanism (rsl_rl augmentation) and/or Digit's `no_jumps`, one at
   a time, comparing against this run.
3. Hip-yaw torque gate (RS06 36 Nm vs BOM's RS03 60 Nm) during turning — **blocks the Phase-1 motor
   order**. Log `applied_torque` on `.*_hip_yaw_joint`; >2–5 % saturation ⇒ upgrade.
4. D436 camera (`D436_CAMERA_CFG` in `project_humanoid.py`) is wired into Play scenes only; its
   orientation still needs one visual verification.
5. Articulated hands: palms currently face **down** (donor `hand_base_link` frame differs from the
   CAD placeholder; the mount transform itself is faithful). Fix with a corrective rotation in the
   wrist→hand fixed joint, then reconvert. Does not affect trained locomotion policies.
6. Teleoperation / data collection track — see `../AI_HANDOFF.md`.
