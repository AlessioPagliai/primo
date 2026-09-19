#!/usr/bin/env python3
"""Mirror the right-side Onshape URDF export into a full robot for Isaac Sim/Lab.

Usage:  python3 mirror_urdf.py [export_dir] [output_dir]
Default export_dir = ~/Downloads/rl, output_dir = ~/Downloads/rl_full

What it does (rerun after every Onshape re-export):
  1. Renames the 17 exported revolutes and their child links to semantic G1-style names.
  2. Converts every `continuous` joint to `revolute` with limits, effort and velocity
     (limits from the G1 mode_11 baseline, sign-corrected against the exported axis;
     effort from the RobStride peak torque of that joint's motor; velocity PROVISIONAL).
  3. Mirrors the right-leg and right-arm subtrees into left twins (y -> -y):
     joints crossing from the central chain use exact world-frame mirroring (no
     symmetry assumption on the parent frame); inside the mirrored subtree local
     transforms are conjugated by D=diag(1,-1,1); axes (ax,ay,az)->(-ax,ay,-az) so the
     SAME command produces the mirrored motion and limits stay identical left/right.
  4. Bakes real mirrored STL meshes (vertex y-flip in link frame + triangle winding
     swap) - no negative scale tricks, Isaac-safe. The mirrored right hand mesh IS the
     left RH56DFX-2L.
  5. Inertials: mass kept, COM y flipped, Ixy/Iyz sign-flipped.
  6. Adds <collision> (copy of visual) for the links in COLLISION_LINKS + left twins.
  7. Writes output_dir/urdf/rl_full.urdf with ../meshes/ relative paths.

Import into Isaac Sim with "merge fixed joints" enabled (massless mate-connector and
root links merge away). PROVISIONAL values marked below must be revisited before
serious RL: neck limits, all velocities, ankle virtual-joint efforts.
"""
import sys, struct, shutil, math
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np

EXPORT = Path(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads/rl").expanduser()
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "~/Downloads/rl_full").expanduser()

