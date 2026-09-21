# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Whole-body position action with a Humanoid shoulder/hip clearance floor."""

from __future__ import annotations

import torch

from isaaclab.envs.mdp.actions import JointPositionAction, JointPositionActionCfg
from isaaclab.utils import configclass


class ShoulderClearanceJointPositionAction(JointPositionAction):
    """Clamp both mirrored Humanoid shoulder-roll targets outward.

    In this Humanoid URDF, positive position on both shoulder-roll joints is
    physically outward because the left/right joint axes are mirrored.
    """

    cfg: "ShoulderClearanceJointPositionActionCfg"

    def __init__(self, cfg: "ShoulderClearanceJointPositionActionCfg", env):
        super().__init__(cfg, env)
        self._shoulder_roll_action_ids = [
            index for index, name in enumerate(self._joint_names) if name.endswith("_shoulder_roll_joint")
        ]
        if len(self._shoulder_roll_action_ids) != 2:
            raise ValueError(
                "Expected exactly two shoulder-roll actions, got "
                f"{[self._joint_names[index] for index in self._shoulder_roll_action_ids]}"
            )

    def process_actions(self, actions: torch.Tensor):
        super().process_actions(actions)
        self._processed_actions[:, self._shoulder_roll_action_ids] = torch.clamp_min(
            self._processed_actions[:, self._shoulder_roll_action_ids],
            self.cfg.minimum_outward_roll_rad,
        )


@configclass
class ShoulderClearanceJointPositionActionCfg(JointPositionActionCfg):
    """Configuration for the shoulder-clearance action term."""

    class_type: type = ShoulderClearanceJointPositionAction
    minimum_outward_roll_rad: float = 0.2617993877991494

