"""판을 길이 방향(z)으로 하프랩(계단식 겹침) 분할 + M3 볼트 구멍."""
import sys, numpy as np, trimesh
src, out_a, out_b, out_png = sys.argv[1:5]
ZC, LAP, CLR, HOLE_D = 150.0, 20.0, 0.2, 3.4      # 분할 중심, 겹침 길이, 틈새, M3 여유 구멍
BOLTS = [(40, 145), (105, 145), (40, 155), (105, 155)]  # (x, z) mm
m = trimesh.load(src)
(x0, y0, z0), (x1, y1, z1) = m.bounds
ym = (y0 + y1) / 2

def box(xa, xb, ya, yb, za, zb):
    b = trimesh.creation.box(extents=[xb - xa, yb - ya, zb - za])
    b.apply_translation([(xa + xb) / 2, (ya + yb) / 2, (za + zb) / 2])
    return b

E = 5  # 여유
z1a, z1b = ZC - LAP / 2, ZC + LAP / 2
keep_a = trimesh.boolean.union([box(x0-E, x1+E, y0-E, y1+E, z0-E, z1a),           # 앞쪽 전체 두께
                                box(x0-E, x1+E, y0-E, ym, z1a - 1, z1b - CLR)])    # 겹침부 아래 절반
keep_b = trimesh.boolean.union([box(x0-E, x1+E, y0-E, y1+E, z1b, z1+E),           # 뒤쪽 전체 두께
                                box(x0-E, x1+E, ym, y1+E, z1a + CLR, z1b + 1)])    # 겹침부 위 절반
holes = trimesh.boolean.union([trimesh.creation.cylinder(radius=HOLE_D / 2, height=40, sections=48,
                               transform=trimesh.transformations.translation_matrix([x, ym, z]) @
                               trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])) for x, z in BOLTS])
A = trimesh.boolean.difference([trimesh.boolean.intersection([m, keep_a]), holes])
B = trimesh.boolean.difference([trimesh.boolean.intersection([m, keep_b]), holes])
for name, p, f in (("A(앞)", A, out_a), ("B(뒤)", B, out_b)):
    p.export(f)
    s = p.bounds[1] - p.bounds[0]
    print(f"{name}: {s[0]:.1f} x {s[2]:.1f} mm (두께 {s[1]:.1f}), watertight={p.is_watertight}, 부피 {p.volume/1000:.1f} cm³ → {f}")
print(f"원본 부피 {m.volume/1000:.1f} cm³, 합 {(A.volume+B.volume)/1000:.1f} cm³ (볼트구멍·틈새만큼 작음)")

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(16, 8), facecolor="white")
c = (m.bounds[0] + m.bounds[1]) / 2
for k, (title, off) in enumerate((("분해 (Exploded)", 30.0), ("조립 (Assembled)", 0.0))):
    ax = fig.add_subplot(1, 2, k + 1, projection="3d")
    for p, col, dz in ((A, (0.25, 0.5, 0.85), -off / 2), (B, (0.95, 0.55, 0.2), off / 2)):
        t = p.triangles[:, :, [0, 2, 1]] - c[[0, 2, 1]] + [0, dz, 0]
        n = p.face_normals[:, [0, 2, 1]]; sh = 0.35 + 0.65 * np.abs(n @ [0.3, 0.4, 0.85])
        ax.add_collection3d(Poly3DCollection(t, facecolors=np.c_[sh * col[0], sh * col[1], sh * col[2]], edgecolors="none"))
    r = 160; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1))
    ax.view_init(30, -60); ax.set_axis_off(); ax.set_title(title, fontsize=15)
plt.rcParams["font.family"] = "AppleGothic"
plt.tight_layout(); plt.savefig(out_png, dpi=120)
