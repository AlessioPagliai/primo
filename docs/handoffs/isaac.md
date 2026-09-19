# ISAAC_HANDOFF — rl_full.urdf (generated 2026-07-18)

For the AI instance on the Isaac Sim PC. This folder is the **training-ready artifact**;
it is generated on the CAD Mac by `mirror_urdf.py` from the raw Onshape export. **Do NOT clean or
convert the raw `rl/rl.urdf` export — it is only the right half, with placeholder masses and no
limits. Everything you flagged (dummy links, placeholder masses, no collisions/limits) is already
fixed HERE.** Project source of truth: `MEMORY.md` in the `umanoide` repo on the CAD Mac.

## What rl_full.urdf contains

- Full robot: 131 links, 30 revolute joints — 6/leg ×2, 7/arm ×2, waist roll+yaw, neck yaw+pitch.
  Left side is an exact machine-verified mirror (0.000 mm on all 13 joint pairs).
- Semantic joint names: `right_hip_pitch_joint` … `left_wrist_yaw_joint`, `waist_roll_joint`,
  `waist_yaw_joint`, `neck_yaw_joint`, `neck_pitch_joint`.
- **Axis convention: same command = mirrored motion; left limits = right limits.**
- Ankle = two serial virtual joints (pitch above roll) at the offset gimbal — the real machine is a
  2×RS06 pushrod differential; the loop is intentionally omitted (project decision; motor-to-joint
  map applied at deploy).
- Masses injected from the BOM/manuals (total 32.25 kg incl. battery 2.27, Thor 1.94, WEHO/Eaton/
  LEV100/IMU). Inertias: geometric tensors scaled to real mass (uniform-density approx).
- Effort limits = RobStride peak torque per joint. **hip_yaw = 36 Nm (RS06 as in CAD) — PENDING
  the sim gate below.** Ankle pitch 72 / roll 36 (differential, PROVISIONAL). Velocities PROVISIONAL
  (conservative). Neck limits PROVISIONAL (±1.57 / ±0.70).
- Collisions: visual-mesh copies on pelvis, ribcage, feet and all leg moving links (15 bodies).
  Arms have none yet — disable arm self-collision for now.
- Meshes: STL, `../meshes/` relative paths, metres, no negative scales.

## Import settings (URDF -> USD)

- Floating base (do NOT fix base), **merge fixed joints = ON** (absorbs `mate_connector_*` dummies
  and the massless `root`), convex decomposition for collisions, self-collision OFF initially.
- Position-drive actuators. Starting PD (RobStride QDD, torque-from-current, no output sensing):
  legs (RS04/RS06 joints) kp ≈ 100–150 Nm/rad, kd ≈ 3–5; arms kp ≈ 40–60, kd ≈ 1–2;
  waist kp ≈ 100, neck kp ≈ 10. Tune from stable-standing behaviour, not from these numbers.

## Acceptance tests (run before any training)

1. Zero pose: robot stands upright, feet flat on ground plane, no interpenetration explosion.
2. Symmetry: command +0.3 rad to BOTH hip rolls -> both legs must swing the SAME way relative to
   the body (outward or inward together). Same test on shoulder rolls.
3. Total articulated mass ≈ 32.2 kg; whole-robot COM at y ≈ 0 in zero pose.
4. Joint limit sanity: knee flexes backward only (−0.09 … +2.88 on the exported sign convention).

## Task for you: the hip-yaw sim gate (RS06 vs RS03)

CAD has RS06 (36 Nm peak) at hip yaw; the locked BOM says RS03 (60 Nm). Decision deferred to
measurement: during turning locomotion (train or scripted twist tests at full 32+ kg model),
log hip-yaw commanded torque. If it saturates at 36 Nm more than ~2–5% of steps during the target
turn rates, report it: the motors get upgraded to RS03 BEFORE the purchase order. This gate blocks
the Phase-1 leg-motor order.

## Known deferred items

- part_58 forearm bracket and the 4 ankle cranks have floor/near-zero masses until the next CAD
  export (materials being fixed); floor value 0.05 kg is applied to any moving link under 5 g.
- Thor/electronics are point masses at their CAD positions; no cable masses.
- Domain randomization for masses/inertias ±15% is appropriate given uniform-density tensors.
