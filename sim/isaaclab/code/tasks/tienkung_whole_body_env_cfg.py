# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Humanoid whole-body flat task using TienKung's periodic walking clock.

This is intentionally separate from the fair G1 task.  It uses the same 28
actions so the gait objective, rather than action-space size, is the controlled
difference.  AMP is excluded until a walking reference is retargeted to this
Humanoid's morphology.
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

from . import gait_rewards
from .g1_whole_body_env_cfg import HumanoidG1WholeBodyFlatEnvCfg, HumanoidG1WholeBodyFlatEnvCfg_PLAY


FEET_SENSOR = SceneEntityCfg(
    "contact_forces",
    body_names=["left_ankle_roll_link", "right_ankle_roll_link"],
    preserve_order=True,
)
FEET_ASSET = SceneEntityCfg(
    "robot",
    body_names=["left_ankle_roll_link", "right_ankle_roll_link"],
    preserve_order=True,
)

TIENKUNG_MAPPED_DEFAULT_POSE = {
    # TienKung2 Lite walking reference, mapped to Humanoid joint names.
    ".*_hip_pitch_joint": -0.5,
    ".*_knee_joint": 1.0,
    ".*_ankle_pitch_joint": -0.5,
    ".*_shoulder_pitch_joint": 0.0,
    ".*_shoulder_yaw_joint": 0.0,
    ".*_elbow_joint": -0.3,
    # Reference is 5.7 degrees; use the requested Humanoid hip-clearance floor.
    ".*_shoulder_roll_joint": 0.2617993877991494,
}


def _install_periodic_rewards(cfg) -> None:
    # Remove the generic air-time incentive that allowed symmetric hopping.
    cfg.rewards.feet_air_time = None
    cfg.rewards.lin_vel_z_l2.weight = -1.0
    cfg.rewards.action_rate_l2.weight = -0.01
    cfg.rewards.feet_slide.weight = -0.25
    cfg.rewards.gait_swing_force = RewTerm(
        func=gait_rewards.gait_swing_force,
        weight=1.0,
        params={"sensor_cfg": FEET_SENSOR},
    )
    cfg.rewards.gait_stance_speed = RewTerm(
        func=gait_rewards.gait_stance_speed,
        weight=1.0,
        params={"asset_cfg": FEET_ASSET},
    )
    cfg.rewards.gait_stance_support_force = RewTerm(
        func=gait_rewards.gait_stance_support_force,
        weight=0.6,
        params={"sensor_cfg": FEET_SENSOR},
    )


@configclass
class HumanoidTienKungPeriodicFlatEnvCfg(HumanoidG1WholeBodyFlatEnvCfg):
    """Twenty-eight-action periodic walking experiment."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.robot.init_state.joint_pos.update(TIENKUNG_MAPPED_DEFAULT_POSE)
        # TienKung's deep crouch shortens the Humanoid root-to-foot distance.
        # 1.091 was TienKung's own root height (robots fell instantly, ep len ~19).
        # Our standing root is 0.78; knee 1.0 rad crouch shortens the leg ~7-9 cm.
        self.scene.robot.init_state.pos = (0.0, 0.0, 0.71)
        _install_periodic_rewards(self)


@configclass
class HumanoidTienKungPeriodicFlatEnvCfg_PLAY(HumanoidG1WholeBodyFlatEnvCfg_PLAY):
    """Deterministic play scene for the periodic walking experiment."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.robot.init_state.joint_pos.update(TIENKUNG_MAPPED_DEFAULT_POSE)
        # 1.091 was TienKung's own root height (robots fell instantly, ep len ~19).
        # Our standing root is 0.78; knee 1.0 rad crouch shortens the leg ~7-9 cm.
        self.scene.robot.init_state.pos = (0.0, 0.0, 0.71)
        _install_periodic_rewards(self)