# ---------------- configuration ----------------
# joints are AUTO-IDENTIFIED by world position at zero pose (robust to exporter
# renumbering and part renames). Reference positions in metres, from the verified
# 2026-07-18 export; tolerance 40 mm. Update here only if the skeleton moves.
REF_POS = {  # name: (x, y, z)
    "right_hip_pitch":      (0.000, -0.0547, -0.1160),
    "right_hip_roll":       (0.0205, -0.1267, -0.1576),
    "right_hip_yaw":        (0.000, -0.1267, -0.2701),
    "right_knee":           (0.000, -0.1300, -0.4393),
    "right_ankle_pitch":    (0.000, -0.0962, -0.7393),
    "right_ankle_roll":     (0.0300, -0.1262, -0.7533),
    "waist_roll":           (0.0200,  0.0000,  0.0000),
    "waist_yaw":            (0.000,  0.0000,  0.1085),
    "right_shoulder_pitch": (0.000, -0.0750,  0.2918),
    "right_shoulder_roll":  (0.0115, -0.1562,  0.2918),
    "right_shoulder_yaw":   (0.000, -0.1562,  0.2118),
    "right_elbow":          (0.000, -0.1762,  0.1052),
    "right_wrist_roll":     (0.1010, -0.1562,  0.1052),
    "right_wrist_pitch":    (0.1495, -0.1822,  0.1052),
    "right_wrist_yaw":      (0.2085, -0.1562,  0.1312),
    "neck_yaw":             (0.000,  0.0000,  0.3678),
    "neck_pitch":           (0.000,  0.0020,  0.3798),
}
MATCH_TOL = 0.040  # m
# limb joint sets used to auto-derive the mirror subtrees
LIMB_SETS = {
    "leg": {"right_hip_pitch", "right_hip_roll", "right_hip_yaw", "right_knee",
            "right_ankle_pitch", "right_ankle_roll"},
    "arm": {"right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw",
            "right_elbow", "right_wrist_roll", "right_wrist_pitch", "right_wrist_yaw"},
}
# canonical limits, RIGHT side, about the canonical +axis (world, zero pose).
# From Unitree G1 mode_11 (asymmetric rolls mirrored to the right side); neck PROVISIONAL.
CANON = {  # name: (world axis, lower, upper, effort Nm, velocity rad/s)
    "right_hip_pitch":      ((0, 1, 0), -2.53, 2.88, 120.0, 10.0),
    "right_hip_roll":       ((1, 0, 0), -2.97, 0.52, 120.0, 10.0),
    "right_hip_yaw":        ((0, 0, 1), -2.76, 2.76,  36.0, 15.0),  # RS06 as in CAD; PENDING sim gate vs RS03
    "right_knee":           ((0, 1, 0), -0.09, 2.88, 120.0, 10.0),
    # ankle efforts DERIVED 2026-07-19 from the real linkage geometry by ankle_map.py
    # (crank 47.75, rods 208/106 eye-to-eye, pitch arm 47.75, roll half-span 43.83 mm).
    # These are the NEUTRAL-POSE pure-axis maxima. The real envelope is COUPLED and
    # configuration-dependent: |t_pitch|/72 + |t_roll|/66 <= 1 at neutral, and pitch max
    # falls to ~46 Nm at full plantarflexion. Isaac Lab must clip with the diamond rule.
    "right_ankle_pitch":    ((0, 1, 0), -0.87, 0.52,  72.0, 15.0),
    "right_ankle_roll":     ((1, 0, 0), -0.26, 0.26,  66.0, 15.0),
    "waist_roll":           ((1, 0, 0), -0.52, 0.52,  60.0, 12.0),
    "waist_yaw":            ((0, 0, 1), -2.62, 2.62,  36.0, 15.0),
    "right_shoulder_pitch": ((0, 1, 0), -3.09, 2.67,  36.0, 15.0),
    "right_shoulder_roll":  ((1, 0, 0), -2.25, 1.59,  36.0, 15.0),
    "right_shoulder_yaw":   ((0, 0, 1), -2.62, 2.62,  14.0, 20.0),
    "right_elbow":          ((0, 1, 0), -1.05, 2.09,  36.0, 15.0),
    "right_wrist_roll":     ((1, 0, 0), -1.97, 1.97,  14.0, 20.0),
    "right_wrist_pitch":    ((0, 1, 0), -1.61, 1.61,  14.0, 20.0),
    "right_wrist_yaw":      ((0, 0, 1), -1.61, 1.61,  14.0, 20.0),
    "neck_yaw":             ((0, 0, 1), -1.57, 1.57,   5.5, 20.0),  # PROVISIONAL range
    "neck_pitch":           ((0, 1, 0), -0.70, 0.70,   5.5, 20.0),  # PROVISIONAL range
}
# first-pass collision bodies: any link whose name contains one of these tokens
# gets a collision copy of its visual (left twins automatic)
COLLISION_TOKENS = ("pelvis", "ribcage", "femur", "tibia", "foot", "ankle_joint",
                    "hip_pitch_to_roll", "hip_roll_to_yaw",
                    # semantic names assigned to revolute children (thigh/shin/gimbal both sides)
                    "hip_pitch_link", "hip_roll_link", "hip_yaw_link", "knee_link",
                    "ankle_pitch_link", "ankle_roll_link")

# ---- mass injection (Onshape's Properties-panel "Mass override" is NOT exported:
# the exporter only uses geometry x material density. So the BOM/manual masses are
# injected here, the single source of truth. Rules match SUBSTRINGS of link names,
# case-insensitive: rename parts in Onshape to contain these tokens and every
# re-export is handled automatically.)
MASS_RULES = [  # (substring, kg)  - checked in order, first match wins
    ("rs04", 1.420), ("rs03", 0.880), ("rs06", 0.621),
    ("rs00", 0.310), ("rs05", 0.191),
    ("rh56", 0.540), ("d435", 0.075), ("d436", 0.075),
    ("battery", 2.270), ("p45b", 2.270),
    ("thor", 1.940), ("jetson", 1.940),
    ("weho", 0.300), ("eaton", 0.151), ("lev100", 0.190), ("imu", 0.030),
]
# motor stator mass by joint (applied to the joint's PARENT link when its exported
# mass is < 5 g, i.e. an unassigned imported STEP)
STATOR_MASS = {
    "right_hip_pitch": 1.420, "right_hip_roll": 1.420, "right_knee": 1.420,
    "right_hip_yaw": 0.880,
    "right_shoulder_pitch": 0.621, "right_shoulder_roll": 0.621, "right_elbow": 0.621,
    "right_shoulder_yaw": 0.310, "right_wrist_roll": 0.310,
    "right_wrist_pitch": 0.310, "right_wrist_yaw": 0.310,
    "waist_yaw": 0.621, "waist_roll": 0.880,
    "neck_yaw": 0.191, "neck_pitch": 0.191,
}
DUMMY_PREFIXES = ("mate_connector", "root")

