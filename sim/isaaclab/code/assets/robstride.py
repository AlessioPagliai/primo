# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the open RobStride humanoid (30-DOF, G1-reference geometry).

Effort/velocity limits mirror the hand-authored values in ``rl_full.urdf``:
RS04 legs 120 Nm, RS06 36 Nm, virtual ankle pitch 72 Nm (2x RS06 differential),
RS00 14 Nm, RS05 neck 5.5 Nm.

* :obj:`ROBSTRIDE_HUMANOID_CFG`: RobStride humanoid from the rl_full Onshape export
"""

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

ROBSTRIDE_USD_PATH = "C:/Users/WKS/Documents/humanoid/rl_full_isaac/usd/rl_full.usd"

ROBSTRIDE_HUMANOID_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=ROBSTRIDE_USD_PATH,
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=8, solver_velocity_iteration_count=4
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        # sole plate bottoms out at -0.7883 in root frame; +8 mm clearance so the feet
        # do not start intersecting the ground (that penetration collapsed the run at
        # spawn: mean episode length 2.4 steps).
        pos=(0.0, 0.0, 0.797),
        joint_pos={
            # Slight leg crouch. Legs at 0 are perfectly straight = a singular pose: the
            # knee has no moment arm, buckles under load, and the robot cannot even stand
            # still with PD holding the pose (stand_test.py: sinks 0.796 -> 0.749 then
            # topples at t=2 s). These are the official G1 neutral angles, which are also
            # what the two runs that actually trained (ep. length 983 / 1000) used.
            ".*_hip_pitch_joint": -0.20,
            ".*_knee_joint": 0.42,
            ".*_ankle_pitch_joint": -0.23,
            # arms down along the body
            ".*_shoulder_pitch_joint": 0.0,
            ".*_shoulder_roll_joint": 0.2617993877991494,  # 15 deg outward, clears the hip
            ".*_elbow_joint": 1.5707963267948966,  # 90 deg: arm along the body
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[".*_hip_pitch_joint", ".*_hip_roll_joint", ".*_knee_joint"],
            effort_limit_sim=120.0,
            velocity_limit_sim=10.0,
            stiffness={
                ".*_hip_pitch_joint": 150.0,
                ".*_hip_roll_joint": 150.0,
                ".*_knee_joint": 150.0,
            },
            damping=5.0,
            armature=0.01,
        ),
        "hip_yaw": ImplicitActuatorCfg(
            joint_names_expr=[".*_hip_yaw_joint"],
            effort_limit_sim=36.0,
            velocity_limit_sim=15.0,
            stiffness=60.0,
            damping=3.0,
            armature=0.01,
        ),
        "waist": ImplicitActuatorCfg(
            joint_names_expr=["waist_roll_joint", "waist_yaw_joint"],
            effort_limit_sim={"waist_roll_joint": 60.0, "waist_yaw_joint": 36.0},
            velocity_limit_sim={"waist_roll_joint": 12.0, "waist_yaw_joint": 15.0},
            stiffness=100.0,
            damping={"waist_roll_joint": 4.0, "waist_yaw_joint": 3.0},
            armature=0.01,
        ),
        "feet": ImplicitActuatorCfg(
            joint_names_expr=[".*_ankle_pitch_joint", ".*_ankle_roll_joint"],
            effort_limit_sim={".*_ankle_pitch_joint": 72.0, ".*_ankle_roll_joint": 36.0},
            velocity_limit_sim=15.0,
            stiffness={".*_ankle_pitch_joint": 40.0, ".*_ankle_roll_joint": 20.0},
            damping={".*_ankle_pitch_joint": 4.0, ".*_ankle_roll_joint": 2.0},
            armature=0.01,
        ),
        "arms": ImplicitActuatorCfg(
            joint_names_expr=[".*_shoulder_pitch_joint", ".*_shoulder_roll_joint", ".*_elbow_joint"],
            effort_limit_sim=36.0,
            velocity_limit_sim=15.0,
            stiffness=40.0,
            damping=2.0,
            armature=0.01,
        ),
        "wrists": ImplicitActuatorCfg(
            joint_names_expr=[".*_shoulder_yaw_joint", ".*_wrist_roll_joint", ".*_wrist_pitch_joint", ".*_wrist_yaw_joint"],
            effort_limit_sim=14.0,
            velocity_limit_sim=20.0,
            stiffness=15.0,
            damping=1.5,
            armature=0.005,
        ),
        "neck": ImplicitActuatorCfg(
            joint_names_expr=["neck_yaw_joint", "neck_pitch_joint"],
            effort_limit_sim=5.5,
            velocity_limit_sim=20.0,
            stiffness=10.0,
            damping=1.0,
            armature=0.005,
        ),
    },
)
"""Configuration for the open RobStride humanoid robot."""

