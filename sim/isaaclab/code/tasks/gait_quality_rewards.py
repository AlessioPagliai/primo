# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Gait-quality rewards: make the robot pick its feet up and keep its torso upright.

Observed problem at ~500 iterations: the policy survives well but shuffles - the swing foot
barely leaves the ground (it would scrape on a real floor), steps are many and tiny rather
than few and deliberate, and the torso leans back.

Terrain note: swing-foot height is measured against the OTHER foot, never against world z.
Absolute world height is exactly what broke the earlier ``base_height`` termination on
generated terrain, where a robot in a pit is "low" while being perfectly fine.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensor

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def feet_swing_clearance(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,
    asset_cfg: SceneEntityCfg,
    target_height: float = 0.10,
    contact_threshold: float = 1.0,
) -> torch.Tensor:
    """Penalise a swing foot that stays lower than ``target_height`` above the stance foot.

    Returns a positive magnitude (use a NEGATIVE weight). Only shortfall is penalised, so
    lifting higher than the target costs nothing.
    """
    contact_sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    asset = env.scene[asset_cfg.name]

    in_contact = (
        contact_sensor.data.net_forces_w_history[:, :, sensor_cfg.body_ids, :].norm(dim=-1).max(dim=1)[0]
        > contact_threshold
    )  # (N, 2)
    foot_z = asset.data.body_pos_w[:, asset_cfg.body_ids, 2]  # (N, 2)
    # local ground reference = the lower foot; terrain-independent
    ground_ref = foot_z.min(dim=1, keepdim=True).values
    clearance = foot_z - ground_ref  # (N, 2), >= 0

    shortfall = (target_height - clearance).clamp(min=0.0)
    swing = (~in_contact).float()
    return torch.sum(shortfall.pow(2) * swing, dim=1)


def foot_landing_velocity(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg,
    near_height: float = 0.06,
) -> torch.Tensor:
    """Penalise fast DOWNWARD foot motion near the ground = soft, pendulum-like landing.

    The user's note: the foot lifts, hangs, then slams down hard at the end of the swing.
    This penalises the vertical descent speed of a foot only while it is close to the ground
    (within ``near_height`` of the lower foot), so the policy must decelerate into contact
    rather than drop onto it. Upward motion and cruising height are not penalised.

    Returns a positive magnitude; use a NEGATIVE weight.
    """
    asset = env.scene[asset_cfg.name]
    foot_z = asset.data.body_pos_w[:, asset_cfg.body_ids, 2]
    foot_vz = asset.data.body_lin_vel_w[:, asset_cfg.body_ids, 2]
    ground_ref = foot_z.min(dim=1, keepdim=True).values
    near = (foot_z - ground_ref < near_height).float()
    descent = foot_vz.clamp(max=0.0).abs()  # downward speed only
    return torch.sum(near * descent.pow(2), dim=1)


def foot_contact_impact(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,
    threshold: float = 400.0,
) -> torch.Tensor:
    """Penalise vertical contact-force spikes above ``threshold`` (hard ground strikes).

    Complements ``foot_landing_velocity``: that shapes the approach, this punishes the impact
    that survives. Weight-per-robot is body weight ~320 N, so a per-foot threshold of ~400 N
    flags strikes clearly above steady single-foot stance. Use a NEGATIVE weight.
    """
    contact_sensor = env.scene.sensors[sensor_cfg.name]
    forces = contact_sensor.data.net_forces_w_history[:, :, sensor_cfg.body_ids, :].norm(dim=-1).max(dim=1)[0]
    return torch.sum((forces - threshold).clamp(min=0.0), dim=1)


def knee_straightness(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg,
    min_bend: float = 0.15,
) -> torch.Tensor:
    """Penalise a knee flexed LESS than ``min_bend`` rad (stiff-leg / locked-knee gait).

    Only straightness is penalised - swing flexion and deep stance bends cost nothing, unlike a
    deviation penalty which also fights the swing. Use a NEGATIVE weight.
    """
    asset = env.scene[asset_cfg.name]
    knee_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    return torch.sum((min_bend - knee_pos).clamp(min=0.0).pow(2), dim=1)


def walking_tall(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg,
    feet_cfg: SceneEntityCfg,
    max_height: float = 0.70,
) -> torch.Tensor:
    """Penalise the pelvis riding HIGHER above the feet than a crouched stance allows.

    Height is measured root-to-mean-foot, never world z (terrain-safe). Walking tall on locked
    knees exceeds ``max_height``; a properly flexed stance does not. Only excess is penalised,
    so crouching lower (stairs) is free. Use a NEGATIVE weight.
    """
    asset = env.scene[asset_cfg.name]
    root_z = asset.data.root_pos_w[:, 2]
    feet_z = asset.data.body_pos_w[:, feet_cfg.body_ids, 2].mean(dim=1)
    h = root_z - feet_z
    return (h - max_height).clamp(min=0.0).pow(2)


def upright_torso(env: ManagerBasedRLEnv, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """Penalise forward/backward torso lean specifically (pitch), not roll.

    ``flat_orientation_l2`` penalises total tilt; this isolates the sagittal lean the robot
    was showing. Uses the projected-gravity x component in the base frame: 0 when upright.
    Returns a positive magnitude (use a NEGATIVE weight).
    """
    asset = env.scene[asset_cfg.name]
    return asset.data.projected_gravity_b[:, 0].pow(2)
