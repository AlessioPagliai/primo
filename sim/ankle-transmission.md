# Ankle differential transmission — derived from CAD, 2026-07-19

> **Provisional geometry.** The crank/rod/pivot dimensions below were extracted from mesh centroids of the Onshape export, not from measured CAD dimensions. Ratios, torque envelope and rod-end angles are therefore indicative only, until the linkage is measured in the CAD and the constants in `ankle_map.py` are replaced.

Companion to `ankle_map.py` (the runnable model). Answers the question "do we need to
simulate the pushrods?" and records the numbers that came out of the real geometry.

## Decision: do NOT simulate the pushrods as bodies

- URDF cannot express closed kinematic loops at all; Isaac/PhysX can (loop-closure joint),
  but it costs solver stability and speed for zero benefit to the policy.
- Every mainstream humanoid RL pipeline (Unitree, MIT, Berkeley) trains on **virtual serial
  ankle joints** and applies the transmission at deploy time. This project already decided
  this (MEMORY 2026-07-12); the geometry below confirms it is a good approximation.
- What DOES have to reach the simulator is the **consequence** of the linkage: the coupled,
  configuration-dependent torque envelope. Everything else is handled by `ankle_map.py`
  outside the policy.

## Geometry (right leg, extracted from the Onshape export, all mm)

| Quantity | Value |
|---|---|
| Crank arm, both motors | 47.75 (horizontal at zero pose) |
| Rod 1 (upper motor) eye-to-eye | 208.01 (BOM body 140 + 2 rod ends) |
| Rod 2 (lower motor) eye-to-eye | 106.01 (BOM body 40 + 2 rod ends) |
| Foot pivot pitch arm | 47.75 forward of the pitch axis |
| Foot pivot lateral half-span | 43.83 (87.65 apart) |
| Rods at zero pose | vertical; cranks at 90° to them (optimal transmission) |

This settles the old BOM question: the AliExpress rod length is the **body** length;
eye-to-eye = body + ~68 mm.

## Transmission (validated: IK→FK round trip exact to machine precision)

```
pitch = -0.500  x (th1 + th2)      common mode   -> ratio 1 : 1
roll  = -0.545  x (th2 - th1)      differential  -> ratio 1.09 : 1
```

Motor travel needed for the full URDF joint range: ±43° for pitch, ±14° for roll,
worst corner (full plantarflex + full roll) th1 = +55.6°, th2 = +31.5°. Well inside RS06 range.

**The ratio is not constant** — available torque varies 46…84 Nm across the workspace
(±25%). For training that is absorbable with domain randomization, but the **deploy-time
map must be the exact nonlinear solve in `ankle_map.py`**, not the linear ratio above.

## Torque envelope (RS06 peak 36 Nm each)

At neutral: pure pitch **72.0 Nm**, pure roll **66.1 Nm**, coupled by

```
|tau_pitch| / 72 + |tau_roll| / 66  <=  1        (diamond, not a box)
```

Continuous (RS06 rated 11 Nm): pitch **22.0 Nm**, roll **20.2 Nm**.

Pitch torque vs ankle angle (roll = 0):

| ankle pitch | available pitch torque |
|---|---|
| −50° (max plantarflex) | 46.0 Nm |
| −25° | 62.6 Nm |
| −15° (typical toe-off) | 66.8 Nm |
| 0° (neutral) | 72.0 Nm |
| +30° (dorsiflex) | 84.2 Nm |

**Corrected the URDF**: ankle roll effort was 36 Nm (a guess), the derived value is 66 Nm —
it had been 1.8× too conservative. Pitch 72 Nm was correct.

## Findings that matter for the machine

1. **Push-off is exactly at the design boundary.** MEMORY estimates ~67 Nm peak plantarflexion
   demand at 45 kg; the mechanism delivers 66.8 Nm at 15° plantarflexion and less beyond.
   Comfortable at ~35–40 kg, zero margin at 45 kg. Do NOT change CAD yet — measure the real
   demand in Isaac (same philosophy as the hip-yaw gate). If it saturates, the fix is a
   **smaller crank arm** (40 mm → 86 Nm) at the cost of ankle speed and higher rod force
   (754 N now → 900 N; igus KARM-08 CL is rated 1.7 kN short-term, so it still fits).
2. **Continuous torque limits the standing posture.** 22 Nm continuous means the standing CoM
   must sit within ~50 mm of the ankle axis (45 kg × 9.81 × 0.05 = 22 Nm). Standing with the
   CoM 90 mm forward would need 40 Nm — fine as a peak, thermally not fine as a pose. Add a
   reward/posture term that keeps the CoP near mid-foot.
3. **Rod ends are comfortably within spec — the old worry is retired.** Worst per-end
   misalignment across the whole workspace is **15.7°** (at full roll) against the igus
   KARM/KALM-08 CL **35°** limit. Pitch costs ~0° (rotation about the pin axis). The earlier
   plan to restrict roll to ±12°, and the conical-spacer / ball-stud upgrade paths, are not
   needed: the full ±15° roll is fine.
4. Zero unreachable poses inside the URDF joint limits; no singularity in range.

## What the Isaac Lab side must add

Clip ankle torques with the diamond rule instead of two independent limits:

```python
# tau_p, tau_r = desired ankle pitch/roll torques (per leg)
s = abs(tau_p) / 72.0 + abs(tau_r) / 66.0
if s > 1.0:
    tau_p, tau_r = tau_p / s, tau_r / s
```

Optionally recompute the two limits per step from `ankle_map.joint_torque_limits(pitch, roll)`
to capture the configuration dependence (cheap: one 2×2 Jacobian). Without this clip, the
policy will learn to demand simultaneous max pitch + max roll, which the real robot cannot do.

## Deploy-time use

```python
from ankle_map import ik, fk
th1, th2 = ik(pitch_cmd, roll_cmd)     # -> the two RS06 position targets
pitch, roll = fk(th1_meas, th2_meas)   # motor feedback -> observation
```

Signs follow the URDF axes but must be confirmed once against the real actuators before the
first powered ankle test.
