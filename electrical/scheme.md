# Electrical Connection Scheme — Open RobStride Humanoid

Written 2026-07-17, updated 2026-07-18 (hand connection verified from the official Inspire manuals now stored in `hands/`).
Matches the BOM revision with hands on the WEHO rail and the hardware precharge chain
(`BOM umanoide G1 - RobStride.xlsx`, total EUR 30,477.03). Drawing: [electrical_scheme.svg](electrical_scheme.svg).
Negative returns are not drawn: every negative goes back to the Eaton PDU negative pole and the battery negative.
The WEHO converter is non-isolated, so the 24 V negative is the same net as the battery negative.

## 1. Power sources

| Source | Use | Connection |
|---|---|---|
| Bicycle Motor Works 13S2P Molicel P45B, 46.8 V nom / 54.6 V full, BMS 45 A cont / 100 A max | Mobile | `XT90-S` discharge lead. The XT90-S is the physical service disconnect: separate it only with the robot stopped and the LEV100 open |
| Matched 54.6 V charger (order with battery) | Charging, bench only | Separate `XT60` charge lead |
| MEAN WELL RSP-3000-48 bench supply (230 VAC in) | Bench bring-up | Feeds the same chain at the main-fuse input instead of the battery. Do not assume it absorbs regeneration |

**Dual-source mode (added 2026-07-19, MS1 requirement):** battery AND grid connected at the same
time. The two sources must NEVER be hard-paralleled — the fixed 48 V supply would float-charge the
13S pack uncontrolled, and either source can back-feed the other. They join through the
`[TO SELECT] Dual-source 48 V OR-ing stage` (one ideal-diode branch per source, common output into
the main fuse; LTC4357/LM5050 class, sized for the bench current). Until that stage is selected
and bench-verified, the safe interim procedure is source swapping at the XT90-S: battery OR grid,
never both plugged in.

## 2. 48 V distribution

```text
BATTERY + ──XT90-S──> BF1 70 A MAIN FUSE (as close to the pack as possible) ──25 mm2 trunk──> SPLIT NODE
                                                                                   │
   ┌───────────────────────────────────────────────────────────────────────────────┤
   │ UNSWITCHED compute branch (always on)                                         │ SWITCHED motor branch
   │                                                                               │
   │  MINI 15 A ──> WEHO WH-C482410 (48 V -> 24 V, 10 A, 240 W)                    ├──> CIT K2 contact ──> 100 ohm 50 W ──┐  (precharge,
   │               + >=22 uF low-ESR cap at the output (to size)                   │                                      │   in parallel
   │               = 24 V RAIL, see section 3                                      ├──> LEV100A5ANG contactor (100 A) ────┤   with LEV100)
   │                                                                               │                                      v
   │                                                                               └───────> EATON 16220-2 PDU (+ / −) <──┘
   │                                                                                          │
   │                                            ┌─────────────────┬──────────────────────────┼──────────────────┬─────────────────┐
   │                                        BF1 70 A          BF1 70 A                   BF1 40 A           BF1 30 A          BF1 30 A
   │                                        16 mm2            16 mm2                     6 mm2              6 mm2             6 mm2
   │                                        LEFT LEG          RIGHT LEG                  WAIST+NECK         LEFT ARM          RIGHT ARM
```

Motor branches (30 actuators; every branch fuse in a Littelfuse `04980921GXM5` covered holder):

| Branch | Fuse | Cable | Motors | CAN bus |
|---|---|---|---|---|
| Left leg | BF1 70 A | 16 mm² | RS04 hip pitch, RS04 hip roll, RS03 hip yaw, RS04 knee, RS06 ankle A, RS06 ankle B | Thor native CAN0 |
| Right leg | BF1 70 A | 16 mm² | same as left leg | Thor native CAN1 |
| Waist + neck | BF1 40 A | 6 mm² | RS03 waist roll, RS06 waist yaw, RS05 neck pan, RS05 neck tilt | CANable #3 |
| Left arm | BF1 30 A | 6 mm² | RS06 shoulder pitch, RS06 shoulder roll, RS00 shoulder yaw, RS06 elbow, RS00 wrist roll, RS00 wrist pitch, RS00 wrist yaw | CANable #1 |
| Right arm | BF1 30 A | 6 mm² | same as left arm | CANable #2 |

