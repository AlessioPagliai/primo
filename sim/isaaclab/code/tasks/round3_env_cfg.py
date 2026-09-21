# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Round 3: a WALK/RUN policy split, mirroring Unitree's own remote modes.

User decision after two video rounds:
  * WALK - conservative, precise positioning: small steps, low speed, must handle backward and
    lateral commands (precision needs all directions). FLAT terrain - matches the use case and
    flat naturally discourages big steps.
  * RUN - faster gait that keeps the stairs capability: rough terrain, but with the big-step
    drivers toned down (round-2 SoftPend/SoftImpact were "not bad but steps too big").

ROOT CAUSE of the big steps, discovered this round: our round-1 "official" recipes were not
official - a corrections layer added a 10 cm foot-clearance reward and a 0.7 s air-time target,
both of which explicitly pay for lifting high and stepping long. Official H1 uses air-time 0.4
with weight 0.25 and NO clearance reward - that is why real H1 policies step small. WALK
variants therefore go back to the official-style shaping (no clearance term, air-time 0.4/0.25),
plus a soft-landing nudge. RUN variants keep a small clearance target (5 cm) for stair traversal.

All six: legs + waist_roll action space, symmetry augmentation, arms held along the body (the
held-pose bug is fixed by events.hold_default_joint_targets - without it, non-action joints
drove to the CAD zero pose in every previous run).
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from . import gait_quality_rewards
from .legs_only_env_cfg import FEET_ASSET, FEET_SENSOR, LEGS_AND_WAIST_ROLL
from .rough_env_cfg import RobstrideRoughEnvCfg, RobstrideRoughEnvCfg_PLAY


def _common(cfg) -> None:
    """Shared by all six: action space, gentle landing nudge, no big-step drivers."""
    cfg.actions.joint_pos.joint_names = LEGS_AND_WAIST_ROLL
    # official-style stepping: air-time 0.4 s at weight 0.25 (H1/G1 values)
    cfg.rewards.feet_air_time.weight = 0.25
    cfg.rewards.feet_air_time.params["threshold"] = 0.4
    # soft-landing nudge (validated in round 2 at this strength)
    cfg.rewards.foot_landing = RewTerm(
        func=gait_quality_rewards.foot_landing_velocity,
        weight=-0.4,
        params={"asset_cfg": FEET_ASSET, "near_height": 0.06},
    )
    cfg.rewards.foot_impact = RewTerm(
        func=gait_quality_rewards.foot_contact_impact,
        weight=-1.0e-4,
        params={"sensor_cfg": FEET_SENSOR, "threshold": 500.0},
    )
    # anti-hop + posture, at nudge strength
    cfg.rewards.no_jumps = RewTerm(
        func=mdp.desired_contacts, weight=-1.0, params={"sensor_cfg": FEET_SENSOR}
    )
    cfg.rewards.upright_torso = RewTerm(func=gait_quality_rewards.upright_torso, weight=-1.0)
    cfg.rewards.lin_vel_z_l2.weight = -1.0
    cfg.rewards.action_rate_l2.weight = -0.008
    # feet forward
    cfg.rewards.hip_yaw_forward = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.25,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*_hip_yaw_joint")},
    )


def _flat(cfg) -> None:
    cfg.scene.terrain.terrain_type = "plane"
    cfg.scene.terrain.terrain_generator = None
    cfg.scene.height_scanner = None
    cfg.observations.policy.height_scan = None
    cfg.curriculum.terrain_levels = None


def _walk_commands(cfg) -> None:
    """Precision envelope: slow, all directions, frequent standing."""
    cfg.commands.base_velocity.ranges.lin_vel_x = (-0.4, 0.6)
    cfg.commands.base_velocity.ranges.lin_vel_y = (-0.3, 0.3)
    cfg.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)
    cfg.commands.base_velocity.rel_standing_envs = 0.15
    cfg.commands.base_velocity.resampling_time_range = (4.0, 9.0)
    # stand precisely when commanded to stand (Digit's term)
    cfg.rewards.stand_still = RewTerm(
        func=mdp.stand_still_joint_deviation_l1,
        weight=-0.3,
        params={
            "command_name": "base_velocity",
            "asset_cfg": SceneEntityCfg("robot", joint_names=LEGS_AND_WAIST_ROLL),
        },
    )


