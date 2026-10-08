import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from shapely import affinity
from shapely.geometry import Polygon, box

from generate_tscircuit import descriptor
from kicad_sexp import child, children, parse


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build/case"
OUTPUT.mkdir(parents=True, exist_ok=True)
export_env = os.environ.copy()
if sys.platform.startswith("linux"):
    export_env["QT_QPA_PLATFORM"] = "offscreen"
geometries = []
reports = []
physical_checks = {}
for side in ("left", "right"):
    board = parse((ROOT / f"build/pcb/fridakeeb_{side}.kicad_pcb").read_text())
    data = descriptor(side)
    outline = [[p["x"], p["y"]] for p in data["outline"]]
    shape = Polygon(outline)
    assert shape.is_valid and shape.area > 1000
    components = {}
    keys = []
    for footprint in children(board, "footprint"):
        ref = next(p[2] for p in children(footprint, "property") if p[1] == "Reference")
        at = child(footprint, "at")
        x, y = float(at[1])-data["origin"][0], data["origin"][1]-float(at[2])
        components[ref] = [x, y]
        if ref.startswith("S") and ref[1:].isdigit():
            keys.append([x, y, float(at[3]) if len(at) > 3 else 0])
    assert len(keys) == 21
    cutouts = [affinity.translate(affinity.rotate(box(-7, -7, 7, 7), a), x, y) for x, y, a in keys]
    assert all(shape.buffer(2.5).covers(cutout) for cutout in cutouts), "Switch cutout crosses plate boundary"
    assert all(a.distance(b) >= 1 for i, a in enumerate(cutouts) for b in cutouts[i+1:]), "Insufficient switch plate web"
    cx, cy = components["MCU1"]
    electronics = box(cx-10, cy-21, cx+10, cy+21)
    assert all(electronics.distance(cutout) >= 1 for cutout in cutouts), "Controller opening clips a switch"
    x0, y0, x1, y1 = shape.bounds
    rx, ry = components["RST1"]
    px, py = components["PWR1"]
    openings = box(cx-10 if side == "left" else x0-10, py-4,
                   x1+10 if side == "left" else cx+10, y1+10)
    wall = shape.buffer(9).difference(shape.buffer(0.8)).difference(openings)
    assert wall.is_valid and wall.geom_type == "Polygon", "Side apertures split the spacer ring"
    bolt_region = shape.buffer(8).difference(shape.buffer(3.5)).difference(openings.buffer(3))
    candidates = []
    boundary = shape.buffer(5.8).exterior
    for index in range(180):
        p = boundary.interpolate(boundary.length*index/180)
        if bolt_region.covers(p.buffer(2)):
            candidates.append(p)
    assert len(candidates) >= 6
    bolts = [min(candidates, key=lambda p: p.x)]
    while len(bolts) < 6:
        p = max(candidates, key=lambda p: min(p.distance(existing) for existing in bolts))
        assert all(p.distance(existing) >= 15 for existing in bolts)
        bolts.append(p)
    for p in bolts:
        assert p.distance(shape) >= 4.6
        assert wall.covers(p.buffer(2)), "Standoff crosses side aperture"
    values = [outline, keys, [[p.x, p.y] for p in bolts], components["MCU1"],
              components["RST1"], components["PWR1"], list(shape.bounds)]
    geometries.append(f"{side}_geometry = {json.dumps(values)};")
    physical_checks[side] = (cutouts, bolts, openings)
    reports.append({"side": side, "keys": len(keys), "pcb_area_mm2": shape.area,
                    "minimum_plate_web_mm": min(a.distance(b) for i, a in enumerate(cutouts) for b in cutouts[i+1:]),
                    "bolts": values[2], "side_apertures": ["USB", "RST", "PWR"],
                    "switch": "Outemu Medium-Low Black; standard MX socket footprint",
                    "pcb_to_plate_gap_mm": 3.5, "plate_thickness_mm": 1.5,
                    "under_pcb_clearance_mm": 4.9, "bottom_thickness_mm": 3,
                    "spacer_stack_mm": [3, 3, 3], "lower_gasket_compressed_mm": 1,
                    "upper_gasket_compressed_mm": 0.5, "bezel_thickness_mm": 3,
                    "status": "mechanical draft; switch height, battery, controller and TrackPoint fit require physical verification"})
(OUTPUT / "geometry.scad").write_text("\n".join(geometries)+"\n")


def exported_shape(path):
    svg = ET.parse(path).getroot()
    assert svg.attrib["width"].endswith("mm") and svg.attrib["height"].endswith("mm")
    polygons = []
    for element in svg.iter():
        if not element.tag.endswith("}path"):
            continue
        data = element.attrib["d"]
        assert set(re.findall(r"[A-Za-z]", data)) <= {"M", "L", "z"}, "Unsupported case contour command"
        for contour in data.split("z")[:-1]:
            values = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", contour)]
            assert len(values) >= 6 and len(values) % 2 == 0
            polygon = Polygon([(values[i], -values[i+1]) for i in range(0, len(values), 2)])
            assert polygon.is_valid and polygon.area > 0
            polygons.append(polygon)
    assert polygons, "Case export has no closed contours"
    shape = polygons[0]
    for polygon in polygons[1:]:
        shape = shape.symmetric_difference(polygon)
    assert shape.is_valid
    return shape, len(polygons)


for side in ("left", "right"):
    cutouts, bolts, openings = physical_checks[side]
    report = next(item for item in reports if item["side"] == side)
    report["exports"] = {}
    for part in ("bottom", "spacer", "plate", "gasket", "bezel"):
        for extension in ("dxf", "svg"):
            subprocess.run(["openscad", "-o", str(OUTPUT / f"{side}-{part}.{extension}"),
                            "-D", f'side="{side}"', "-D", f'part="{part}"',
                            str(ROOT / "case/sandwich.scad")], check=True, env=export_env)
        actual, contours = exported_shape(OUTPUT / f"{side}-{part}.svg")
        assert actual.geom_type == "Polygon", (side, part, "Disconnected case pieces")
        if part in ("plate", "bezel"):
            assert all(actual.intersection(c.buffer(-0.01)).area < 0.0001 for c in cutouts), "Export blocks switch cutout"
        if part in ("bottom", "spacer", "bezel"):
            assert all(actual.intersection(p.buffer(1.08)).area < 0.0001 for p in bolts), "Export blocks bolt hole"
        if part in ("plate", "spacer", "bezel", "gasket"):
            assert actual.intersection(openings.buffer(-0.01)).area < 0.0001, "Export blocks side access"
        report["exports"][part] = {"area_mm2": actual.area, "closed_contours": contours}
    subprocess.run(["openscad", "-o", str(OUTPUT / f"{side}-assembly.csg"),
                    "-D", f'side="{side}"', str(ROOT / "case/sandwich.scad")], check=True, env=export_env)
    print(f"{side}: exported five sandwich layers with 21 MX cutouts and six external standoffs")
(OUTPUT / "mechanical-checks.json").write_text(json.dumps(reports, indent=2)+"\n")
