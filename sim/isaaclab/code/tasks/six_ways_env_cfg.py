# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Six reward recipes compared under identical conditions.

Every variant shares:
  * action space = 12 leg joints + ``waist_roll_joint`` only (no arm swing, no waist yaw,
    no neck) - user requirement;
  * left-right symmetry augmentation (the change that visibly fixed the lame gait);
  * the gait-quality corrections: swing-foot clearance, longer air time, upright torso,
    and Digit's ``no_jumps`` anti-hop counterweight;
  * rough terrain with stairs, arms held along the body at elbow +90 deg.

Only the reward *philosophy* differs, so the six runs are a controlled comparison:

  1. ``G1``      - official Isaac Lab G1 weights (our current best-known baseline)
  2. ``TienKung``- periodic gait clock, LOOSENED vs the earlier attempt that collapsed
  3. ``Digit``   - Digit's 18-term set, but pushes OFF and forward-only commands
                   (keeping those two was why the faithful Digit port stalled at ~18)
  4. ``H1``      - Unitree H1 weights: stronger foot-slide and deviation penalties
  5. ``Cassie``  - deliberately minimal reward set, as a "less shaping is more" control
  6. ``Hybrid``  - G1 tracking + Digit orientation/anti-jump + strong action-rate damping
                   (-0.01) to address the twitching seen in every run so far
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from . import gait_rewards
from .legs_only_env_cfg import FEET_ASSET, FEET_SENSOR, HumanoidG1CorrectedEnvCfg, HumanoidG1CorrectedEnvCfg_PLAY


# ---------------------------------------------------------------- 2. TienKung (loosened)
def _tienkung(cfg) -> None:
    """Periodic gait clock. Softer than the first attempt, which collapsed to ~90 steps.

    Changes vs that attempt: the generic air-time reward is KEPT (halved) instead of removed,
    and the clock terms carry lower weights, so the fixed 0.85 s schedule guides the gait
    rather than dictating it on top of every other new constraint.
    """
    if cfg.rewards.feet_air_time is not None:
        cfg.rewards.feet_air_time.weight = 0.5
    cfg.rewards.gait_swing_force = RewTerm(
        func=gait_rewards.gait_swing_force, weight=0.5, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.gait_stance_speed = RewTerm(
        func=gait_rewards.gait_stance_speed, weight=0.5, params={"asset_cfg": FEET_ASSET}
    )
    cfg.rewards.gait_stance_support_force = RewTerm(
        func=gait_rewards.gait_stance_support_force, weight=0.3, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.action_rate_l2.weight = -0.01
    cfg.rewards.feet_slide.weight = -0.25


# ---------------------------------------------------------------- 3. Digit (pushes off)
def _digit(cfg) -> None:
    cfg.rewards.termination_penalty.weight = -100.0
    cfg.rewards.dof_torques_l2.weight = -1.0e-6
    cfg.rewards.dof_acc_l2.weight = -2.0e-7
    cfg.rewards.action_rate_l2.weight = -0.008
    cfg.rewards.flat_orientation_l2.weight = -2.5
    cfg.rewards.feet_slide.weight = -0.25
    cfg.rewards.ang_vel_xy_l2 = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.1)
    cfg.rewards.stand_still = RewTerm(
        func=mdp.stand_still_joint_deviation_l1,
        weight=-0.4,
        params={
            "command_name": "base_velocity",
            "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_hip_.*", ".*_knee_joint", ".*_ankle_.*"]),
        },
    )
    # the two Digit settings we deliberately do NOT copy: pushes stay off and commands stay
    # forward-only, because keeping them is what stalled the faithful port at ~18 steps.
    cfg.events.push_robot = None


# ---------------------------------------------------------------- 4. H1
def _h1(cfg) -> None:
    cfg.rewards.termination_penalty.weight = -200.0
    cfg.rewards.track_ang_vel_z_exp.weight = 1.0
    cfg.rewards.feet_slide.weight = -0.25
    cfg.rewards.joint_deviation_hip.weight = -0.2
    cfg.rewards.joint_deviation_arms.weight = -0.2
    cfg.rewards.joint_deviation_torso.weight = -0.1
    cfg.rewards.dof_torques_l2.weight = 0.0
    cfg.rewards.action_rate_l2.weight = -0.005
    cfg.rewards.dof_acc_l2.weight = -1.25e-7


# ---------------------------------------------------------------- 5. Cassie (minimal)
def _cassie(cfg) -> None:
    """Strip the shaping back to Cassie's five terms, as a control on over-shaping."""
    cfg.rewards.joint_deviation_arms = None
    cfg.rewards.joint_deviation_torso = None
    cfg.rewards.upright_torso = None
    cfg.rewards.track_lin_vel_xy_exp.weight = 2.0
    cfg.rewards.track_ang_vel_z_exp.weight = 1.0
    cfg.rewards.dof_torques_l2.weight = -5.0e-6
    if cfg.rewards.feet_air_time is not None:
        cfg.rewards.feet_air_time.weight = 2.5
    cfg.rewards.action_rate_l2.weight *= 1.5
    cfg.rewards.dof_acc_l2.weight *= 1.5


# ---------------------------------------------------------------- 6. Hybrid
def _hybrid(cfg) -> None:
    """Best-of: G1 tracking, Digit's orientation/anti-jump, hard action-rate damping."""
    cfg.rewards.flat_orientation_l2.weight = -2.5
    cfg.rewards.upright_torso.weight = -3.0
    cfg.rewards.no_jumps.weight = -1.5
    cfg.rewards.feet_slide.weight = -0.25
    cfg.rewards.action_rate_l2.weight = -0.01   # the twitching fix
    cfg.rewards.dof_acc_l2.weight = -2.0e-7
    cfg.rewards.ang_vel_xy_l2 = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.1)


_FLAVOURS = {
    "G1": None,  # the corrected base already IS the G1 recipe
    "TienKung": _tienkung,
    "Digit": _digit,
    "H1": _h1,
    "Cassie": _cassie,
    "Hybrid": _hybrid,
}


def _make(name, base, play: bool):
    fn = _FLAVOURS[name]

    @configclass
    class _Cfg(base):
        def __post_init__(self):
            super().__post_init__()
            if fn is not None:
                fn(self)

    _Cfg.__name__ = f"Humanoid{name}Way{'Play' if play else ''}EnvCfg"
    return _Cfg


# generated classes, e.g. HumanoidG1WayEnvCfg / HumanoidG1WayPlayEnvCfg
for _n in _FLAVOURS:
    globals()[f"Humanoid{_n}WayEnvCfg"] = _make(_n, HumanoidG1CorrectedEnvCfg, False)
    globals()[f"Humanoid{_n}WayPlayEnvCfg"] = _make(_n, HumanoidG1CorrectedEnvCfg_PLAY, True)
