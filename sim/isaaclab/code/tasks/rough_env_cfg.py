# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.utils import configclass

from . import events as robstride_events

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp
from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import (
    LocomotionVelocityRoughEnvCfg,
    RewardsCfg,
    TerminationsCfg,
)

##
# Pre-defined configs
##
from isaaclab_assets import ROBSTRIDE_HUMANOID_CFG  # isort: skip


@configclass
class RobstrideRewards(RewardsCfg):
    """Reward terms for the RobStride humanoid velocity task."""

    termination_penalty = RewTerm(func=mdp.is_terminated, weight=-200.0)
    track_lin_vel_xy_exp = RewTerm(
        func=mdp.track_lin_vel_xy_yaw_frame_exp,
        weight=1.0,
        params={"command_name": "base_velocity", "std": 0.5},
    )
    track_ang_vel_z_exp = RewTerm(
        func=mdp.track_ang_vel_z_world_exp, weight=2.0, params={"command_name": "base_velocity", "std": 0.5}
    )
    feet_air_time = RewTerm(
        func=mdp.feet_air_time_positive_biped,
        weight=0.25,
        params={
            "command_name": "base_velocity",
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=".*_ankle_roll_link"),
            "threshold": 0.4,
        },
    )
    feet_slide = RewTerm(
        func=mdp.feet_slide,
        weight=-0.1,
        params={
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=".*_ankle_roll_link"),
            "asset_cfg": SceneEntityCfg("robot", body_names=".*_ankle_roll_link"),
        },
    )

    # Penalize ankle joint limits
    dof_pos_limits = RewTerm(
        func=mdp.joint_pos_limits,
        weight=-1.0,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_ankle_pitch_joint", ".*_ankle_roll_joint"])},
    )
    # Penalize deviation from default of the joints that are not essential for locomotion
    joint_deviation_hip = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.1,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_hip_yaw_joint", ".*_hip_roll_joint"])},
    )
    joint_deviation_arms = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.1,
        params={
            "asset_cfg": SceneEntityCfg(
                "robot",
                joint_names=[
                    ".*_shoulder_pitch_joint",
                    ".*_shoulder_roll_joint",
                    ".*_shoulder_yaw_joint",
                    ".*_elbow_joint",
                    ".*_wrist_roll_joint",
                    ".*_wrist_pitch_joint",
                    ".*_wrist_yaw_joint",
                ],
            )
        },
    )
    joint_deviation_torso = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.1,
        params={
            "asset_cfg": SceneEntityCfg(
                "robot",
                joint_names=["waist_roll_joint", "waist_yaw_joint", "neck_yaw_joint", "neck_pitch_joint"],
            )
        },
    )


@configclass
class RobstrideTerminations(TerminationsCfg):
    """Fall detection for the RobStride humanoid."""

    # Digit uses the same 0.7 rad gate. It stops policies from learning to
    # crawl while still permitting the body lean needed for locomotion.
    base_orientation = DoneTerm(func=mdp.bad_orientation, params={"limit_angle": 0.7})

    # Flat-terrain safeguard for falls that do not produce a reliable torso
    # contact because of merged collision geometry.
    base_height = DoneTerm(func=mdp.root_height_below_minimum, params={"minimum_height": 0.50})


