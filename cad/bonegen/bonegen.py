#!/usr/bin/env python3
"""bonegen - regenerate a structural "bone" between actuators by topology optimisation.

Input : a JSON config (see thigh.json) + the STL meshes of the robot (metres, root frame, zero pose).
Output: out/<name>/  density.npy, optimized.stl, final.stl (exact CAD interfaces kept), report.json
Units : mm, N, MPa.  Usage: python bonegen.py thigh.json [--pitch 5] [--iters 60] [--vol 1.0]
"""
import argparse, json, os, struct, time, warnings
import numpy as np
warnings.filterwarnings('ignore', category=RuntimeWarning)   # macOS Accelerate: spurious matmul warnings
from scipy import ndimage, sparse
import pyamg

# ---------------------------------------------------------------- meshes and voxels
def load_stl(path, scale=1000.0):
    d = open(path, 'rb').read(); n = struct.unpack('<I', d[80:84])[0]
    assert 84 + 50 * n == len(d), 'binary STL expected: ' + path
    a = np.frombuffer(d, dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]), count=n, offset=84)['v']
    return a.reshape(-1, 3, 3).astype(np.float64) * scale

def save_stl(path, tris):
    tris = np.asarray(tris, np.float32); n = len(tris)
    rec = np.zeros(n, dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    rec['v'] = tris.reshape(n, 9)
    with open(path, 'wb') as f:
        f.write(b'bonegen'.ljust(80, b' ')); f.write(struct.pack('<I', n)); f.write(rec.tobytes())

def voxelize(tris, origin, pitch, shape):
    """occupancy at voxel centres by parity ray casting along +z (watertight meshes)"""
    nx, ny, nz = shape
    cnt = np.zeros((nx, ny, nz + 1), np.int32)
    xs = origin[0] + (np.arange(nx) + 0.5) * pitch + 1.23e-4 * pitch      # tiny jitter: never hit an edge exactly
    ys = origin[1] + (np.arange(ny) + 0.5) * pitch + 2.71e-4 * pitch
    for t in tris:
        lo = t.min(0); hi = t.max(0)
        i0 = max(int(np.ceil((lo[0] - xs[0]) / pitch)), 0); i1 = min(int(np.floor((hi[0] - xs[0]) / pitch)), nx - 1)
        j0 = max(int(np.ceil((lo[1] - ys[0]) / pitch)), 0); j1 = min(int(np.floor((hi[1] - ys[0]) / pitch)), ny - 1)
        if i0 > i1 or j0 > j1: continue
        (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = t
        den = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if abs(den) < 1e-12: continue
        X, Y = np.meshgrid(xs[i0:i1 + 1], ys[j0:j1 + 1], indexing='ij')
        a = ((y2 - y3) * (X - x3) + (x3 - x2) * (Y - y3)) / den
        b = ((y3 - y1) * (X - x3) + (x1 - x3) * (Y - y3)) / den
        m = (a >= 0) & (b >= 0) & (a + b <= 1)
        if not m.any(): continue
        Z = a * z1 + b * z2 + (1 - a - b) * z3
        k = np.clip(np.ceil((Z[m] - origin[2]) / pitch - 0.5).astype(int), 0, nz)
        ii, jj = np.nonzero(m)
        np.add.at(cnt, (ii + i0, jj + j0, k), 1)
    return (np.cumsum(cnt, axis=2)[:, :, :nz] % 2) == 1

def fraction(tris, origin, pitch, shape, s=3):
    """solid fraction per voxel (supersampled): keeps thin walls that a centre test would lose"""
    fine = voxelize(tris, origin, pitch / s, tuple(n * s for n in shape))
    return fine.reshape(shape[0], s, shape[1], s, shape[2], s).mean(axis=(1, 3, 5))

def find_holes(tris, ax, rng, lo, hi, pf=0.5, dmin=2.5, dmax=14):
    """round holes seen along an axis inside a slab of a part: [(centre in the two other axes), diameter]"""
    lo = np.array(lo, float).copy(); hi = np.array(hi, float).copy(); lo[ax], hi[ax] = rng
    shp = tuple(np.maximum(1, np.ceil((hi - lo) / pf)).astype(int)); occ = voxelize(tris, lo, pf, shp).mean(axis=ax) > 0.6
    holes, nh = ndimage.label(ndimage.binary_fill_holes(occ) & ~occ); out = []
    for k in range(1, nh + 1):
        d = 2 * np.sqrt((holes == k).sum() * pf * pf / np.pi)
        if dmin <= d <= dmax: out.append((np.array(ndimage.center_of_mass(holes == k)) * pf + np.delete(lo, ax) + pf / 2, d))
    return out

def rot(axis, th):
    a = np.asarray(axis, float); a /= np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K

def centres(origin, pitch, shape):
    g = np.meshgrid(*[origin[i] + (np.arange(shape[i]) + 0.5) * pitch for i in range(3)], indexing='ij')
    return np.stack([x.ravel() for x in g], 1)

def swept(tris, pts, c, axis, angles, p_f):
    """which points are touched by the body while it turns about the axis (occupancy lookup, body voxelised once)"""
    lo = tris.reshape(-1, 3).min(0) - p_f; hi = tris.reshape(-1, 3).max(0) + p_f
    shp = tuple(np.ceil((hi - lo) / p_f).astype(int)); occ = voxelize(tris, lo, p_f, shp)
    hit = np.zeros((len(angles), len(pts)), bool)
    for n, th in enumerate(angles):
        with np.errstate(all='ignore'):          # macOS Accelerate raises spurious matmul warnings
            q = (pts - c) @ rot(axis, -th).T + c
        idx = np.floor((q - lo) / p_f).astype(int)
        ok = ((idx >= 0) & (idx < np.array(shp))).all(1)
        hit[n, ok] = occ[idx[ok, 0], idx[ok, 1], idx[ok, 2]]
    return hit

# ---------------------------------------------------------------- finite elements (8-node bricks on the voxel grid)
def ke_h8(nu, h):
    C = np.zeros((6, 6)); C[:3, :3] = nu; C[np.arange(3), np.arange(3)] = 1 - nu; C[3:, 3:] = np.eye(3) * (1 - 2 * nu) / 2
    C /= (1 + nu) * (1 - 2 * nu)
    nat = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], float)
    K = np.zeros((24, 24)); g = 1 / np.sqrt(3)
    for gp in nat * g:
        dN = nat * (1 + nat[:, [1, 2, 0]] * gp[[1, 2, 0]]) * (1 + nat[:, [2, 0, 1]] * gp[[2, 0, 1]]) / 8 * (2 / h)
        B = np.zeros((6, 24))
        for a in range(8):
            dx, dy, dz = dN[a]
            B[:, 3 * a:3 * a + 3] = [[dx, 0, 0], [0, dy, 0], [0, 0, dz], [dy, dx, 0], [0, dz, dy], [dz, 0, dx]]
        K += B.T @ C @ B * (h / 2) ** 3
    return K

