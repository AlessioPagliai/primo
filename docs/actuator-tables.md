# MOTOR SPEC TABLES — primo (scannable master reference)

> Quick-look spec tables for every motor we researched. The short rationale is in [motor-selection.md](motor-selection.md), the dated record in [handoffs/ai-memory.md](handoffs/ai-memory.md).
> Datasheet-confirmed numbers are exact; `~` = estimate. Backlash units matter: planetary in **arcmin (')**, harmonic in **arcsec (")** — harmonic has ~60× less backlash.
> **Status: the robot is all RobStride (section 4), decided 2026-06-20/21. Sections 1 and 3b record earlier choices and are superseded.**
> Data last updated 2026-06-21; status labels corrected 2026-09-21.

---

## 1. SUPERSEDED 2026-06-20 — all-Encos list of 2026-06-19, 3 sizes + ankle trial (34 on the quote list = 30 in robot + 4 trial)

| Model | Ø mod | Weight | Peak Nm | Cont Nm | Ratio | Cont/Peak RPM | Qty | Joints |
|---|---|---|---|---|---|---|---|---|
| EC-A6416-P2-25 | Ø88 | 805 g | 120 | 40 | 25:1 | 107/120 | 6 | legs: hip pitch/roll, knee |
| EC-A4315-P2-36 | Ø56 | 485 g | 75 | 25 | 36:1 | 109/117 | 16 | ankle×4, shoulder×6, elbow×2, hip-yaw×2, waist×2 |
| EC-A2806-P2-36 | Ø44 | 162 g | 12 | 3 | 36:1 | 207/220 | 8 | wrist×6 + neck×2 |
| EC-A4310-P2-36 | Ø56 | 382 g | 36 | 12 | 36:1 | 75/89 | 4 | ankle TRIAL spares |

---

## 2. ENCOS — full PLANETARY lineup (datasheet V3.15EAP)

| Model | Ratio | Ø mod | Length | Weight | Cont Nm | Peak Nm | Cont/Peak RPM | Kt (Nm/A) | Backlash | Nm/kg | Foxtech $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EC-A2806-P2-36 | 36:1 | Ø44 | 44 | 162 g | 3 | 12 | 207/220 | 1.35 | 12' | 74 | ~320 (est) |
| EC-A4310-P2-36 | 36:1 | Ø56 | 60.5 | 382 g | 12 | 36 | 75/89* | 1.4 | 10' | 94 | 500 |
| EC-A4315-P2-36 | 36:1 | Ø56 | 69.5 | 485 g | 25 | 75 | 109/117 | 2.8 | 10' | **155** | 520 |
| EC-A6408-P2-25 | 25:1 | Ø88 | 59.5 | 604 g | ~20 | 60 | — | — | — | — | — |
| EC-A6416-P2-25 | 25:1 | Ø88 | 67.5 | 805 g | 40 | 120 | 107/120 | 2.74 | 15' | 149 | 650 |
| EC-A8112-P1-18 | 18:1 | ~Ø81 | ~ | ~830 g | ~ | ~94 | — | — | — | — | — |
| EC-A10020-P2-24 | 24:1 | ~Ø100 | ~ | ~1350 g | ~85 | ~127 | ~57 | — | — | — | — |

*A4310 measured at 24 V → at 48 V speed ~1.5–2×. All: dual encoder, CAN/CAN-FD 1 Mbps, cross-roller bearing.

---

## 3. ENCOS — full HARMONIC lineup (datasheet V3.15EAP) — **all have dual encoder; flexspline → deflection torque sensing VIABLE**

| Model | Ratio | Ø mod | Length | Weight | Cont Nm | Peak Nm | Cont/Peak RPM | Kt (Nm/A) | Backlash | Nm/kg | Foxtech $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EC-A3814-H14-107 | 107:1 | Ø53 | 78.5 | 434 g | 20 | 60 | 47/52 | 4.2 | **10"** | 138 | 680 |
| EC-A5013-H17-100 | 100:1 | Ø63 | 81.5 | 630 g | 30 | 90 | 33/38 | 5.9 | **10"** | 143 | 780 |
| EC-A6013-H20-100 | 100:1 | Ø73 | 84 | 906 g | 40 | 130 | 45/47 | 5.6 | **10"** | 143 | — |

**Harmonic note:** backlash ~10 **arcsec** (vs ~10 arcmin planetary → 60× tighter) and the compliant flexspline winds up measurably, so the dual encoder CAN estimate torque from deflection (like ZeroErr) — the planetary models can't. BUT it's SLOW (33–52 RPM, like ZeroErr) and Encos doesn't ship a turnkey torque function (you'd DIY the deflection→torque, marginal with their 0.1–0.2° encoder accuracy).

