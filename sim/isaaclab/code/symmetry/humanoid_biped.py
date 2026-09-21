# Copyright (c) 2022-2026, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Left-right symmetry augmentation for the Humanoid biped.

Motivation: the trained policies survive well (episode length ~940) but walk with a visibly
lame, asymmetric gait - one leg is held straight and barely swings. This survived 500
iterations of rough-terrain fine-tuning, so it is entrenched in the weights rather than a
terrain artefact. No official Isaac Lab biped (H1, G1, Cassie, Digit) has any symmetry
mechanism; only ANYmal uses ``RslRlSymmetryCfg``. This module provides the biped equivalent.

For every sampled state the policy also trains on its mirror image, so an asymmetric gait
can no longer be a stable optimum.

Why this is simpler than ANYmal's version: our URDF mirrors the joint axes themselves
("same command produces mirrored motion, left/right limits identical" - see mirror_urdf.py),
so mirroring joint data is a plain left<->right SWAP with **no per-joint sign flips**.
ANYmal needs sign flips because its joints share a world-frame axis convention.

Base-frame quantities still flip under the y -> -y mirror:
    lin_vel  (x,  y, z) -> ( x, -y,  z)
    ang_vel  (x,  y, z) -> (-x,  y, -z)
    gravity  (x,  y, z) -> ( x, -y,  z)
    command (vx, vy, wz)-> (vx, -vy, -wz)

Central joints (waist, neck) have no partner: roll and yaw negate, pitch is unchanged.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

__all__ = ["compute_symmetric_states"]

# cache, keyed by id(env): (joint_perm, joint_sign, obs_slices)
_CACHE: dict = {}


def _build_maps(env: ManagerBasedRLEnv):
    """Resolve joint permutation/sign and observation term offsets once per env."""
    robot = env.scene["robot"]
    names = robot.joint_names
    n = len(names)

    perm = list(range(n))
    sign = torch.ones(n, device=env.device)
    for i, name in enumerate(names):
        if name.startswith("left_"):
            partner = "right_" + name[len("left_") :]
        elif name.startswith("right_"):
            partner = "left_" + name[len("right_") :]
        else:
            # central joint: roll/yaw negate under a left-right mirror, pitch does not
            if "roll" in name or "yaw" in name:
                sign[i] = -1.0
            continue
        if partner not in names:
            raise ValueError(f"symmetry: joint '{name}' has no mirror partner '{partner}'")
        perm[i] = names.index(partner)

    perm_t = torch.tensor(perm, device=env.device, dtype=torch.long)

    # observation term layout (order is the order they are declared in the cfg)
    term_names = env.observation_manager.active_terms["policy"]
    term_dims = [int(d[0]) if hasattr(d, "__len__") else int(d) for d in env.observation_manager.group_obs_term_dim["policy"]]
    offsets, start = {}, 0
    for tname, dim in zip(term_names, term_dims):
        offsets[tname] = (start, start + dim)
        start += dim

    return perm_t, sign, offsets


def _mirror_obs(env: ManagerBasedRLEnv, obs: torch.Tensor) -> torch.Tensor:
    perm, sign, off = _CACHE[id(env)]
    out = obs.clone()
    dev = obs.device
    flip_xz = torch.tensor([1.0, -1.0, 1.0], device=dev)   # y negated
    flip_ang = torch.tensor([-1.0, 1.0, -1.0], device=dev)  # roll/yaw negated
    flip_cmd = torch.tensor([1.0, -1.0, -1.0], device=dev)  # vy and wz negated

    for term, mult in (
        ("base_lin_vel", flip_xz),
        ("base_ang_vel", flip_ang),
        ("projected_gravity", flip_xz),
        ("velocity_commands", flip_cmd),
    ):
        if term in off:
            s, e = off[term]
            out[:, s:e] = obs[:, s:e] * mult

    for term in ("joint_pos", "joint_vel", "actions"):
        if term in off:
            s, e = off[term]
            block = obs[:, s:e]
            if block.shape[1] == perm.shape[0]:
                out[:, s:e] = block[:, perm] * sign
            else:
                # action term may cover a subset of joints; fall back to no-op with a warning
                out[:, s:e] = block

    if "height_scan" in off:
        s, e = off["height_scan"]
        span = e - s
        if span == 187:  # GridPatternCfg(resolution=0.1, size=[1.6, 1.0]) -> 11 x 17, y-major
            out[:, s:e] = obs[:, s:e].view(-1, 11, 17).flip(dims=[1]).reshape(-1, span)
        else:
            out[:, s:e] = obs[:, s:e]

    return out


def _mirror_actions(env: ManagerBasedRLEnv, actions: torch.Tensor) -> torch.Tensor:
    perm, sign, _ = _CACHE[id(env)]
    if actions.shape[1] != perm.shape[0]:
        # action space is a joint subset: build a subset permutation lazily
        robot = env.scene["robot"]
        act_names = env.action_manager.get_term("joint_pos")._joint_names
        idx = {nm: i for i, nm in enumerate(act_names)}
        sub_perm, sub_sign = [], []
        for nm in act_names:
            if nm.startswith("left_"):
                p = "right_" + nm[len("left_") :]
            elif nm.startswith("right_"):
                p = "left_" + nm[len("right_") :]
            else:
                sub_perm.append(idx[nm])
                sub_sign.append(-1.0 if ("roll" in nm or "yaw" in nm) else 1.0)
                continue
            sub_perm.append(idx[p])
            sub_sign.append(1.0)
        perm = torch.tensor(sub_perm, device=actions.device, dtype=torch.long)
        sign = torch.tensor(sub_sign, device=actions.device)
    return actions[:, perm] * sign


@torch.no_grad()
def compute_symmetric_states(env: ManagerBasedRLEnv, obs=None, actions=None):
    """Augment a batch with its left-right mirror (2x the batch)."""
    unwrapped = env.unwrapped if hasattr(env, "unwrapped") else env
    if id(unwrapped) not in _CACHE:
        _CACHE[id(unwrapped)] = _build_maps(unwrapped)

    obs_aug = None
    if obs is not None:
        if isinstance(obs, torch.Tensor):
            b = obs.shape[0]
            obs_aug = torch.zeros(b * 2, obs.shape[1], device=obs.device)
            obs_aug[:b] = obs
            obs_aug[b:] = _mirror_obs(unwrapped, obs)
        else:  # TensorDict
            b = obs.batch_size[0]
            obs_aug = obs.repeat(2)
            obs_aug["policy"][:b] = obs["policy"]
            obs_aug["policy"][b:] = _mirror_obs(unwrapped, obs["policy"])

    actions_aug = None
    if actions is not None:
        b = actions.shape[0]
        actions_aug = torch.zeros(b * 2, actions.shape[1], device=actions.device)
        actions_aug[:b] = actions
        actions_aug[b:] = _mirror_actions(unwrapped, actions)

    return obs_aug, actions_aug
