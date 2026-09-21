# Setup and reproduction

## Environment

| Component | Version | Note |
|---|---|---|
| Python | 3.11 | Isaac Sim 5.1 requires it |
| Isaac Sim | 5.1.0 | `pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com` |
| Isaac Lab | 2.3.2 | source checkout, editable install (`isaaclab.bat --install`) |
| PyTorch | 2.7.0+cu128 | pinned by `isaacsim-core` |
| **tensordict** | **0.8.3** | **pin required** — 0.13 crashes inside Kit (`_C.pyd` access violation) |
| **NVIDIA driver** | **580.88** | **pin required** on Blackwell — 595.x crashes the RTX renderer |
| RSL-RL | as shipped with Isaac Lab 2.3.2 | |

GPU used: RTX PRO 6000 Blackwell (96 GB). Six concurrent runs at 1024 envs draw about 26 GB,
126 W, 63 C — comfortable. Do not stack other heavy training on top; the machine hard-reset once
when a VLA training job was added.

## Where the files go

The task package is an Isaac Lab extension, so the files must sit inside the Isaac Lab source tree:

```
code/assets/robstride.py
code/assets/project_humanoid.py
        -> source/isaaclab_assets/isaaclab_assets/robots/
           then add `from .robstride import *` to robots/__init__.py

code/tasks/*.py
code/tasks/agents/*.py
        -> source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/robstride/

code/symmetry/humanoid_biped.py
        -> source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/mdp/symmetry/
           then add `from . import humanoid_biped` to symmetry/__init__.py

code/scripts/*
        -> anywhere; they take absolute paths
```

**Edit one path**: `ROBSTRIDE_USD_PATH` at the top of `robstride.py` points at the converted robot
USD. Change it to wherever your `rl_full.usd` lives.

## Building the robot USD from the URDF

```bash
isaaclab.bat -p scripts/tools/convert_urdf.py \
    /path/to/rl_full.urdf /path/to/out/rl_full.usd --merge-joints --headless
```

Before converting, apply the foot-collision fix (full-mesh foot collision is both unstable and
geometrically wrong — see LESSONS.md C1):

```bash
python code/scripts/simplify_foot_collision.py     # rewrites the two foot links to a sole-plate box
python code/scripts/audit_collisions.py            # reports box-vs-mesh fidelity for every body
```

Merged body names the configs depend on: root = `root`, torso = `waist_yaw_link`,
feet = `left/right_ankle_roll_link`.

## Standard run command

Every element of this matters — see LESSONS.md section D:

```
cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& ^
  call <venv>\Scripts\activate.bat && cd /d <IsaacLab> && ^
  call <IsaacLab>\isaaclab.bat -p <script> [--headless] > <UNIQUE_log_file> 2>&1"
```

- full path to `isaaclab.bat` (a bare name fails after `cd` in cmd)
- `PYTHONUNBUFFERED=1` or your diagnostics disappear
- `OMNI_CRASHREPORTER_ENABLED=0` or crash-dump uploads stall startup
- a **unique log file per launch** — reusing one wedges the process

For multiple runs use `code/scripts/launch_sequential.ps1`: it launches one, waits for its first
`Learning iteration` line, then launches the next. Fixed staggers are not reliable.

## Task IDs

The chosen policy:

- `Isaac-Velocity-R5-KneeHard-v0` / `-Play-v0`

Other registered families (all the experiments described in HANDOFF.md):

| family | variants |
|---|---|
| `Isaac-Velocity-{Flat,Rough}-Robstride-v0` | original baselines |
| `Isaac-Velocity-Way-<X>-v0` | G1, TienKung, Digit, H1, Cassie, Hybrid |
| `Isaac-Velocity-Soft-<X>-v0` | Soft, SoftImpact, SoftSlow, SoftTiny, SoftClock, SoftPend |
| `Isaac-Velocity-R3-<X>-v0` | WalkG1, WalkH1, WalkTiny, RunPend, RunImpact, RunG1 |
| `Isaac-Velocity-R4-<X>-v0` | PendBase, PendShort, PendLow, PendSlow, ImpactShort, PendTrack |
| `Isaac-Velocity-R5-<X>-v0` | ArmsFwd, KneeSoft, **KneeHard**, Crouch, KneeDefault, KneeTorque |

## Train, play, measure

```bash
# train the chosen recipe
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-R5-KneeHard-v0 --num_envs 1024 --headless

# play a checkpoint (NOTE: full path, unlike train.py)
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-R5-KneeHard-Play-v0 --num_envs 4 \
    --video --video_length 1000 --headless \
    --checkpoint /abs/path/kneehard_model_2999.pt

# measure knee flexion (the check that should gate every reward change)
isaaclab.bat -p code/scripts/knee_probe.py \
    --task Isaac-Velocity-R5-KneeHard-Play-v0 \
    --checkpoint /abs/path/kneehard_model_2999.pt --headless

# confirm symmetry augmentation is really active (it can silently no-op)
isaaclab.bat -p code/scripts/verify_symmetry.py --headless
```

When copying a recorded video, poll the file size until it stops changing — ffmpeg finishes
writing after `play.py` returns.

## Other tools

| script | what it answers |
|---|---|
| `knee_probe.py` | Do the knees actually bend? (mean angle, % time straight) |
| `verify_symmetry.py` | Is the symmetry augmentation really mirroring, or silently no-op? |
| `foot_zero_check.py` | Is the URDF mirror exact? (FK root to both feet at zero pose) |
| `audit_collisions.py` | How well does each collision primitive match its mesh? |
| `simplify_foot_collision.py` | Rewrite foot collision to the true sole plate |
| `preview_pose.py` | Render a joint pose from two angles (sweep several values at once) |
| `joint_jog.py` | Interactive GUI slider per joint, robot fixed in space |
| `stand_test.py` | Hold the default pose and report height/tilt (see LESSONS.md B5 for its limits) |
| `launch_sequential.ps1` | Launch several runs safely |
| `probe_all.ps1` / `record_r4.ps1` | Batch measurement / batch video recording |