class Grid:
    def __init__(self, origin, pitch, shape):
        self.o, self.h, self.shape = np.asarray(origin, float), pitch, shape
        nx, ny, nz = shape; self.nel = nx * ny * nz
        nid = np.arange((nx + 1) * (ny + 1) * (nz + 1)).reshape(nx + 1, ny + 1, nz + 1)
        off = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
        self.enodes = np.stack([nid[a:nx + a, b:ny + b, c:nz + c].ravel() for a, b, c in off], 1)
        self.edof = (3 * self.enodes[:, :, None] + np.arange(3)).reshape(self.nel, 24)
        g = np.meshgrid(*[self.o[i] + np.arange(shape[i] + 1) * pitch for i in range(3)], indexing='ij')
        self.xyz = np.stack([x.ravel() for x in g], 1); self.ndof = 3 * len(self.xyz)
        self.KE = ke_h8(0.35, pitch)

    def solve(self, Ee, active, fixed_nodes, F, U0=None):
        """Ee: modulus per element, active: elements in the model, F: (ndof, ncases)"""
        el = np.nonzero(active)[0]; ed = self.edof[el]
        K = sparse.coo_matrix(((self.KE.ravel()[None, :] * Ee[el, None]).ravel(),
                               (np.repeat(ed, 24, 1).ravel(), np.tile(ed, (1, 24)).ravel())), shape=(self.ndof,) * 2).tocsr()
        nodes = np.zeros(len(self.xyz), bool); nodes[self.enodes[el].ravel()] = True; nodes[fixed_nodes] = False
        nn = np.nonzero(nodes)[0]; free = (3 * nn[:, None] + np.arange(3)).ravel()
        Kff = K[free][:, free].tobsr(blocksize=(3, 3))
        p = self.xyz[nn] - self.xyz[nn].mean(0); Bm = np.zeros((len(free), 6))
        for i in range(3): Bm[i::3, i] = 1
        Bm[0::3, 4] = p[:, 2]; Bm[0::3, 5] = -p[:, 1]; Bm[1::3, 3] = -p[:, 2]; Bm[1::3, 5] = p[:, 0]; Bm[2::3, 3] = p[:, 1]; Bm[2::3, 4] = -p[:, 0]
        ml = pyamg.smoothed_aggregation_solver(Kff, B=Bm, max_coarse=300)
        U = np.zeros_like(F)
        for c in range(F.shape[1]):
            x0 = None if U0 is None else U0[free, c]
            U[free, c] = ml.solve(F[free, c], x0=x0, tol=1e-7, accel='cg', maxiter=400)
        return U

