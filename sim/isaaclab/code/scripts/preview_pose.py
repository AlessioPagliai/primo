"""Headless video of the robot holding a given arm pose - no GUI window needed.

Robot is fixed in space, gravity off, so it just holds the pose for inspection.
Edit POSE below and rerun.
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
parser.add_argument("--elbow", type=str, default="1.5708", help="comma-separated rad values to render")
parser.add_argument("--shoulder_roll", type=float, default=0.2617993877991494)
parser.add_argument("--shoulder_pitch", type=float, default=0.0)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.headless = True
args_cli.enable_cameras = True

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import os

import imageio
import torch

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import Articulation, ArticulationCfg
from isaaclab.sensors import Camera, CameraCfg
from isaaclab.sim import SimulationContext

USD_PATH = "C:/Users/WKS/Documents/humanoid/rl_full_isaac/usd/rl_full.usd"
OUT_DIR = "C:/Users/WKS/Documents/humanoid/rl_full_isaac/training_runs/pose_preview"

ROBOT_CFG = ArticulationCfg(
    prim_path="/World/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path=USD_PATH,
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=True),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, fix_root_link=True,
            solver_position_iteration_count=8, solver_velocity_iteration_count=4,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(pos=(0.0, 0.0, 1.0), joint_pos={".*": 0.0}),
    actuators={
        "all": ImplicitActuatorCfg(joint_names_expr=[".*"], stiffness=400.0, damping=40.0, armature=0.01),
    },
)


def main():
    sim = SimulationContext(sim_utils.SimulationCfg(dt=1 / 120, device=args_cli.device))
    # dark background + directional key light so the white robot actually has contrast
    dome = sim_utils.DomeLightCfg(intensity=120.0, color=(0.15, 0.17, 0.22))
    dome.func("/World/Light", dome)
    key = sim_utils.DistantLightCfg(intensity=1800.0, angle=2.0, color=(1.0, 0.98, 0.95))
    key.func("/World/KeyLight", key, orientation=(0.86, 0.35, 0.15, 0.33))
    ground = sim_utils.GroundPlaneCfg(color=(0.12, 0.13, 0.16))
    ground.func("/World/ground", ground)
    robot = Articulation(ROBOT_CFG)

    # two views: front-left 3/4 and pure side
    cams = {}
    for name, eye in (("view_3q", (2.0, 2.0, 1.4)), ("view_side", (0.0, 3.0, 1.2))):
        cfg = CameraCfg(
            prim_path=f"/World/cam_{name}",
            height=720, width=1280,
            data_types=["rgb"],
            spawn=sim_utils.PinholeCameraCfg(focal_length=24.0, clipping_range=(0.1, 30.0)),
        )
        cams[name] = Camera(cfg)

    sim.reset()
    for name, eye in (("view_3q", (2.0, 2.0, 1.4)), ("view_side", (0.0, 3.0, 1.2))):
        cams[name].set_world_poses_from_view(
            torch.tensor([eye], device=sim.device), torch.tensor([[0.0, 0.0, 1.0]], device=sim.device)
        )

    names = robot.joint_names
    os.makedirs(OUT_DIR, exist_ok=True)
    sim_dt = sim.get_physics_dt()

    # sweep several elbow candidates in one run so they can be compared side by side
    candidates = [float(x) for x in str(args_cli.elbow).split(",")]
    for elbow in candidates:
        targets = robot.data.default_joint_pos.clone()
        applied = {}
        for i, n in enumerate(names):
            if n.endswith("_elbow_joint"):
                targets[0, i] = elbow; applied[n] = elbow
            elif n.endswith("_shoulder_roll_joint"):
                targets[0, i] = args_cli.shoulder_roll; applied[n] = args_cli.shoulder_roll
            elif n.endswith("_shoulder_pitch_joint"):
                targets[0, i] = args_cli.shoulder_pitch; applied[n] = args_cli.shoulder_pitch
        print(f"[POSE] elbow={elbow:+.4f} rad ({elbow*57.2958:+.1f} deg)")

        for _ in range(300):
            robot.set_joint_position_target(targets)
            robot.write_data_to_sim()
            sim.step()
            robot.update(sim_dt)
            for c in cams.values():
                c.update(sim_dt)

        for name, cam in cams.items():
            img = cam.data.output["rgb"][0, ..., :3].cpu().numpy()
            path = os.path.join(OUT_DIR, f"elbow_{elbow*57.2958:+06.1f}deg_{name}.png")
            imageio.imwrite(path, img)
            print("[POSE] wrote", path)

    # report achieved angles
    for i, n in enumerate(names):
        if n in applied:
            print(f"[POSE] {n}: target={applied[n]:+.4f} achieved={robot.data.joint_pos[0, i].item():+.4f}")


if __name__ == "__main__":
    main()
    simulation_app.close()