@configclass
class RobstrideRoughEnvCfg(LocomotionVelocityRoughEnvCfg):
    rewards: RobstrideRewards = RobstrideRewards()
    terminations: RobstrideTerminations = RobstrideTerminations()

    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # Scene
        self.scene.robot = ROBSTRIDE_HUMANOID_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # Whole-body actions, exactly like the official G1 task: the base ActionsCfg uses
        # joint_names=[".*"] and G1's own config never overrides it.
        # torso body (battery + Thor merged here) carries the height scanner
        self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/waist_yaw_link"

        # Randomization
        self.events.push_robot = None
        self.events.add_base_mass = None
        self.events.reset_robot_joints.params["position_range"] = (1.0, 1.0)
        self.events.base_external_force_torque.params["asset_cfg"].body_names = ["waist_yaw_link"]
        self.events.reset_base.params = {
            "pose_range": {"x": (-0.5, 0.5), "y": (-0.5, 0.5), "yaw": (-3.14, 3.14)},
            "velocity_range": {
                "x": (0.0, 0.0),
                "y": (0.0, 0.0),
                "z": (0.0, 0.0),
                "roll": (0.0, 0.0),
                "pitch": (0.0, 0.0),
                "yaw": (0.0, 0.0),
            },
        }
        self.events.base_com = None
        # CRITICAL for any task whose action space excludes joints: without this, excluded
        # joints' PD targets are never written and default to ZERO, so "held" arms actually
        # drive to the CAD zero pose (hands forward) instead of the configured default pose.
        # See events.hold_default_joint_targets docstring.
        self.events.hold_default_targets = EventTerm(
            func=robstride_events.hold_default_joint_targets, mode="reset"
        )

        # Rewards
        # exact official G1 rough values
        self.rewards.lin_vel_z_l2.weight = 0.0
        self.rewards.undesired_contacts = None
        self.rewards.flat_orientation_l2.weight = -1.0
        self.rewards.action_rate_l2.weight = -0.005
        self.rewards.dof_acc_l2.weight = -1.25e-7
        self.rewards.dof_acc_l2.params["asset_cfg"] = SceneEntityCfg(
            "robot", joint_names=[".*_hip_.*", ".*_knee_joint"]
        )
        self.rewards.dof_torques_l2.weight = -1.5e-7
        self.rewards.dof_torques_l2.params["asset_cfg"] = SceneEntityCfg(
            "robot", joint_names=[".*_hip_.*", ".*_knee_joint", ".*_ankle_.*"]
        )

        # Commands
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)

        # terminations
        # The pelvis collision is merged into ``root`` and torso collision into
        # ``waist_yaw_link``. Either contacting the ground is a fall.
        self.terminations.base_contact.params["sensor_cfg"].body_names = ["root", "waist_yaw_link"]
        # mdp.root_height_below_minimum compares against WORLD z and its docstring states it
        # is "currently only supported for flat terrains". On generated terrain a robot in a
        # pit or on descending stairs is already below the threshold at t=0 and terminates on
        # the first frame (this pinned every rough run to episode length 1-8 while the same
        # policy scored 983 on flat). The flat config re-enables it, where it is valid.
        self.terminations.base_height = None


@configclass
class RobstrideRoughEnvCfg_PLAY(RobstrideRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Camera follows robot 0. Without this the viewer sits at a fixed world pose while the
        # robots spawn on terrain patches spread across a large grid, so recorded videos can
        # show empty scenery with the robots off-frame.
        self.viewer.origin_type = "asset_root"
        self.viewer.asset_name = "robot"
        self.viewer.env_index = 0
        # eye/lookat are offsets from the robot ROOT (pelvis, ~0.78 m up), not world coords.
        # lookat z negative to aim at the legs/feet. Eye raised and pulled back vs before: the
        # black/blue video frames were the follow-camera clipping through stair/terrain geometry
        # as it tracked the robot. A higher, further eye looking gently down keeps the mesh out
        # of the near plane while still framing the feet.
        self.viewer.eye = (3.2, 3.2, 2.0)
        self.viewer.lookat = (0.0, 0.0, -0.3)

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.episode_length_s = 40.0
        # spawn the robot randomly in the grid (instead of their terrain levels)
        self.scene.terrain.max_init_terrain_level = None
        # reduce the number of terrains to save memory
        if self.scene.terrain.terrain_generator is not None:
            self.scene.terrain.terrain_generator.num_rows = 5
            self.scene.terrain.terrain_generator.num_cols = 5
            self.scene.terrain.terrain_generator.curriculum = False

        self.commands.base_velocity.ranges.lin_vel_x = (1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)
        self.commands.base_velocity.ranges.heading = (0.0, 0.0)
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing
        self.events.base_external_force_torque = None
        self.events.push_robot = None
