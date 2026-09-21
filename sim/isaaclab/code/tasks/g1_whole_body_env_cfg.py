# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Faithful G1-style flat task mapped to the Humanoid's corresponding body joints.

This variant intentionally changes only the action mapping relative to
``RobstrideFlatEnvCfg``.  Reward terms and weights remain untouched so the
experiment isolates the effect of restoring the whole-body G1 action space.

G1 has 29 body DOFs.  The Humanoid maps 28 corresponding DOFs because it has
waist roll/yaw but no waist pitch.  The Humanoid's two additional neck joints are
held at their defaults and are not locomotion actions.
"""

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

from .flat_env_cfg import RobstrideFlatEnvCfg, RobstrideFlatEnvCfg_PLAY
from .safe_actions import ShoulderClearanceJointPositionActionCfg

from isaaclab_assets import HUMANOID_ARTICULATED_HANDS_CFG  # isort: skip


G1_MAPPED_BODY_JOINTS = [
    # 12 leg joints
    ".*_hip_yaw_joint",
    ".*_hip_roll_joint",
    ".*_hip_pitch_joint",
    ".*_knee_joint",
    ".*_ankle_pitch_joint",
    ".*_ankle_roll_joint",
    # G1 has waist roll/pitch/yaw; the Humanoid has roll/yaw only.
    "waist_roll_joint",
    "waist_yaw_joint",
    # 14 arm joints
    ".*_shoulder_pitch_joint",
    ".*_shoulder_roll_joint",
    ".*_shoulder_yaw_joint",
    ".*_elbow_joint",
    ".*_wrist_roll_joint",
    ".*_wrist_pitch_joint",
    ".*_wrist_yaw_joint",
]

HUMANOID_BODY_OBSERVATION_JOINTS = G1_MAPPED_BODY_JOINTS + ["neck_yaw_joint", "neck_pitch_joint"]

G1_MAPPED_DEFAULT_POSE = {
    # Official Isaac Lab G1 neutral joint pose mapped by physical function.
    ".*_hip_pitch_joint": -0.20,
    ".*_knee_joint": 0.42,
    ".*_ankle_pitch_joint": -0.23,
    ".*_shoulder_pitch_joint": 0.35,
    ".*_elbow_joint": 0.87,
    # Humanoid-specific clearance adaptation: G1 uses about 9.2 degrees.
    # Both Humanoid joint coordinates are positive in the outward direction.
    ".*_shoulder_roll_joint": 0.2617993877991494,
}


def _install_articulated_hands_and_safe_whole_body_action(cfg) -> None:
    cfg.scene.robot = HUMANOID_ARTICULATED_HANDS_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
    cfg.scene.robot.init_state.joint_pos.update(G1_MAPPED_DEFAULT_POSE)
    # Preserve the current zero-pose foot height after introducing G1's bent legs.
    cfg.scene.robot.init_state.pos = (0.0, 0.0, 0.825)
    cfg.actions.joint_pos = ShoulderClearanceJointPositionActionCfg(
        asset_name="robot",
        joint_names=G1_MAPPED_BODY_JOINTS,
        scale=0.5,
        use_default_offset=True,
        minimum_outward_roll_rad=0.2617993877991494,
    )
    # The imported articulated hands add 24 PhysX DOFs because Isaac 5.1 does
    # not retain URDF mimic tags. Keep locomotion observations body-only.
    cfg.observations.policy.joint_pos.params = {
        "asset_cfg": SceneEntityCfg("robot", joint_names=HUMANOID_BODY_OBSERVATION_JOINTS)
    }
    cfg.observations.policy.joint_vel.params = {
        "asset_cfg": SceneEntityCfg("robot", joint_names=HUMANOID_BODY_OBSERVATION_JOINTS)
    }


@configclass
class HumanoidG1WholeBodyFlatEnvCfg(RobstrideFlatEnvCfg):
    """G1 reward pipeline with all 28 corresponding Humanoid body DOFs."""

    def __post_init__(self):
        super().__post_init__()
        _install_articulated_hands_and_safe_whole_body_action(self)


@configclass
class HumanoidG1WholeBodyFlatEnvCfg_PLAY(RobstrideFlatEnvCfg_PLAY):
    """Small deterministic play scene for the whole-body G1-style policy."""

    def __post_init__(self):
        super().__post_init__()
        _install_articulated_hands_and_safe_whole_body_action(self)
        # Onboard D436 view in Play/teleop scenes only (never the 2048 training envs).
        from isaaclab_assets.robots.project_humanoid import D436_CAMERA_CFG

        self.scene.d436_camera = D436_CAMERA_CFG
