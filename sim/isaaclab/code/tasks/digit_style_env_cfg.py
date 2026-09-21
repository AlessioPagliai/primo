# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Digit-style rough-terrain task mapped onto this Humanoid.

Digit is the most heavily engineered biped config shipped with Isaac Lab (~18 reward terms
vs ~10 for G1/H1) and the only one with an explicit anti-jumping term, which is exactly the
failure mode we keep hitting. Everything transferable is copied verbatim from
``config/digit/rough_env_cfg.py``; the deviations are listed below.

Kept from our own setup (per user):
  * initial pose - arms along the body (shoulder_pitch 0, shoulder_roll +15 deg, elbow 90 deg)
    and the measured spawn height, i.e. ROBSTRIDE_HUMANOID_CFG unchanged.

Deliberate deviations from Digit, with reasons:
  * ``joint_deviation_knee``: Digit penalises ``.*_tarsus`` deviation. Its tarsus is part of a
    closed leg linkage; our knee is the primary actuated flexion joint, so penalising its
    deviation would directly fight walking. Dropped.
  * ``undesired_contacts`` on ``.*_rod``/``.*_tarsus``: those bodies do not exist here. Dropped.
  * Action set: Digit drives legs + arms explicitly. We add the two waist joints because on this
    morphology the waist sits in the pelvis-to-torso chain that Digit simply does not have.
    Neck stays PD-held, matching Digit's lack of a neck.
  * Body-name mapping: ``.*_leg_toe_roll`` -> ``.*_ankle_roll_link`` (our ground-contact bodies),
    ``torso_base`` -> ``root`` + ``waist_yaw_link`` (merged pelvis/torso collision).
  * Pushes stay ENABLED: Digit is the one official biped that keeps them, and this run is meant
    to be Digit-faithful.
"""

import math

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp
from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg

from isaaclab_assets import ROBSTRIDE_HUMANOID_CFG  # isort: skip


LEG_JOINTS = [
    ".*_hip_yaw_joint",
    ".*_hip_roll_joint",
    ".*_hip_pitch_joint",
    ".*_knee_joint",
    ".*_ankle_pitch_joint",
    ".*_ankle_roll_joint",
]
ARM_JOINTS = [
    ".*_shoulder_pitch_joint",
    ".*_shoulder_roll_joint",
    ".*_shoulder_yaw_joint",
    ".*_elbow_joint",
    ".*_wrist_roll_joint",
    ".*_wrist_pitch_joint",
    ".*_wrist_yaw_joint",
]
WAIST_JOINTS = ["waist_roll_joint", "waist_yaw_joint"]
ACTION_JOINTS = LEG_JOINTS + ARM_JOINTS + WAIST_JOINTS
FEET = ".*_ankle_roll_link"


@configclass
class DigitStyleRewards:
    """Digit's reward set, joint/body names mapped to this Humanoid."""

    termination_penalty = RewTerm(func=mdp.is_terminated, weight=-100.0)
    track_lin_vel_xy_exp = RewTerm(
        func=mdp.track_lin_vel_xy_yaw_frame_exp,
        weight=1.0,
        params={"command_name": "base_velocity", "std": math.sqrt(0.25)},
    )
    track_ang_vel_z_exp = RewTerm(
        func=mdp.track_ang_vel_z_world_exp,
        weight=1.0,
        params={"command_name": "base_velocity", "std": math.sqrt(0.25)},
    )
    feet_air_time = RewTerm(
        func=mdp.feet_air_time_positive_biped,
        weight=0.25,
        params={
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=FEET),
            "threshold": 0.8,
            "command_name": "base_velocity",
        },
    )
    feet_slide = RewTerm(
        func=mdp.feet_slide,
        weight=-0.25,
        params={
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=FEET),
            "asset_cfg": SceneEntityCfg("robot", body_names=FEET),
        },
    )
    dof_torques_l2 = RewTerm(func=mdp.joint_torques_l2, weight=-1.0e-6)
    dof_acc_l2 = RewTerm(
        func=mdp.joint_acc_l2,
        weight=-2.0e-7,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=LEG_JOINTS + ARM_JOINTS)},
    )
    action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-0.008)
    flat_orientation_l2 = RewTerm(func=mdp.flat_orientation_l2, weight=-2.5)
    stand_still = RewTerm(
        func=mdp.stand_still_joint_deviation_l1,
        weight=-0.4,
        params={
            "command_name": "base_velocity",
            "asset_cfg": SceneEntityCfg("robot", joint_names=LEG_JOINTS),
        },
    )
    lin_vel_z_l2 = RewTerm(func=mdp.lin_vel_z_l2, weight=-2.0)
    ang_vel_xy_l2 = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.1)
    # the anti-hopping term: penalises every step where NO foot is in contact
    no_jumps = RewTerm(
        func=mdp.desired_contacts,
        weight=-0.5,
        params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names=[FEET])},
    )
    dof_pos_limits = RewTerm(
        func=mdp.joint_pos_limits,
        weight=-1.0,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_ankle_pitch_joint", ".*_ankle_roll_joint"])},
    )
    joint_deviation_hip_roll = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.1,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*_hip_roll_joint")},
    )
    joint_deviation_hip_yaw = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.2,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*_hip_yaw_joint")},
    )
    joint_deviation_feet = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.1,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_ankle_pitch_joint", ".*_ankle_roll_joint"])},
    )
    joint_deviation_arms = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.2,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=ARM_JOINTS)},
    )
    joint_deviation_torso = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.2,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=WAIST_JOINTS + ["neck_.*_joint"])},
    )


