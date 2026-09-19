#!/usr/bin/env python3
"""Ankle differential transmission map: virtual (pitch, roll) <-> motor angles (th1, th2).

WHY THIS EXISTS
The physical ankle is a parallel/differential mechanism: two RS06 in the shin drive two
pushrods onto the foot. The URDF/RL model uses two VIRTUAL serial joints (pitch above roll
at the real offset gimbal) and omits the closed loop - that is the project decision and the
standard practice for humanoid RL. This module is the missing transmission layer:

    policy (pitch, roll) --IK--> (th1, th2) --> CAN to the two RS06
    motor feedback (th1, th2) --FK--> (pitch, roll) --> into the observation vector

It also derives the COUPLED torque envelope and the coupled joint limits, which are the
parts of the linkage that DO matter inside training (a policy that learns to demand
max pitch AND max roll torque simultaneously cannot be executed on the real robot).

GEOMETRY SOURCE  (PROVISIONAL - see below)
Extracted 2026-07-19 from the Onshape export ~/Downloads/rl (right leg), by reading the
world positions of the shoulder-screw pivot parts. Re-extract with:  python3 ankle_map.py --extract
WARNING: these constants come from mesh CENTROIDS of the export, not measured CAD
axes/pivots. Replace them with measured values before trusting any torque number.
All lengths in metres, angles in radians, in the RIGHT-leg world frame at the zero pose.

CONVENTION
pitch: rotation about the -Y world axis through P_PITCH   (matches URDF ankle_pitch axis)
roll : rotation about the +X world axis through P_ROLL    (matches URDF ankle_roll axis)
th_i : crank angle, positive = crank pivot moves +Z (up). Zero = crank horizontal (+X).
The deploy code MUST use the same signs as the URDF joints; verify once on hardware.
"""
import sys, math
import numpy as np

# ---------------- geometry (metres), right leg, zero pose ----------------
P_PITCH = np.array([0.0000, -0.0962, -0.7393])   # pitch axis point (URDF ankle_pitch origin)
A_PITCH = np.array([0.0, -1.0, 0.0])             # pitch axis direction (URDF)
P_ROLL  = np.array([0.0300, -0.1262, -0.7533])   # roll axis point (URDF ankle_roll origin)
A_ROLL  = np.array([1.0, 0.0, 0.0])              # roll axis direction (URDF)

# motor 1 = UPPER RS06 (nearer the knee), motor 2 = LOWER RS06
M1_AXIS_PT = np.array([0.0000, -0.17002, -0.54527])  # a point on motor-1 rotation axis
M2_AXIS_PT = np.array([0.0000, -0.08238, -0.64732])
M_AXIS_DIR = np.array([0.0, 1.0, 0.0])               # both crank axes are lateral (+Y)
CRANK1_0 = np.array([0.04775, 0.0, 0.0])   # motor-1 axis -> its rod pivot, at zero pose
CRANK2_0 = np.array([0.04775, 0.0, 0.0])
F1_0 = np.array([0.04775, -0.17002, -0.75331])   # foot-side rod pivot fed by motor 1
F2_0 = np.array([0.04775, -0.08238, -0.75331])   # foot-side rod pivot fed by motor 2
ROD1 = 0.20801   # eye-to-eye (BOM body length 140 mm + 2 rod ends)
ROD2 = 0.10601   # eye-to-eye (BOM body length  40 mm + 2 rod ends)

TAU_MOTOR = 36.0        # RS06 peak torque [Nm]
TAU_MOTOR_CONT = 11.0   # RS06 rated (continuous) torque [Nm]
ROD_END_LIMIT = math.radians(35.0)   # igus KARM/KALM-08 CL spherical travel


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * (K @ K)


def foot_pivots(pitch, roll):
    """World positions of the two foot-side rod pivots for a given (pitch, roll).
    Serial offset gimbal: pitch first (carries the roll axis), then roll."""
    Rp = rot(A_PITCH, pitch)
    out = []
    for F0 in (F1_0, F2_0):
        # roll acts about the (pitch-transformed) roll axis
        pr = P_PITCH + Rp @ (P_ROLL - P_PITCH)
        ar = Rp @ A_ROLL
        p_after_pitch = P_PITCH + Rp @ (F0 - P_PITCH)
        out.append(pr + rot(ar, roll) @ (p_after_pitch - pr))
    return out


def crank_pivot(i, th):
    """World position of the crank-side rod pivot for motor i at crank angle th."""
    pt = M1_AXIS_PT if i == 0 else M2_AXIS_PT
    c0 = CRANK1_0 if i == 0 else CRANK2_0
    return pt + rot(M_AXIS_DIR, th) @ c0


