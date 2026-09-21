"""Replace the two foot links' mesh collision with a simple box primitive.

Full-mesh convex-decomposed collision on a plate-shaped part with small screw-hole
detail is a known source of contact-solver instability (jitter/vibration) against the
ground plane. Every reference biped (G1, H1, Cassie, Digit) uses simplified foot
collision, not raw meshes. Box dims/center are computed directly from the STL vertex
extents (both foot links have identity collision <origin>, verified against the URDF).
"""
import xml.etree.ElementTree as ET

URDF = r"C:\Users\WKS\Documents\humanoid\rl_full_isaac\rl_full\urdf\rl_full.urdf"

# (link_name, size_xyz, center_xyz) = the SOLE PLATE ONLY, measured from the STL.
#
# NOTE: an earlier version of this script used the full-mesh AABB, which was wrong twice:
#   - height 48.9 mm instead of 11.9 mm -> a solid brick up to the top of the ankle
#     bracket, whose vertical side faces would catch on stair edges that the real
#     thin plate clears;
#   - width 81.5 mm instead of 70.0 mm -> that 81.5 was the ankle BRACKET width, not
#     the sole, giving the policy a 16% oversized support polygon (optimistic balance
#     that would not transfer to the real robot).
# These values are the true load-bearing plate: 199.9 x 70.0 x 11.9 mm.
FOOT_BOXES = {
    "part_22_foot": ((0.199897, 0.070000, 0.011862), (0.033333, -0.126700, -0.782375)),
    "left_part_22_foot": ((0.199897, 0.070000, 0.011862), (0.033333, 0.126700, -0.782375)),
}

tree = ET.parse(URDF)
robot = tree.getroot()
changed = 0
for link in robot.findall("link"):
    name = link.get("name")
    if name not in FOOT_BOXES:
        continue
    size, center = FOOT_BOXES[name]
    coll = link.find("collision")
    if coll is None:
        print(f"WARNING: {name} has no <collision> element, skipping")
        continue
    origin = coll.find("origin")
    if origin is None:
        origin = ET.SubElement(coll, "origin")
    origin.set("xyz", f"{center[0]:.6f} {center[1]:.6f} {center[2]:.6f}")
    origin.set("rpy", "0 0 0")
    geom = coll.find("geometry")
    for child in list(geom):
        geom.remove(child)
    ET.SubElement(geom, "box", {"size": f"{size[0]:.6f} {size[1]:.6f} {size[2]:.6f}"})
    changed += 1
    print(f"{name}: collision -> box size={size} center={center}")

if changed != 2:
    raise SystemExit(f"ERROR: expected to patch 2 foot links, patched {changed}")

src = ET.tostring(robot, encoding="unicode")
with open(URDF, "w") as f:
    f.write('<?xml version="1.0" ?>\n' + src)
print("written", URDF)
