# Traps and lessons

Each entry is symptom, cause, fix. These cost hours individually. Most are not specific to this
robot — the Isaac Lab ones apply to any humanoid locomotion project.

---

## A. Reward design

### A1. A locked-knee gait is what your reward set is quietly asking for
**Symptom** — the robot walks on straight, stiff legs. Looks wrong, survives fine.
**Cause** — a locked knee carries body load through structure at near-zero torque. A flexed knee
pays `dof_torques_l2` every step. If nothing in the reward *asks* for flexion, locking is optimal.
**Fix** — an explicit penalty on straightness, strong enough to matter:
`knee_straightness(min_bend=0.25)` at weight -2.0. Measured effect: 96% of time straight becomes
0.4%. A weak version (-0.5, min 0.15) does literally nothing.
**Generalises to** — any posture you assume will "emerge". If it costs torque and earns nothing,
it will not emerge.

### A2. Constraining the symptom is not changing the incentive
**Symptom** — capping pelvis height to force a crouch had no effect on knee angle (94.5% straight).
**Cause** — the robot satisfied the height cap by other means (ankle/hip posture) while keeping the
knees locked.
**Fix** — penalise the quantity you actually care about.

### A3. New penalties belong at nudge strength, not constraint strength
**Symptom** — added several gait-quality penalties at once; all six variants plateaued at ~65
episode length and looked like broken recipes.
**Cause** — combined penalty magnitude suppressed early exploration. The policy could not find any
behaviour that scored well, so it found none.
**Fix** — halve everything (about -0.3 to -1.0 for shaping terms). Five of six then reached 555-859.

### A4. Episode length measures not-falling, not gait quality
**Symptom** — 983/1000 episode length and 0.03 velocity error, with a visibly lame gait.
**Fix** — judge gait on video and on measured joint angles. Survival metrics saturate long before
quality does, and past that point they cannot rank recipes at all.

### A5. Rewarding long air time rewards hopping
**Symptom** — raising the air-time threshold for longer steps produced jumping.
**Cause** — air-time reward pays for *being airborne*; a two-foot hop maximises it.
**Fix** — pair it with `no_jumps` (`mdp.desired_contacts`, penalising timesteps where no foot is in
contact) so the air time must come from one foot at a time.

### A6. The fixed periodic gait clock does not work on this morphology
**Symptom** — four separate attempts (TienKung-style 0.85 s swing/stance clock) all failed:
episode length ~90 while siblings reached 555-859.
**Cause** — a rigid timing schedule over-constrains once combined with any other gait shaping.
**Fix** — do not use it here. Alternating gait emerges from `feet_air_time` + `no_jumps` alone.

### A7. Bipeds get no symmetry help from Isaac Lab, and they benefit from it
**Symptom** — persistent asymmetric limp that survived reward retuning and terrain fine-tuning.
**Cause** — no official Isaac Lab biped config (H1, G1, Cassie, Digit) uses symmetry augmentation.
Only ANYmal, a quadruped, does.
**Fix** — `code/symmetry/humanoid_biped.py`, wired via `RslRlSymmetryCfg(use_data_augmentation=True)`.
Reached the same episode length in ~1/3 the iterations and visibly reduced the limp. Because this
URDF mirrors the joint axes, mirroring is a plain left-right swap with **no per-joint sign flips**
(ANYmal needs them). Base-frame quantities still flip: lin_vel y, ang_vel x and z, gravity y,
command vy and wz, and the height-scan grid.
**Verify it is actually running** — `verify_symmetry.py`. The augmentation has dimension-mismatch
fallbacks that silently no-op, which would look identical to "symmetry did not help".

### A8. Fine-tuning cannot restructure an entrenched gait
**Symptom** — 500 iterations of rough-terrain fine-tuning on a lame flat policy: still lame.
**Fix** — retrain from scratch when the *shape* of the behaviour is wrong. Fine-tune only for
adaptation (new terrain, new speeds), not correction.

---

## B. Isaac Lab API traps

### B1. `base_height` termination is flat-terrain-only — it silently kills rough training
**Symptom** — every rough-terrain run pinned at 1-8 episode length while the same policy scored
983 on flat.
**Cause** — `mdp.root_height_below_minimum` compares against **absolute world z**. Its own docstring
says "currently only supported for flat terrains". On generated terrain, a robot spawned in a pit or
on descending stairs is already below threshold at t=0 and terminates on frame one.
**Fix** — `self.terminations.base_height = None` in any rough config. Keep it on flat, where it is a
useful fall detector.
**How to catch this class of bug fast** — read `Episode_Termination/*` in the log before changing
anything. It names the killer directly.

### B2. Joints outside the action space are NOT held at your configured pose
**Symptom** — arms configured along the body kept appearing in the CAD forward pose in every video,
across many runs.
**Cause** — action terms write PD targets only for joints in the action space. Joints outside it
never get a target, so their drives pull toward **zero** — which is the URDF zero pose, not your
`init_state.joint_pos`. `init_state` sets the spawn *state* and the action offset, not the held
*target*. Isaac Lab's `reset_scene_to_default` has an opt-in `reset_joint_targets` flag that
acknowledges exactly this.
**Fix** — `code/tasks/events.py`: a reset-mode event writing default targets for **all** joints.
**Verify** — extract a frame from the actual training/play video, do not trust a standalone preview
script (a preview loop that writes all targets every step will always look correct).

### B3. Flat and rough have different observation sizes
**Symptom** — a flat checkpoint will not load into a rough task.
**Cause** — rough adds a 187-dim height scan (grid 0.1 m resolution, 1.6 x 1.0 m).
**Fix** — for flat-to-rough transfer, disable the height scanner (blind rough-terrain locomotion)
so the observation vector matches.

