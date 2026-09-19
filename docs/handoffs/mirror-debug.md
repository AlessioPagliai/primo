# MIRROR_DEBUG_HANDOFF — trained policy is broken, suspect mirrored URDF

Written 2026-07-18 on the CAD Mac, for the AI instance on the Isaac Sim PC.
User trained a policy on `rl_full.urdf` and it is "super broken" — cause not yet isolated.
This doc hands over the mirroring pipeline plus a concrete debugging plan. Read this before
touching `mirror_urdf.py`.

## What "broken" could mean — narrow it down FIRST

"Broken policy" has causes that have nothing to do with mirroring: reward shaping, PD gains,
episode termination conditions, observation normalization, domain randomization ranges. Before
assuming the URDF, run the four checks below (from `ISAAC_HANDOFF.md`) if you haven't already —
they take minutes and immediately tell you whether the asset is even the right layer to debug.

1. Zero pose: robot stands upright, feet flat, no interpenetration explosion on spawn.
2. Symmetry: command +0.3 rad to BOTH hip rolls -> both legs must swing the SAME way relative
   to the body (both outward, or both inward). Repeat for shoulder rolls.
3. Total articulated mass ~32.2 kg; whole-robot COM at y ~ 0 in zero pose.
4. Knee flexes backward only.

**If test 1 or 2 fails, the URDF is implicated — keep reading.** If all four pass and the robot
holds a commanded static pose correctly but the *trained policy* still fails, the problem is very
likely reward/PD/training-side, not geometry — say so back to the user rather than re-deriving
the mirror math.

## What is verified about the mirror pipeline (don't re-derive from scratch)

`mirror_urdf.py` (repo root, CAD Mac) mirrors a right-side-only Onshape URDF export into a full
robot. This has been checked twice with an independent FK script (not just re-reading the code):

- 30 revolute joints, all 13 left/right pairs at **exactly 0.000 mm** position error and exact
  axis mirror (`aerr` < 1e-6) under the convention below.
- Whole-robot COM y = 0.1 mm in the zero pose.
- Kinematic chain confirmed connected root->pelvis->hip_pitch->...->femur (no hanging subtrees).
- Total mass 32.25 kg, matches BOM-injected component masses.

**Mirror convention** (this is the part most likely to hide a real bug if wrong — verify it
independently on the actual robot before assuming it's fine just because positions match):

- Local origins: `xyz: (x,y,z) -> (x,-y,z)`; `rpy: (r,p,y) -> (-r,p,-y)`.
- Joint axis: `(ax,ay,az) -> (-ax,ay,-az)`.
- Net effect: **the same joint command (same sign) produces mirrored motion on both sides, and
  left/right limits are numerically identical.** This is a DESIGN CHOICE the user asked for
  ("joints of left part should still work as the ones of the right"), not the only valid
  convention. If Isaac Lab, your action-space wrapper, or a reference motion/observation config
  assumes a DIFFERENT convention (e.g. mirrored sign so a positive hip-roll command means
  "adduct" on both sides some other way, or raw URDF axis without any correction), the geometry
  can be perfectly correct while producing a policy that looks broken because commands are being
  interpreted with the wrong sign somewhere in the RL stack. **Check this first** — it is the
  most likely subtle mismatch between a "geometrically correct" URDF and a "trains correctly"
  URDF, and it would NOT be caught by the symmetry check above (which only measures geometry, not
  command semantics).
- Inertials: mass unchanged, COM y flipped, `Ixy`/`Iyz` sign-flipped, `Ixx/Iyy/Izz/Ixz` unchanged.
- Meshes: real vertex-flipped STLs (y flip + triangle winding swap, normals recomputed) — NOT
  negative scale. If you see inside-out geometry or inverted collision normals on the LEFT side
  only, check `mirror_stl()` in the script, but this was visually spot-checked already.

## Known-provisional values (real candidates for "broken" if limits/torques are the issue)

From `mirror_urdf.py`'s `CANON` dict, NOT yet validated against real hardware or careful analysis:

- **All joint velocities** — conservative guesses (10-20 rad/s depending on joint), never derived
  from RobStride datasheets. If the policy wants faster joint speeds than allowed, or the guessed
  caps are unrealistically high for actual actuators, torque/velocity commands could saturate in
  ways that look like "broken" behavior.
- **Ankle pitch/roll effort** (72 / 36 Nm) — provisional estimate of the 2xRS06 differential
  transmission, not a measured or rigorously derived value. Wrong effort here directly breaks
  standing/push-off.
- **Neck limits** (+-1.57 / +-0.70 rad) — guessed, not from any G1 or hardware source.
- **Hip yaw effort** = 36 Nm (RS06, matches current CAD) — this is a KNOWN OPEN QUESTION, not a
  bug: locked BOM wants RS03 (60 Nm) instead. Log hip-yaw torque saturation during turning; if
  it saturates often, that's expected and is a real hardware gate, not a mirroring defect.

## What is explicitly NOT yet done to the URDF (do not assume it's handled)

- No real collision primitives — 15 bodies use full visual meshes copied as collisions
  (convex-decomposed by the importer). Bad collision geometry (foot especially) is a classic
  cause of "policy looks broken / feet clip through ground / robot vibrates".
- Arms/wrists have NO collision geometry at all.
- PD gains, action space, default pose, reward terms are entirely out of scope for this script —
  those live in your Isaac Lab config, not in the URDF.

## Suggested debugging order

1. Run the 4 acceptance tests above if not already done. Report exact pass/fail per test.
2. If symmetry test (test 2) fails in Isaac even though the offline FK check on the CAD Mac
   passed: the discrepancy is almost certainly in how Isaac Lab's action wrapper maps policy
   outputs to joint commands for left vs right (see "mirror convention" above), not in the URDF
   file itself. Compare your action-to-joint mapping code against the convention stated above.
3. If test 1 fails (doesn't stand / explodes on spawn): check PD gains are set on EVERY joint
   (a joint with no drive config is passive and will flop — this was flagged in the earlier
   handoff for the neck) and check foot collision geometry / initial penetration.
4. If it stands under a scripted PD pose but the TRAINED policy is broken: this is almost
   certainly reward/observation/action-space/domain-randomization, not the URDF. Do not keep
   pulling on the mirror thread — report back what specifically breaks (falls immediately? one
   leg drags? oscillates? asymmetric gait despite symmetric reward?) so the CAD Mac side can help
   target the fix instead of re-auditing geometry that has already passed independent checks.

## Files you need

- `mirror_urdf.py` — the generator, repo root on the CAD Mac (also viewable there; ask the user
  to paste it or `cat` it into this session if you need the source directly).
- `~/Downloads/rl_full/urdf/rl_full.urdf` + `~/Downloads/rl_full/meshes/` — the last verified
  build (2026-07-18 12:06, 32.25 kg, symmetry OK). If this is not what was imported into Isaac,
  get the exact file that was actually used for training first — a stale or hand-edited copy
  would explain everything without any bug in the pipeline.
- `ISAAC_HANDOFF.md` — general import/PD/acceptance-test guidance, written same day.

## Report back

Once isolated, report to the CAD Mac session (via the user) with: which of the 4 tests failed,
and if it's a genuine geometry/mirror bug, the specific joint/link name and the numeric
discrepancy (not just "it's mirrored wrong") so it can be fixed once in `mirror_urdf.py` and
re-verified with the same FK script rather than patched by hand in the URDF.
