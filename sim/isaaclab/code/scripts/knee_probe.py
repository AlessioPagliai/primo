"""Measure knee flexion by patching the stock play.py loop - avoids rebuilding the RSL-RL runner.

Runs the real play.py machinery (which loads checkpoints correctly) and samples joint state each
step via a wrapper around env.step. Prints [KNEE] statistics at the end.

Usage: -p knee_probe.py --task <PlayTaskId> --checkpoint <path> --headless
"""

import argparse
import runpy
import sys

import torch

# --- parse our own args, then hand a clean argv to play.py -------------------------------
ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--task", required=True)
ap.add_argument("--checkpoint", required=True)
ap.add_argument("--headless", action="store_true")
ap.add_argument("--num_envs", type=int, default=32)
known, _ = ap.parse_known_args()

PLAY = r"C:\Users\WKS\isaac\IsaacLab\scripts\reinforcement_learning\rsl_rl\play.py"
# play.py imports its sibling `cli_args` module by bare name
sys.path.insert(0, r"C:\Users\WKS\isaac\IsaacLab\scripts\reinforcement_learning\rsl_rl")
sys.argv = [
    PLAY,
    "--task", known.task,
    "--checkpoint", known.checkpoint,
    "--num_envs", str(known.num_envs),
]
if known.headless:
    sys.argv.append("--headless")

# --- patch ManagerBasedRLEnv.step to record knee state ------------------------------------
# NOTE: isaaclab.envs pulls in pxr, which only exists once the Kit app is up. play.py launches
# the app itself, so we install the patch lazily via a meta-path hook that fires the moment
# isaaclab.envs.manager_based_rl_env is first imported (inside play.py, after AppLauncher).
import importlib.abc  # noqa: E402
import importlib.machinery  # noqa: E402

_KNEE = {"pos": [], "height": [], "ids": None, "feet": None, "n": 0}


def _probe_step(self, action):
    out = _PATCH["orig"](self, action)
    robot = self.scene["robot"]
    if _KNEE["ids"] is None:
        _KNEE["ids"] = [i for i, n in enumerate(robot.joint_names) if n.endswith("_knee_joint")]
        _KNEE["feet"] = [i for i, n in enumerate(robot.body_names) if "ankle_roll" in n]
    _KNEE["n"] += 1
    if _KNEE["n"] > 100:  # skip startup transient
        _KNEE["pos"].append(robot.data.joint_pos[:, _KNEE["ids"]].detach().clone())
        rz = robot.data.root_pos_w[:, 2]
        fz = robot.data.body_pos_w[:, _KNEE["feet"], 2].mean(dim=1)
        _KNEE["height"].append((rz - fz).detach().clone())
    if _KNEE["n"] >= 600:
        _report()
        raise SystemExit(0)
    return out


def _report():
    if not _KNEE["pos"]:
        print("[KNEE] no samples")
        return
    k = torch.cat(_KNEE["pos"]).flatten().float()
    h = torch.cat(_KNEE["height"]).flatten().float()
    straight = (k.abs() < 0.10).float().mean().item() * 100
    print("=" * 70)
    print(f"[KNEE] knee deg: mean={k.mean()*57.3:6.1f}  range={k.min()*57.3:6.1f}..{k.max()*57.3:6.1f}"
          f"  std={k.std()*57.3:5.1f}")
    print(f"[KNEE] time nearly STRAIGHT (<5.7 deg): {straight:5.1f}%")
    print(f"[KNEE] pelvis above feet: {h.mean():.3f} m")
    print("=" * 70)


_PATCH = {"orig": None, "done": False}


class _Hook(importlib.abc.MetaPathFinder):
    """Install the step patch as soon as the env module is imported by play.py."""

    def find_spec(self, name, path, target=None):
        if name == "isaaclab.envs.manager_based_rl_env" and not _PATCH["done"]:
            _PATCH["done"] = True

            def _late():
                import isaaclab.envs.manager_based_rl_env as m

                _PATCH["orig"] = m.ManagerBasedRLEnv.step
                m.ManagerBasedRLEnv.step = _probe_step

            _PATCH["late"] = _late
        return None


sys.meta_path.insert(0, _Hook())


def _install_after_import():
    """After play.py finishes its imports the module exists; patch it then."""
    import isaaclab.envs.manager_based_rl_env as m

    if _PATCH["orig"] is None:
        _PATCH["orig"] = m.ManagerBasedRLEnv.step
        m.ManagerBasedRLEnv.step = _probe_step


# play.py builds the env inside main(); patch right after its imports by wrapping gym.make
import gymnasium as gym  # noqa: E402

_orig_make = gym.make


def _make_and_patch(*a, **kw):
    _install_after_import()
    return _orig_make(*a, **kw)


gym.make = _make_and_patch

runpy.run_path(PLAY, run_name="__main__")
