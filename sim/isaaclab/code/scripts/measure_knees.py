"""Measure actual knee flexion of a trained policy - objective answer to "do the knees bend?".

Rolls out a checkpoint and reports knee-angle statistics (mean/min/max, and how much of the time
the knee is nearly straight). Straight-leg walking shows a mean near 0 with a small range; a
proper gait shows a clear stance/swing spread.

Usage: -p measure_knees.py --task <PlayTaskId> --checkpoint <full path>
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
parser.add_argument("--task", type=str, required=True)
parser.add_argument("--checkpoint", type=str, required=True)
parser.add_argument("--steps", type=int, default=600)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.headless = True

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import isaaclab_tasks  # noqa: F401
from isaaclab_tasks.utils import parse_env_cfg
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner
from isaaclab_tasks.utils import load_cfg_from_registry

cfg = parse_env_cfg(args_cli.task, device=args_cli.device, num_envs=32)
env = gym.make(args_cli.task, cfg=cfg)
env = RslRlVecEnvWrapper(env)

# registry returns a config OBJECT; play.py reads .class_name off it and passes .to_dict()
agent_cfg = load_cfg_from_registry(args_cli.task, "rsl_rl_cfg_entry_point")
agent_dict = agent_cfg.to_dict() if hasattr(agent_cfg, "to_dict") else dict(agent_cfg)
agent_dict.setdefault("class_name", "OnPolicyRunner")
runner = OnPolicyRunner(env, agent_dict, log_dir=None, device=args_cli.device)
runner.load(args_cli.checkpoint)
policy = runner.get_inference_policy(device=args_cli.device)

robot = env.unwrapped.scene["robot"]
knee_ids = [i for i, n in enumerate(robot.joint_names) if n.endswith("_knee_joint")]
hip_ids = [i for i, n in enumerate(robot.joint_names) if n.endswith("_hip_pitch_joint")]
feet_ids = [i for i, n in enumerate(robot.body_names) if "ankle_roll" in n]

obs, _ = env.get_observations()
knees, heights = [], []
for i in range(args_cli.steps):
    with torch.inference_mode():
        obs, _, _, _ = env.step(policy(obs))
    if i > 100:  # discard startup transient
        knees.append(robot.data.joint_pos[:, knee_ids].clone())
        root_z = robot.data.root_pos_w[:, 2]
        feet_z = robot.data.body_pos_w[:, feet_ids, 2].mean(dim=1)
        heights.append((root_z - feet_z).clone())

k = torch.cat(knees).flatten()
h = torch.cat(heights).flatten()
straight = (k.abs() < 0.10).float().mean().item() * 100
print("=" * 70)
print(f"[KNEE] task={args_cli.task}")
print(f"[KNEE] knee angle rad: mean={k.mean():.3f} min={k.min():.3f} max={k.max():.3f} std={k.std():.3f}")
print(f"[KNEE] knee angle deg: mean={k.mean()*57.3:.1f} range={k.min()*57.3:.1f}..{k.max()*57.3:.1f}")
print(f"[KNEE] fraction of time nearly STRAIGHT (<0.10 rad = 5.7 deg): {straight:.1f}%")
print(f"[KNEE] pelvis height above feet: mean={h.mean():.3f} m  (locked-leg stance is tall)")
print("=" * 70)

env.close()
simulation_app.close()