# ---------------------------------------------------------------- WALK variants (flat)
def _walk_g1(cfg) -> None:
    _common(cfg); _flat(cfg); _walk_commands(cfg)
    # G1 flat reward deltas (official)
    cfg.rewards.track_ang_vel_z_exp.weight = 1.0
    cfg.rewards.dof_torques_l2.weight = -2.0e-6
    cfg.rewards.dof_torques_l2.params["asset_cfg"] = SceneEntityCfg(
        "robot", joint_names=[".*_hip_.*", ".*_knee_joint"]
    )


def _walk_h1(cfg) -> None:
    _common(cfg); _flat(cfg); _walk_commands(cfg)
    # H1 deltas: stronger slide/deviation discipline
    cfg.rewards.feet_slide.weight = -0.25
    cfg.rewards.joint_deviation_hip.weight = -0.2
    cfg.rewards.track_ang_vel_z_exp.weight = 1.0
    cfg.rewards.dof_torques_l2.weight = 0.0


def _walk_tiny(cfg) -> None:
    _walk_h1(cfg)
    # smallest envelope: slower still, shortest steps, extra smoothness
    cfg.commands.base_velocity.ranges.lin_vel_x = (-0.3, 0.4)
    cfg.rewards.feet_air_time.params["threshold"] = 0.3
    cfg.rewards.action_rate_l2.weight = -0.01


# ---------------------------------------------------------------- RUN variants (rough)
def _run_pend(cfg) -> None:
    _common(cfg)
    # small clearance for stairs + whole-swing pendulum shaping (round-2 favourite)
    cfg.rewards.feet_clearance = RewTerm(
        func=gait_quality_rewards.feet_swing_clearance,
        weight=-2.0,
        params={"sensor_cfg": FEET_SENSOR, "asset_cfg": FEET_ASSET, "target_height": 0.05},
    )
    cfg.rewards.foot_landing.params["near_height"] = 0.15
    cfg.rewards.foot_landing.weight = -0.3


def _run_impact(cfg) -> None:
    _common(cfg)
    cfg.rewards.feet_clearance = RewTerm(
        func=gait_quality_rewards.feet_swing_clearance,
        weight=-2.0,
        params={"sensor_cfg": FEET_SENSOR, "asset_cfg": FEET_ASSET, "target_height": 0.05},
    )
    cfg.rewards.foot_impact.weight = -2.0e-4  # doubled strike penalty


def _run_g1(cfg) -> None:
    """Closest to the 'G1-700 feel': plain G1 rewards + symmetry, official stepping, rough."""
    _common(cfg)
    cfg.rewards.track_ang_vel_z_exp.weight = 2.0


_WALKS = {"WalkG1": _walk_g1, "WalkH1": _walk_h1, "WalkTiny": _walk_tiny}
_RUNS = {"RunPend": _run_pend, "RunImpact": _run_impact, "RunG1": _run_g1}


def _make(name, fn, base, play):
    @configclass
    class _Cfg(base):
        def __post_init__(self):
            super().__post_init__()
            fn(self)

    _Cfg.__name__ = f"Humanoid{name}{'Play' if play else ''}EnvCfg"
    return _Cfg


for _n, _f in {**_WALKS, **_RUNS}.items():
    globals()[f"Humanoid{_n}EnvCfg"] = _make(_n, _f, RobstrideRoughEnvCfg, False)
    globals()[f"Humanoid{_n}PlayEnvCfg"] = _make(_n, _f, RobstrideRoughEnvCfg_PLAY, True)
