# CAD

Onshape, public document: [umanoide](https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/59ae5f441832129ecb22c193)

Only the right side and the centre are modelled. Onshape assembly mirror does not work for real components (a mirrored motor does not exist), so the left side is generated in the simulation pipeline; in CAD, reuse the same parts and mate them to the mirrored skeleton points. Joint positions come from the Unitree G1 `g1_29dof_mode_11` URDF ([sim/g1_joints_reference.csv](../sim/g1_joints_reference.csv)).

Motors are imported STEP files from the manufacturer (not included here, see [docs/references.md](../docs/references.md)). `motor_proxy.fs` is a FeatureScript that draws RobStride envelope proxies with bolt patterns.

## 3MF

First printed parts, Bambu Studio projects, settings inside the files.

| File | Part | Print |
|---|---|---|
| [ankle-gimbal.3mf](3mf/ankle-gimbal.3mf) | foot–shin offset gimbal, two Ø8 shoulder-screw axes stacked in Z, pitch above roll | Bambu PPA-CF, H2C, 0.4 nozzle, 0.2 mm, 1 wall, 90 % grid infill |
| [leg-test-plate.3mf](3mf/leg-test-plate.3mf) | femur, hip roll-to-yaw bracket, tibia — fit test | PLA, H2S, 0.4 nozzle, 60 % infill |

More parts follow as the design is frozen.

## Ankle

Two RS06 in the shin, one 47 mm crank each, two pushrods with igus rod ends onto the foot. Both motors move both axes: pitch = sum, roll = difference. Pins: shoulder screws Ø8 × M6, 45 mm for the gimbal axes, 16 mm for the rod-end pivots.
