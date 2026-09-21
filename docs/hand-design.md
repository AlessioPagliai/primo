# Custom Humanoid Hand Design

Shared engineering handoff for the user and the AI sessions.

Last updated: 2026-07-29

## Project Status

The humanoid will initially use the commercial Inspire Robots
`RH56DFX-2L` and `RH56DFX-2R` hands already represented in CAD and the BOM.
They remain the first-build baseline.

In parallel, the project will develop and open-source its own five-finger
hand. This is a planned project workstream, not merely a component comparison.
The custom hand is intended to replace the Inspire hands after validation.

Do not remove the Inspire hands from the active BOM until the custom hand has
passed force, backlash, heating, impact, lifetime, communication, and
integration tests.

## Intended Kinematics

Target: 15 independently actuated DoF per hand, three per digit.

| Digit | DoF 1 | DoF 2 | DoF 3 |
|---|---|---|---|
| Index, middle, ring, little | MCP abduction/adduction | MCP flexion/extension | PIP flexion/extension |
| Thumb | CMC opposition/reposition | CMC or MCP flexion/extension | IP flexion/extension |

The thumb must not blindly copy the four-finger axis arrangement. Opposition
is required for useful pinch grasps.

The DIP joints can initially be mechanically coupled to their corresponding
PIP joints or left passive. This preserves three controlled DoF per digit
without adding a fourth actuator.

The preferred architecture places an actuator physically at each controlled
joint. Tendon actuation remains the fallback if no sufficiently compact,
controllable, and reproducible commercial actuator is available.

## Packaging Reality

The DYNAMIXEL X330 envelope is `20 x 34 x 26 mm`. Although compact for a smart
servo, it is large for a human-scale PIP joint:

- A bare 20 mm motor thickness becomes approximately 24-28 mm after adding
  structural cheeks and an opposite-side support.
- The 34 mm body consumes most of a phalanx length.
- Adjacent fingers can collide during abduction.
- A motor mounted at the PIP increases distal inertia.
- Connectors and moving cable loops require additional clearance.

Therefore, XL330/XC330 actuators are suitable in a palm or forearm and possibly
at selected MCP joints, but are poor candidates for every direct PIP joint.

## Actuator Comparison

Torque values must distinguish sustainable/rated operation from momentary
stall torque.

| Actuator | Size | Mass | Rated or conservative torque | Stall or maximum torque | Control and feedback | Status |
|---|---:|---:|---:|---:|---|---|
| Waveshare `SC09` / Feetech `SCS009` | 23.2 x 12.0 x 25.5 mm | 12.5 g | 0.0686 Nm | 0.2256 Nm | TTL bus; position, estimated load, speed, voltage | Leading retail direct-joint prototype candidate |
| DYNAMIXEL `XL330-M288-T` | 20 x 34 x 26 mm | 18 g | about 0.104 Nm | 0.52 Nm | Absolute magnetic encoder, current control, current/temperature feedback, TTL | Technically better, but bulky on fingers |
| DYNAMIXEL `XC330-T288-T` | 20 x 34 x 26 mm | 23 g | about 0.20 Nm | 1.00 Nm | Absolute encoder, current control, metal gears, TTL | Strong and durable but bulky and expensive |
| KST `X06` | 20 x 7 x 16.6 mm | 6 g | 0.040 Nm | 0.176 Nm | PWM; no normal runtime telemetry | Fits easily but weak and poor for state logging |
| AGFRC `A20CLS` | 23 x 12 x 27.5 mm | 20 g | not published | 0.735 Nm advertised at 8.4 V | PWM, potentiometer, no normal runtime current telemetry | Compact and strong, but weak research interface |
| Harmonic Drive `RSF-3C` | approximately diameter 20 x 47 mm | 31 g | 0.03-0.11 Nm | 0.13-0.30 Nm, ratio-dependent | Incremental encoder; external servo driver required | Robot-grade but long, expensive, quotation-oriented |
| Bonsystems `BCSA Micro` | diameter 18 mm; other dimensions unpublished | unpublished | unpublished | unpublished | Unpublished | Promising dedicated finger actuator, not BOM-ready |

### Product Links

- SC09 product and CAD: <https://www.waveshare.com/SC09-Servo.htm>
- SC09 documentation: <https://www.waveshare.com/wiki/SC09_Servo>
- XL330-M288-T European supplier:
  <https://www.generationrobots.com/it/403817-servomotore-dynamixel-xl330-m288-t.html>
- XL330 official manual and CAD:
  <https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/>
- XC330-T288-T European supplier:
  <https://www.generationrobots.com/it/403891-servomotore-dynamixel-xc330-t288-t.html>
- XC330 official documentation:
  <https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/>
- KST X06 European supplier:
  <https://openelab.io/it/products/kst-x06-v6-hv-servo>
- AGFRC A20CLS manufacturer:
  <https://www.agfrc.com/index.php?id=2429>
- AGFRC A20CLS European supplier:
  <https://www.monsterhopups.de/Servo-AGF-RC-A20CLS>
- Harmonic Drive RSF-Supermini:
  <https://staging.harmonicdrive.net/products/actuators-and-motors/solid-shaft-actuators/rsf-supermini>
- Bonsystems BCSA Micro:
  <https://en.bonsystems.com/media-center/product-video/micro-actuator-bcsa-micro-series-promotion-viedo/>

## SC09 Versus XL330 Torque

The XL330 is not merely a more expensive SC09. It is stronger and provides
substantially better sensing and control:

- Conservative normal torque ratio:
  `0.104 / 0.0686 = 1.52`.
- Stall torque ratio:
  `0.52 / 0.2256 = 2.30`.
