import sys, numpy as np, trimesh, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "AppleGothic"
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Polygon
a, b, out = trimesh.load(sys.argv[1]), trimesh.load(sys.argv[2]), sys.argv[3]
BL, OR = (0.25, 0.5, 0.85), (0.95, 0.55, 0.2)
fig = plt.figure(figsize=(18, 11), facecolor="white")

def top(ax, p, col, title):
    s = p.section(plane_normal=[0, 1, 0], plane_origin=[0, 1.0, 0]).to_planar(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]))[0]
    for poly in s.polygons_full:
        ax.add_patch(Polygon(np.array(poly.exterior.coords), fc=col, ec="k", lw=1))
        for r in poly.interiors: ax.add_patch(Polygon(np.array(r.coords), fc="white", ec="k", lw=.8))
    lo, hi = p.bounds
    ax.set_xlim(lo[0]-5, hi[0]+5); ax.set_ylim(lo[2]-5, hi[2]+5); ax.set_aspect("equal")
    ax.set_title(f"{title}\n{hi[0]-lo[0]:.0f} × {hi[2]-lo[2]:.0f} mm", fontsize=14); ax.set_xlabel("mm"); ax.grid(alpha=.3)

top(fig.add_subplot(2, 3, 1), a, BL, "A (앞쪽 조각) — 위에서 본 모습")
top(fig.add_subplot(2, 3, 2), b, OR, "B (뒤쪽 조각) — 위에서 본 모습")

ax = fig.add_subplot(2, 3, 3)  # 이음부 옆 단면 (x=72, 판 중앙)
for p, col in ((a, BL), (b, OR)):
    s = p.section(plane_normal=[1, 0, 0], plane_origin=[72.5, 0, 0])
    pl, T = s.to_2D()
    for poly in pl.polygons_full:
        pts = np.c_[np.array(poly.exterior.coords), np.zeros(len(poly.exterior.coords)), np.ones(len(poly.exterior.coords))] @ T.T
        ax.add_patch(Polygon(pts[:, [2, 1]], fc=col, ec="k", lw=1))
ax.set_xlim(125, 175); ax.set_ylim(-6, 12); ax.set_aspect("equal"); ax.grid(alpha=.3)
ax.set_title("이음부 확대 (옆 단면)\n20 mm 겹침, 각 2.75 mm 두께 + M3 볼트", fontsize=14); ax.set_xlabel("길이 방향 mm")

ax = fig.add_subplot(2, 1, 2, projection="3d")
c = (a.bounds[0] + b.bounds[1]) / 2
for p, col in ((a, BL), (b, OR)):
    t = p.triangles[:, :, [0, 2, 1]] - c[[0, 2, 1]]
    n = p.face_normals[:, [0, 2, 1]]; sh = .35 + .65 * np.abs(n @ [.3, .4, .85])
    ax.add_collection3d(Poly3DCollection(t, facecolors=np.c_[sh*col[0], sh*col[1], sh*col[2]], edgecolors="none"))
r = 140; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r/4, r/4); ax.set_box_aspect((1, 1, .25))
ax.view_init(35, -60); ax.set_axis_off(); ax.set_title("조립 상태 (파랑 A + 주황 B)", fontsize=14)
plt.tight_layout(); plt.savefig(out, dpi=110)
