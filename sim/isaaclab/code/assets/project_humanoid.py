# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Project Humanoid assets with articulated RH56-compatible hands."""

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.sensors import CameraCfg

from .robstride import ROBSTRIDE_HUMANOID_CFG

# RealSense D436 RGB camera at the CAD mount on neck_pitch_link (URDF transform of
# the d435i_solid placeholder: xyz=(0.0149, -0.0020, 0.0695), rpy=(pi/2, 0, pi/2)).
# Nominal D436 RGB: 1280x800, 90 x 65 deg FOV -> focal 10.48 mm at 20.955 mm aperture.
# NOTE: mechanical housing origin, not the calibrated optical center - verify the
# viewport once in a Play run and refine; on hardware use librealsense intrinsics.
D436_CAMERA_CFG = CameraCfg(
    prim_path="{ENV_REGEX_NS}/Robot/neck_pitch_link/d436_rgb",
    update_period=1.0 / 30.0,
    height=800,
    width=1280,
    data_types=["rgb", "distance_to_image_plane"],
    spawn=sim_utils.PinholeCameraCfg(
        focal_length=10.48, horizontal_aperture=20.955, clipping_range=(0.05, 20.0)
    ),
    offset=CameraCfg.OffsetCfg(
        pos=(0.0149, -0.0020, 0.0695), rot=(0.5, 0.5, 0.5, 0.5), convention="ros"
    ),
)


HUMANOID_ARTICULATED_HANDS_USD_PATH = (
    "C:/Users/WKS/Documents/humanoid/rl_full_isaac/"
    "humanoid_articulated_hands/usd/humanoid_articulated_hands.usd"
)

# Keep the legacy asset as the mechanical-body source, but expose the new
# variant only under the robot's actual temporary name: Humanoid.
HUMANOID_ARTICULATED_HANDS_CFG = ROBSTRIDE_HUMANOID_CFG.copy()
HUMANOID_ARTICULATED_HANDS_CFG.spawn.usd_path = HUMANOID_ARTICULATED_HANDS_USD_PATH
HUMANOID_ARTICULATED_HANDS_CFG.init_state.joint_pos.update(
    {
        ".*_(thumb|index|middle|ring|little)_.*_joint": 0.0,
    }
)
HUMANOID_ARTICULATED_HANDS_CFG.actuators["hands"] = ImplicitActuatorCfg(
    # The importer expands URDF mimic joints, so the six-channel adapter sends
    # coupled targets to all 24 PhysX finger DOFs.
    joint_names_expr=[".*_(thumb|index|middle|ring|little)_.*_joint"],
    effort_limit_sim=1.0,
    velocity_limit_sim=4.6,
    stiffness=10.0,
    damping=0.2,
    armature=0.001,
)

HUMANOID_FIXED_BASE_ARTICULATED_HANDS_CFG = HUMANOID_ARTICULATED_HANDS_CFG.copy()
HUMANOID_FIXED_BASE_ARTICULATED_HANDS_CFG.spawn.articulation_props.fix_root_link = True