Motor power/CAN drops: RS03 and RS04 use `AMASS XT30UW-F` power plus `JST GH 1.25` CAN connectors;
RS06, RS00 and RS05 use the combined Seeed `BCCA4011` XT30 (2+2) leads (16 AWG power + 26 AWG CAN in one cable).

## 3. 24 V rail (always on, from the WEHO)

| Tap fuse (MINI, 58 VDC) | Load | Notes |
|---|---|---|
| 10 A | Thor `J74` Micro-Fit 3.0 power input | Pins 1–2 = +24 V, pins 3–4 = GND (NVIDIA pinout, verify on the kit); 2+2 contacts, 18 AWG each; Molex 43025-0400 housing + 43030 contacts; Thor nvpmodel capped at 130 W (~5.4 A) |
| 15 A | Both RH56DFX hands | 2 A max each documented; one shared fused branch routed inside the two arm trunks. OPEN DECISION: hands stay powered during e-stop unless a small 24 V relay is added in this branch |
| 2 A | Waveshare USB hub power input (7–36 V) | Hub supplies its own 5 V ports |
| 2 A | Safety-control chain (section 4) | A WEHO failure drops the chain and the motor bus: fail-safe |

Power budget (user decision 2026-07-17): Thor 130 W + hands 96 W + hub/interfaces ≈ 241 W vs 240 W rated —
over budget only at fully coincident peak, riding the 12 A over-current margin. Bench-log before locomotion.

## 4. Safety / power-up chain (pure hardware, 24 V)

```text
24 V RAIL ──MINI 2 A──> E-STOP XB4BS8442 (NC, latching, external, metal bezel) ──> node A
node A ──[START XB5AA31 (NO, momentary)] ─┬─> node B
node A ──[K1 seal-in contact] ────────────┘
node B ──> K1 latch coil (CIT A2K1CSQ24VDC1.6 #2)  [TVS 1.5KE33CA]
node B ──> K2 precharge coil (CIT A2K1CSQ24VDC1.6 #1)  [TVS 1.5KE33CA]
node B ──> H3YN-2 DC24 timer supply (ON-delay, initial 10 s, freeze at 4-5 tau measured)
timer NO contact ──> LEV100 coil  [TVS 1.5KE33CA]
```

Behavior:

1. Press START: K1 latches through its own contact, K2 closes (precharge through the 100 ohm resistor begins),
   the timer starts. The RobStride actuators boot during precharge and report VBUS over CAN: this is the free
   bus-voltage measurement used to calibrate the delay.
2. Timer expires: LEV100 closes on an already-charged bus (no arc), the resistor path is bypassed.
3. E-stop pressed (or 24 V lost): K1, K2, timer and LEV100 all drop, the motor bus is dead. Thor, hub, camera,
   IMU and audio stay alive on the unswitched rail and log the event.
4. Releasing the e-stop restarts nothing: only START does. Thor additionally refuses motor enable until VBUS
   telemetry matches battery voltage, but software is not part of the chain.

## 5. Data connections (Thor port map)

Note on "native CAN": the Thor dev kit has NO CAN connector on the I/O panel. CAN0/CAN1 come out
of the **J47 internal pin header** on the carrier board (CAN_H/CAN_L directly, transceivers
on-board per the NVIDIA docs note of 2026-07-12) through a custom crimped harness — the BOM row
`[TO DESIGN qty0] Wiring Thor J47` — whose mating connector and pinout must be verified on the
physical kit before purchase. Fallback if verification contradicts the docs: two more CANable Pro
on USB, no other change.

