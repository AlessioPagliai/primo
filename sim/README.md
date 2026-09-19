# Simulation

## URDF

Export the right side + centre from Onshape (URDF exporter, `rl/urdf/rl.urdf` + `rl/meshes/`), then:

```bash
python3 mirror_urdf.py ~/Downloads/rl ~/Downloads/rl_full
```

The script identifies the 17 exported joints by position, renames them (`right_hip_pitch_joint` …), converts them to revolute with limits and RobStride torque limits, mirrors leg and arm into the left side, bakes mirrored STL meshes, injects the real masses (motors, battery, Thor, electronics are recognised by name) and adds first collision bodies. Result: 30 joints, verified symmetric to 0.000 mm, 32 kg.

Ready package: [umanoide-urdf.zip](https://storage.googleapis.com/riverfamily/umanoide/umanoide-urdf.zip). Import into Isaac Sim with *merge fixed joints* on, floating base, self-collision off.

## Ankle transmission

`ankle_map.py` — exact inverse/forward kinematics of the pushrod differential, Jacobian, coupled torque envelope. The simulator uses two virtual joints (pitch, roll); this map converts them to the two motor angles at deploy time. Geometry constants are provisional, see [ankle-transmission.md](ankle-transmission.md).

## Isaac Lab

Notes for the import, gains, acceptance tests and the walking policy setup: [docs/handoffs/isaac.md](../docs/handoffs/isaac.md). Legs run the RL policy; arms, hands and neck are teleoperated ([docs/handoffs/teleop.md](../docs/handoffs/teleop.md)).

Walking on rough terrain (Isaac Lab): [walk-kneehard.mp4](https://storage.googleapis.com/riverfamily/umanoide/videos/walk-kneehard.mp4) · [walk-kneetorque.mp4](https://storage.googleapis.com/riverfamily/umanoide/videos/walk-kneetorque.mp4)