# ---------------- helpers ----------------
def rpy2R(r, p, y):
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    return np.array([[cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
                     [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
                     [-sp,   cp*sr,            cp*cr]])

def R2rpy(R):
    p = math.asin(max(-1.0, min(1.0, -R[2, 0])))
    if abs(math.cos(p)) > 1e-9:
        r = math.atan2(R[2, 1], R[2, 2]); y = math.atan2(R[1, 0], R[0, 0])
    else:
        r = math.atan2(-R[1, 2], R[1, 1]); y = 0.0
    return r, p, y

def fv(v):  # format vector
    return " ".join(f"{x:.9g}" for x in v)

def pv(s, n=3, default=0.0):
    return np.array([float(x) for x in s.split()]) if s else np.full(n, default)

M = np.diag([1.0, -1.0, 1.0])   # world mirror (XZ plane)
D = np.diag([1.0, -1.0, 1.0])   # local frame flip

def conj_origin(el):
    """xyz -> (x,-y,z); rpy -> (-r, p, -y) : conjugation by D."""
    if el is None:
        return
    xyz = pv(el.get("xyz", "0 0 0")); rpy = pv(el.get("rpy", "0 0 0"))
    el.set("xyz", fv(D @ xyz)); el.set("rpy", fv([-rpy[0], rpy[1], -rpy[2]]))

# ---------------- load ----------------
tree = ET.parse(EXPORT / "urdf" / "rl.urdf")
robot = tree.getroot()
robot.set("name", "rl_full")
links = {l.get("name"): l for l in robot.findall("link")}
joints = {j.get("name"): j for j in robot.findall("joint")}
children_of = {}
for j in robot.findall("joint"):
    children_of.setdefault(j.find("parent").get("link"), []).append(j)

# ---------------- 2b: inject real masses ----------------
def set_link_mass(l, target):
    ine = l.find("inertial")
    if ine is None:
        return False
    m = ine.find("mass"); it = ine.find("inertia")
    old_m = float(m.get("value"))
    if abs(old_m - target) < 1e-9:
        return False
    if old_m > 1e-6:
        # geometry-derived tensor with uniform density: scale linearly with mass
        k = target / old_m
        for key in ("ixx", "iyy", "izz", "ixy", "ixz", "iyz"):
            it.set(key, f"{float(it.get(key)) * k:.9g}")
    else:
        # degenerate: rebuild as solid box of the visual-mesh AABB
        mesh = l.find("visual/geometry/mesh")
        dims = np.array([0.05, 0.05, 0.05])
        if mesh is not None:
            fn = EXPORT / "meshes" / mesh.get("filename").split("/")[-1]
            try:
                data = fn.read_bytes()
                n = struct.unpack_from("<I", data, 80)[0]
                tri = np.frombuffer(data[84:84 + n * 50], dtype=np.uint8).reshape(n, 50)[:, :48].view("<f4").reshape(n, 4, 3)
                v = tri[:, 1:].reshape(-1, 3)
                dims = np.maximum(v.max(0) - v.min(0), 0.01)
            except Exception:
                pass
        ix = target / 12 * (dims[1] ** 2 + dims[2] ** 2)
        iy = target / 12 * (dims[0] ** 2 + dims[2] ** 2)
        iz = target / 12 * (dims[0] ** 2 + dims[1] ** 2)
        for key, val in (("ixx", ix), ("iyy", iy), ("izz", iz), ("ixy", 0), ("ixz", 0), ("iyz", 0)):
            it.set(key, f"{val:.9g}")
    m.set("value", f"{target:.9g}")
    return True

mass_report = []
for l in robot.findall("link"):
    n = l.get("name").lower()
    if n.startswith(DUMMY_PREFIXES):
        continue
    for pat, kg in MASS_RULES:
        if pat in n:
            if set_link_mass(l, kg):
                mass_report.append(f"  set {l.get('name')} -> {kg} kg  (rule '{pat}')")
            break
for jn, kg in STATOR_MASS.items():
    j = joints.get(jn + "_joint")
    if j is None:
        continue
    pl = links[j.find("parent").get("link")]
    ine = pl.find("inertial")
    if ine is not None and float(ine.find("mass").get("value")) < 0.005:
        if set_link_mass(pl, kg):
            mass_report.append(f"  set {pl.get('name')} -> {kg} kg  (stator of {jn})")


# FK at zero pose
world = {"root": (np.eye(3), np.zeros(3))}
stack = ["root"]
while stack:
    ln = stack.pop()
    for j in children_of.get(ln, []):
        o = j.find("origin")
        xyz = pv(o.get("xyz", "0 0 0")) if o is not None else np.zeros(3)
        rpy = pv(o.get("rpy", "0 0 0")) if o is not None else np.zeros(3)
        Rp, tp = world[ln]
        world[j.find("child").get("link")] = (Rp @ rpy2R(*rpy), tp + Rp @ xyz)
        stack.append(j.find("child").get("link"))

# ---------------- 1+2: rename and set limits on the exported revolutes ----------------
# auto-match exported revolute/continuous joints to REF_POS by world position
auto_map = {}
for j in robot.findall("joint"):
    if j.get("type") not in ("continuous", "revolute"):
        continue
    pos = world[j.find("child").get("link")][1]
    best, bd = None, 1e9
    for name, ref in REF_POS.items():
        d = float(np.linalg.norm(pos - np.array(ref)))
        if d < bd:
            best, bd = name, d
    if bd > MATCH_TOL:
        sys.exit(f"ERROR: joint {j.get('name')} at {pos} matches no reference joint "
                 f"(closest {best} at {bd*1000:.1f} mm). Skeleton moved? Update REF_POS.")
    if best in auto_map:
        sys.exit(f"ERROR: {best} matched twice ({auto_map[best]} and {j.get('name')}).")
    auto_map[best] = j.get("name")
missing = set(REF_POS) - set(auto_map)
if missing:
    sys.exit(f"ERROR: joints not found in export: {sorted(missing)}")
print("joint auto-match OK:", ", ".join(f"{v}->{k}" for k, v in sorted(auto_map.items())))

# ---------------- 1b: repair limbs the exporter left hanging from the world ----------
# (Onshape Group mates sometimes lose an edge in export; geometry/world poses stay
# correct, so we re-root the hanging chain and bolt its anchor back to the pelvis.)
def rebuild_maps():
    global links, joints, children_of, link_parent
    links = {l.get("name"): l for l in robot.findall("link")}
    joints = {j.get("name"): j for j in robot.findall("joint")}
    children_of = {}
    for j in robot.findall("joint"):
        children_of.setdefault(j.find("parent").get("link"), []).append(j)
    link_parent = {j.find("child").get("link"): j for j in robot.findall("joint")}

rebuild_maps()
rev_auto = {v: k for k, v in auto_map.items()}
pelvis_link = joints[auto_map["waist_roll"]].find("parent").get("link")

def named_strictly_below(ln):
    s = set(); st = [ln]
    while st:
        x = st.pop()
        for jj in children_of.get(x, []):
            nm = rev_auto.get(jj.get("name"))
            if nm: s.add(nm)
            st.append(jj.find("child").get("link"))
    return s

for limb, first in (("leg", "right_hip_pitch"), ("arm", "right_shoulder_pitch")):
    j0 = joints[auto_map[first]]
    cur = j0.find("parent").get("link"); under_root = cur
    while cur != "root" and cur in link_parent:
        under_root = cur
        cur = link_parent[cur].find("parent").get("link")
    if cur != "root":
        continue
    top_joint = link_parent[under_root]
    if not top_joint.get("name").startswith("hanging"):
        continue  # properly attached through the pelvis chain
    print(f"WARNING: the {limb} was exported HANGING from the world origin (the exporter "
          f"lost a Group-mate edge; the CAD itself is fine). Re-rooting the chain and "
          f"re-attaching it to {pelvis_link} from the preserved world poses.")
    ca = j0.find("child").get("link"); pa = j0.find("parent").get("link")
    others = LIMB_SETS[limb] - {first}
    anchor = ca if not (named_strictly_below(ca) & others) else pa
    # collect the path anchor -> under_root BEFORE touching anything, then reverse each joint
    path = []
    lnk = anchor
    while lnk != under_root:
        jj = link_parent[lnk]
        path.append(jj)
        lnk = jj.find("parent").get("link")
    for jj in path:
        P = jj.find("parent").get("link"); C = jj.find("child").get("link")
        o = jj.find("origin")
        xyz = pv(o.get("xyz", "0 0 0")); rpy = pv(o.get("rpy", "0 0 0"))
        RT = rpy2R(*rpy)
        o.set("xyz", fv(-(RT.T @ xyz))); o.set("rpy", fv(R2rpy(RT.T)))
        jj.find("parent").set("link", C); jj.find("child").set("link", P)
        a = jj.find("axis")
        if a is not None and jj.get("type") in ("continuous", "revolute"):
            a.set("xyz", fv(-(RT @ pv(a.get("xyz")))))
    robot.remove(top_joint)
    Rp, tp = world[pelvis_link]; Ra, ta = world[anchor]
    nj = ET.SubElement(robot, "joint", {"name": f"{limb}_anchor_to_pelvis", "type": "fixed"})
    ET.SubElement(nj, "origin", {"xyz": fv(Rp.T @ (ta - tp)), "rpy": fv(R2rpy(Rp.T @ Ra))})
    ET.SubElement(nj, "parent", {"link": pelvis_link})
    ET.SubElement(nj, "child", {"link": anchor})
    rebuild_maps()

# recompute FK on the repaired tree
world = {"root": (np.eye(3), np.zeros(3))}
_st = ["root"]
while _st:
    _l = _st.pop()
    for _j in children_of.get(_l, []):
        _o = _j.find("origin")
        _xyz = pv(_o.get("xyz", "0 0 0")) if _o is not None else np.zeros(3)
        _rpy = pv(_o.get("rpy", "0 0 0")) if _o is not None else np.zeros(3)
        _Rp, _tp = world[_l]
        world[_j.find("child").get("link")] = (_Rp @ rpy2R(*_rpy), _tp + _Rp @ _xyz)
        _st.append(_j.find("child").get("link"))

rename_link = {}
for name, jn in auto_map.items():
    j = joints[jn]
    child = j.find("child").get("link")
    rename_link[child] = name + "_link"
    j.set("name", name + "_joint")
    j.set("type", "revolute")
    axis_local = pv(j.find("axis").get("xyz"))
    Rc, _ = world[child]
    a_world = Rc @ axis_local
    canon_axis, lo, hi, eff, vel = CANON[name]
    if float(np.dot(a_world, np.array(canon_axis, float))) < 0:
        lo, hi = -hi, -lo
    ET.SubElement(j, "limit", {"lower": f"{lo:.6g}", "upper": f"{hi:.6g}",
                               "effort": f"{eff:.6g}", "velocity": f"{vel:.6g}"})

def apply_renames(root, mapping):
    for l in root.findall("link"):
        if l.get("name") in mapping:
            l.set("name", mapping[l.get("name")])
    for j in root.findall("joint"):
        for tag in ("parent", "child"):
            e = j.find(tag)
            if e.get("link") in mapping:
                e.set("link", mapping[e.get("link")])

apply_renames(robot, rename_link)
links = {l.get("name"): l for l in robot.findall("link")}
joints = {j.get("name"): j for j in robot.findall("joint")}
children_of = {}
for j in robot.findall("joint"):
    children_of.setdefault(j.find("parent").get("link"), []).append(j)
world = {(rename_link.get(k, k)): v for k, v in world.items()}

# ---------------- 3: mirror the two subtrees ----------------
mirrored_meshes = {}  # original filename -> mirrored filename

def mirror_mesh_name(fn):
    stem, ext = fn.rsplit(".", 1)
    return f"{stem}_mirror.{ext}"

def leftname(n):
    return n.replace("right_", "left_") if n.startswith("right_") else "left_" + n

def clone_link(l):
    n = ET.fromstring(ET.tostring(l))
    n.set("name", leftname(l.get("name")))
    ine = n.find("inertial")
    if ine is not None:
        conj_origin(ine.find("origin"))
        it = ine.find("inertia")
        if it is not None:
            it.set("ixy", f"{-float(it.get('ixy')):.9g}")
            it.set("iyz", f"{-float(it.get('iyz')):.9g}")
    for tag in ("visual", "collision"):
        for e in n.findall(tag):
            conj_origin(e.find("origin"))
            mesh = e.find("geometry/mesh")
            if mesh is not None:
                fn = mesh.get("filename").split("/")[-1]
                mirrored_meshes[fn] = mirror_mesh_name(fn)
                mesh.set("filename", "package://rl/meshes/" + mirror_mesh_name(fn))
    return n

# auto-derive mirror roots: highest link whose subtree contains exactly one limb set
link_parent_joint = {j.find("child").get("link"): j for j in robot.findall("joint")}
subtree_named = {}
def named_below(ln):
    if ln in subtree_named:
        return subtree_named[ln]
    s = set()
    for j in children_of.get(ln, []):
        nm = j.get("name")[:-6] if j.get("name").endswith("_joint") else None
        if nm in CANON:
            s.add(nm)
        s |= named_below(j.find("child").get("link"))
    subtree_named[ln] = s
    return s

MIRROR_ROOTS = []
for limb, jset in LIMB_SETS.items():
    cands = [ln for ln in links if named_below(ln) == jset]
    if not cands:
        sys.exit(f"ERROR: no subtree contains exactly the {limb} joints - tree unexpected.")
    # highest candidate = the one none of whose ancestors is also a candidate
    root_link = None
    for ln in cands:
        pj = link_parent_joint.get(ln)
        if pj is None or pj.find("parent").get("link") not in cands:
            up = pj.find("parent").get("link") if pj is not None else None
            if root_link is None or up == "root" or (pj is not None and named_below(up) != jset):
                root_link = ln
    pj = link_parent_joint.get(root_link)
    if pj is None or pj.find("parent").get("link") in ("root",) or root_link.startswith("mate_connector"):
        sys.exit(f"ERROR: the {limb} is NOT attached to the central body - it hangs from "
                 f"the world origin ({root_link}). Fix the missing fastened mate in Onshape "
                 f"(e.g. hip-pitch motor to pelvis) and re-export.")
    # exclude fixed branches directly under the root that contain no limb joints
    excl = set()
    for j in children_of.get(root_link, []):
        c = j.find("child").get("link")
        if not named_below(c) & jset and j.get("type") == "fixed" and not c.startswith("mate_connector"):
            excl.add(c)
    if excl:
        print(f"  {limb}: mirroring subtree '{root_link}', excluding central branches: {sorted(excl)}")
    MIRROR_ROOTS.append((pj.get("name"), root_link, excl))

new_elems = []
for cross_jn, sub_root, exclude in MIRROR_ROOTS:
    # collect subtree links (skip excluded branches)
    sub = []
    st = [sub_root]
    while st:
        ln = st.pop()
        sub.append(ln)
        for j in children_of.get(ln, []):
            c = j.find("child").get("link")
            if c not in exclude:
                st.append(c)
    subset = set(sub)
    # clone links
    for ln in sub:
        new_elems.append(clone_link(links[ln]))
    # crossing joint: exact world-frame mirror (parent stays central)
    cj = joints[cross_jn]
    parent = cj.find("parent").get("link")
    Rp, tp = world[parent]
    Rc, tc = world[sub_root]
    Rl = M @ Rc @ D                      # left child world rotation (proper)
    tl = M @ tc                          # left child world position
    Rj = Rp.T @ Rl
    tj = Rp.T @ (tl - tp)
    nj = ET.fromstring(ET.tostring(cj))
    nj.set("name", leftname(cross_jn))
    nj.find("child").set("link", leftname(sub_root))
    o = nj.find("origin")
    if o is None:
        o = ET.SubElement(nj, "origin")
    o.set("xyz", fv(tj)); o.set("rpy", fv(R2rpy(Rj)))
    new_elems.append(nj)
    # interior joints: local conjugation by D
    for ln in sub:
        for j in children_of.get(ln, []):
            c = j.find("child").get("link")
            if c not in subset:
                continue
            nj = ET.fromstring(ET.tostring(j))
            nj.set("name", leftname(j.get("name")))
            nj.find("parent").set("link", leftname(ln))
            nj.find("child").set("link", leftname(c))
            conj_origin(nj.find("origin"))
            a = nj.find("axis")
            if a is not None:
                ax = pv(a.get("xyz"))
                a.set("xyz", fv([-ax[0], ax[1], -ax[2]]))  # same command = mirrored motion
            new_elems.append(nj)     # limits (if revolute) stay identical by construction

for e in new_elems:
    robot.append(e)

# ---------------- 6: collisions ----------------
def wants_collision(name):
    n = name.lower()
    return any(tok in n for tok in COLLISION_TOKENS)
for l in robot.findall("link"):
    if wants_collision(l.get("name")) and l.find("collision") is None:
        v = l.find("visual")
        if v is not None:
            c = ET.fromstring(ET.tostring(v))
            c.tag = "collision"
            for mat in c.findall("material"):
                c.remove(mat)
            l.append(c)

# ---------------- 4+7: meshes and output ----------------
(OUT / "urdf").mkdir(parents=True, exist_ok=True)
(OUT / "meshes").mkdir(parents=True, exist_ok=True)
for f in (EXPORT / "meshes").iterdir():
    if f.suffix.lower() == ".stl":
        shutil.copy2(f, OUT / "meshes" / f.name)

def mirror_stl(src, dst):
    data = src.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:400]:  # ASCII STL
        out = []
        vbuf = []
        for line in data.decode(errors="ignore").splitlines():
            s = line.strip()
            if s.startswith("vertex"):
                x, y, z = (float(v) for v in s.split()[1:4])
                vbuf.append((x, -y, z))
                if len(vbuf) == 3:
                    v0, v1, v2 = vbuf
                    e1 = np.subtract(v1, v0); e2 = np.subtract(v2, v0)
                    nrm = np.cross(e2, e1)  # swapped winding
                    n_ = nrm / (np.linalg.norm(nrm) or 1)
                    out.append(f"  facet normal {fv(n_)}\n    outer loop\n"
                               f"      vertex {fv(v0)}\n      vertex {fv(v2)}\n      vertex {fv(v1)}\n"
                               f"    endloop\n  endfacet")
                    vbuf = []
            elif s.startswith(("facet", "outer", "endloop", "endfacet")):
                continue
            elif s.startswith("solid"):
                out.append("solid mirrored")
            elif s.startswith("endsolid"):
                out.append("endsolid mirrored")
        dst.write_text("\n".join(out) + "\n")
        return
    n = struct.unpack_from("<I", data, 80)[0]
    arr = np.frombuffer(data[84:84 + n * 50], dtype=np.uint8).reshape(n, 50).copy()
    tri = arr[:, :48].view("<f4").reshape(n, 4, 3)   # normal, v0, v1, v2
    tri[:, :, 1] *= -1.0                             # y flip (normal + vertices)
    tri[:, [2, 3]] = tri[:, [3, 2]]                  # swap winding
    tri[:, 0] *= -1.0                                # normal = M n after winding swap: recompute sign
    e1 = tri[:, 2] - tri[:, 1]; e2 = tri[:, 3] - tri[:, 1]
    nrm = np.cross(e1, e2)
    ln = np.linalg.norm(nrm, axis=1, keepdims=True); ln[ln == 0] = 1
    tri[:, 0] = nrm / ln
    dst.write_bytes(data[:80] + struct.pack("<I", n) + arr.tobytes())

for orig, mir in mirrored_meshes.items():
    mirror_stl(EXPORT / "meshes" / orig, OUT / "meshes" / mir)

src = ET.tostring(robot, encoding="unicode")
src = src.replace("package://rl/meshes/", "../meshes/")
(OUT / "urdf" / "rl_full.urdf").write_text('<?xml version="1.0" ?>\n' + src)

print("MASS INJECTION:")
print("\n".join(mass_report) if mass_report else "  (nothing matched)")
print("STILL < 5 g (rename in Onshape so a MASS_RULES token matches, or confirm they are truly light):")
for l in robot.findall("link"):
    n = l.get("name")
    if n.lower().startswith(DUMMY_PREFIXES) or n.startswith("left_"):
        continue
    ine = l.find("inertial")
    if ine is not None and float(ine.find("mass").get("value")) < 0.005:
        print(f"  {n}")

for j in robot.findall("joint"):
    if j.get("type") != "revolute":
        continue
    cl = None
    for l in robot.findall("link"):
        if l.get("name") == j.find("child").get("link"):
            cl = l; break
    ine = cl.find("inertial") if cl is not None else None
    if ine is not None and float(ine.find("mass").get("value")) < 0.005:
        set_link_mass(cl, 0.05)
        print(f"  SAFETY: moving link {cl.get('name')} was < 5 g -> floored to 0.05 kg "
              f"(assign its real material in Onshape!)")

nrev = sum(1 for j in robot.findall("joint") if j.get("type") == "revolute")
print(f"written {OUT/'urdf'/'rl_full.urdf'}")
print(f"links: {len(robot.findall('link'))}  joints: {len(robot.findall('joint'))}  revolute: {nrev}")
print(f"mirrored meshes: {len(mirrored_meshes)}")