```text
THOR native CAN0 (J47) ──120R──[ left leg bus: 6 motors, 1 Mbps, ~45% ]──120R
THOR native CAN1 (J47) ──120R──[ right leg bus: 6 motors, 1 Mbps, ~45% ]──120R
THOR USB-A #1 ──> RealSense D436 head camera (USB 3, direct; keep off the hub)
THOR USB-A #2 ──> Waveshare USB3.2 HUB 4U (powered from 24 V)
                   ├─> MKS CANable Pro #1 ──120R──[ left arm bus: 7 motors, ~53% ]──120R
                   ├─> MKS CANable Pro #2 ──120R──[ right arm bus: 7 motors, ~53% ]──120R
                   ├─> MKS CANable Pro #3 ──120R──[ waist+neck bus: 4 motors, ~30% ]──120R
                   └─> Phidgets MOT0110 pelvis IMU (CBL4011 USB cable, 280 mm)
THOR USB-C #1 ──LINDY 36940──> Waveshare 2CH RS485 ── CH A ──> LEFT hand RS485
                                                    └─ CH B ──> RIGHT hand RS485
THOR USB-C #2 ──LINDY 41899──> Waveshare USB TO AUDIO ──PH2.0──> PUI AS03604AR speaker (mic on board)
THOR USB-C debug: recovery/flash only, keep free
```

### Hand connection detail (verified 2026-07-18 from `hands/` manuals)

Each RH56DFX has **one GX12 5-pin aviation plug** carrying both power and communication
(RH56 series user manual §1.4.1 — confirm unchanged on the delivered DFX; no DFX-specific manual is published, ask Inspire at order):

| GX12 pin | Signal | Comes from |
|---|---|---|
| 1 | GND | 24 V negative (shared 15 A hand branch, in the arm trunk) |
| 2 | VCC 24 V | 15 A hand fuse on the WEHO rail |
| 3 | RS485 A+ | Waveshare 2CH adapter, that hand's channel |
| 4 | RS485 B− | Waveshare 2CH adapter, that hand's channel |
| 5 | GND | ground reference for RS485 |

RH56DFX electrical data (2026-02 official selection guide): DC 24 V ±10%, quiescent 0.09 A, **peak 2 A**
(this officially confirms the WEHO power-budget figure), 540 g. RS485 defaults: 115200 bps, 8N1;
register protocol (0xEB 0x90 framing) or MODBUS RTU (0x03/0x06/0x10); one `HAND_ID` per hand — assign
left = 1, right = 2 (each hand is alone on its channel, but distinct IDs prevent mistakes when bench-testing
both on one bus, which the protocol supports up to 254 nodes).

CAN wiring rules: Belden `9841NH` (LSZH) shielded 120 ohm pair, bus topology with short stubs, exactly two
`YAGEO MFR-25FBF52-120R` terminations per bus (10 total). The CANable Pro adapters are STM32F072
candleLight/gs_usb, galvanically isolated; do not substitute the STM32G431 "V2.0". Set a nonzero
`CAN_TIMEOUT` on every actuator and bench-test the safe stop. The final CAN-ID / connector / termination-point
map is the `HAR-MAP-01` deliverable.

## 6. Gated before wiring (do not build from this document alone)

- Electrical-engineer release: wire gauges, connector pinouts, fuse coordination, grounding and shield
  termination, e-stop and precharge wiring (`SEQ-PWR-01` drawing), WEHO output capacitor.
- Physical verification: Thor `J74`/`J47` pinouts on the delivered kit, XT90-S gender on the delivered pack,
  RobStride GH-connector mating on a sample harness, D436 delivered outline, and the GX12 connector/pinout on
  the delivered RH56DFX hands (series-manual data; DFX-specific manual not published).
- Decisions still open: e-stop relay in the hand branch (yes/no); battery order gates (BMS trip curve, regen
  charge limit, Italy shipping).
