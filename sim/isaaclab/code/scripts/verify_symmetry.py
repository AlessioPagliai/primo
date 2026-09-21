"""Prove the symmetry augmentation actually mirrors states (it has silent fallbacks).

Builds the real env, takes one observation, runs it through compute_symmetric_states, and
checks that in the mirrored copy the left joint values equal the original right ones and the
base y-quantities are negated. Fails loudly if any part silently passed data through.
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.headless = True

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch

import isaaclab_tasks  # noqa: F401
from isaaclab_tasks.utils import parse_env_cfg
import gymnasium as gym

from isaaclab_tasks.manager_based.locomotion.velocity.mdp.symmetry import humanoid_biped

TASK = "Isaac-Velocity-Rough-Robstride-v0"

cfg = parse_env_cfg(TASK, device=args_cli.device, num_envs=16)
env = gym.make(TASK, cfg=cfg)
obs_dict, _ = env.reset()
raw = env.unwrapped

# step a few times with random actions so the state is not the symmetric default pose
for _ in range(25):
    a = torch.randn(raw.num_envs, raw.action_manager.total_action_dim, device=raw.device) * 0.3
    obs_dict, *_ = env.step(a)

obs = obs_dict["policy"] if isinstance(obs_dict, dict) else obs_dict
actions = torch.randn(raw.num_envs, raw.action_manager.total_action_dim, device=raw.device)

obs_aug, act_aug = humanoid_biped.compute_symmetric_states(raw, obs, actions)
b = obs.shape[0]
mirrored = obs_aug[b:] if obs_aug.shape[0] == 2 * b else None

print("[VERIFY] obs in:", tuple(obs.shape), "-> out:", tuple(obs_aug.shape))
print("[VERIFY] act in:", tuple(actions.shape), "-> out:", tuple(act_aug.shape))
assert mirrored is not None, "augmentation did not double the batch"

perm, sign, off = humanoid_biped._CACHE[id(raw)]
names = raw.scene["robot"].joint_names
print("[VERIFY] obs terms:", {k: v for k, v in off.items()})

ok = True

# 1) joint_pos block: mirrored[left] must equal original[right]
s, e = off["joint_pos"]
jp_o, jp_m = obs[:, s:e], mirrored[:, s:e]
checked = 0
for i, n in enumerate(names):
    if not n.startswith("left_"):
        continue
    j = names.index("right_" + n[len("left_"):])
    d = (jp_m[:, i] - jp_o[:, j]).abs().max().item()
    checked += 1
    if d > 1e-5:
        print(f"[VERIFY] FAIL joint_pos {n}: mirrored != original right partner (max diff {d:.2e})")
        ok = False
print(f"[VERIFY] joint_pos: checked {checked} left/right pairs")

# 2) the mirrored block must actually DIFFER from the original (i.e. not a pass-through)
diff = (jp_m - jp_o).abs().max().item()
print(f"[VERIFY] joint_pos max |mirrored - original| = {diff:.4f}  (must be > 0)")
if diff < 1e-6:
    print("[VERIFY] FAIL: mirrored joint block is identical to the original - augmentation is a NO-OP")
    ok = False

# 3) base_lin_vel y must be negated
s, e = off["base_lin_vel"]
dy = (mirrored[:, s + 1] + obs[:, s + 1]).abs().max().item()
print(f"[VERIFY] base_lin_vel y negated: residual {dy:.2e} (must be ~0)")
if dy > 1e-5:
    ok = False

# 4) height scan must be flipped, not copied
if "height_scan" in off:
    s, e = off["height_scan"]
    hd = (mirrored[:, s:e] - obs[:, s:e]).abs().max().item()
    print(f"[VERIFY] height_scan max |mirrored - original| = {hd:.4f} (must be > 0)")
    if hd < 1e-6:
        print("[VERIFY] FAIL: height_scan not mirrored")
        ok = False

# 5) actions mirrored
am = act_aug[b:]
ad = (am - actions).abs().max().item()
print(f"[VERIFY] actions max |mirrored - original| = {ad:.4f} (must be > 0)")
if ad < 1e-6:
    ok = False

print("[VERIFY] RESULT:", "PASS - symmetry augmentation is genuinely active" if ok else "FAIL")
env.close()
simulation_app.close()