@configclass
class DigitStyleTerminations:
    """Digit's terminations. Note Digit has NO base-height term - correct for terrain."""

    time_out = DoneTerm(func=mdp.time_out, time_out=True)
    base_contact = DoneTerm(
        func=mdp.illegal_contact,
        params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names=["root", "waist_yaw_link"]), "threshold": 1.0},
    )
    base_orientation = DoneTerm(func=mdp.bad_orientation, params={"limit_angle": 0.7})


@configclass
class HumanoidDigitStyleRoughEnvCfg(LocomotionVelocityRoughEnvCfg):
    rewards: DigitStyleRewards = DigitStyleRewards()
    terminations: DigitStyleTerminations = DigitStyleTerminations()

    def __post_init__(self):
        super().__post_init__()
        # Digit's control rate
        self.decimation = 4
        self.sim.dt = 0.005

        # our robot, our arms-along-the-body pose (user requirement)
        self.scene.robot = ROBSTRIDE_HUMANOID_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/waist_yaw_link"
        self.scene.contact_forces.history_length = self.decimation
        self.scene.contact_forces.update_period = self.sim.dt
        self.scene.height_scanner.update_period = self.decimation * self.sim.dt

        # Digit drives legs + arms; we add waist (see module docstring)
        self.actions.joint_pos.joint_names = ACTION_JOINTS
        self.actions.joint_pos.scale = 0.5
        self.actions.joint_pos.use_default_offset = True

        # Digit's events: pushes and base-mass randomisation stay on
        self.events.add_base_mass.params["asset_cfg"] = SceneEntityCfg("robot", body_names="waist_yaw_link")
        self.events.base_external_force_torque.params["asset_cfg"] = SceneEntityCfg(
            "robot", body_names=["root", "waist_yaw_link"]
        )
        self.events.reset_robot_joints.params["position_range"] = (1.0, 1.0)
        self.events.base_com = None

        # Digit's command ranges - note lateral and BACKWARD walking are trained here
        self.commands.base_velocity.ranges.lin_vel_x = (-0.8, 0.8)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.5, 0.5)
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)
        self.commands.base_velocity.rel_standing_envs = 0.1
        self.commands.base_velocity.resampling_time_range = (3.0, 8.0)


@configclass
class HumanoidDigitStyleRoughEnvCfg_PLAY(HumanoidDigitStyleRoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.scene.terrain.max_init_terrain_level = None
        if self.scene.terrain.terrain_generator is not None:
            self.scene.terrain.terrain_generator.num_rows = 5
            self.scene.terrain.terrain_generator.num_cols = 5
            self.scene.terrain.terrain_generator.curriculum = False
        self.observations.policy.enable_corruption = False
        self.events.base_external_force_torque = None
        self.events.push_robot = None
