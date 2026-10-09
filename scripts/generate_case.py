import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from shapely import affinity
from shapely.geometry import Polygon, box, LineString

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
under_pcb_clearance = parameters['standoff_height'] + parameters['standoff_shim'] - parameters['plate_to_pcb_gap'] - parameters['pcb_thickness']
assert under_pcb_clearance >= 13.9 + parameters["damping_thickness"]
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
    cutouts = [affinity.translate(affinity.rotate(box(-parameters["switch_cutout"]/2, -parameters["switch_cutout"]/2, parameters["switch_cutout"]/2, parameters["switch_cutout"]/2), a), x, y) for x, y, a in keys]
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
    wall = shape.buffer(expansion).difference(shape.buffer(0.8)).difference(openings)
    assert wall.is_valid and wall.geom_type == "Polygon", "Mounting area is disconnected"
    bolt_region = wall.buffer(-3.9)
    candidates = []
    boundary = shape.buffer(5.3).exterior
    for index in range(180):
        p = boundary.interpolate(boundary.length*index/180)
        if bolt_region.covers(p):
            candidates.append(p)
    assert len(candidates) >= 6
    bolts = [min(candidates, key=lambda p: p.x)]
    while len(bolts) < 6:
        p = max(candidates, key=lambda p: min(p.distance(existing) for existing in bolts))
        assert all(p.distance(existing) >= 15 for existing in bolts)
        bolts.append(p)
    for p in bolts:
        assert p.distance(shape) >= 4.6
        assert wall.covers(p.buffer(3.9)), "Standoff crosses the plate opening"
    desired_battery_center = [(components["S8"][i]+components["S11"][i])/2 for i in (0, 1)]
    rf_exclusion = box(cx-14, cy-23, cx+14, cy+23)
    battery_candidates = []
    for dx in range(-20, 21):
        for dy in range(-15, 16):
            bx, by = desired_battery_center[0]+dx, desired_battery_center[1]+dy
            envelope = box(bx-32, by-20, bx+32, by+20)
            if shape.buffer(-2).covers(envelope) and envelope.distance(rf_exclusion) >= 10:
                battery_candidates.append((dx*dx+dy*dy, bx, by))
    assert battery_candidates, "No protected large-battery envelope fits clear of RF"
    _, bx, by = min(battery_candidates)
    battery_center = [bx, by]
    battery_envelope = box(bx-32, by-20, bx+32, by+20)
    assert under_pcb_clearance-parameters["damping_thickness"]-0.5-8.5-0.5 >= 4.4, "Battery collides with underside component reservation"
    values = [outline, keys, [[p.x, p.y] for p in bolts], components["MCU1"],
              components["RST1"], components["PWR1"], list(shape.bounds), battery_center]
    geometries.append(f"{side}_geometry = {json.dumps(values)};")
    flange_x = shape.bounds[2] + expansion + parameters['flange_clearance']
    t, deduction = parameters['bottom_thickness'], parameters['bend_deduction']
    bend_x = flange_x + t - deduction/2
    bend_lines = [LineString([(sign*bend_x, parameters['flange_y_min']),
                              (sign*bend_x, parameters['flange_y_max'])]) for sign in (-1,1)]
    minimum_bend_hole_distance = min(p.distance(line) - parameters['bolt_diameter']/2 for p in bolts for line in bend_lines)
    assert minimum_bend_hole_distance >= 0.472*25.4/2, 'Bolt hole enters the press-brake deformation zone'
    corner_relief = bend_x - (shape.bounds[2]+expansion)
    assert corner_relief >= 0.118*25.4, 'Insufficient natural corner relief'
    assert parameters['flange_height'] > parameters['bend_radius']
    assert 2*flange_x >= 2*parameters['flange_height'], 'U-channel tooling cannot reach the base'
    assert parameters['flange_height'] >= 0.303*25.4, 'Flange below supplier minimum'
    assert flange_x-(abs(cx)+14) >= 10, 'Bent metal enters the controller RF reservation'
    physical_checks[side] = (cutouts, bolts, openings, bend_lines)
    guide = ['<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="150mm" viewBox="-100 -75 200 150">']
    for line in bend_lines:
        (x0,y0),(x1,y1) = line.coords
        guide.append(f'<path d="M {x0} {-y0} L {x1} {-y1}" fill="none" stroke="blue" stroke-width="0.3"/>')
    guide.append('</svg>')
    (OUTPUT/f'{side}-bend-lines.svg').write_text('\n'.join(guide)+'\n')
    bends = {'material':'5052 H32 aluminum', 'thickness_mm':t, 'angle_degrees':90, 'direction':'both flanges up',
             'radius_mm':parameters['bend_radius'], 'deduction_mm':deduction, 'flange_height_mm':parameters['flange_height'],
             'flat_bend_lines_mm':[list(line.coords) for line in bend_lines],
             'minimum_hole_to_bend_mm':minimum_bend_hole_distance, 'natural_corner_relief_mm':corner_relief,
             'status':'supplier bend simulation and physical fit pending',
             'source':'https://sendcutsend.com/bending-calculator/'}
    (OUTPUT/f'{side}-bends.json').write_text(json.dumps(bends,indent=2)+'\n')
    reports.append({"side": side, "keys": len(keys), "pcb_area_mm2": shape.area,
                    "minimum_plate_web_mm": min(a.distance(b) for i, a in enumerate(cutouts) for b in cutouts[i+1:]),
                    "bolts": values[2], "side_apertures": ["USB", "RST", "PWR"],
                    "switch": "Outemu Medium-Low Black; standard MX socket footprint",
                    "pcb_to_plate_gap_mm": parameters["plate_to_pcb_gap"], "plate_thickness_mm": parameters["plate_thickness"],
                    "under_pcb_clearance_mm": under_pcb_clearance, "bottom_thickness_mm": parameters["bottom_thickness"],
                    "standoff_height_mm": parameters["standoff_height"], "standoff_shim_mm": parameters["standoff_shim"],
                    "damping_thickness_mm": parameters["damping_thickness"], "bends": bends,
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
    cutouts, bolts, openings, bend_lines = physical_checks[side]
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
            assert actual.intersection(openings.buffer(-0.01)).area < 0.0001, "Export blocks side access"
        report["exports"][part] = {"area_mm2": actual.area, "closed_contours": contours}
    subprocess.run(["openscad", "-o", str(OUTPUT / f"{side}-assembly.csg"),
                    "-D", f'side="{side}"', str(ROOT / "case/sandwich.scad")], check=True, env=export_env)
    dxf = (OUTPUT/f'{side}-bottom-flat.dxf').read_text()
    marker = '  0\nENDSEC'
    entity_start = dxf.index('ENTITIES')
    end_entities = dxf.index(marker, entity_start)
    entities = ''
    for line in bend_lines:
        (x0,y0),(x1,y1) = line.coords
        entities += f'  0\nLINE\n  8\n0\n 10\n{x0}\n 20\n{y0}\n 30\n0\n 11\n{x1}\n 21\n{y1}\n 31\n0\n'
    (OUTPUT/f'{side}-bottom-bent.dxf').write_text(dxf[:end_entities]+entities+dxf[end_entities:])
    print(f"{side}: exported three case layers, 21 switch cutouts and six standoff holes")
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
