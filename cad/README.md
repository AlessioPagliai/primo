# CAD

Onshape, public document: [primo](https://cad.onshape.com/documents/2a6d830c153f862229ff478f/w/82c50406ffe66995476ba0a1/e/6ac57dbaf03b523effa40409) (in Onshape it is still titled "humanoid")

Only the right side and the centre are modelled. Onshape assembly mirror does not work for real components (a mirrored motor does not exist), so the left side is generated in the simulation pipeline; in CAD, reuse the same parts and mate them to the mirrored skeleton points. Joint positions come from the Unitree G1 `g1_29dof_mode_11` URDF ([sim/g1_joints_reference.csv](../sim/g1_joints_reference.csv)).

Motors are imported STEP files from the manufacturer (not included here, see [docs/references.md](../docs/references.md)). `motor_proxy.fs` is a FeatureScript that draws RobStride envelope proxies with bolt patterns.

## STL

`stl/` — the printed structure: 20 parts, 35 files, millimetres, left and right where the part is mirrored. Exported from the current CAD through the URDF pipeline, in link coordinates: orient them in the slicer. Design state, not print-validated. For STEP or a finer tessellation export from the Onshape document.

| Area | Parts |
|---|---|
| leg | `hip_pitch_to_roll`, `hip_roll_to_yaw`, `femur`, `tibia`, `ankle_crank_upper`, `ankle_crank_lower`, `ankle_gimbal`, `foot` |
| torso | `pelvis`, `waist_roll_to_yaw`, `ribcage`, `neck_yaw_to_pitch`, `head` |
| arm | `shoulder_pitch_to_roll`, `shoulder_roll_to_yaw`, `elbow`, `elbow_pitch_to_forearm_roll`, `forearm_roll_to_pitch`, `forearm_pitch_to_yaw`, `wrist` |

Bought, not printed: motors, hands, battery, computer, camera, converters, pushrods, rod ends, screws. They are in the [BOM](../bom/bom.xlsx); their meshes exist only in [sim/meshes](../sim/meshes/) for the simulation.

## 3MF

First printed parts, Bambu Studio projects, settings inside the files.

| File | Part | Print |
|---|---|---|
| [ankle-gimbal.3mf](3mf/ankle-gimbal.3mf) | foot–shin offset gimbal, two Ø8 shoulder-screw axes stacked in Z, pitch above roll | Bambu PPA-CF, H2C, 0.4 nozzle, 0.2 mm, 1 wall, 90 % grid infill |
| [leg-test-plate.3mf](3mf/leg-test-plate.3mf) | femur, hip roll-to-yaw bracket, tibia — fit test | PLA, H2S, 0.4 nozzle, 60 % infill |

More parts follow as the design is frozen.

## Ankle

Two RS06 in the shin, one 47 mm crank each, two pushrods with igus rod ends onto the foot. Both motors move both axes: pitch = sum, roll = difference. Pins: shoulder screws Ø8 × M6, 45 mm for the gimbal axes, 16 mm for the rod-end pivots.
