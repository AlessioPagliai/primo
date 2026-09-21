# Humanoid Locomotion — RL Training Handoff

Reinforcement-learning locomotion for an open-hardware 30-DOF humanoid (all-RobStride QDD
actuators, Unitree G1 as the geometric reference), trained in **NVIDIA Isaac Sim 5.1 / Isaac Lab
2.3.2** with **RSL-RL PPO**.

This folder contains the trained walking policy, every config needed to reproduce it, the
diagnostic tooling built along the way, and — most importantly — **a written record of what went
wrong and why**, so the next person does not repeat five rounds of mistakes.

## In this repository

The robot is called **primo**. This folder is the training package exactly as it left the simulation workstation; only this section was added.

- **URDF** — `rl_full.urdf` in these documents is [sim/urdf/primo.urdf](../urdf/primo.urdf), meshes in [sim/meshes/](../meshes/). Same export, robot name changed to `primo`. Checked: the foot mesh here has the extents the foot-collision script expects (sole at z = −0.7883 m, centre x 0.0333, y ∓0.1267).
- **USD** — not included, it is built from the URDF: foot-collision fix, then `convert_urdf.py --merge-joints` ([setup/INSTALL.md](setup/INSTALL.md)). `primo.urdf` still has the mesh collision on the feet, so run `simplify_foot_collision.py` on a copy first.
- **Paths** — written on a Windows workstation, the files point to `C:\Users\WKS\...`. Edit before running:

| File | What to change |
|---|---|
| `code/assets/robstride.py` | `ROBSTRIDE_USD_PATH` → your converted USD |
| `code/assets/project_humanoid.py` | asset folder |
| `code/scripts/simplify_foot_collision.py`, `audit_collisions.py`, `foot_zero_check.py`, `solve_elbow_angle.py` | `URDF` (and `MESHES`) → `sim/urdf/primo.urdf`, `sim/meshes/` |
| `code/scripts/preview_pose.py`, `joint_jog.py` | `USD_PATH`, `OUT_DIR` |
| `code/scripts/knee_probe.py` | `PLAY` and the `sys.path` line → your Isaac Lab checkout |
| `code/scripts/*.ps1` | venv, Isaac Lab and log folders |

`policy/params_as_trained/env.yaml` keeps the original paths on purpose: it is the record of the run.

- **Policy input and output** — read from the checkpoint and from `env.yaml`:
  - observation 272 = base linear velocity 3 · base angular velocity 3 · projected gravity 3 · velocity command 3 · joint positions relative to default 30 · joint velocities 30 · last action 13 · height scan 187 (1.6 × 1.0 m grid, 0.1 m)
  - action 13 = hip yaw, roll, pitch, knee, ankle pitch, ankle roll ×2 + waist roll. Joint position targets = default pose + 0.5 × action
  - 50 Hz control (physics 0.005 s × decimation 4), actor MLP 512-256-128 ELU, no observation normalisation
  - commands trained: forward 0–1.0 m/s, no lateral, yaw ±1.0 rad/s through a heading command
  - the joint order is the one Isaac Lab resolves from the articulation (`preserve_order: false`), not the order of the list above: read it from the running environment before any deploy
  - the ankle outputs are the two virtual joints (pitch, roll): on the robot they go through [sim/ankle_map.py](../ankle_map.py) to the two motors
- **Licence** — `code/assets/`, `code/symmetry/` and `code/tasks/` derive from Isaac Lab and keep its BSD-3-Clause licence ([code/LICENSE](code/LICENSE)). Everything else, scripts, documents and the policy, is CC0 like the rest of the repository.
- **Where it continues** — open items in [NEXT_STEPS.md](NEXT_STEPS.md). The first one, the hip-yaw torque gate, decides RS03 or RS06 on hip yaw and blocks the leg order.

## What is here

| Path | What it is |
|---|---|
| `policy/` | The chosen policy (`kneehard_model_2999.pt`), a video of it walking, and the exact env/agent YAML it trained with |
| `code/tasks/` | Isaac Lab task definitions: rewards, terminations, action spaces, every recipe tried |
| `code/assets/` | Robot articulation config — PD gains, effort/velocity limits from the real RobStride motors |
| `code/symmetry/` | Left-right symmetry augmentation for a biped (Isaac Lab ships this only for quadrupeds) |
| `code/scripts/` | Diagnostic tools: knee probe, collision audit, pose preview, symmetry verifier, launchers |
| `setup/INSTALL.md` | Environment, exact versions, the two version pins that are not optional, run command |
| `HANDOFF.md` | **The full story** — the journey round by round, what failed and why |
| `LESSONS.md` | **The traps** — distilled, each with symptom → cause → fix |
| `RESULTS.md` | Measured numbers for every experiment |
| `NEXT_STEPS.md` | What to do next (push robustness, unlocking joints, the motor gate) with the traps mapped |
| `reference/` | Raw project memory and the URDF-side handoff, kept verbatim |

## The policy

`policy/kneehard_model_2999.pt` — 3000 PPO iterations, rough terrain with stairs.

- Action space: 12 leg joints + waist roll (13 DOF). Arms/wrists/neck are PD-held.
- Measured gait: mean knee flexion **36.1°**, range −5°…116°, nearly-straight only **0.4 %** of the time.
- Survives ~87 % of a 1000-step episode on generated rough terrain including 5–23 cm stairs.
- Left-right symmetric (symmetry augmentation active during training).

## Reproduce

See `setup/INSTALL.md`, then:

```bash
# train
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-R5-KneeHard-v0 --num_envs 1024 --headless

# watch a trained policy
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-R5-KneeHard-Play-v0 --num_envs 4 \
    --checkpoint /abs/path/to/kneehard_model_2999.pt

# measure whether the knees actually bend (don't trust your eyes)
isaaclab.bat -p code/scripts/knee_probe.py \
    --task Isaac-Velocity-R5-KneeHard-Play-v0 --checkpoint /abs/path/model.pt --headless
```

## Status and next steps

Working: stable symmetric walking on rough terrain and stairs, bent knees, soft landings,
arms held along the body.

Not yet done:
1. **Hip-yaw torque gate** — log applied torque on `*_hip_yaw_joint` during turning. If it
   saturates the 36 Nm RS06 limit for >2–5 % of steps, the BOM's RS03 (60 Nm) is required.
   **This measurement blocks the Phase-1 motor purchase.**
2. Push/disturbance robustness (no push randomisation has ever been enabled).
3. Unlocking more joints (arm swing, waist yaw) for a more natural gait.
4. Domain randomisation (mass, friction, latency) before any sim-to-real attempt.
5. A separate conservative "walk mode" for precise positioning — see `HANDOFF.md` round 3 for
   how *not* to do it.
