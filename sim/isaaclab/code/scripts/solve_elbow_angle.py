"""Solve the exact elbow_joint angle that swings the forearm from the CAD-zero
'hands forward' pose to 'hand pointing straight down' (arm along the body),
using the real joint axis/geometry from rl_full.urdf - no guessing.
"""
import math
import xml.etree.ElementTree as ET
import numpy as np

URDF = r"C:\Users\WKS\Documents\humanoid\rl_full_isaac\rl_full\urdf\rl_full.urdf"


def pv(s):
    return np.array([float(x) for x in s.split()])


def rpy2R(r, p, y):
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    return np.array([[cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
                      [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
                      [-sp, cp*sr, cp*cr]])


tree = ET.parse(URDF)
robot = tree.getroot()
joints = {j.get("name"): j for j in robot.findall("joint")}
children_of = {}
for j in robot.findall("joint"):
    children_of.setdefault(j.find("parent").get("link"), []).append(j)

# FK at all-zero pose to get world rotation of right_elbow_link
world = {"root": np.eye(3)}
stack = ["root"]
while stack:
    ln = stack.pop()
    for j in children_of.get(ln, []):
        o = j.find("origin")
        rpy = pv(o.get("rpy", "0 0 0")) if o is not None else np.zeros(3)
        Rp = world[ln]
        world[j.find("child").get("link")] = Rp @ rpy2R(*rpy)
        stack.append(j.find("child").get("link"))

for side, elbow_j, wrist_j in (
    ("right", "right_elbow_joint", "right_wrist_roll_joint"),
    ("left", "left_elbow_joint", "left_wrist_roll_joint"),
):
    ej = joints[elbow_j]
    elbow_link = ej.find("child").get("link")
    R_elbow_world = world[elbow_link]  # world orientation of the elbow's child link at zero pose
    axis_local = pv(ej.find("axis").get("xyz"))
    axis_local = axis_local / np.linalg.norm(axis_local)

    wj = joints[wrist_j]
    v_local = pv(wj.find("origin").get("xyz"))  # forearm vector in elbow_link's own local frame

    target_world = np.array([0.0, 0.0, -1.0])  # straight down
    target_local = R_elbow_world.T @ target_world

    # decompose both vectors perpendicular to the rotation axis
    v_perp = v_local - axis_local * np.dot(axis_local, v_local)
    t_perp = target_local - axis_local * np.dot(axis_local, target_local)
    v_perp_n = v_perp / np.linalg.norm(v_perp)
    t_perp_n = t_perp / np.linalg.norm(t_perp)

    theta = math.atan2(np.dot(axis_local, np.cross(v_perp_n, t_perp_n)), np.dot(v_perp_n, t_perp_n))

    lo, hi = (float(x) for x in (ej.find("limit").get("lower"), ej.find("limit").get("upper")))
    print(f"{side}: forearm_local={v_local.round(4)} axis_local={axis_local.round(3)} "
          f"target_local={target_local.round(3)}")
    print(f"{side}: theta = {theta:.6f} rad = {math.degrees(theta):.2f} deg   "
          f"(joint limits [{lo:.3f}, {hi:.3f}] rad)  {'OK' if lo <= theta <= hi else 'OUT OF RANGE!'}")
