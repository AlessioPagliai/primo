# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Round 4: single-variable refinements of the PROVEN round-2 recipes.

Round-3 post-mortem: SoftPend/SoftImpact (round 2) walked well with bent knees; the user asked
for smaller steps. Round 3 redesigned instead of refining - air-time (swing) weight cut 1.0->0.25,
clearance removed from walks, slow commands + stand-still incentives added - and the result was
walks that stand still (standing became the reward optimum) and runs that drag straight legs
(with the swing incentive starved, not-lifting minimises the remaining penalties).

Round 4 method: take round-2 SoftPend/SoftImpact EXACTLY as they were (same weights, same
commands) and vary ONE step-size knob per run. All on rough/mixed terrain per user. The
held-pose fix (arms along body) is active everywhere and is the only global change vs round 2.

  1. PendBase    - SoftPend exact rerun (control: confirms round-2 behaviour reproduces)
  2. PendShort   - only change: air-time threshold 0.5 -> 0.4 (shorter swings)
  3. PendLow     - only change: clearance target 0.07 -> 0.05 (lower lift)
  4. PendSlow    - only change: forward command cap 1.0 -> 0.7 (slower = naturally shorter)
  5. ImpactShort - SoftImpact + the two step knobs combined (air 0.4 + clearance 0.05)
  6. PendTrack   - only change: velocity-tracking weight 1.0 -> 1.5 (sharper command adherence,
                   guards against any drift toward the standing optimum)
"""

from isaaclab.utils import configclass

from .legs_only_env_cfg import HumanoidG1CorrectedEnvCfg, HumanoidG1CorrectedEnvCfg_PLAY
from .soft_ways_env_cfg import _soft_impact, _soft_pend


def _pend_base(cfg) -> None:
    _soft_pend(cfg)


def _pend_short(cfg) -> None:
    _soft_pend(cfg)
    cfg.rewards.feet_air_time.params["threshold"] = 0.4


def _pend_low(cfg) -> None:
    _soft_pend(cfg)
    cfg.rewards.feet_clearance.params["target_height"] = 0.05


def _pend_slow(cfg) -> None:
    _soft_pend(cfg)
    cfg.commands.base_velocity.ranges.lin_vel_x = (0.0, 0.7)


def _impact_short(cfg) -> None:
    _soft_impact(cfg)
    cfg.rewards.feet_air_time.params["threshold"] = 0.4
    cfg.rewards.feet_clearance.params["target_height"] = 0.05


def _pend_track(cfg) -> None:
    _soft_pend(cfg)
    cfg.rewards.track_lin_vel_xy_exp.weight = 1.5


_FLAVOURS = {
    "PendBase": _pend_base,
    "PendShort": _pend_short,
    "PendLow": _pend_low,
    "PendSlow": _pend_slow,
    "ImpactShort": _impact_short,
    "PendTrack": _pend_track,
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