---

## 3b. CUBEMARS — QDD + high-reduction in ONE ecosystem (MIT-mode, dual-encoder) — evaluated, NOT chosen (briefly the chosen supplier before 2026-06-20, on wrong dimensions)

| Model | Ratio | Peak Nm | Rated Nm | Size | Weight | Backdrivable | Our use |
|---|---|---|---|---|---|---|---|
| ~~AK40-10~~ | 10:1 | 4.1 | ~1.5 | ~~Ø46~~ | ~~200 g~~ | ✅ QDD | WRONG SIZE, kept for the record. Real data in the last row |
| AK45-10 | 10:1 | 7 | ~2 | Ø53×43 | 260 g | ✅ QDD | wrist |
| ~~AK70-9 V3.0~~ | 9:1 | 29 | 8.5 | ~~Ø70~~ | ~~~720 g~~ | ✅ QDD | WRONG SIZE, the model name was read as the diameter: this error produced the CubeMars choice. Real data two rows below |
| AK80-9 V3.0 | 9:1 | 22 | 9 | Ø80 | 485 g | ✅ QDD | (light mid) |
| AK10-9 V3.0 | 9:1 | 53 | 18 | Ø98×61.7 | 940 g | ✅ QDD | ankle pitch, hip yaw, waist |
| AK70-9 V3.0 | 9:1 | 29 | 8.5 | **Ø89×49** | 540 g | ✅ QDD | ankle roll, spalla, gomito (NB: Ø89 = come RS06 Ø88, NON Ø70!) |
| **AKE90-8** | 8:1 | **170** | 55 | **Ø107.5×43.5** (1.4 kg, 121 Nm/kg) | 1.4 kg | ✅ QDD | **LEGS: hip pitch/roll, knee** (NB: Ø107.5 ~ come RS04, NON Ø90) |
| AKH70-16 | 16:1 | 85 | 26 | Ø70 hollow | — | ⚠️ semi | (compact-strong alt) |
| AK45-36 | 36:1 | 24 | 8 | **Ø55×54** | 340 g | ❌ stiff | EVAL+REJECTED: slim (Ø55) ma 36:1 chiude futureproofing (force/compliance/dinamica), PESSIMO sulla caviglia (giunto di contatto). Vedi nota. |
| AK80-64 | 64:1 | 120 | 48 | **Ø98×61.9** | 850 g | ❌ stiff | NON piu' piccolo di RS04 (Ø98 vs Ø110); stiff -> inutile sulle gambe |
| AK40-10 | 10:1 | 4.1 | 1.3 | **Ø53×37** | 185 g | ✅ QDD | collo (ma RS05 Ø46 piu' piccolo) |

**DECISIONE 2026-06-21 (riapertura CubeMars chiusa): RESTA TUTTO QDD, niente 36:1.** L'utente ha riaperto per l'AK45-36 36:1 (Ø55 vs RS06 Ø88 = bracci/caviglia piu' snelli). VERDETTO ONESTO dopo 3 domande utente: (1) QDD e' piu' FUTUREPROOF - il 36:1 chiude PER SEMPRE force/impedance control + compliance + tolleranza impatti su quel giunto (ergastolo hardware, non aggiornabile via sw). (2) 36:1 PESSIMO sulla CAVIGLIA (giunto di contatto, vuole compliance al massimo) -> tenere caviglia QDD. (3) Sui BRACCI il 36:1 e' ok SOLO per manipolazione a posizione di OGGI (ACT/diffusion), ma uccide la manipolazione contact-rich/compliant futura. Siccome l'utente tiene al futureproofing/smart-control -> **TUTTO QDD, AK45-36 SCARTATO**. Bracci/caviglia chunky (Ø88) = prezzo cosmetico+~2.5kg, NON limita la capacita'; il 36:1 si'. Mappa RobStride bloccata da AI RESTA valida (o CubeMars-QDD AKE90 per gambe piu' forti 170 vs 120 Nm). NB: avevo sovra-venduto l'AK45-36 nel turno precedente, l'utente ha corretto giustamente.

CubeMars (T-Motor / Sanrui, 17 yr, IPO 2026) spans QDD->high-reduction -> pick backdrivable where it matters. More mature than RobStride. ~~Slimmer leg actuator (AKE90 Ø90 vs RS04 Ø110)~~ — correction: AKE90-8 is Ø107.5, the same diameter class as RS04; it is thinner (43.5 vs 56 mm) and stronger (170 vs 120 Nm), not slimmer.

## 4. ROBSTRIDE — **CHOSEN** — QDD (~9:1, MIT-Cheetah lineage, torque from current, NO sensor)

Specific torque is calculated on the complete actuator as `output torque / actuator mass`. The `>10 Nm/kg` target is
normally quoted using peak torque, but rated specific torque is also shown because it is the more conservative thermal check.

| Model | Ø mm | Ratio | Peak Nm | Rated Nm | Mass kg | Peak Nm/kg | Rated Nm/kg | Peak >10 | Rated >10 | Length mm | Encoder | Price ~ | Current use / note |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---|---:|---|
| RobStride 05 | Ø46 | 7.75:1 | 5.5 | 1.6 | 0.191 | **28.8** | **8.4** | PASS | **FAIL** | — | dual | ~$110 | neck only; not a major load-bearing joint |
| RobStride 00 | Ø57 | 10:1 | 14 | 5 | 0.310 | **45.2** | **16.1** | PASS | PASS | 51 | dual | ~$125 | shoulder yaw x2 + wrists x6 = 8 selected |
| RobStride 02 | Ø78 | 7.75:1 | 17 | 6 | 0.380 | **44.7** | **15.8** | PASS | PASS | 45.5 | dual | ~$145 | reserve, not currently selected |
| RobStride 06 | Ø88 | 9:1 | 36 | 11 | 0.621 | **58.0** | **17.7** | PASS | PASS | 49 | dual | ~$210 | ankles x4 + waist yaw x1 + shoulder pitch/roll x4 + elbows x2 = **11** selected |
| **RobStride 03** | **Ø106** | **9:1** | **60** | **20** | **0.900** | **66.7** | **22.2** | **PASS** | **PASS** | **56** | **dual** | **~$225** | waist roll x1 + **hip yaw x2** = **3** selected (hip yaw upgraded from RS06 2026-06-21: 45 kg aggressive turn ~36 Nm = RS06 limit -> RS03 60 Nm headroom) |
| RobStride 04 | Ø110 | 9:1 | 120 | 40 | 1.420 | **84.5** | **28.2** | PASS | PASS | 50 | dual | ~$255 | hip pitch/roll + knees, 6 total |

Source for mass, rated torque and peak torque: [RobStride Product Specification 2025-06-26](https://files.seeedstudio.com/products/RobStride/%E7%81%B5%E8%B6%B3%E6%97%B6%E4%BB%A3%E4%BA%A7%E5%93%81%E8%A7%84%E6%A0%BC%E4%BB%8B%E7%BB%8D%20RobStride%20Product%20Specification%20Document%2020250626.pdf).
Retail links: [RS00](https://www.seeedstudio.com/Robostride-00-Actuator-p-6664.html), [RS02](https://www.seeedstudio.com/Robostride-02-Actuator-p-6665.html), [RS03](https://www.seeedstudio.com/Robostride-03-Actuator-p-6774.html), [RS04](https://www.seeedstudio.com/Robostride-04-Actuator-p-6775.html), [RS05](https://www.seeedstudio.com/Robostride-05-Actuator-p-6666.html), [RS06](https://www.seeedstudio.com/Robostride-06-Actuator-p-6668.html).

Also: RS01 (**single encoder — avoid**). All QDD ~8–10:1, dual encoder, CAN 1M, 48V, FOC — backdrivable, torque from current out-of-box, NO instrumentation. Bigger per Nm than Encos.
**Map updated 2026-06-21 (30 actuators, ≈ 20.913 kg):** RS04 x6 hip pitch/roll+knees; **RS03 x3 waist-roll + hip-yaw x2**; **RS06 x11** ankles/waist-yaw/shoulder-pitch-roll/elbows; RS00 x8 shoulder-yaw+wrists; RS05 x2 neck. (Was: RS03 x1 + RS06 x13 / 20.355 kg; hip yaw moved RS06->RS03, +0.558 kg.) Waist pitch is deleted; hip pitch supplies sagittal torso motion. Ankle = **DIFFERENTIAL** (2 RS06 in shin, 2 push-rods to one foot shaft, sum=pitch / diff=roll; pitch uses both motors -> ~72 Nm, covers 45 kg push-off without leverage).

---

## 5. ALTERNATIVES EVALUATED (reference / rejected)

| Brand / model | Type | Ø | Peak Nm | Weight | Max RPM | Torque sensing | Verdict |
|---|---|---|---|---|---|---|---|
| **ZeroErr eRob 70F** | harmonic | Ø70 | 35 | 0.77 kg | 60 | **integrated (sensor + dual-enc + brake + driver)** | smallest I-series; ankle pick (tight push-off) |
| ZeroErr eRob 70I | Ø70 | Ø70 | 70 | 0.88 kg | 60 | integrated | mid/ankle-strong |
| ZeroErr eRob 80F | harmonic | Ø80 | 71 | 0.89 kg | 60 | integrated | knee/hip light |
| ZeroErr eRob 80I | harmonic | Ø80 | 112 | 1.09 kg | 60 | integrated | knee/hip (the "strong" pick) |
| ZeroErr eRob 90I | harmonic | Ø90 | 191 | 1.64 kg | 60 | integrated | heavy |
| ZeroErr eRob 110I | harmonic | Ø110 | 408 | 2.68 kg | 60 | integrated | — |
| ZeroErr eRob 142I/170I | harmonic | Ø142/170 | 892/1180 | 6.7/9.5 kg | 40 | integrated | industrial |
| ZeroErr eRob T-series | harmonic | +3–8 | same | heavier | 60 | integrated | RIGHT-ANGLE (corner) variants |
| Honpine / Leaderdrive / Laifual | harmonic | varies | varies | — | — | integrated torque-sensor option | ZeroErr PEERS, cheaper (CN); Leaderdrive=RobotEra supplier |
| HEBI X-series | SEA | — | — | — | — | series-elastic torque fb | US, best API, premium, lower torque density |
| Innfos/DAMIAO SCA | QDD | — | — | — | — | torque sensing | lighter (QDD) alternative |
| CubeMars AK10-9 | QDD | Ø98 | ~50 | 940 g | fast | current only | gap at 36 Nm; ecosystem |
| CubeMars AK70-10 | QDD | Ø89 | 25 | — | fast | current only | — |
| CubeMars AK40-10 | QDD | Ø53 | 4 | 185 g | fast | current only | — |
| Steadywin GIM3510-8 | QDD | Ø46 | 6.3 | — | — | dual-enc | wrist option |
| Steadywin GIM6010-36 | planet | Ø70 | 36 | — | slow | dual-enc | mid, 36:1 stiff |
| Dynamixel PH54/PH42 | cycloidal >300:1 | — | ~25–44 | 340 g+ | 29–33 | position servo | wrong class (not backdrivable, costly) |
| Damiao DM-J4310 | QDD | — | ~10 | — | fast | dual-enc | cheap ($116), single-ecosystem |

**ZeroErr rejected for legs:** min Ø70 / 0.77 kg (too big for ankle) + **60 RPM max** (too slow for dynamic). Confirmed from official eRob page.

---

## 6. TORQUE-SENSING OPTIONS (since Encos planetary = stiff, can't self-sense)

| Approach | How | Mass / size | Cost | Difficulty | Notes |
|---|---|---|---|---|---|
| **Sensorless UKF estimate** | Fuse motor current + encoders + IMU + **foot GRF** in an observer (IIT ergoCub, open-source) | ~zero added | low (sw) | medium (friction ID + tuning) | **Best fit** — avoids per-joint sensors. RMSE 0.05–2.5 Nm. Friction model is for harmonic → re-ID for planetary. |
| Strain-gauge flange | 4 gauges ±45° full bridge on a designed spoke/tube | ~zero | low ($) | high (bonding, thermal) | lightest, no compliance; craft-heavy |
| Dual mag-encoder flexure | 2 magnetic encoders across a torsion spring | tens of g | low ($) | medium | becomes a stiff SEA; easy electronics |
| Magnetoelastic (non-contact) | magnetize shaft, read field | small | buy (NCTE) | very high DIY | stiff, non-contact; = Tesla |
| Harmonic w/ deflection | use Encos-H / ZeroErr flexspline windup | in-actuator | motor cost | turnkey (ZeroErr) | needs harmonic, slow |
| Foot GRF (chosen for feet) | 4 load cells at foot corners, or strain gauges on the sole plate | ~zero (gauges) | ~€50 (gauges) / cheap | low–med | gives Fz + CoP/ZMP (the wrench the estimator needs). **Bota REJECTED** (cost+distal weight). |
| ~~Ready-made 6-axis F/T (Bota)~~ | ~~Rokubi/PixONE/MiniONE~~ | ~~30–500 g~~ | ~~$1–3k ea~~ | none | REJECTED 2026-06-19: too costly + distal weight. |

---

## Legend
- **Cont Nm** = continuous/rated (thermal-limited); **Peak Nm** = short-duration max.
- **Ø mod** = real module outer diameter (NOT the stator Ø in the Encos name).
- Encos name = EC-A[stator Ø][stator height]-[P planetary / H harmonic][stages]-[REDUCTION].
- All Encos (planetary AND harmonic) = dual encoder + CAN/CAN-FD; planetary can't self-sense torque (too stiff), harmonic can (flexspline).
