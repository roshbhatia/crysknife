import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from shapely import affinity
from shapely.ops import unary_union
from shapely.geometry import Polygon, box, Point

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
parameters = {name: float(value) for name, value in re.findall(
    r'^(\w+) = (-?[\d.]+);$', (ROOT/'case/parameters.scad').read_text(), re.M)}
under_pcb_clearance = parameters['standoff_height'] + parameters['standoff_shim']
assert under_pcb_clearance >= 13.9 + parameters["damping_thickness"]
assert abs(parameters["plate_to_pcb_gap"]-parameters["upper_spacer_height"]-parameters["upper_spacer_shim"]) < 1e-6
thread_engagement = {}
for name, stack in (("top", parameters["plate_thickness"]+parameters["screw_head_washer"]+parameters["plate_to_pcb_gap"]+parameters["pcb_thickness"]+parameters["standoff_shim"]),
                    ("bottom", parameters["bottom_thickness"]+parameters["screw_head_washer"])):
    engagement = parameters[f"{name}_screw_length"]-stack
    thread_engagement[name] = engagement
    assert 2 <= engagement <= parameters["standoff_thread_depth"]-0.5, (name, "Unsafe screw engagement", engagement)
hardware_radius = max(parameters["standoff_diameter"], parameters["washer_diameter"])/2
expansion = parameters['outline_expansion']
for side in ("left", "right"):
    board = parse((ROOT / f"build/pcb/crysknife_{side}.kicad_pcb").read_text())
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
    outer_cutout_margins = {}
    outer_bottom_cutouts = {}
    for ref in ('S1', 'S4'):
        x, y = components[ref]
        cutout = box(x-parameters['switch_cutout']/2, y-parameters['switch_cutout']/2,
                     x+parameters['switch_cutout']/2, y+parameters['switch_cutout']/2)
        assert shape.covers(cutout), f'{ref}: outer bottom cutout crosses PCB edge'
        margin = shape.boundary.distance(cutout)
        assert margin >= 4, f'{ref}: outer bottom PCB margin is below 4 mm'
        outer_cutout_margins[ref] = margin
        outer_bottom_cutouts[ref] = cutout
    cutouts = [affinity.translate(affinity.rotate(box(-parameters["switch_cutout"]/2, -parameters["switch_cutout"]/2, parameters["switch_cutout"]/2, parameters["switch_cutout"]/2), a), x, y) for x, y, a in keys]
    assert all(shape.buffer(expansion, join_style='mitre').covers(cutout) for cutout in cutouts), "Switch cutout crosses plate boundary"
    assert all(a.distance(b) >= 1 for i, a in enumerate(cutouts) for b in cutouts[i+1:]), "Insufficient switch plate web"
    cx, cy = components["MCU1"]
    electronics = box(cx-parameters["controller_width"]/2, cy-parameters["controller_length"]/2,
                      cx+parameters["controller_width"]/2, cy+parameters["controller_length"]/2)
    bolts = [Point(components[f"MH{n}"]) for n in range(1,5)]
    mounts = [hole for hole in data["holes"] if hole["ref"].startswith("MH")]
    assert len(mounts) == len(bolts) == 4
    mount_diameter = mounts[0]["diameter"]
    assert all(hole["diameter"] == mount_diameter for hole in mounts)
    assert abs(mount_diameter-parameters["bolt_diameter"]) < 1e-6, "PCB and plates must use matching M2 screw holes"
    plate_material = shape.buffer(expansion, join_style="mitre").difference(unary_union(cutouts))
    bolt_margin = parameters["bolt_diameter"]/2 + 1.5*parameters["plate_thickness"]
    for p in bolts:
        assert shape.covers(p.buffer(hardware_radius+0.5)), "Mounting hole crosses PCB edge"
        assert plate_material.covers(p.buffer(bolt_margin)), "Insufficient material around plate screw"
    keycaps = [affinity.translate(affinity.rotate(box(-9,-9,9,9), a), x,y) for x,y,a in keys]
    minimum_keycap_gap = min(a.distance(b) for i,a in enumerate(keycaps) for b in keycaps[i+1:])
    assert minimum_keycap_gap >= 0.5, "Adjacent keycaps overlap or leave insufficient clearance"
    desired_battery_center = [(components["S8"][i]+components["S11"][i])/2 for i in (0, 1)]
    rf_exclusion = box(cx-14, cy-23, cx+14, cy+23)
    battery_candidates = []
    for dx in range(-20, 21):
        for dy in range(-15, 16):
            bx, by = desired_battery_center[0]+dx, desired_battery_center[1]+dy
            envelope = box(bx-32, by-20, bx+32, by+20)
            if (shape.buffer(-2).covers(envelope) and envelope.distance(rf_exclusion) >= 10
                    and all(envelope.distance(p) >= hardware_radius+0.5 for p in bolts)):
                battery_candidates.append((dx*dx+dy*dy, bx, by))
    assert battery_candidates, "No protected large-battery envelope fits clear of RF"
    _, bx, by = min(battery_candidates)
    battery_center = [bx, by]
    battery_envelope = box(bx-32, by-20, bx+32, by+20)
    assert under_pcb_clearance-parameters["damping_thickness"]-0.5-8.5-0.5 >= 4.4, "Battery collides with underside component reservation"
    values = [outline, keys, [[p.x, p.y] for p in bolts], components["MCU1"],
              components["RST1"], components["PWR1"], list(shape.bounds), battery_center, mount_diameter]
    geometries.append(f"{side}_geometry = {json.dumps(values)};")
    physical_checks[side] = (cutouts, bolts, electronics, outer_bottom_cutouts)
    reports.append({"side": side, "keys": len(keys), "pcb_area_mm2": shape.area,
                    "outer_bottom_pcb_clearance_mm": outer_cutout_margins,
                    "minimum_plate_web_mm": min(a.distance(b) for i, a in enumerate(cutouts) for b in cutouts[i+1:]),
                    "bolts": values[2], "standoff_count": 4, "pcb_mount_hole_mm": mount_diameter,
                    "minimum_keycap_gap_mm": minimum_keycap_gap, "controls": "accessible through open plate sides",
                    "switch": "Outemu Medium-Low Black; standard MX socket footprint",
                    "pcb_to_plate_gap_mm": parameters["plate_to_pcb_gap"], "plate_thickness_mm": parameters["plate_thickness"],
                    "under_pcb_clearance_mm": under_pcb_clearance, "bottom_thickness_mm": parameters["bottom_thickness"],
                    "standoff_height_mm": parameters["standoff_height"], "standoff_shim_mm": parameters["standoff_shim"],
                    "upper_spacer_mm": parameters["upper_spacer_height"], "upper_spacer_shim_mm": parameters["upper_spacer_shim"],
                    "top_screw_mm": parameters["top_screw_length"], "bottom_screw_mm": parameters["bottom_screw_length"],
                    "nominal_thread_engagement_mm": thread_engagement,
                    "damping_thickness_mm": parameters["damping_thickness"], "bends": False,
                    "controller": {"mount": "face up beneath carrier", "covered_by_plate": True,
                                   "reserved_gap_mm": parameters["controller_gap"], "height_requires_samples": True},
                    "battery": {"sku": "Adafruit 2011", "capacity_mAh": 2000,
                                "nominal_mm": [60, 36, 7], "reserved_mm": [64, 40, 8.5],
                                "center_mm": battery_center, "rf_clearance_mm": battery_envelope.distance(rf_exclusion),
                                "underside_component_reservation_mm": 4.4, "foam_mm": 0.5,
                                "insulating_cover_and_air_mm": 0.5},
                    "status": "mechanical draft; switch height, battery, controller fit require physical verification"})
