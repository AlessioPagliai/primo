#!/usr/bin/env python3
"""tiny orthographic renderer (numpy z-buffer): python render.py out.png  title:mesh1.stl[,mesh2.stl@grey]  ..."""
import sys, numpy as np
from skimage import io
import bonegen as bg
def draw(tris_list, view, box, px=2.0):
    ia, ib, idp, sgn = view                      # image axes, depth axis, viewing direction sign
    W = int((box[ia][1] - box[ia][0]) * px); H = int((box[ib][1] - box[ib][0]) * px)
    img = np.ones((H, W, 3)); zb = np.full((H, W), -1e9)
    for tris, col in tris_list:
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        L = np.array([0.35, -0.5, 0.8]); L[idp] = sgn * 0.75; L /= np.linalg.norm(L); sh = 0.35 + 0.65 * np.clip(np.abs(n @ L), 0, 1)
        P = np.stack([(tris[:, :, ia] - box[ia][0]) * px, (box[ib][1] - tris[:, :, ib]) * px, tris[:, :, idp] * sgn], 2)
        for t, s in zip(P, sh):
            x0, x1 = int(max(np.floor(t[:, 0].min()), 0)), int(min(np.ceil(t[:, 0].max()), W - 1)); y0, y1 = int(max(np.floor(t[:, 1].min()), 0)), int(min(np.ceil(t[:, 1].max()), H - 1))
            if x0 > x1 or y0 > y1: continue
            den = (t[1, 1] - t[2, 1]) * (t[0, 0] - t[2, 0]) + (t[2, 0] - t[1, 0]) * (t[0, 1] - t[2, 1])
            if abs(den) < 1e-9: continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            a = ((t[1, 1] - t[2, 1]) * (X - t[2, 0]) + (t[2, 0] - t[1, 0]) * (Y - t[2, 1])) / den; b = ((t[2, 1] - t[0, 1]) * (X - t[2, 0]) + (t[0, 0] - t[2, 0]) * (Y - t[2, 1])) / den
            m = (a >= 0) & (b >= 0) & (a + b <= 1); Z = a * t[0, 2] + b * t[1, 2] + (1 - a - b) * t[2, 2]
            sub = zb[y0:y1 + 1, x0:x1 + 1]; m &= Z > sub; sub[m] = Z[m]; img[y0:y1 + 1, x0:x1 + 1][m] = np.array(col) * s
    return img
if __name__ == '__main__':
    import os
    out = sys.argv[1]; md = next(p for p in ('meshes/', '../../sim/meshes/', '../../umanoide-release/sim/meshes/') if os.path.isdir(p)); box = {0: (-100, 100), 1: (-200, -55), 2: (-640, -200)}
    grey, blue = (0.55, 0.55, 0.58), (0.35, 0.55, 0.85)
    near = [(bg.load_stl(md + f), grey) for f in ('Part_1_rs04.stl', 'Part_4_rs06.stl', 'Part_11_rs06.stl')] + [(bg.load_stl(md + f), blue) for f in ('Part_18_tibia.stl', 'Part_40_hip_roll_to_yaw.stl')]
    cols = []
    for spec in sys.argv[2:]:
        f = spec.split(':')[1]; t = bg.load_stl(f, 1.0 if f.startswith('out/') else 1000.0); bone = [(t, (0.95, 0.55, 0.15))]
        side = draw(bone + near, (0, 2, 1, -1), box); front = draw(bone + near, (1, 2, 0, 1), box)
        top = draw(bone, (0, 1, 2, 1), {0: (-100, 100), 1: (-200, -55), 2: box[2]})           # bone alone seen from above: flange holes
        topc = np.ones((side.shape[0], top.shape[1], 3)); topc[:top.shape[0]] = top; g = np.ones((side.shape[0], 14, 3))
        cols.append(np.concatenate([side, g, front, g, topc, np.ones((side.shape[0], 46, 3))], 1))
    io.imsave(out, (np.concatenate(cols, 1) * 255).astype(np.uint8), check_contrast=False); print('saved', out)
