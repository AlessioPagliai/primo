# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Second-generation recipes, tuned from the user's video feedback on the six-way bake-off.

Winner of round 1: **Hybrid** (G1 tracking + Digit orientation/anti-jump + hard action-rate
damping). All six here build on it and address the specific faults the user called out:

  * "foot comes up, stays up, then goes down very fast and hits the ground hard" -> want a
    rounder, pendulum-like up/down with a gentle landing. New rewards ``foot_landing_velocity``
    (decelerate into contact) and ``foot_contact_impact`` (punish the strike that survives).
  * "steps too big, feet lifted too much" (worse at 3000) -> lower clearance target
    (0.10 -> 0.06 m) and shorter air-time threshold (0.7 -> 0.45 s); one variant also lowers
    the commanded speed so the natural step is shorter.
  * "feet point outward like a ballerina because hip yaw is rotated" (Digit/TienKung) -> a
    stronger hip-yaw deviation penalty keeps the toes forward.
  * arms along the body, not 90 deg forward. Arms are PD-held (not in the action space), so the
    pose is cosmetic for the gait; set here and trivially changed without retraining.

The six differ only in HOW the soft landing and step size are pursued, so the user can pick the
feel they want:

  1. ``Soft``      - landing-velocity penalty only
  2. ``SoftImpact``- + contact-force impact penalty
  3. ``SoftSlow``  - both, plus a lower commanded velocity (shorter steps)
  4. ``SoftTiny``  - both, plus the lowest clearance/air-time (smallest, gentlest steps)
  5. ``SoftClock`` - both, plus a light periodic clock for an even up/down rhythm
  6. ``SoftPend``  - both, but the landing penalty is applied over the whole swing, not just
                     near the ground, pushing hardest toward a smooth pendulum arc
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from . import gait_quality_rewards, gait_rewards
from .legs_only_env_cfg import FEET_ASSET, FEET_SENSOR, HumanoidG1CorrectedEnvCfg, HumanoidG1CorrectedEnvCfg_PLAY

# arms along the body: elbow near its most-downward within the joint limit (see MEMORY - the
# forearm cannot reach fully vertical inside the current elbow limit, 1.95 is the closest natural
# hang). shoulder_pitch 0, shoulder_roll +15 deg outward for hip clearance.
ARMS_ALONG_BODY = {
    ".*_shoulder_pitch_joint": 0.0,
    ".*_shoulder_roll_joint": 0.2617993877991494,
    ".*_elbow_joint": 1.5707963267948966,  # user-confirmed: exactly 90 deg = hands down
}


def _soft_base(cfg) -> None:
    # --- start from the Hybrid recipe (round-1 winner) ---
    # NOTE: round 2a stacked strong penalties (upright -3.0, no_jumps -1.5, plus new landing/
    # impact/hip-yaw terms) and all six plateaued at ~65 by iter 400 - the penalties blocked
    # early exploration. These are softened to nudges: gait quality is shaped, not forced.
    cfg.rewards.flat_orientation_l2.weight = -1.5
    cfg.rewards.upright_torso.weight = -1.0
    cfg.rewards.no_jumps.weight = -1.0
    cfg.rewards.feet_slide.weight = -0.2
    cfg.rewards.action_rate_l2.weight = -0.008
    cfg.rewards.dof_acc_l2.weight = -1.5e-7

    # --- arms along the body (cosmetic; arms are PD-held) ---
    cfg.scene.robot.init_state.joint_pos.update(ARMS_ALONG_BODY)

    # --- smaller steps, less foot lift (a bit less aggressive than 2a) ---
    cfg.rewards.feet_clearance.params["target_height"] = 0.07
    if cfg.rewards.feet_air_time is not None:
        cfg.rewards.feet_air_time.params["threshold"] = 0.5

    # --- feet point forward, no ballerina splay (gentle) ---
    cfg.rewards.hip_yaw_forward = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.25,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*_hip_yaw_joint")},
    )


def _soft(cfg) -> None:
    _soft_base(cfg)
    cfg.rewards.foot_landing = RewTerm(
        func=gait_quality_rewards.foot_landing_velocity,
        weight=-0.4,
        params={"asset_cfg": FEET_ASSET, "near_height": 0.06},
    )


def _soft_impact(cfg) -> None:
    _soft(cfg)
    cfg.rewards.foot_impact = RewTerm(
        func=gait_quality_rewards.foot_contact_impact,
        weight=-1.0e-4,
        params={"sensor_cfg": FEET_SENSOR, "threshold": 500.0},
    )


def _soft_slow(cfg) -> None:
    _soft_impact(cfg)
    # shorter natural step by asking for less speed
    cfg.commands.base_velocity.ranges.lin_vel_x = (0.0, 0.7)


def _soft_tiny(cfg) -> None:
    _soft_impact(cfg)
    cfg.rewards.feet_clearance.params["target_height"] = 0.04
    if cfg.rewards.feet_air_time is not None:
        cfg.rewards.feet_air_time.params["threshold"] = 0.35
        cfg.rewards.feet_air_time.weight = 0.5


def _soft_clock(cfg) -> None:
    _soft_impact(cfg)
    cfg.rewards.gait_swing_force = RewTerm(
        func=gait_rewards.gait_swing_force, weight=0.4, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.gait_stance_speed = RewTerm(
        func=gait_rewards.gait_stance_speed, weight=0.4, params={"asset_cfg": FEET_ASSET}
    )


def _soft_pend(cfg) -> None:
    _soft_impact(cfg)
    # apply the landing-velocity penalty over the whole swing, not just near the ground,
    # so the entire up/down follows a smooth decelerating arc
    cfg.rewards.foot_landing.params["near_height"] = 0.15
    cfg.rewards.foot_landing.weight = -0.3


_FLAVOURS = {
    "Soft": _soft,
    "SoftImpact": _soft_impact,
    "SoftSlow": _soft_slow,
    "SoftTiny": _soft_tiny,
    "SoftClock": _soft_clock,
    "SoftPend": _soft_pend,
}


def _make(name, base, play):
    fn = _FLAVOURS[name]

    @configclass
    class _Cfg(base):
        def __post_init__(self):
            super().__post_init__()
            fn(self)

    _Cfg.__name__ = f"Humanoid{name}{'Play' if play else ''}EnvCfg"
    return _Cfg


for _n in _FLAVOURS:
    globals()[f"Humanoid{_n}EnvCfg"] = _make(_n, HumanoidG1CorrectedEnvCfg, False)
    globals()[f"Humanoid{_n}PlayEnvCfg"] = _make(_n, HumanoidG1CorrectedEnvCfg_PLAY, True)
