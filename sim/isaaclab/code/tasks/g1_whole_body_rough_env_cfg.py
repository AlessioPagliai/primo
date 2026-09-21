# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Rough-terrain fine-tune of the trained flat G1-whole-body policy.

Purpose: the flat policy survives (episode length ~983) but walks with a visibly lame,
asymmetric gait. Varied foot placement on rough terrain is a known way to break that kind
of entrenched habit, and starting from a policy that can already stand avoids the cold-start
failure we hit when training rough from scratch (episode length stuck at 3-8).

The height scanner is deliberately DISABLED so the observation vector stays identical to
the flat task (100 dims). That is what makes ``--resume`` from the flat checkpoint possible
at all; it also means this is blind rough-terrain locomotion, which tends to produce more
robust proprioceptive policies.
"""

from isaaclab.utils import configclass

from .g1_whole_body_env_cfg import _install_articulated_hands_and_safe_whole_body_action
from .rough_env_cfg import RobstrideRoughEnvCfg, RobstrideRoughEnvCfg_PLAY


def _blind_rough(cfg) -> None:
    _install_articulated_hands_and_safe_whole_body_action(cfg)
    # no height scan -> observation dim matches the flat task so the checkpoint loads
    cfg.scene.height_scanner = None
    cfg.observations.policy.height_scan = None
    # CRITICAL: mdp.root_height_below_minimum measures WORLD z and its own docstring says
    # it is "currently only supported for flat terrains". On generated terrain, any robot
    # spawned in a pit or on descending stairs is already under the 0.50 m threshold at
    # t=0, so it terminates on the first frame. That is what pinned every rough run to an
    # episode length of 1-8 while the identical policy scored 983 on flat.
    cfg.terminations.base_height = None


@configclass
class HumanoidG1WholeBodyRoughEnvCfg(RobstrideRoughEnvCfg):
    """G1 rewards + whole-body actions on rough terrain, blind (no height scan)."""

    def __post_init__(self):
        super().__post_init__()
        _blind_rough(self)


@configclass
class HumanoidG1WholeBodyRoughEnvCfg_PLAY(RobstrideRoughEnvCfg_PLAY):
    def __post_init__(self):
        super().__post_init__()
        _blind_rough(self)
