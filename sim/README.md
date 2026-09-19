# Simulation

## URDF

`urdf/primo.urdf` — 30 joints, masses, limits, RobStride torque limits, first collision bodies, 32 kg. `meshes/` — 233 STL in metres, every part including the bought ones, used by the URDF. Import into Isaac Sim with *merge fixed joints* on, floating base, self-collision off.

To rebuild it after a CAD change: export the right side + centre from Onshape (URDF exporter, `rl/urdf/rl.urdf` + `rl/meshes/`), then

```bash
python3 mirror_urdf.py ~/Downloads/rl ~/Downloads/rl_full
```

The script identifies the 17 exported joints by position, renames them (`right_hip_pitch_joint` …), converts them to revolute with limits and torque limits, mirrors leg and arm into the left side, bakes mirrored STL meshes (`*_mirror.stl`), injects the real masses (motors, battery, Thor, electronics are recognised by name) and adds collision bodies. Verified symmetric to 0.000 mm. The raw export used for the current URDF is in `onshape_export/rl.urdf`; its meshes are the files in `meshes/` without `_mirror`. What is verified and what is provisional: [docs/handoffs/mirror-debug.md](../docs/handoffs/mirror-debug.md).

## Ankle transmission

`ankle_map.py` — exact inverse/forward kinematics of the pushrod differential, Jacobian, coupled torque envelope. The simulator uses two virtual joints (pitch, roll); this map converts them to the two motor angles at deploy time. Geometry constants are provisional, see [ankle-transmission.md](ankle-transmission.md).

## Isaac Lab

Notes for the import, gains, acceptance tests and the walking policy setup: [docs/handoffs/isaac.md](../docs/handoffs/isaac.md). Legs run the RL policy; arms, hands and neck are teleoperated ([docs/handoffs/teleop.md](../docs/handoffs/teleop.md)). Training code: [isaaclab/](isaaclab/), still to be added from the workstation.

Walking on rough terrain: [video at 2:06](https://youtu.be/QdLxUgaU2rU) · [walk-kneehard.mp4](https://storage.googleapis.com/riverfamily/primo/videos/walk-kneehard.mp4) · [walk-kneetorque.mp4](https://storage.googleapis.com/riverfamily/primo/videos/walk-kneetorque.mp4)