(OUTPUT / "geometry.scad").write_text("\n".join(geometries)+"\n")
(ROOT / "case/geometry.scad").write_text("\n".join(geometries)+"\n")


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
    cutouts, bolts, electronics, outer_bottom_cutouts = physical_checks[side]
    report = next(item for item in reports if item["side"] == side)
    report["exports"] = {}
    for part in ("bottom-flat", "plate", "damping"):
        for extension in ("dxf", "svg"):
            subprocess.run(["openscad", "-o", str(OUTPUT / f"{side}-{part}.{extension}"),
                            "-D", f'side="{side}"', "-D", f'part="{part}"',
                            str(ROOT / "case/sandwich.scad")], check=True, env=export_env)
        actual, contours = exported_shape(OUTPUT / f"{side}-{part}.svg")
        assert actual.geom_type == "Polygon", (side, part, "Disconnected case pieces")
        if part == "plate":
            assert all(actual.intersection(c.buffer(-0.01)).area < 0.0001 for c in cutouts), "Export blocks switch cutout"
        if part in ("bottom-flat", "plate", "damping"):
            assert all(actual.intersection(p.buffer(1.08)).area < 0.0001 for p in bolts), "Export blocks bolt hole"
        if part == "plate":
            assert actual.covers(electronics.buffer(-0.01)), "Top plate does not cover controller"
            outer_plate_margins = {}
            for ref, cutout in outer_bottom_cutouts.items():
                margin = actual.exterior.distance(cutout)
                assert margin >= 4 + expansion - 0.01, f'{ref}: exported outer bottom plate margin is too small'
                outer_plate_margins[ref] = margin
            report['outer_bottom_plate_clearance_mm'] = outer_plate_margins
        report["exports"][part] = {"area_mm2": actual.area, "closed_contours": contours}
    subprocess.run(["openscad", "-o", str(OUTPUT / f"{side}-assembly.csg"),
                    "-D", f'side="{side}"', str(ROOT / "case/sandwich.scad")], check=True, env=export_env)
    print(f"{side}: exported three flat case layers, 21 switch cutouts and four standoff holes")
(OUTPUT / "mechanical-checks.json").write_text(json.dumps(reports, indent=2)+"\n")

for extension in ('dxf', 'svg'):
    subprocess.run(['openscad', '-o', str(OUTPUT/f'switch-fit-coupon.{extension}'), '-D',
                    'part="switch-fit-coupon"', str(ROOT/'case/sandwich.scad')], check=True, env=export_env)

for side in ('left', 'right'):
    for part in ('assembly', 'bottom'):
        target = OUTPUT/f'{side}-{part}.3mf'
        subprocess.run(['openscad', '-o', str(target), '-D', f'side="{side}"', '-D',
                        f'part="{part}"', str(ROOT/'case/sandwich.scad')], check=True, env=export_env)
        assert target.stat().st_size > 1000, 'Missing 3D model'
