"""상판에 케이블 통과용 네모 창(모서리 둥근 직사각형)을 뚫는다. 창 좌표는 원본 STL 좌표 (x: 폭, z: 길이, mm).

    python3 tools/add_windows.py original.stl out.stl
기존 구멍과의 거리, 판 가장자리 레일 폭을 검사해서 출력한다.
"""
import sys, numpy as np, trimesh
from shapely.geometry import box as sbox, Point

src, dst = sys.argv[1:3]
# (x0, x1, z0, z1): 기존 구멍·볼트 이음부(z 140~160)를 피한 자리
WINDOWS = [(45, 100, 100, 126),   # 앞판, 폭 145 mm 구간
           (42, 103, 168, 186),   # 뒷판, 폭 109 mm 구간 (이음부 뒤)
           (50, 95, 223, 236)]    # 뒷판, 뒤쪽 구멍 사이
R = 4.0                            # 모서리 반경

m = trimesh.load(src)
lo, hi = m.bounds
sec = m.section(plane_normal=[0, 1, 0], plane_origin=[0, (lo[1] + hi[1]) / 2, 0])
p2, T = sec.to_2D()
poly = p2.polygons_full[0]
def to3(c):
    c = np.asarray(c); return (np.c_[c, np.zeros(len(c)), np.ones(len(c))] @ T.T)[:, [0, 2]]
outline = __import__("shapely.geometry", fromlist=["Polygon"]).Polygon(to3(poly.exterior.coords))
holes = [__import__("shapely.geometry", fromlist=["Polygon"]).Polygon(to3(r.coords)) for r in poly.interiors]

cutters = []
for x0, x1, z0, z1 in WINDOWS:
    w = sbox(x0 + R, z0 + R, x1 - R, z1 - R).buffer(R, quad_segs=8)
    dh = min(w.distance(h) for h in holes)
    rail = outline.exterior.distance(w)
    assert outline.contains(w), "창이 판 밖으로 나감"
    print(f"창 x{x0}-{x1} z{z0}-{z1} ({x1-x0}×{z1-z0} mm): 가장 가까운 구멍까지 {dh:.1f} mm, 판 가장자리까지 {rail:.1f} mm")
    pts = np.array(w.exterior.coords)[:-1]
    prism = trimesh.creation.extrude_polygon(__import__("shapely.geometry", fromlist=["Polygon"]).Polygon(pts), height=hi[1] - lo[1] + 4)
    # extrude 는 (x,y) 평면을 z 방향으로 → (x, z_plate) 평면을 y 방향으로 돌림
    prism.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
    prism.vertices[:, 2] *= -1; prism.invert() if prism.volume < 0 else None
    prism.apply_translation([0, lo[1] - 2 - prism.bounds[0][1], 0])
    cutters.append(prism)

out = trimesh.boolean.difference([m] + cutters)
print(f"부피 {m.volume/1000:.1f} → {out.volume/1000:.1f} cm³ ({(1-out.volume/m.volume)*100:.0f}% 감소), watertight={out.is_watertight}")
out.export(dst)
