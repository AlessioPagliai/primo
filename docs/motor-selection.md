# Motor selection

primo uses 30 RobStride quasi-direct-drive actuators. That was decided on 2026-06-20/21, after an all-Encos plan (the route of the Asimov robot) and a CubeMars plan had each been adopted and dropped. This page is the short version. Every number is in [actuator-tables.md](actuator-tables.md); the dated record, with the mistakes, is in [handoffs/ai-memory.md](handoffs/ai-memory.md).

## What was asked of a motor

- low reduction, backdrivable (QDD, 6–10:1): current ≈ torque, stiffness that can be dosed from the controller, tolerance to impacts. It is what Unitree G1 does, and RL walking on it needs no torque sensor
- driver inside, CAN, two encoders (single-encoder versions such as RS01 are excluded, whatever the brand)
- orderable by anyone, with public dimensions and CAD, at a price a university or a maker can pay
- one family from 5 to 120 Nm: one firmware, one debug tool, one set of spares
- compared at equal torque: size and mass first, then cost, then availability

## Timeline

| Date | Step |
|---|---|
| 2026-06-14 | brands compared at equal torque. RobStride is the baseline BOM |
| 2026-06-16 | Asimov v1 taken as reference (same parallel ankle). Its Encos motor map rebuilt joint by joint, Encos quote asked to Foxtech |
| 2026-06-17 | reduction ratio studied for walking: 6–9:1 is the QDD range, reflected inertia grows with the square of the ratio |
| 2026-06-19 | all-Encos list finalised: A6416 ×6 legs, A4315 ×16 mid joints, A2806 ×8 wrists and neck, A4310 ×4 ankle trial |
| 2026-06-20 | reverted: QDD architecture, RobStride supplier, Unitree G1 as the reference. A CubeMars plan made just before is dropped, it rested on wrong dimensions |
| 2026-06-21 | CubeMars AK45-36 (36:1, slim) evaluated for arms and ankles and rejected: all QDD, no high reduction anywhere. Map locked: RS04 ×6, RS03 ×3, RS06 ×11, RS00 ×8, RS05 ×2, 20.9 kg of actuators. Accepted cost: ≈ 45 kg and ≈ 1.40 m instead of 35 kg and 1.20 m |
| 2026-06-23 | RobStride against CubeMars class by class: no switch |

## Asimov and Encos

