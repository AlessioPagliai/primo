# Standard motors, or the housing as the bone

primo uses standard actuator modules: a closed cylinder with a bolt circle on the body and a bolt circle on the rotating output face. The best commercial humanoids use custom actuators whose housing is the structural link itself. This page records what that difference costs, what stays valid in the future, and how a later version of the robot could move towards integrated housings. Market statements are general knowledge on 2026-09-21, not a verified survey.

## Two families

| | Standard module (RobStride, CubeMars, Encos, cobot joints) | Custom integrated (Unitree, Tesla, Figure) |
|---|---|---|
| Interface | bolt circle on the body, bolt circle on the output face | the link is the housing, or clamps around it |
| Who can build it | anyone, parts can be ordered | only the maker |
| Torque per mass | RS04 ≈ 84 Nm/kg | Unitree custom ≈ 189 Nm/kg |
| Housing | dead mass, carried inside a bone | structure, heat sink and cable duct at once |
| Robot | primo ≈ 45 kg | G1 ≈ 35 kg |

Both families will keep existing. Robot arms built from standard joint modules bolted to simple links have been an industry for fifteen years; humanoids on standard modules already walk (Asimov on Encos, ToddlerBot on Dynamixel, primo in simulation). The number of module makers grows and prices fall. The penalty of the standard route is mass and bulk at the joints, not the ability to walk. For an open source robot standard modules are the point: a custom housing cannot be rebuilt by others.

## What is future proof and what is not

- Not future proof: bones drawn around the exact shape of one motor.
- Future proof: the motor as a swappable box with a declared interface — axis, envelope, body holes, output holes — and bones regenerated from that description. This is what [cad/bonegen/](../cad/bonegen/) does. A better module (lighter, hollow shaft, clampable) then costs one entry in the motor list and a new run.
- Mounting rule kept for every motor: one bone on the body holes (outer), the other bone on the output holes (inner), both on the output face. The consequence is measured in the CAD knee: the thigh is a ring plate on the 10 body holes, the shank reaches the 6 output holes through a Ø50 hub in the middle of that ring, so the shank stands off by the thickness of the thigh plate (10 mm + 2 mm gap) and the thigh screws must be counterbored.
- Clamping a bone around the motor body, as on the G1, suits aluminium links: clamp and heat sink in one. With printed PA-CF it insulates the motor (rated torque is a thermal limit: RS04 120 Nm peak, 40 Nm rated), creeps under preload, and RobStride housings are not specified for radial clamping. Face screws with metal inserts remain the right joint for a printed robot.

## The integrated route, if a later version takes it

What can be bought is a frameless motor kit: two bare rings, the stator (iron stack with the windings) and the rotor (ring with the magnets). Catalogue items from several makers. Nobody makes the stator or the rotor themselves. Everything else is made or sourced:

- housing: holds the stator by press or bonded fit and is its heat path, so aluminium
- rotor hub, rotor bearings, and an output bearing that carries the joint moments (crossed roller or a thin-section pair)
- gearbox, the hard part. Low reduction: a single-stage planetary in hardened steel from a gear shop. Berkeley Humanoid Lite prints a cycloidal stage in plastic. High reduction: a harmonic component set, three parts made to be built into a custom housing
- two encoders (rotor and output), magnet ring and sensor chip
- driver board with field-oriented control and CAN
- assembly: retaining compound, fits of a few hundredths, a jig to insert the rotor against the pull of the magnets

A complete low-reduction actuator with gearbox, encoders, driver and hollow shaft, sold without housing so that only the housing is printed, is not a catalogue item as far as known. There is a mechanical reason: in a planetary actuator the housing is part of the gearbox, it carries the ring gear and the bearing seats. The closest things are harmonic servo kits made for integration (high reduction and expensive: rejected for the legs in [motor-selection.md](motor-selection.md)), housed modules with a hollow shaft, and asking a module maker for an OEM variant with a custom housing.

Metal printing the housing: services print AlSi10Mg, but as printed it is rough and accurate to about ±0.1–0.2 mm. Stator bore, bearing seats and gear seat are finish-machined afterwards in any case. A plain round housing is cheaper and more precise turned from bar. Printing pays when the housing is also the bone: organic shape printed near net, functional seats machined in one setup.

RobStride and CubeMars are this recipe sold as a product, descended from the MIT Mini Cheetah actuator. At about EUR 200 per actuator it cannot be beaten on cost; the gain would be integration only, against months of development per actuator size, with gear quality and heat as the main risks.

## Suggested path

1. This version on standard modules, bones generated by [cad/bonegen/](../cad/bonegen/).
2. A cheap step available at once: metal bones (machined or printed aluminium) on the hottest joints with the same motors, for stiffness and a real heat path.
3. Later, as a separate experiment on one joint (knee): frameless kit, planetary stage, open driver, on a bench against an RS04 — torque, heat, backlash. Because every bone is generated from a motor interface, the robot can adopt such an actuator joint by joint.
