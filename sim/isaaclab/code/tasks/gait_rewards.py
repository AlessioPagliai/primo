# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Periodic walking rewards adapted from Open-X-Humanoid/TienKung-Lab.

The implementation is manager-environment compatible: phase is derived from
Isaac Lab's episode clock, so no custom environment state is required.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensor

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def _gait_phase(env: ManagerBasedRLEnv, cycle_s: float, phase_offsets: tuple[float, float]) -> torch.Tensor:
    time_in_cycles = env.episode_length_buf * env.step_dt / cycle_s
    offsets = torch.tensor(phase_offsets, device=env.device, dtype=torch.float32)
    return torch.remainder(time_in_cycles.unsqueeze(1) + offsets.unsqueeze(0), 1.0)


def gait_clock(phase: torch.Tensor, air_ratio: float, transition: float) -> tuple[torch.Tensor, torch.Tensor]:
    """Return smooth swing and stance masks used by TienKung-Lab."""
    swing = (phase >= transition) & (phase <= air_ratio - transition)
    stance = (phase >= air_ratio + transition) & (phase <= 1.0 - transition)
    enter_swing = phase < transition
    leave_swing = (phase > air_ratio - transition) & (phase < air_ratio + transition)
    wrap = phase > 1.0 - transition
    swing_mask = (
        swing.float()
        + (0.5 + phase / (2.0 * transition)) * enter_swing.float()
        - (phase - air_ratio - transition) / (2.0 * transition) * leave_swing.float()
        + 0.0 * stance.float()
        + (phase - 1.0 + transition) / (2.0 * transition) * wrap.float()
    )
    return swing_mask, 1.0 - swing_mask


def gait_swing_force(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,
    cycle_s: float = 0.85,
    phase_offsets: tuple[float, float] = (0.38, 0.88),
    air_ratio: float = 0.38,
    transition: float = 0.02,
    force_gain: float = 200.0,
) -> torch.Tensor:
    """Reward near-zero foot force during each scheduled swing phase."""
    sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    force = torch.linalg.vector_norm(sensor.data.net_forces_w[:, sensor_cfg.body_ids, :], dim=-1)
    swing, _ = gait_clock(_gait_phase(env, cycle_s, phase_offsets), air_ratio, transition)
    return torch.sum(swing * torch.exp(-force_gain * torch.square(force)), dim=1)


def gait_stance_speed(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg,
    cycle_s: float = 0.85,
    phase_offsets: tuple[float, float] = (0.38, 0.88),
    air_ratio: float = 0.38,
    transition: float = 0.02,
    speed_gain: float = 100.0,
) -> torch.Tensor:
    """Reward low foot speed during each scheduled stance phase."""
    asset = env.scene[asset_cfg.name]
    speed = torch.linalg.vector_norm(asset.data.body_lin_vel_w[:, asset_cfg.body_ids, :], dim=-1)
    _, stance = gait_clock(_gait_phase(env, cycle_s, phase_offsets), air_ratio, transition)
    return torch.sum(stance * torch.exp(-speed_gain * torch.square(speed)), dim=1)


def gait_stance_support_force(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,
    cycle_s: float = 0.85,
    phase_offsets: tuple[float, float] = (0.38, 0.88),
    air_ratio: float = 0.38,
    transition: float = 0.02,
    force_gain: float = 10.0,
) -> torch.Tensor:
    """Reward non-zero support force during each scheduled stance phase."""
    sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    force = torch.linalg.vector_norm(sensor.data.net_forces_w[:, sensor_cfg.body_ids, :], dim=-1)
    _, stance = gait_clock(_gait_phase(env, cycle_s, phase_offsets), air_ratio, transition)
    return torch.sum(stance * (1.0 - torch.exp(-force_gain * torch.square(force))), dim=1)