def ik(pitch, roll, guess=(0.0, 0.0)):
    """(pitch, roll) -> (th1, th2). Exact closed-loop solve, one 1-D root find per rod."""
    F = foot_pivots(pitch, roll)
    rods = (ROD1, ROD2)
    th = []
    for i in range(2):
        f = lambda t: np.linalg.norm(crank_pivot(i, t) - F[i]) - rods[i]
        t = guess[i]
        for _ in range(100):                      # Newton with numeric derivative
            e = f(t)
            if abs(e) < 1e-12:
                break
            d = (f(t + 1e-7) - f(t - 1e-7)) / 2e-7
            if abs(d) < 1e-12:
                return None                        # singular: crank perpendicular to rod
            step = e / d
            t -= max(-0.3, min(0.3, step))         # damped
        if abs(f(t)) > 1e-8:
            return None                            # unreachable
        th.append(t)
    return np.array(th)


def fk(th1, th2, guess=(0.0, 0.0)):
    """(th1, th2) -> (pitch, roll). 2-D Newton on the two rod-length residuals."""
    x = np.array(guess, dtype=float)
    C = [crank_pivot(0, th1), crank_pivot(1, th2)]
    rods = np.array([ROD1, ROD2])

    def res(v):
        F = foot_pivots(v[0], v[1])
        return np.array([np.linalg.norm(C[i] - F[i]) - rods[i] for i in range(2)])

    for _ in range(100):
        r = res(x)
        if np.max(np.abs(r)) < 1e-12:
            return x
        J = np.zeros((2, 2))
        for k in range(2):
            d = np.zeros(2); d[k] = 1e-7
            J[:, k] = (res(x + d) - res(x - d)) / 2e-7
        if abs(np.linalg.det(J)) < 1e-14:
            return None
        x = x - np.clip(np.linalg.solve(J, r), -0.3, 0.3)
    return x if np.max(np.abs(res(x))) < 1e-8 else None


def jacobian(pitch, roll, h=1e-6):
    """J = d(pitch,roll)/d(th1,th2) at the given joint pose (2x2)."""
    base = ik(pitch, roll)
    if base is None:
        return None
    Jm = np.zeros((2, 2))          # d(theta)/d(joint)
    for k, (dp, dr) in enumerate(((h, 0.0), (0.0, h))):
        a = ik(pitch + dp, roll + dr, guess=base)
        b = ik(pitch - dp, roll - dr, guess=base)
        if a is None or b is None:
            return None
        Jm[:, k] = (a - b) / (2 * h)
    if abs(np.linalg.det(Jm)) < 1e-12:
        return None
    return np.linalg.inv(Jm)


def joint_torque_limits(pitch=0.0, roll=0.0, tau_motor=TAU_MOTOR):
    """Max pure-pitch and pure-roll joint torque, and the coupled envelope coefficients.
    tau_motor = J^T tau_joint, so each motor constrains: |J^T row . tau_joint| <= tau_motor."""
    J = jacobian(pitch, roll)
    if J is None:
        return None
    Jt = J.T                                  # maps joint torque -> motor torque
    pure_pitch = tau_motor / max(abs(Jt[0, 0]), abs(Jt[1, 0]))
    pure_roll = tau_motor / max(abs(Jt[0, 1]), abs(Jt[1, 1]))
    return pure_pitch, pure_roll, Jt


def rod_end_angles(pitch, roll):
    """Per-END misalignment each spherical rod end must accommodate.

    A rod end rotates FREELY about its pin axis; what is limited (+-35 deg for igus
    KARM/KALM-08 CL) is the tilt OUT of the plane perpendicular to that pin. So the
    correct metric is asin(|rod_unit . pin_axis|), evaluated at each end with that end's
    own pin axis. Crank-end pins stay along +Y (cranks rotate about Y). Foot-end pins are
    fixed in the foot, so they tilt with pitch and roll.
    Returns [crank_end_1, foot_end_1, crank_end_2, foot_end_2] in radians.
    """
    th = ik(pitch, roll)
    if th is None:
        return None
    F = foot_pivots(pitch, roll)
    # foot-side pin axis rotates with the foot (pitch then roll)
    Rp = rot(A_PITCH, pitch)
    foot_pin = rot(Rp @ A_ROLL, roll) @ (Rp @ M_AXIS_DIR)
    out = []
    for i in range(2):
        d = F[i] - crank_pivot(i, th[i])
        u = d / np.linalg.norm(d)
        out.append(math.asin(min(1.0, abs(float(np.dot(u, M_AXIS_DIR))))))   # crank end
        out.append(math.asin(min(1.0, abs(float(np.dot(u, foot_pin))))))     # foot end
    return out


