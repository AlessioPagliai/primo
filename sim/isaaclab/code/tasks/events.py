# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Custom event terms for the Humanoid tasks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.managers import SceneEntityCfg

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv


def hold_default_joint_targets(
    env: ManagerBasedEnv, env_ids: torch.Tensor, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")
) -> None:
    """Write default joint-position targets for ALL joints on reset.

    THE BUG THIS FIXES: Isaac Lab action terms write PD targets only for the joints in the
    action space. Joints outside it (arms/wrists/neck in our legs-only tasks) never receive a
    target, so their drives pull toward ZERO - the CAD zero pose (hands forward at chest
    height). That is why every legs-only policy trained/rendered with arms in the export pose
    regardless of what ``init_state.joint_pos`` said: init_state only sets the spawn STATE,
    not the drive TARGET. (Isaac Lab's ``reset_scene_to_default`` has an opt-in
    ``reset_joint_targets`` flag acknowledging exactly this.)

    Registering this as a ``reset`` event writes default targets for every joint; the action
    term then overwrites its own subset each step, and the held joints genuinely hold the
    configured default pose.
    """
    asset = env.scene[asset_cfg.name]
    asset.set_joint_position_target(asset.data.default_joint_pos[env_ids], env_ids=env_ids)
    asset.set_joint_velocity_target(asset.data.default_joint_vel[env_ids], env_ids=env_ids)