[Asimov v1](https://github.com/asimovinc/asimov-1) is the closest open robot: 1.2 m, 35 kg, 25 DoF, the same two-motor parallel ankle. It uses Encos actuators on every joint, five models ([their documentation](https://docs.menlo.ai/asimov/1)):

| Encos model | Gearbox | Qty | Joints on Asimov |
|---|---|---:|---|
| EC-A4310-P2-36 | planetary 36:1 | 10 | ankles ×4, elbows ×2, wrist yaw ×2, neck ×2 |
| EC-A4315-P2-36 | planetary 36:1 | 4 | knees ×2, shoulder roll ×2 |
| EC-A6416-P2-25 | planetary 25:1 | 3 | hip pitch ×2, waist yaw |
| EC-A5013-H17-100 | harmonic 100:1 | 4 | hip roll ×2, shoulder pitch ×2 |
| EC-A3814-H14-107 | harmonic 107:1 | 4 | hip yaw ×2, shoulder yaw ×2 |

The map comes from their leg BOM and spreadsheet, the arm joints matched through the `armature` values of their simulation model. Encos is Nanjing Inks Intelligent Technology, resold by Foxtech and AIFITLAB. About USD 7 000 for the 25 actuators.

What Encos does better, and it is not small:

| 36 Nm class | Size | Mass | Nm/kg | Reduction | Price |
|---|---|---:|---:|---|---|
| Encos EC-A4310-P2-36 | Ø56 × 60.5 | 382 g | 94 | 36:1 | ≈ USD 500–700 |
| RobStride RS06 | Ø88 × 49 | 621 g | 58 | 9:1 | ≈ EUR 200 |

On the legs EC-A6416 is Ø88 and 805 g against Ø106 and 1 420 g of RS04, same 120 Nm peak: −3.7 kg on six joints. Stiff and precise in position, which is good for calm walking and for position-based manipulation policies (ACT, diffusion).

Why it was not chosen:

- reduction. Reflected inertia against RobStride 9:1 is about 8× at 25:1 and 16× at 36:1, 100× and more on the harmonic joints. The joint is less backdrivable, answers worse to impacts, and current stops being a usable measure of torque. The worst place is the ankle, the contact joint, exactly where Asimov has 36:1
- it cannot be fixed later. High reduction walks well when every actuator has an output torque sensor (the Tesla route). Encos planetary has none and is too stiff to estimate torque from its two encoders. A QDD keeps force control, compliance and contact-rich manipulation open by software; 36:1 closes them in hardware
- reproducibility. Encos is sold on quotation by resellers, without public CAD or dimensions. Foxtech answered quickly, but price to Italy, CAD and lead time were still open when the decision was taken. RobStride has public specifications and STEP, and is in stock at Seeed Studio and several other shops
- price: about 3.5× at 36 Nm; the 150 Nm Encos A10020 is ≈ USD 2 250 against ≈ USD 255 of RS04
- the target moved. Asimov fitted a light, tethered robot that walks calmly on flat floor. primo carries its battery, weighs ≈ 45 kg and is meant for rough terrain, pushes and later dynamic motion: the Unitree G1 class, which is QDD

Honest note: for calm walking plus position-based manipulation only, Encos was judged the better fit (2026-06-20). RobStride was chosen for what the robot should be able to become. The price is paid in size and mass: Ø88 ankles and arms, a longer shin, about 2.5 kg more between ankles and arms.

## CubeMars

Same family of actuator as RobStride (low-reduction QDD, MIT Mini Cheetah lineage; T-Motor is the same company). A first CubeMars plan rested on reading the model name as the diameter: AK70-9 is Ø89 × 49, not Ø70; AKE90-8 is Ø107.5 × 43.5, not Ø90. With the real sizes:

| Class, joints | RobStride | CubeMars | Verdict |
|---|---|---|---|
| ≈ 5 Nm, neck | RS05 Ø46 × 44, 191 g, 5.5 / 1.6 Nm | AK40-10 Ø53 × 37, 185 g, 4.1 / 1.3 Nm | RS05: smaller and stronger |
| 10–15 Nm, wrists, shoulder yaw | RS00 Ø57 × 51, 310 g, 14 / 5 Nm | AKE60-8 Ø69 × 25, 260 g, 12.5 / 5 Nm · AK45-10 Ø53 × 43, 260 g, 7 / 2.5 Nm | RS00. AKE60-8 only if thickness is the problem |
| 25–36 Nm, ankles, shoulders, elbows | RS06 Ø88 × 49, 621 g, 36 / 11 Nm | AK70-9 Ø89 × 49, 540 g, 29 / 8.5 Nm · AKE80-8 Ø87 × 32, 570 g, 30 / 12 Nm | no CubeMars win: same size and weaker, or thinner with external driver |
| 50–60 Nm, hip yaw, waist roll | RS03 Ø98 × 54, 900 g, 60 / 20 Nm | AK10-9 Ø98 × 62, 940 g, 53 / 18 Nm | RS03 |
| 120–170 Nm, hip pitch and roll, knee | RS04 Ø106 face, ≈ Ø120 envelope × 56, 1 420 g, 120 / 40 Nm | AKE90-8 Ø107.5 × 43.5, 1 400 g, 170 / 55 Nm | the only real CubeMars upgrade |

Torque is peak / rated. CubeMars has nothing compact around 36 Nm, where primo has most of its joints, and its AKE motors need an external driver; RobStride has the driver inside and no gap from RS05 to RS04. CubeMars costs about twice (AKE90-8 ≈ USD 484 plus driver against ≈ USD 255). It was not dropped for control reasons: it was dropped to keep one ecosystem, together with Damiao.

Still open as an upgrade: AKE90-8 on hips and knees, +50 Nm and 13 mm thinner at the same mass, if the simulated leg torques ask for it. The slim 36:1 AK45-36 (Ø55 × 54, 24 / 8 Nm) was rejected for the same reason as Encos.

## Others

| Candidate | Type | Outcome |
|---|---|---|
| Dynamixel PH42, PH54 | cycloidal position servo, 300–500:1 | wrong class: not backdrivable, 29–33 rpm, PH54 USD 3 541 and still 44 Nm. ToddlerBot walks on small Dynamixel servos, at 3.4 kg |
| ZeroErr eRob | harmonic, torque sensor, brake and driver inside | from Ø70 and 0.77 kg, 60 rpm: too big for the ankle, slow for the knee, expensive |
| Honpine, Leaderdrive, Laifual | harmonic with torque sensor option | same category as ZeroErr, quotes asked, not pursued |
| HEBI X-series | series elastic | premium, low torque density |
| Steadywin GIM3510, GIM6010-36 | small planetary, MIT protocol, public CAD | candidate for wrists in the Encos plan. Not needed with RS00 |
| MyActuator RMD-X | planetary | best ROS 2 support and CAD, bigger per Nm |
| Damiao DM-J4310 | QDD | cheap, removed with CubeMars to keep one ecosystem |
| RobStride RS01 | QDD, one encoder | excluded |
| RobStride RS02 | QDD, 17 / 6 Nm | reserve at quantity 0 |

## Open

- hip yaw: RS03 in the BOM, RS06 in the CAD. Decided by the torque measured in simulation: [sim/isaaclab/NEXT_STEPS.md](../sim/isaaclab/NEXT_STEPS.md)
- check simulated torques against the rated figures, not the peak ones: RS04 is 120 Nm peak and 40 Nm rated
- leg upgrade to AKE90-8 only if those torques ask for it
