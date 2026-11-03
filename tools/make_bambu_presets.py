"""Bambu Studio CLI용 X2D 프리셋(machine/process/filament JSON) 생성: 시스템 프리셋 상속을 풀고 강화 설정 적용.

    python3 tools/make_bambu_presets.py <출력폴더>
"""
import json, os, sys
P = "/Applications/BambuStudio.app/Contents/Resources/profiles/BBL"
def load(kind, name):
    d = json.load(open(f"{P}/{kind}/{name}.json"))
    if d.get("inherits"):
        base = load(kind, d["inherits"]); base.update(d); d = base
    return d
out = sys.argv[1]
m = load("machine", "Bambu Lab X2D 0.4 nozzle")
p = load("process", "0.20mm Standard @BBL X2D")
f = load("filament", "Bambu PETG-CF @BBL X2D 0.4 nozzle")
for d in (m, p, f): d.pop("inherits", None); d["from"] = "system"
for k in ("wall_loops", "top_shell_layers", "bottom_shell_layers", "sparse_infill_density", "sparse_infill_pattern", "brim_type"):
    print(k, "=", p.get(k))
p.update({"wall_loops": "4", "top_shell_layers": "5", "bottom_shell_layers": "5",
          "sparse_infill_density": "40%", "sparse_infill_pattern": "gyroid", "brim_type": "auto_brim",
          "curr_bed_type": "Textured PEI Plate"})
for n, d in (("machine", m), ("process", p), ("filament", f)):
    json.dump(d, open(f"{out}/{n}.json", "w"), indent=1)
print("machine", m.get("name"), "| bed", m.get("printable_area"), "| nozzle", m.get("nozzle_diameter"))
print("filament", f.get("name"), "| temp", f.get("nozzle_temperature"), "| compatible:", [x for x in f.get("compatible_printers", []) if "X2D" in x][:3])
