# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Round 5: make the knees bend.

Observation: every round-4 policy walks with locked, straight knees. User's hypothesis - the
arms-down fix caused it, since that is the only change vs round 2 (which bent its knees).

Mechanism that makes this plausible: with arms held FORWARD (the held-pose bug, rounds 1-2),
~4 kg of arm mass sat ahead of the hips and knee flexion was how the policy balanced that
forward CoM. With arms down, that compensation is unnecessary - and straight-leg walking is the
energy-optimal gait our reward set ALLOWS, because a locked knee carries load through structure
at near-zero torque while a flexed knee pays `dof_torques_l2` every step. Nothing in the rewards
ever asked for knee flexion; round 2's bend was likely an accident of the bug.

Two things are therefore worth testing at once: whether the arms really are the cause, and
several direct ways to require flexion.

  1. ArmsFwd      - HYPOTHESIS TEST: round-4 recipe, arms back to the old forward pose. If this
                    alone restores bent knees, the user's hypothesis is confirmed.
  2. KneeSoft     - + knee_straightness penalty, gentle (-0.5, min bend 0.15 rad)
  3. KneeHard     - + knee_straightness penalty, strong (-2.0, min bend 0.25 rad)
  4. Crouch       - + walking_tall penalty: pelvis may not ride higher than 0.70 m above the feet
  5. KneeDefault  - + default knee pose 0.42 rad (G1 neutral) with a deviation penalty pulling
                    toward it, i.e. bend as the resting posture rather than a hard rule
  6. KneeTorque   - + knee_straightness AND the torque penalty removed on knees, so flexion is
                    no longer taxed at all (tests the energy-optimality explanation directly)
"""

from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp

from . import gait_quality_rewards
from .legs_only_env_cfg import FEET_ASSET, HumanoidG1CorrectedEnvCfg, HumanoidG1CorrectedEnvCfg_PLAY
from .soft_ways_env_cfg import _soft_pend

KNEES = SceneEntityCfg("robot", joint_names=".*_knee_joint")
ARMS_FORWARD_OLD = {  # the pre-fix pose that rounds 1-2 actually trained with
    ".*_shoulder_pitch_joint": 0.0,
    ".*_shoulder_roll_joint": 0.0,
    ".*_elbow_joint": 0.0,
}


def _base(cfg) -> None:
    _soft_pend(cfg)  # the round-4 recipe, unchanged


def _arms_fwd(cfg) -> None:
    """Hypothesis test: identical to round 4 except the arms go back to the CAD-forward pose."""
    _base(cfg)
    cfg.scene.robot.init_state.joint_pos.update(ARMS_FORWARD_OLD)


def _knee_soft(cfg) -> None:
    _base(cfg)
    cfg.rewards.knee_bend = RewTerm(
        func=gait_quality_rewards.knee_straightness,
        weight=-0.5,
        params={"asset_cfg": KNEES, "min_bend": 0.15},
    )


def _knee_hard(cfg) -> None:
    _base(cfg)
    cfg.rewards.knee_bend = RewTerm(
        func=gait_quality_rewards.knee_straightness,
        weight=-2.0,
        params={"asset_cfg": KNEES, "min_bend": 0.25},
    )


def _crouch(cfg) -> None:
    _base(cfg)
    cfg.rewards.walking_tall = RewTerm(
        func=gait_quality_rewards.walking_tall,
        weight=-3.0,
        params={"asset_cfg": SceneEntityCfg("robot"), "feet_cfg": FEET_ASSET, "max_height": 0.70},
    )


def _knee_default(cfg) -> None:
    _base(cfg)
    cfg.scene.robot.init_state.joint_pos.update({".*_knee_joint": 0.42})
    cfg.rewards.knee_posture = RewTerm(
        func=mdp.joint_deviation_l1, weight=-0.3, params={"asset_cfg": KNEES}
    )


def _knee_torque(cfg) -> None:
    """Remove the torque tax on knees, so bending is no longer the expensive option."""
    _base(cfg)
    cfg.rewards.knee_bend = RewTerm(
        func=gait_quality_rewards.knee_straightness,
        weight=-1.0,
        params={"asset_cfg": KNEES, "min_bend": 0.20},
    )
    cfg.rewards.dof_torques_l2.params["asset_cfg"] = SceneEntityCfg(
        "robot", joint_names=[".*_hip_.*", ".*_ankle_.*"]  # knees excluded
    )


_FLAVOURS = {
    "ArmsFwd": _arms_fwd,
    "KneeSoft": _knee_soft,
    "KneeHard": _knee_hard,
    "Crouch": _crouch,
    "KneeDefault": _knee_default,
    "KneeTorque": _knee_torque,
}


def _make(name, fn, base, play):
    @configclass
    class _Cfg(base):
        def __post_init__(self):
            super().__post_init__()
            fn(self)

    _Cfg.__name__ = f"Humanoid{name}{'Play' if play else ''}EnvCfg"
    return _Cfg


for _n, _f in _FLAVOURS.items():
    globals()[f"Humanoid{_n}EnvCfg"] = _make(_n, _f, HumanoidG1CorrectedEnvCfg, False)
    globals()[f"Humanoid{_n}PlayEnvCfg"] = _make(_n, _f, HumanoidG1CorrectedEnvCfg_PLAY, True)
