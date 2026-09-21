# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Legs+waist-roll tasks with gait-quality corrections, in two reward flavours.

User-requested changes after watching the symmetry policy at iteration 500:
  1. Action space limited to ankle-through-waist-roll: the 12 leg joints plus
     ``waist_roll_joint``. Waist yaw, arms, wrists and neck are PD-held and NOT commanded.
  2. Feet must actually clear the ground - the policy was shuffling and would scrape a real
     floor. Adds ``feet_swing_clearance`` (10 cm target above the stance foot).
  3. Longer, more deliberate steps instead of many tiny ones: ``feet_air_time`` threshold
     raised 0.4 -> 0.7 s and its weight increased.
  4. Torso must stay upright rather than leaning back: new ``upright_torso`` term isolating
     sagittal lean, plus a stronger ``flat_orientation_l2``.

Both flavours run with left-right symmetry augmentation (see mdp/symmetry/humanoid_biped.py),
which is what visibly reduced the lame gait.

* ``...G1Corrected...``      - G1 reward set + the four corrections above
* ``...TienKungCorrected...`` - same corrections but with TienKung's periodic gait clock
  replacing the generic air-time incentive
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from . import gait_quality_rewards, gait_rewards
from .rough_env_cfg import RobstrideRoughEnvCfg, RobstrideRoughEnvCfg_PLAY

# ankle -> waist roll. Deliberately excludes waist_yaw, arms, wrists, neck.
LEGS_AND_WAIST_ROLL = [
    ".*_hip_yaw_joint",
    ".*_hip_roll_joint",
    ".*_hip_pitch_joint",
    ".*_knee_joint",
    ".*_ankle_pitch_joint",
    ".*_ankle_roll_joint",
    "waist_roll_joint",
]
FEET_SENSOR = SceneEntityCfg("contact_forces", body_names=".*_ankle_roll_link", preserve_order=True)
FEET_ASSET = SceneEntityCfg("robot", body_names=".*_ankle_roll_link", preserve_order=True)


def _apply_corrections(cfg) -> None:
    # 1. restricted action space
    cfg.actions.joint_pos.joint_names = LEGS_AND_WAIST_ROLL

    # 2. lift the feet (target 10 cm above the stance foot)
    cfg.rewards.feet_clearance = RewTerm(
        func=gait_quality_rewards.feet_swing_clearance,
        weight=-2.0,
        params={"sensor_cfg": FEET_SENSOR, "asset_cfg": FEET_ASSET, "target_height": 0.10},
    )

    # 3. fewer, longer steps
    if cfg.rewards.feet_air_time is not None:
        cfg.rewards.feet_air_time.weight = 1.0
        cfg.rewards.feet_air_time.params["threshold"] = 0.7

    # 4. torso upright, no fore/aft lean
    cfg.rewards.upright_torso = RewTerm(func=gait_quality_rewards.upright_torso, weight=-2.0)
    cfg.rewards.flat_orientation_l2.weight = -2.0

    # 5. NO JUMPING. Digit's term: penalise every step where neither foot is in contact.
    #    Raising the air-time threshold to 0.7 s rewards long swings, which on its own also
    #    rewards being airborne on BOTH feet - this is the counterweight that forces the long
    #    swing to come from one foot at a time instead of a hop.
    cfg.rewards.no_jumps = RewTerm(
        func=mdp.desired_contacts,
        weight=-1.0,
        params={"sensor_cfg": FEET_SENSOR},
    )
    # keep vertical bouncing expensive as well
    cfg.rewards.lin_vel_z_l2.weight = -2.0

    # the waist roll joint is now commanded, so keep it near neutral rather than cranked over
    cfg.rewards.joint_deviation_torso.weight = -0.5


@configclass
class HumanoidG1CorrectedEnvCfg(RobstrideRoughEnvCfg):
    """G1 rewards + the four gait-quality corrections."""

    def __post_init__(self):
        super().__post_init__()
        _apply_corrections(self)


@configclass
class HumanoidG1CorrectedEnvCfg_PLAY(RobstrideRoughEnvCfg_PLAY):
    def __post_init__(self):
        super().__post_init__()
        _apply_corrections(self)


def _apply_tienkung_clock(cfg) -> None:
    """Replace the generic air-time incentive with TienKung's alternating gait clock."""
    cfg.rewards.feet_air_time = None
    cfg.rewards.gait_swing_force = RewTerm(
        func=gait_rewards.gait_swing_force, weight=1.0, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.gait_stance_speed = RewTerm(
        func=gait_rewards.gait_stance_speed, weight=1.0, params={"asset_cfg": FEET_ASSET}
    )
    cfg.rewards.gait_stance_support_force = RewTerm(
        func=gait_rewards.gait_stance_support_force, weight=0.6, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.action_rate_l2.weight = -0.01  # TienKung value, also damps the twitching
    cfg.rewards.feet_slide.weight = -0.25


@configclass
class HumanoidTienKungCorrectedEnvCfg(HumanoidG1CorrectedEnvCfg):
    """Same corrections, but TienKung's 0.85 s periodic gait objective."""

    def __post_init__(self):
        super().__post_init__()
        _apply_tienkung_clock(self)


@configclass
class HumanoidTienKungCorrectedEnvCfg_PLAY(HumanoidG1CorrectedEnvCfg_PLAY):
    def __post_init__(self):
        super().__post_init__()
        _apply_tienkung_clock(self)
