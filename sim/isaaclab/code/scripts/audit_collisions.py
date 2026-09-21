"""Audit collision geometry: how well does each primitive/mesh approximate the real part?

For the foot box: compares the box volume against the actual mesh volume, and reports
how much the box over-covers the true sole footprint (an oversized support polygon makes
the policy optimistic vs the real robot).
"""
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

MESHES = Path(r"C:\Users\WKS\Documents\humanoid\rl_full_isaac\rl_full\meshes")
URDF = Path(r"C:\Users\WKS\Documents\humanoid\rl_full_isaac\rl_full\urdf\rl_full.urdf")


def load_stl(p):
    d = p.read_bytes()
    n = struct.unpack_from("<I", d, 80)[0]
    tri = np.frombuffer(d[84:84 + n * 50], dtype=np.uint8).reshape(n, 50)[:, :48].view("<f4").reshape(n, 4, 3)
    return tri[:, 1:], n  # (n,3,3) vertices


def mesh_volume(tris):
    v0, v1, v2 = tris[:, 0], tris[:, 1], tris[:, 2]
    return abs(np.sum(np.einsum("ij,ij->i", v0, np.cross(v1, v2))) / 6.0)


print("=" * 78)
print("FOOT: box primitive vs real mesh")
tris, ntri = load_stl(MESHES / "Part_22_foot.stl")
v = tris.reshape(-1, 3)
lo, hi = v.min(0), v.max(0)
size = hi - lo
box_vol = float(np.prod(size))
m_vol = mesh_volume(tris)
print(f"  triangles         : {ntri}")
print(f"  AABB size (m)     : {size.round(4)}")
print(f"  box volume        : {box_vol*1e6:.1f} cm^3")
print(f"  true mesh volume  : {m_vol*1e6:.1f} cm^3  ({100*m_vol/box_vol:.1f}% of box)")

# footprint analysis: sole = lowest 8 mm of the mesh
sole_mask = v[:, 2] < lo[2] + 0.008
sole = v[sole_mask]
if len(sole):
    s_lo, s_hi = sole.min(0), sole.max(0)
    s_size = (s_hi - s_lo)[:2]
    # convex-hull-free estimate of true sole area: grid occupancy
    gx = np.linspace(s_lo[0], s_hi[0], 120)
    gy = np.linspace(s_lo[1], s_hi[1], 120)
    cell = (gx[1] - gx[0]) * (gy[1] - gy[0])
    ix = np.clip(np.searchsorted(gx, sole[:, 0]) - 1, 0, 118)
    iy = np.clip(np.searchsorted(gy, sole[:, 1]) - 1, 0, 118)
    occupied = len(set(zip(ix.tolist(), iy.tolist())))
    true_area = occupied * cell
    box_area = float(size[0] * size[1])
    print(f"  sole bbox (m)     : {s_size.round(4)}  (box footprint {size[0]:.4f} x {size[1]:.4f})")
    print(f"  box footprint area: {box_area*1e4:.1f} cm^2")
    print(f"  ~true sole area   : {true_area*1e4:.1f} cm^2 (sampled)  -> box over-covers "
          f"~{100*(box_area/true_area - 1):.0f}%")

print()
print("=" * 78)
print("ALL COLLISION BODIES currently in the URDF")
tree = ET.parse(URDF)
robot = tree.getroot()
rows = []
for link in robot.findall("link"):
    coll = link.findall("collision")
    if not coll:
        continue
    for c in coll:
        g = c.find("geometry")
        box = g.find("box")
        mesh = g.find("mesh")
        if box is not None:
            rows.append((link.get("name"), "BOX", box.get("size"), "-"))
        elif mesh is not None:
            fn = mesh.get("filename").split("/")[-1]
            try:
                t, n = load_stl(MESHES / fn)
                rows.append((link.get("name"), "MESH", fn, f"{n} tris"))
            except Exception:
                rows.append((link.get("name"), "MESH", fn, "?"))
print(f"  total collision bodies: {len(rows)}")
total_tris = 0
for name, kind, detail, extra in sorted(rows):
    print(f"  {name:38s} {kind:5s} {detail:34s} {extra}")
    if kind == "MESH" and extra.endswith("tris"):
        total_tris += int(extra.split()[0])
print(f"  total collision triangles (mesh bodies): {total_tris}")
