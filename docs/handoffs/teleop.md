# TELEOP_HANDOFF — Meta Quest teleop of the humanoid in Isaac Sim (Mode A)

Written 2026-07-19 on the CAD Mac, for the AI instance on the Isaac Sim workstation.
Goal chosen by the user: **Mode A** — the Quest is a *tracking device only*; the operator watches
the Isaac Sim viewport as a normal 2D window over AnyDesk. NOT immersive stereo-in-headset (that
would be Mode B / CloudXR, explicitly rejected for now).

Read `ISAAC_HANDOFF.md` first for the robot asset. This doc is the teleop layer on top of it.

## The one fact that shapes everything

**AnyDesk carries only the workstation's screen + your keyboard/mouse. It does NOT carry Quest
tracking.** So the Quest's poses need their own network path to the workstation, completely
separate from AnyDesk. Everything below assumes you build that path.

Why Mode A is feasible remotely: teleop poses are tiny (head + 2 wrists + fingers + buttons, a
few hundred bytes at ~72 Hz) and cross the internet fine. The hard thing (low-latency stereo
video *to* the headset) is simply not in this design — the operator looks at the 2D AnyDesk feed.

## Architecture

```
Quest (with operator, remote)                Workstation (Isaac Sim + you)
  controllers/hands/head pose                  pose receiver (server)
        |  WebXR or native app                       |
        |  poses over network  ----------------->  retargeting
        |  (Tailscale or tunnel)                     |  wrists -> arm IK
                                                     |  fingers -> hand DOF
                                                     |  thumbstick -> walk cmd
                                                     v
                                              Isaac Sim articulation
                                                 arms/hands = teleop targets
                                                 legs = trained walking policy
                                                     |
  operator watches this viewport  <--- AnyDesk 2D ---+
```

## Humanoid-specific control split (do NOT puppet the legs)

Over any network link you cannot joint-puppet a walking humanoid's legs — balance dies. Split:

- **Legs (12 joints)**: the trained RL walking policy from the training work, taking a
  *velocity/heading command* (from a Quest thumbstick), NOT direct joint teleop.
- **Arms (7/side), hands (6 DOF/side), optionally neck (2, only if head-worn / Setup A2)**:
  teleoperated, retargeted from the Quest. These are latency-tolerant.

This keeps balance local + autonomous and sends only the latency-tolerant part over the wire.

## Robot integration points (from this project's asset — these are solid)

Joint names in `rl_full.urdf` for the teleop targets:
- Right arm: `right_shoulder_pitch/roll/yaw_joint`, `right_elbow_joint`,
  `right_wrist_roll/pitch/yaw_joint`. Left mirror-named. **7-DOF per arm -> redundant IK**
  (damped least squares / Lula; see VERIFY section).
- Hands: Inspire **RH56DFX = 6 actuated DOF per hand** (not full finger control), 24 V, RS485.
  In sim they are the hand joints under `..._wrist_yaw_link`. Human fingers must be retargeted to
  these 6 DOF, or in the simplest first version driven by a single grip scalar.
- Neck: `neck_yaw_joint`, `neck_pitch_joint` — optionally follow head yaw/pitch (nice, low value;
  do last).
- All joints already carry position/effort/velocity limits in the URDF — clamp teleop targets to
  them; never command outside.

Coordinate-frame calibration (essential): see the operator-ergonomics section below for the
user's actual method (headset on the neck, timed capture). Wrist targets are then
`robot_shoulder + scale * (quest_wrist - quest_wrist_at_calib)`, expressed relative to the
headset (torso) frame. Scale human reach to robot reach; this also bounds the workspace.

## Operator ergonomics — two possible setups (user still deciding)

The operator is remote and cannot see the workstation monitor except over AnyDesk. Two ways to
run Mode A; both stream the same tiny pose data up. The difference is where the operator sees the
sim and whether the headset is on the head.

### Setup A1 — headset on the neck, watch the external AnyDesk screen (simplest to bootstrap)
Hang the Quest around the neck facing forward, arms in a known initial pose, start on a short
**countdown timer** that captures the zero reference; head is outside the headset looking at the
AnyDesk window on the operator's own PC/laptop. No video needs to go to the headset at all —
poses only go up. Fastest path to prove the pipe. Consequences it MUST handle:
- **Proximity sensor is the #1 blocker.** The Quest sleeps/pauses the session the instant it
  thinks it is off a head. Worn on the neck it WILL trigger this. Defeat it: tape over the
  proximity sensor and/or disable auto-wake/sleep (menu path is OS-version-dependent — VERIFY).
  If tracking "randomly stops," this is almost always why. Test a session survives 60 s off-head
  before building on it.
- **Headset pose = torso/chest reference, not head.** Do wrist math relative to the headset
  frame. No head tracking -> no head->neck mapping in this setup.
- **Controller-in-FOV constraint.** Chest-facing cameras track hands held in front of the torso
  well; arms high/wide/behind lose tracking and drift on IMU. Roughly matches the robot's
  reach-in-front workspace, so tolerable — clamp/hold a limb when its controller goes untracked.

