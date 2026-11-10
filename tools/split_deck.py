"""판을 길이 방향 하프랩(20 mm)으로 2분할 + 볼트 구멍 4개 + 출력 방향 STL.
축 자동 판별(가장 긴 축=길이, 가장 짧은 축=두께). 자를 위치는 기존 작은 구멍에서 가장 먼 곳을 자동 탐색.

    python3 tools/split_deck.py deck.stl out_dir [--max 246]
"""
import sys, os, argparse, numpy as np, trimesh
from shapely.geometry import Polygon, LineString, Point

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--max", type=float, default=246.0)
ap.add_argument("--lap", type=float, default=20.0); a = ap.parse_args()
LAP, CLR, HOLE_D = a.lap, 0.2, 3.4
m = trimesh.load(a.src); m.apply_scale(1000 if m.extents.max() < 5 else 1)
# 표준 좌표로 회전: x=길이, y=폭, z=두께
ax = np.argsort(m.extents)[::-1]; R = np.zeros((4, 4)); R[3, 3] = 1
for new, old in enumerate(ax): R[new, old] = 1
if np.linalg.det(R[:3, :3]) < 0: R[1] *= -1
m.apply_transform(R); m.apply_translation(-m.bounds[0])
Lx, Wy, Tz = m.extents
sec = m.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, Tz / 2]); p2, T = sec.to_2D()
to3 = lambda c: (np.c_[np.asarray(c), np.zeros(len(c)), np.ones(len(c))] @ T.T)[:, :2]
poly = max(p2.polygons_full, key=lambda p: p.area)
outline = Polygon(to3(poly.exterior.coords)); holes = [Polygon(to3(r.coords)) for r in poly.interiors]
small = [h for h in holes if h.area < 200]

best = None
for c in np.arange(LAP, Lx - LAP, 0.5):
    c1, c2 = c - LAP / 2, c + LAP / 2
    if c2 > a.max or Lx - c1 > a.max: continue
    d = min(LineString([(x, -1e3), (x, 1e3)]).distance(h) for x in (c1, c1 + CLR, c2 - CLR, c2) for h in small)
    if best is None or d > best[0]: best = (d, c)
d, c = best
print(f"자르는 중심 x={c:.1f} mm (이음 {c-LAP/2:.1f}~{c+LAP/2:.1f}), 자르는 선~구멍 최소 {d:.1f} mm")

ok = lambda x, w: outline.contains(Point(x, w).buffer(HOLE_D / 2 + 3)) and all(Point(x, w).buffer(HOLE_D / 2 + 3).distance(h) > 0 for h in holes)
ws = [w for w in np.arange(6, Wy - 6, 0.5) if ok(c - 5, w) and ok(c + 5, w)]
w1, w2 = min(ws, key=lambda w: abs(w - Wy * 0.25)), min(ws, key=lambda w: abs(w - Wy * 0.75))
bolts = [(c - 5, w1), (c + 5, w1), (c - 5, w2), (c + 5, w2)]
print("볼트(x, 폭) mm:", [(round(x, 1), round(w, 1)) for x, w in bolts])

def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b
E, zm = 5, Tz / 2
keep_a = trimesh.boolean.union([box(-E, c - LAP / 2, -E, Wy + E, -E, Tz + E), box(-E, c + LAP / 2 - CLR, -E, Wy + E, -E, zm)])
keep_b = trimesh.boolean.union([box(c + LAP / 2, Lx + E, -E, Wy + E, -E, Tz + E), box(c - LAP / 2 + CLR, Lx + E, -E, Wy + E, zm, Tz + E)])
cyl = trimesh.boolean.union([trimesh.creation.cylinder(radius=HOLE_D / 2, height=Tz + 10, sections=48, transform=trimesh.transformations.translation_matrix([x, w, zm])) for x, w in bolts])
A = trimesh.boolean.difference([trimesh.boolean.intersection([m, keep_a]), cyl])
B = trimesh.boolean.difference([trimesh.boolean.intersection([m, keep_b]), cyl])
os.makedirs(a.out, exist_ok=True)
for name, p, flip in (("A", A, False), ("B", B, True)):
    p.export(f"{a.out}/deck_{name}.stl")
    q = p.copy()
    if flip: q.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))  # 겹침부(위 절반)를 베드로
    q.apply_translation(-q.bounds[0])
    down = q.face_normals[:, 2] < -0.9; zc = q.triangles_center[down, 2]
    print(f"{name}: {q.extents[0]:.1f} x {q.extents[1]:.1f} x {q.extents[2]:.1f} mm, watertight={q.is_watertight}, 떠 있는 아랫면 {q.area_faces[down][zc > 1e-4].sum():.1f} mm²")
    q.export(f"{a.out}/print_deck_{name}.stl")
print(f"부피 원본 {m.volume/1000:.1f} cm³ / 합 {(A.volume + B.volume)/1000:.1f} cm³")
