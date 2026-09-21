"""Compute cumulative foot-link rotation at zero joint angles from rl_full.urdf.

If CAD zero pose = flat feet, cumulative rotation root->foot should be identity.
Reports the per-side error as intrinsic XYZ euler (roll, pitch, yaw) in degrees.
"""

import math
import xml.etree.ElementTree as ET

import numpy as np

URDF = r"C:\Users\WKS\Documents\humanoid\rl_full_isaac\rl_full\urdf\rl_full.urdf"


def rpy_to_mat(r, p, y):
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
    Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx  # URDF fixed-axis rpy


def mat_to_rpy(R):
    p = math.asin(max(-1, min(1, -R[2, 0] * -1)))  # pitch = asin(-R[2,0])... use standard
    pitch = math.asin(max(-1.0, min(1.0, -R[2, 0])))
    roll = math.atan2(R[2, 1], R[2, 2])
    yaw = math.atan2(R[1, 0], R[0, 0])
    return roll, pitch, yaw


tree = ET.parse(URDF)
root = tree.getroot()
joints = {}
child_of = {}
for j in root.findall("joint"):
    name = j.get("name")
    parent = j.find("parent").get("link")
    child = j.find("child").get("link")
    o = j.find("origin")
    rpy = [float(x) for x in (o.get("rpy", "0 0 0").split() if o is not None else "0 0 0".split())]
    joints[child] = (name, parent, rpy, j.get("type"))

# find root link (never a child)
children = set(joints.keys())
parents = {v[1] for v in joints.values()}
root_link = (parents - children).pop()

for target_kw in ("part_22_foot",):
    for link in children:
        if link.endswith(target_kw):
            chain = []
            cur = link
            while cur != root_link:
                jname, parent, rpy, jtype = joints[cur]
                chain.append((jname, rpy, jtype))
                cur = parent
            chain.reverse()
            R = np.eye(3)
            for jname, rpy, jtype in chain:
                R = R @ rpy_to_mat(*rpy)
            roll, pitch, yaw = mat_to_rpy(R)
            print(f"{link}: roll={math.degrees(roll):+.3f} deg  pitch={math.degrees(pitch):+.3f} deg  yaw={math.degrees(yaw):+.3f} deg")
            # also show the last few joints' own rpy for context
            for jname, rpy, jtype in chain[-4:]:
                print(f"    {jname} ({jtype}): rpy=[{rpy[0]:+.5f} {rpy[1]:+.5f} {rpy[2]:+.5f}]")
print(f"(root link: {root_link})")
