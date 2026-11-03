import sys, numpy as np, trimesh
m = trimesh.load(sys.argv[1])
print("watertight", m.is_watertight, "bounds", np.round(m.bounds, 2))
lo, hi = m.bounds
sec = m.section(plane_normal=[0, 1, 0], plane_origin=[0, (lo[1] + hi[1]) / 2, 0])
p2, T = sec.to_2D()
polys = p2.polygons_full
print("polys", len(polys))
P = polys[0]
# to_2D 좌표 → 원래 x,z 로 되돌리기 위해 3D 꼭짓점에서 직접 구멍 범위 계산
for poly in polys:
    print("area", round(poly.area), "holes", len(poly.interiors))
holes3d = []
for ring in P.interiors:
    pts = np.c_[np.array(ring.coords), np.zeros(len(ring.coords)), np.ones(len(ring.coords))] @ T.T
    holes3d.append((pts[:, 0].min(), pts[:, 0].max(), pts[:, 2].min(), pts[:, 2].max()))
for h in sorted(holes3d, key=lambda h: h[2]):
    print("hole x %.1f..%.1f  z %.1f..%.1f  d=%.1f" % (h[0], h[1], h[2], h[3], h[1] - h[0]))
# 길이 방향(z) 따라 폭
for z in np.arange(lo[2] + 5, hi[2], 10):
    s = m.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, z])
    if s is None: continue
    b = s.bounds
    print("z=%6.1f width x %.1f..%.1f (%.1f)" % (z, b[0][0], b[1][0], b[1][0] - b[0][0]))