### B4. `play.py` and `train.py` take checkpoints differently
`play.py --checkpoint` wants a **full path**. `train.py` wants `--load_run <dir> --checkpoint
<filename>`, and `--resume` is a flag (`--resume True` is a parse error). `train.py --resume` also
searches inside the *new* experiment directory, so seed it with the source checkpoint first.

### B5. Straight legs at zero are a singular pose
Legs at all-zeros have no knee moment arm and buckle under load. Use a slight crouch as the default
(G1 neutral: hip pitch -0.20, knee 0.42, ankle pitch -0.23).
**But note** — a humanoid is not expected to stand passively with fixed PD gains. A "does it stand
still?" test returning FALLS is **not** a valid asset gate; real humanoids need active balance.
Do not conclude the asset is broken from that test (this was concluded once, wrongly).

---

## C. Asset and collision

### C1. Foot collision: use the sole plate, not the mesh bounding box
**Symptom (first attempt, wrong)** — replaced the foot mesh with a box built from the full-mesh AABB:
48.9 mm tall and 81.5 mm wide.
**Why wrong** — the true load-bearing sole plate is 199.9 x 70.0 x **11.9** mm. The 81.5 mm came from
the ankle *bracket*, not the sole, giving a **16% oversized support polygon** — a policy flattered in
sim that would not transfer. The 48.9 mm height made a brick whose vertical faces catch stair edges
the real thin plate clears.
**Fix** — measure the sole band specifically (lowest ~12 mm of the mesh) and box that.
`simplify_foot_collision.py` and `audit_collisions.py` do this and report box-vs-mesh fidelity.

### C2. Full-mesh collision on packed assemblies jitters under self-collision
The ankle gimbal cluster (screws, cranks, joint block) as raw convex-decomposed meshes overlaps at
rest and vibrates. With self-collision **off** (the training default) it is harmless. Simplify those
volumes before ever enabling self-collision.

### C3. Verify the URDF mirror with FK before blaming geometry
`foot_zero_check.py` walks the kinematic chain: rotation root to both feet at zero pose should be
exactly identity and symmetric. It was, here — which correctly ruled out the mirror pipeline early
and saved a lot of wasted geometry debugging.

---

## D. Tooling and workflow

### D1. Measure the thing you are judging
Two full rounds were spent tuning step size while the knees were locked and nobody had measured a
joint angle. `knee_probe.py` (patches `play.py`'s `env.step` to sample joint state during a rollout)
turns "do the knees bend?" into a number in ~3 minutes. Build the probe before the third argument
about what a video shows.
Implementation note: rebuilding the RSL-RL runner by hand fails on nested `class_name` keys — patch
the stock `play.py` instead, and insert the script directory on `sys.path` (it imports `cli_args`).

### D2. `PYTHONUNBUFFERED=1`, always
Redirected Python output is buffered. Without this, diagnostics vanish and a working process looks
hung.

### D3. Unique log file per launch
Reusing a log path while a previous process tears down causes a file-sharing violation that
silently wedges the new process. This was misdiagnosed for a long time as "two Isaac instances kill
each other". They do not — several coexist fine.

### D4. Launch runs sequentially, not on a fixed stagger
Isaac takes about 90 s to boot. Six launches 12 s apart all crashed ("Failed to set root link
transforms"). Even a 90 s fixed stagger wedged 4 of 6 once. The reliable pattern: launch one,
**wait for its first `Learning iteration` line**, then launch the next
(`launch_sequential.ps1`). Add a load gate between batches and a health watchdog during training.

### D5. ffmpeg finishes writing asynchronously
Copying the mp4 immediately after `play.py` returns yields a truncated file that renders as an
empty scene. Poll the file size until stable before copying. This produced a full round of
"there are no robots in the video".

### D6. The Play camera does not follow the robot by default
On rough terrain the robots spawn across a large tile grid and walk out of frame, so the video looks
empty. Set `viewer.origin_type = "asset_root"`, `viewer.asset_name = "robot"`. Note `viewer.eye` and
`viewer.lookat` are **offsets from the robot root** (pelvis, ~0.78 m up), not world coordinates —
`lookat` z must be negative to see the feet. Keep the eye high or the camera clips through stair
geometry and produces black frames.

### D7. Do not change five variables at once
Stated plainly because it was violated repeatedly and cost the most time overall. When a result is
bad, change one thing. Keep an unchanged control run in every batch — it is what tells you whether
the baseline still reproduces.

### D8. Distinguish a slow start from a broken recipe by the right reference
Recipes with heavy penalties legitimately start slow. G1/H1/Cassie hit ~900 by iteration 340;
Hybrid started at 178 and only recovered to 850 by iteration 700 — and Digit went 66 to 828. Judge
against the *slow* reference curve and give a run until iteration ~500-600 before killing it. Two
good runs were nearly killed on early evidence.

---

## E. Machine and environment

- **NVIDIA driver 580.88** for Isaac Sim 5.1 on Blackwell. 595.x crashes the renderer. Pin it.
- **tensordict 0.8.3**. 0.13 crashes inside Kit with torch 2.7.
- **Do not stack a VLA training run on top of six RL runs** — the machine hard-reset. Six RL runs
  alone at 1024 envs use only ~26 GB GPU, 126 W, 63 C. Coordinate heavy workloads.
- Headless rendering is far more reliable than the interactive GUI on this setup. When the GUI
  stalls, render a video instead of fighting it.