def wrench_to_nodes(xyz, nodes, centre, Fv, Mv):
    """spread a force + moment on a node set: f_i = a + b x r_i (least norm, like an RBE3)"""
    r = xyz[nodes] - centre; G = np.zeros((6, 6)); A = []
    for ri in r:
        S = np.array([[0, -ri[2], ri[1]], [ri[2], 0, -ri[0]], [-ri[1], ri[0], 0]])
        Ai = np.hstack([np.eye(3), -S]); A.append(Ai); G[:3] += Ai; G[3:] += S @ Ai
    z = np.linalg.solve(G, np.hstack([Fv, Mv]))
    return np.array([Ai @ z for Ai in A])

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('config'); ap.add_argument('--pitch', type=float)
    ap.add_argument('--iters', type=int, default=60); ap.add_argument('--vol', type=float); ap.add_argument('--setup-only', action='store_true'); ap.add_argument('--remesh', action='store_true', help='reuse out/.../density.npy, redo check + meshes')
    ap.add_argument('--find-holes', nargs=2, metavar=('MESH', 'AXIS@LO:HI'), help='list the round holes of a mesh inside a slab, e.g. motor.stl y@-120:-112')
    a = ap.parse_args(); cfg = json.load(open(a.config)); here = os.path.dirname(os.path.abspath(a.config))
    if a.find_holes:
        t = load_stl(os.path.join(os.path.normpath(os.path.join(here, cfg['mesh_dir'])), a.find_holes[0])); axn, rg = a.find_holes[1].split('@'); ax = 'xyz'.index(axn); p = t.reshape(-1, 3)
        for cm, d in find_holes(t, ax, tuple(float(v) for v in rg.split(':')), p.min(0) - 1, p.max(0) + 1): print(np.round(cm, 1).tolist(), round(d, 1))
        return
    md = os.path.normpath(os.path.join(here, cfg['mesh_dir'])); M = lambda f: load_stl(os.path.join(md, f))
    h = a.pitch or cfg['pitch_mm']; vol = a.vol or cfg.get('volume_ratio', 1.0)
    env = np.array(cfg['envelope_mm'], float); o = env[:, 0]; shape = tuple(np.ceil((env[:, 1] - env[:, 0]) / h).astype(int))
    out = os.path.join(here, 'out', cfg['name'] + f'_p{h:g}'); os.makedirs(out, exist_ok=True)
    print(f'grid {shape} = {np.prod(shape)} elements at {h} mm'); t0 = time.time()
    pts = centres(o, h, shape); rep = {'name': cfg['name'], 'pitch_mm': h, 'assumptions': cfg.get('assumptions', '')}

    has_bone = bool(cfg.get('bone_mesh')); bone_tris = M(cfg['bone_mesh']) if has_bone else None
    bone = fraction(bone_tris, o, h, shape, 3) if has_bone else np.zeros(shape)
    force_void = np.zeros(shape, bool); pad_geo = []
    # interfaces: the current bone is kept exactly where it meets the actuators
    iface = {}
    for it in cfg['interfaces']:
        if it['type'] == 'pads':                 # pads around the motor's screw holes: solid pad, empty hole, empty head/tool channel
            ax = 'xyz'.index(it['axis']); oth = [i for i in range(3) if i != ax]; sd = it['side']; f0 = it['face']
            along = (pts[:, ax] - f0) * sd; pad = np.zeros(len(pts), bool)
            for hx in it['holes']:
                rr = np.hypot(pts[:, oth[0]] - hx[0], pts[:, oth[1]] - hx[1])
                pad |= (rr <= it['pad_d'] / 2) & (along >= 0) & (along <= it['pad_t'])
                force_void |= ((rr <= it['hole_d'] / 2) & (along >= 0) & (along <= it['pad_t'] + it['access_len'])).reshape(shape)
                force_void |= ((rr <= it['head_d'] / 2) & (along > it['pad_t'] - it.get('head_depth', 0)) & (along <= it['pad_t'] + it['access_len'])).reshape(shape)   # counterbore + tool path
                pad_geo.append((ax, oth, hx, f0, sd, it))
            if it.get('ring'):                      # optional ring joining the pads: [centre_a, centre_b, r_in, r_out]
                ca, cb, r0, r1 = it['ring']; rr = np.hypot(pts[:, oth[0]] - ca, pts[:, oth[1]] - cb); pad |= (rr >= r0) & (rr <= r1) & (along >= 0) & (along <= it['pad_t'])
            iface[it['name']] = pad.reshape(shape) & ~force_void; print(' interface', it['name'], int(iface[it['name']].sum()), 'voxels (pads)'); continue
        if it['type'] == 'slab':
            ax = 'xyz'.index(it['axis']); reg = (pts[:, ax] >= it['range'][0]) & (pts[:, ax] <= it['range'][1])
        else:                                   # near a motor: its bounding cylinder/box grown by dist
            t = M(it['mesh']).reshape(-1, 3); lo, hi = t.min(0) - it['dist_mm'], t.max(0) + it['dist_mm']
            reg = ((pts >= lo) & (pts <= hi)).all(1)
        iface[it['name']] = (reg.reshape(shape) & (bone > 0.3)); print(' interface', it['name'], int(iface[it['name']].sum()), 'voxels')
    solid = np.any(list(iface.values()), axis=0)

    # keep-outs: bodies that move with the bone, bodies that sweep past it, screw access
    void = np.zeros(shape, bool); grow = int(np.ceil(cfg.get('clearance_mm', 3) / h)); rom = {}
    for f in cfg.get('keepout_static', []): void |= voxelize(M(f), o, h, shape)
    for sw in cfg.get('sweeps', []):
        tris = np.concatenate([M(f) for f in sw['meshes']]); n = int(np.ceil((sw['range'][1] - sw['range'][0]) / np.radians(3))) + 1
        ang = np.linspace(sw['range'][0], sw['range'][1], n); hit = swept(tris, pts, np.array(sw['axis_point'], float), sw['axis'], ang, min(h / 2, 2.0))
        clash = (hit & ((bone > 0.6) & ~solid).ravel()[None, :]).sum(1) * h ** 3 if has_bone else np.zeros(len(ang))            # mm3 of the CURRENT bone touched, per angle
        bad = ang[clash > 200]; rom[sw['name']] = {'range_rad': sw['range'], 'current_bone_clash_angles_deg': [round(float(np.degrees(x)), 1) for x in bad[:: max(1, len(bad) // 8)]],
                                                     'max_clash_mm3': float(clash.max())}
        lim = sw.get('use_range', sw['range']); use = (ang >= lim[0]) & (ang <= lim[1]); sv = hit[use].any(0).reshape(shape); void |= sv
        rom[sw['name']]['interface_inside_swept_volume_mm3'] = float((sv & solid).sum() * h ** 3)     # pads that a neighbour would hit
    if grow: void = ndimage.binary_dilation(void, iterations=grow)
    for acc in cfg.get('screw_access', []):         # holes found in the current flange -> keep a straight tool path free
        ax = 'xyz'.index(acc['axis']); pf = 1.0; lo = o.copy(); hi = env[:, 1].copy(); lo[ax], hi[ax] = acc['range']
        shp = tuple(np.ceil((hi - lo) / pf).astype(int)); occ = voxelize(bone_tris, lo, pf, shp).mean(axis=ax) > 0.6
        holes, nh = ndimage.label(ndimage.binary_fill_holes(occ) & ~occ); found = []
        for k in range(1, nh + 1):
            d = 2 * np.sqrt((holes == k).sum() * pf * pf / np.pi)
            if 2.5 <= d <= 14:
                cm = np.array(ndimage.center_of_mass(holes == k)) * pf + np.delete(lo, ax) + pf / 2; found.append([*np.round(cm, 1), round(d, 1)])
                oth = [i for i in range(3) if i != ax]; rr = np.hypot(pts[:, oth[0]] - cm[0], pts[:, oth[1]] - cm[1]) <= d / 2 + acc.get('head_clearance_mm', 3.5)
                s = acc['side']; along = (pts[:, ax] < acc['range'][0]) & (pts[:, ax] > acc['range'][0] - acc['length_mm']) if s < 0 else (pts[:, ax] > acc['range'][1]) & (pts[:, ax] < acc['range'][1] + acc['length_mm'])
                void |= (rr & along).reshape(shape)
        rom.setdefault('screw_holes', {})[acc['name']] = found; print(' screw holes', acc['name'], len(found))
    for hp in cfg.get('head_pockets', []):          # {"centre":[x,y,z], "axis":"z", "diameter_mm":10, "depth_mm":6, "side":-1}
        ax = 'xyz'.index(hp['axis']); oth = [i for i in range(3) if i != ax]; c0 = np.array(hp['centre'], float)
        rr = np.hypot(pts[:, oth[0]] - c0[oth[0]], pts[:, oth[1]] - c0[oth[1]]) <= hp['diameter_mm'] / 2
        dd = (pts[:, ax] - c0[ax]) * hp.get('side', -1); void |= (rr & (dd >= 0) & (dd <= hp['depth_mm'])).reshape(shape)
    void &= ~solid; void |= force_void; solid &= ~force_void; design = ~void & ~solid
    rep['rom_check_current_bone'] = rom; rep['voxels'] = {'design': int(design.sum()), 'solid_interface': int(solid.sum()), 'keepout': int(void.sum())}
    print(' design', design.sum(), 'solid', solid.sum(), 'void', void.sum(), f'  setup {time.time() - t0:.0f}s')
    np.save(os.path.join(out, 'design.npy'), design); np.save(os.path.join(out, 'solid.npy'), solid); np.save(os.path.join(out, 'bone_current.npy'), bone)
    if a.setup_only: json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1); return

    # loads
    G = Grid(o, h, shape); E0 = cfg.get('E_MPa', 6000.0); Emin = 1e-4 * E0; pen = 3.0
    fixn = np.unique(G.enodes[iface[cfg['fixed_interface']].ravel()]); ln = np.setdiff1d(np.unique(G.enodes[iface[cfg['load_interface']].ravel()]), fixn)
    F = np.zeros((G.ndof, len(cfg['load_cases'])))
    for c, lc in enumerate(cfg['load_cases']):
        f = wrench_to_nodes(G.xyz, ln, np.array(cfg['load_centre'], float), np.array(lc['F_N'], float), np.array(lc['M_Nmm'], float))
        F[(3 * ln[:, None] + np.arange(3)).ravel(), c] = f.ravel()
    # baseline: the current bone under the same loads
    if has_bone:
        xb = np.maximum(bone, solid).ravel(); Ub = G.solve(Emin + xb * (E0 - Emin), xb > 0.02, fixn, F); cb = (F * Ub).sum(0)
    else: cb = np.array(cfg['baseline_compliance_Nmm'], float)      # current bone, measured once in CAD-interface mode
    print(' current bone compliance [N mm]:', np.round(cb, 2)); w = 1.0 / cb
    vt = vol * (bone.sum() if has_bone else cfg['volume_cm3'] * 1000 / h ** 3); vfd = float(np.clip((vt - solid.sum()) / design.sum(), 0.03, 0.95)); print(f' design volume fraction {vfd:.3f}')
    # SIMP + density filter + optimality criteria
    r = cfg.get('filter_mm', 2.2 * h) / h; n = int(np.ceil(r)); g = np.mgrid[-n:n + 1, -n:n + 1, -n:n + 1]; ker = np.maximum(0, r - np.sqrt((g ** 2).sum(0)))
    Hs = ndimage.convolve(np.ones(shape), ker, mode='constant'); filt = lambda v: ndimage.convolve(v, ker, mode='constant') / Hs
    x = np.where(design, vfd, 0.0); U = None; active = (design | solid).ravel()
    for itn in range(0 if a.remesh else a.iters):
        xp = filt(x); xp[void] = 0; xp[solid] = 1; xv = xp.ravel()
        U = G.solve(Emin + xv ** pen * (E0 - Emin), active, fixn, F, U)
        ce = np.zeros(G.nel)
        for c in range(F.shape[1]):
            ue = U[G.edof, c]; ce += w[c] * np.einsum('ij,jk,ik->i', ue, G.KE, ue)
        dc = ndimage.convolve((-pen * xv ** (pen - 1) * (E0 - Emin) * ce).reshape(shape) / Hs, ker, mode='constant')
        dv = ndimage.convolve(np.ones(shape) / Hs, ker, mode='constant')
        l1, l2 = 1e-12, 1e12
        while (l2 - l1) / (l1 + l2) > 1e-4:
            lm = 0.5 * (l1 + l2); xn = np.clip(x * np.sqrt(np.maximum(-dc, 0) / dv / lm), np.maximum(0, x - 0.2), np.minimum(1, x + 0.2))
            xn = np.where(design, xn, 0.0)
            if xn[design].mean() > vfd: l1 = lm
            else: l2 = lm
        ch = float(np.abs(xn - x).max()); x = xn; obj = float((w * (F * U).sum(0)).sum())
        print(f' it {itn + 1:3d}  objective {obj:.3f} (current bone = {F.shape[1]}.000)  change {ch:.3f}  {time.time() - t0:.0f}s', flush=True)
        if ch < 0.01 and itn > 15: break
    if a.remesh: xp = np.load(os.path.join(out, 'density.npy'))
    else: xp = filt(x); xp[void] = 0; xp[solid] = 1; np.save(os.path.join(out, 'density.npy'), xp)
    # final check on the thresholded (printable) design, same volume as requested
    lvl = np.sort(xp.ravel())[::-1][int(min(vt, xp.size - 1))]; xs = (xp >= max(lvl, 0.3)).astype(float); xs[solid] = 1
    Uf = G.solve(Emin + xs.ravel() * (E0 - Emin), xs.ravel() > 0, fixn, F); cf = (F * Uf).sum(0)
    rep.update({'load_cases': [l['name'] for l in cfg['load_cases']], 'compliance_current_Nmm': cb.tolist(), 'compliance_optimized_Nmm': cf.tolist(),
                'stiffness_gain_per_case': (cb / cf).tolist(), 'volume_current_cm3': float(vt / vol * h ** 3 / 1000), 'volume_optimized_cm3': float(xs.sum() * h ** 3 / 1000)})
    print(' stiffness gain per load case (optimized / current):', np.round(cb / cf, 2), ' volume ratio', round(xs.sum() / (vt / vol), 3))
    # surface: upsample, smooth, marching cubes
    from skimage import measure
    up = 2; vol3 = ndimage.gaussian_filter(ndimage.zoom(np.pad(np.where(solid, 1.0, xp * xs), 1), up, order=1), 0.8)
    iso = float(np.clip(np.sort(vol3.ravel())[::-1][int(xs.sum() * up ** 3)], 0.15, 0.6))   # surface level that keeps the volume of the checked design
    v, fcs, _, _ = measure.marching_cubes(vol3, iso); v = o + (v / up - 1 + 0.5 / up) * h
    import trimesh
    tm = trimesh.Trimesh(v, fcs)
    if tm.volume < 0: tm.invert()               # marching cubes orientation depends on the axis order
    trimesh.smoothing.filter_taubin(tm, iterations=15); tm.export(os.path.join(out, 'optimized.stl'))
    try:                                            # exact CAD interfaces back in: final = (optimized - regions) + (current bone in regions) - motors
        import manifold3d as m3
        def man(tris):
            vv, inv = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
            return m3.Manifold(m3.Mesh(vert_properties=vv.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
        res = man(tm.triangles); regs = None; cur = man(bone_tris) if has_bone else None
        def cyl(ax, oth, c2, a0, a1, rad):
            c = m3.Manifold.cylinder(abs(a1 - a0), rad, rad, 48); c = c.rotate([0, 90, 0]) if ax == 0 else c.rotate([-90, 0, 0]) if ax == 1 else c
            t = [0, 0, 0]; t[ax] = min(a0, a1); t[oth[0]], t[oth[1]] = c2[0], c2[1]; return c.translate(t)
        for it in cfg['interfaces']:
            if it['type'] == 'pads': continue
            if it['type'] == 'slab':
                lo, hi = env[:, 0].copy() - 5, env[:, 1].copy() + 5; ax = 'xyz'.index(it['axis']); lo[ax], hi[ax] = it['range']
            else:
                t = M(it['mesh']).reshape(-1, 3); lo, hi = t.min(0) - it['dist_mm'], t.max(0) + it['dist_mm']
            box = m3.Manifold.cube(list(hi - lo)).translate(list(lo)); regs = box if regs is None else regs + box
        fin = (res - regs) + (cur ^ regs) if regs is not None else res
        for ax, oth, hx, f0, sd, it in pad_geo:     # exact pads, holes and head channels
            fin = fin + cyl(ax, oth, hx, f0, f0 + sd * it['pad_t'], it['pad_d'] / 2)
        for it in cfg['interfaces']:                  # nothing may cross a mounting face: trim the smoothed surface on the motor side
            if it['type'] == 'pads' and it.get('ring'):
                ax = 'xyz'.index(it['axis']); oth = [i for i in range(3) if i != ax]
                fin = fin - cyl(ax, oth, it['ring'][:2], it['face'], it['face'] - it['side'] * 25, it['ring'][3] + 4)
        for ax, oth, hx, f0, sd, it in pad_geo:
            fin = fin - cyl(ax, oth, hx, f0 - sd * 1, f0 + sd * (it['pad_t'] + it['access_len']), it['hole_d'] / 2)
            fin = fin - cyl(ax, oth, hx, f0 + sd * (it['pad_t'] - it.get('head_depth', 0)), f0 + sd * (it['pad_t'] + it['access_len']), it['head_d'] / 2)
        for f in cfg.get('keepout_static', []): fin = fin - man(M(f))
        me = fin.to_mesh(); tri = np.asarray(me.vert_properties)[:, :3][np.asarray(me.tri_verts)]; save_stl(os.path.join(out, 'final.stl'), tri)
        rep['final_volume_cm3'] = float(fin.volume() / 1000)
    except Exception as e:
        rep['final_mesh_error'] = repr(e); print(' exact interface union failed:', e)
    json.dump(rep, open(os.path.join(out, 'report.json'), 'w'), indent=1); print(' done', out, f'{time.time() - t0:.0f}s')

if __name__ == '__main__':
    main()
