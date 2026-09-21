"""Can the robot stand still? Spawns it exactly as training does, holds the default
pose with the training PD gains, zero policy actions, and reports height over time.

If it stays up -> the physics/pose/collision are fine and the problem is RL config.
If it falls -> the problem is the asset, and no reward tuning will fix it.
"""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
args_cli.headless = True

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import isaaclab.sim as sim_utils
from isaaclab.assets import Articulation
from isaaclab.sim import SimulationContext

from isaaclab_assets import ROBSTRIDE_HUMANOID_CFG

cfg = ROBSTRIDE_HUMANOID_CFG.replace(prim_path="/World/Robot")


def main():
    sim = SimulationContext(sim_utils.SimulationCfg(dt=1 / 200, device=args_cli.device))
    g = sim_utils.GroundPlaneCfg()
    g.func("/World/ground", g)
    light = sim_utils.DomeLightCfg(intensity=1500.0)
    light.func("/World/light", light)

    robot = Articulation(cfg)
    sim.reset()

    names = robot.body_names
    feet = [i for i, n in enumerate(names) if "ankle_roll" in n]
    spawn_z = cfg.init_state.pos[2]
    print(f"[STAND] spawn_z={spawn_z}")
    print(f"[STAND] default joint pos (non-zero): "
          f"{{k: round(v,4) for k,v in zip(robot.joint_names, robot.data.default_joint_pos[0].tolist()) if abs(v)>1e-6}}")

    sim_dt = sim.get_physics_dt()
    for step in range(1001):
        robot.set_joint_position_target(robot.data.default_joint_pos)
        robot.write_data_to_sim()
        sim.step()
        robot.update(sim_dt)
        if step % 100 == 0:
            root_z = robot.data.root_pos_w[0, 2].item()
            grav = robot.data.projected_gravity_b[0]
            tilt = float((grav[:2] ** 2).sum() ** 0.5)  # 0 = upright
            feet_z = [round(robot.data.body_pos_w[0, i, 2].item(), 4) for i in feet]
            t = step * sim_dt
            print(f"[STAND] t={t:5.2f}s root_z={root_z:.4f} tilt={tilt:.3f} feet_z={feet_z}")

    final_z = robot.data.root_pos_w[0, 2].item()
    grav = robot.data.projected_gravity_b[0]
    tilt = float((grav[:2] ** 2).sum() ** 0.5)
    verdict = "STANDS" if (final_z > 0.6 and tilt < 0.3) else "FALLS"
    print(f"[STAND] VERDICT: {verdict}  (final root_z={final_z:.4f}, tilt={tilt:.3f})")


if __name__ == "__main__":
    main()
    simulation_app.close()