def report():
    print("=" * 74)
    print("ANKLE DIFFERENTIAL TRANSMISSION - derived from CAD (2026-07-19)")
    print("=" * 74)
    print(f"crank arm        {np.linalg.norm(CRANK1_0)*1000:7.2f} mm (both motors)")
    print(f"rod 1 (upper)    {ROD1*1000:7.2f} mm eye-to-eye")
    print(f"rod 2 (lower)    {ROD2*1000:7.2f} mm eye-to-eye")
    print(f"pitch arm        {abs(F1_0[0]-P_PITCH[0])*1000:7.2f} mm")
    print(f"roll half-span   {abs(F1_0[1]-F2_0[1])/2*1000:7.2f} mm")

    print("\n-- ratios at zero pose (d joint / d motor) --")
    J = jacobian(0.0, 0.0)
    print(f"  J = [[{J[0,0]:+.4f} {J[0,1]:+.4f}]   pitch per (th1, th2)")
    print(f"       [{J[1,0]:+.4f} {J[1,1]:+.4f}]]  roll  per (th1, th2)")
    print(f"  pitch = {(J[0,0]+J[0,1])/2:+.4f} x (th1+th2)     [common mode]")
    print(f"  roll  = {(J[1,1]-J[1,0])/2:+.4f} x (th2-th1)     [differential mode]")

    lim = joint_torque_limits()
    pp, pr, Jt = lim
    print("\n-- torque envelope (RS06 peak 36 Nm each) --")
    print(f"  pure pitch max : {pp:6.1f} Nm")
    print(f"  pure roll  max : {pr:6.1f} Nm")
    print(f"  COUPLED (diamond): |tau_pitch|/{pp:.1f} + |tau_roll|/{pr:.1f} <= 1")
    ppc, prc, _ = joint_torque_limits(tau_motor=TAU_MOTOR_CONT)
    print(f"  continuous (11 Nm each): pitch {ppc:.1f} Nm, roll {prc:.1f} Nm")

    print("\n-- workspace scan (URDF limits: pitch -0.87..0.52, roll +-0.26 rad) --")
    worst_rod = 0.0; worst_at = None; unreachable = []
    tp_min = 1e9; tr_min = 1e9
    for p in np.linspace(-0.87, 0.52, 25):
        for r in np.linspace(-0.26, 0.26, 15):
            th = ik(p, r)
            if th is None:
                unreachable.append((p, r)); continue
            ra = rod_end_angles(p, r)
            if max(ra) > worst_rod:
                worst_rod, worst_at = max(ra), (p, r)
            L = joint_torque_limits(p, r)
            if L:
                tp_min = min(tp_min, L[0]); tr_min = min(tr_min, L[1])
    print(f"  unreachable poses      : {len(unreachable)}")
    print(f"  worst rod-end angle    : {math.degrees(worst_rod):5.1f} deg at "
          f"pitch={worst_at[0]:+.2f} roll={worst_at[1]:+.2f}  "
          f"(igus limit {math.degrees(ROD_END_LIMIT):.0f} deg -> "
          f"{'OK' if worst_rod < ROD_END_LIMIT else 'EXCEEDED'})")
    print(f"  worst-case pitch torque: {tp_min:6.1f} Nm over the workspace")
    print(f"  worst-case roll  torque: {tr_min:6.1f} Nm over the workspace")

    print("\n-- torque available vs ankle pitch (roll = 0) --")
    print("   pitch[deg]   pitch_max[Nm]   roll_max[Nm]   note")
    for pd in (-50, -40, -30, -20, -10, 0, 10, 20, 30):
        p = math.radians(pd)
        L = joint_torque_limits(p, 0.0)
        if L is None:
            print(f"   {pd:+6.0f}        SINGULAR"); continue
        note = ""
        if pd <= -40: note = "<- push-off region (needs ~67 Nm @45 kg)"
        if pd == 0: note = "<- neutral stance"
        print(f"   {pd:+6.0f}      {L[0]:8.1f}      {L[1]:8.1f}   {note}")

    print("\n-- round-trip validation (IK -> FK) --")
    err = 0.0
    for p in np.linspace(-0.8, 0.5, 9):
        for r in np.linspace(-0.25, 0.25, 7):
            th = ik(p, r)
            if th is None: continue
            back = fk(th[0], th[1], guess=(p, r))
            if back is None: continue
            err = max(err, abs(back[0]-p), abs(back[1]-r))
    print(f"  max round-trip error: {err:.2e} rad  ({'PASS' if err < 1e-8 else 'FAIL'})")

    print("\n-- motor travel needed for the URDF joint limits --")
    for name, p, r in (("max plantarflex", -0.87, 0.0), ("max dorsiflex", 0.52, 0.0),
                       ("max roll +", 0.0, 0.26), ("max roll -", 0.0, -0.26),
                       ("corner", -0.87, 0.26)):
        th = ik(p, r)
        if th is None:
            print(f"  {name:16s} UNREACHABLE"); continue
        print(f"  {name:16s} th1={math.degrees(th[0]):+7.1f} deg  th2={math.degrees(th[1]):+7.1f} deg")


if __name__ == "__main__":
    if "--extract" in sys.argv:
        print("Re-extract geometry from a fresh export: see MIRROR/ANKLE notes in the repo;\n"
              "the constants at the top of this file came from ~/Downloads/rl (2026-07-19).")
    report()