### Setup A2 — headset on the head, Isaac view piped into an in-headset 2D panel (better, preferred)
Wear the Quest normally; the teleop stack shows the Isaac viewport as a **flat 2D panel** inside
its immersive scene (mono video over the stack's video-back channel — NOT stereo sim rendering,
so still cheap, not CloudXR/Mode B). This is what the user meant by "stream the AnyDesk screen to
the Quest" — implement it as the stack streaming the sim viewport to a panel, NOT by running the
AnyDesk app on the Quest (a 2D AnyDesk window and an immersive tracking session conflict). Gains:
- **Head tracking restored** -> head->neck mapping becomes available (Phase 4).
- **Natural controller FOV** (hands in front of the face) -> much better arm tracking than A1.
- **No proximity-sensor problem** (worn normally).
- Calibration still by timer or by a controller button (both work; head is in the headset now).
Cost: one mono video stream over the internet to the headset. Latency on the *view* is tolerable
for manipulation (legs are autonomous, so nothing balance-critical rides on your eyes). On the
workstation you capture the Isaac viewport frames and feed them into the stack's WebRTC video
track — VERIFY the exact hook in your Isaac version and in Open-TeleVision/Vuer.

### Recommendation
Bring up with **A1 poses-only** (Phases 0-2) to validate tracking and retargeting with the least
plumbing, then switch to **A2** for real use once poses are proven, adding the viewport-to-panel
video stream. Calibration is timer-based and re-runnable in both (the operator will drift and
re-zero); at capture, store each wrist pose relative to the headset frame as the zero.

## Phased plan (each phase independently testable — do them in order)

**Phase 0 — network path.** Get poses reachable from Quest to workstation. Two proven options
(pick per the stack's NAT/HTTPS needs, verify locally):
- *Tailscale overlay*: install on the workstation and sideload the Android APK on the Quest ->
  they share a virtual LAN; `tailscale cert` can provide the HTTPS a WebXR page needs.
- *Public tunnel* (cloudflared/ngrok): gives a public HTTPS URL the Quest browser opens from home
  wifi with nothing sideloaded — simplest, but check WebRTC/NAT traversal for the chosen stack.
Success test: from the Quest browser, load a page served by the workstation.

**Phase 1 — poses flowing.** Stand up the pose receiver and print head + 2 wrist poses on the
workstation at ~72 Hz. Recommended stack: **Open-TeleVision / Vuer** (open-source, built exactly
for Quest-over-internet teleop: WebXR in the Quest browser, poses over WebRTC to a Python
server). You only need its *input-streaming* half for Mode A; its video-back half is optional.
UX note for Mode A: the operator wears the headset on the neck with their head outside it (see
"Operator ergonomics" above), so nothing is rendered to the lenses and passthrough vs VR does not
matter — but the Quest **proximity sensor must be defeated** or the session dies the moment the
headset leaves the head. Success test: with the headset OFF the head (on a desk/neck), poses keep
streaming for 60 s and numbers move correctly when the controllers move.

**Phase 2 — simplest arm teleop, legs holding.** Controllers only (more robust than hand
tracking). Map controller position -> wrist end-effector target -> arm IK -> position-drive the 7
arm joints. Map trigger (0-1) -> single grip closure scalar on all 6 hand DOF. Legs: hold a
standing pose (policy in stand mode, or a fixed default posture). Watch in Isaac over AnyDesk.
Success test: operator reaches, sim arm follows; trigger closes the hand.

**Phase 3 — locomotion command.** Thumbstick -> (vx, vy, yaw_rate) -> into the walking policy's
command input. Now the operator walks the robot around while arms teleop. Success test: robot
walks on stick input and stays balanced while arms are moved.

**Phase 4 (optional, later) — dexterous hands.** Quest hand tracking -> finger retargeting to the
RH56DFX 6 DOF (the **dex-retargeting** library supports Inspire hands — verify a config exists for
RH56DFX specifically). NOTE: hand tracking needs the hands in the headset camera FOV — natural in
Setup A2 (head-worn), more restrictive in A1 (neck-worn); validate before committing. Neck teleop
(head pose -> `neck_yaw_joint`/`neck_pitch_joint`) is available ONLY in A2 (head-worn); in A1 the
headset pose is the torso, so keep the neck fixed there.

## VERIFY LOCALLY — do not assume from this doc

I do not have your Isaac install in front of me; confirm these on the workstation rather than
trusting versions I might misstate:
- **Isaac Sim / Isaac Lab version and its IK API.** Recent Isaac has Lula IK / articulation
  kinematics in the motion-generation extension, and Isaac Lab has its own controllers — use
  whatever your installed version actually ships. Don't hard-code an API from memory.
- **Open-TeleVision current repo state / dependencies** (Vuer version, WebRTC/TURN needs). Check
  the live repo; it moves.
- **dex-retargeting** having a ready RH56DFX/Inspire config (Phase 4 only).
- **The walking policy's command interface** — how it accepts (vx, vy, yaw). That lives in the
  training code on your side, not here.
- Whether WebXR passthrough vs a native Quest app fits the operator's setup better.

## Latency reality (set expectations)

Manipulation reach/grasp tolerates ~100-200 ms round trip; fine here. Balance/locomotion does
NOT — which is exactly why legs are autonomous. Do not let anyone try to joint-puppet the legs
over this link.

## Report back to the CAD Mac session (via the user)

Once Phase 2 works, report: which network path you used, which teleop stack, and the IK approach —
so it can be recorded in MEMORY.md as the project's teleop decision for the next agents.
