"""Interactive joint-by-joint jog tool, like assembling/checking the robot in CAD.

Spawns the robot FIXED in space (no falling, gravity off) with one on-screen slider
per joint. Drag a slider to move exactly that joint and watch what happens visually -
does the leg bend the way it should, does anything clip through another part, is
left/right symmetric for the same slider value.
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import omni.ui as ui
import torch

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import Articulation, ArticulationCfg
from isaaclab.sim import SimulationContext

USD_PATH = "C:/Users/WKS/Documents/humanoid/rl_full_isaac/usd/rl_full.usd"

ROBOT_CFG = ArticulationCfg(
    prim_path="/World/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path=USD_PATH,
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(disable_gravity=True),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            # off for this diagnostic pass: the ankle cluster's un-simplified collision
            # meshes overlap at rest and self-collision makes them vibrate, which would
            # be mistaken for a joint-motion bug. Re-enable once ankle collisions are
            # simplified from full visual meshes to real primitives.
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
    sim = SimulationContext(sim_utils.SimulationCfg(dt=1 / 200, device=args_cli.device))
    sim.set_camera_view(eye=(2.2, 2.2, 1.4), target=(0.0, 0.0, 0.9))
    sim_utils.GroundPlaneCfg().func("/World/defaultGroundPlane", sim_utils.GroundPlaneCfg())
    sim_utils.DomeLightCfg(intensity=2200.0, color=(0.9, 0.9, 0.9)).func("/World/Light", sim_utils.DomeLightCfg())

    robot = Articulation(ROBOT_CFG)
    sim.reset()

    joint_names = robot.joint_names
    limits = robot.data.joint_pos_limits[0].cpu().numpy()
    targets = torch.zeros(1, len(joint_names), device=robot.device)

    # proposed arms-down pose, so it's visible immediately on open (drag to adjust further)
    import re
    DEFAULTS = {
        r".*_shoulder_pitch_joint": 0.0,
        r".*_shoulder_roll_joint": 0.2617993877991494,
        r".*_elbow_joint": 1.5707963267948966,
    }
    for i, name in enumerate(joint_names):
        for pat, val in DEFAULTS.items():
            if re.fullmatch(pat, name):
                targets[0, i] = val

    window = ui.Window("Joint Jog - drag to move ONE joint at a time", width=520, height=900)
    sliders = {}
    with window.frame:
        with ui.ScrollingFrame():
            with ui.VStack(spacing=4):
                for i, name in enumerate(joint_names):
                    lo, hi = float(limits[i, 0]), float(limits[i, 1])
                    with ui.HStack(height=22):
                        ui.Label(name, width=220)
                        model = ui.SimpleFloatModel(float(targets[0, i].item()))

                        def make_cb(idx):
                            def cb(m):
                                targets[0, idx] = m.get_value_as_float()
                            return cb

                        model.add_value_changed_fn(make_cb(i))
                        ui.FloatSlider(model=model, min=lo, max=hi, step=0.01)
                        sliders[name] = model

    print("[JOG] window ready. Drag a slider; robot is fixed in space, gravity off.")
    print("[JOG] joint order:", joint_names)

    sim_dt = sim.get_physics_dt()
    while simulation_app.is_running():
        robot.set_joint_position_target(targets)
        robot.write_data_to_sim()
        sim.step()
        robot.update(sim_dt)


if __name__ == "__main__":
    main()
    simulation_app.close()