- XL330 encoder resolution: 4096 positions over 360 degrees, 0.088 degrees.
- SC09 sensor resolution: 1024 positions over 300 degrees, 0.293 degrees.
- XL330 supports measured-current control and current-limited position control.
- SC09 reports an estimated load value, not calibrated joint torque.

The SC09 advantage is packaging and cost:

- Thickness: 12 mm instead of 20 mm.
- Bounding volume: approximately 7.1 cubic centimetres instead of 17.7.
- Mass: 12.5 g instead of 18 g.
- Retail price: approximately USD 8.99 instead of about EUR 40.20.

## Approximate Fingertip Force

First-order estimate:

`fingertip force = joint torque / distance from joint to contact`

This ignores changing contact geometry, transmission losses, compliance, and
multi-joint load sharing.

| Joint and assumed lever | SC09 rated | SC09 stall | XL330 conservative | XL330 stall |
|---|---:|---:|---:|---:|
| MCP, 70 mm | 0.98 N | 3.22 N | 1.49 N | 7.43 N |
| PIP, 30 mm | 2.29 N | 7.52 N | 3.47 N | 17.33 N |

Stall force is momentary. It must never be used as sustainable grasp force.

The SC09 is dimensionally plausible for a direct-joint hand, but its
approximately 1 N rated MCP fingertip force makes it a light-manipulation
candidate. A complete grasp is also limited by the thumb opposition joint and
the available fingertip friction.

## Complete-Hand Implications

### Fifteen SC09 Actuators

- Actuator mass: approximately 187.5 g per hand.
- Motor purchase cost: approximately USD 135 per hand before shipping/tax.
- Theoretical simultaneous stall current: 15 A at 6 V.
- One shared TTL bus is possible, with adequate parallel power distribution.
- Suitable for a compact first prototype and light manipulation.
- Not yet proven adequate for useful box lifting or tool operation.

### Fifteen XL330 Actuators

- Actuator mass: 270 g per hand.
- Motor purchase cost: approximately EUR 603 per hand.
- Theoretical simultaneous stall current: about 22.1 A at 5 V.
- Better torque, state feedback, current limiting, SDK, and ROS support.
- Poor direct-PIP packaging.
- Better suited to protected palm/forearm tendon actuation.

### Mixed XL330 and SC09

A possible architecture would use XL330 motors at MCP flexion and SC09 motors
at MCP abduction and PIP flexion. This improves proximal torque while keeping
the fingers thinner.

However:

- The two products use different serial protocols.
- They require separate UART/protocol handling even if both use a common
  approximately 5 V power rail.
- The mechanical and control behaviour would be inconsistent across joints.

This remains an option, not a selected design.

## Mechanical Requirements

Every direct rotary joint should include:

- A motor-driven side and a coaxial passive support on the opposite side.
- A fork or double-shear structure rather than a long cantilever from the
  servo horn.
- Mechanical end stops before software or internal servo limits.
- Replaceable joint modules and accessible fasteners.
- Cable strain relief and a controlled flex loop at each moving joint.
- Finger pads with known friction and some passive compliance.
- Clearance for adjacent fingers throughout abduction and full flexion.
- A protected cable route that cannot enter pinch points.

The final CAD should model the complete actuator, horn, opposite support,
fasteners, connectors, cable bend radius, and service clearance. Comparing
only bare motor bodies is insufficient.

## Sensing And Learning Requirements

For teleoperation, ACT policies, and simulation-to-real work, record at least:

- Commanded joint position.
- Measured joint position.
- Joint velocity.
- Motor current or the best available load estimate.
- Bus voltage.
- Temperature when available.
- Command and feedback timestamps.

The SC09 does not provide measured current or temperature. Its load value must
be characterized experimentally and must not be treated as calibrated torque.
External fingertip tactile sensors or force-sensitive resistors may eventually
be required for controlled grasping.

## Validation Plan

Do not purchase 30 custom-hand actuators before validating one finger.

### Prototype 1

Build one index finger with:

- MCP abduction/adduction.
- MCP flexion.
- PIP flexion.
- A passive or coupled DIP.
- The intended structural material, bearings/supports, cables, and fingertip
  pad.

SC09 is the current first actuator to test because it is inexpensive and
dimensionally plausible. This is a test choice, not the final hand lock.

### Measurements

1. Sustained fingertip force for at least 60 seconds.
2. Peak force without using prolonged stall.
3. Loaded position error.
4. Backlash and deadband in both directions.
5. Temperature over repeated grasp cycles.
6. Impact survival with conservative test loads.
7. Wear after repeated cycles.
8. Bus update rate with three nodes, then fifteen nodes.
9. Simultaneous current draw during realistic grasps.
10. Ability to identify joint state accurately enough for teleoperation and
    policy training.

### Selection Gate

Freeze the actuator and hand CAD only after the prototype demonstrates:

- Sufficient sustainable force for the intended objects.
- Acceptable backlash and repeatability.
- No thermal failure in repeated use.
- Adequate impact durability.
- Reliable multi-node communication.
- A realistic power and wiring architecture.

If SC09 fails force or sensing requirements, compare a stronger direct module,
a mixed MCP/PIP design, or a palm-mounted tendon architecture. Do not solve a
failed actuator test by designing around advertised stall torque.

## Current Decision Summary

- Inspire RH56DFX remains the first humanoid hand.
- A custom open-source 15-DoF hand will be developed in parallel.
- Direct joint actuation is preferred.
- XL330/XC330 are too bulky for every human-scale PIP joint.
- SC09 is the leading low-cost direct-joint prototype candidate, but it is
  weaker and less observable than XL330.
- No custom-hand actuator is procurement-locked.
- The immediate next step is one instrumented three-DoF finger prototype.

