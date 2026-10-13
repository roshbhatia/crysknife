from pathlib import Path
import csv
import json
import re
from collections import Counter
import cadquery as cq
import ezdxf
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon, Point, box, MultiPoint
from shapely.affinity import rotate, translate
from shapely.ops import unary_union
from generate import ROOT, DATA, solid, holes, export_step, normalize_text, render, COLORS

OUT = ROOT/'manufacturing/enclosures/f-750-rigid-sandwich'
PRE = ROOT/'previews/enclosures/f-750'
OUT.mkdir(parents=True, exist_ok=True)
PRE.mkdir(parents=True, exist_ok=True)
PARAM = {k: float(v) for k, v in re.findall(r'^(\w+) = (-?[\d.]+);$', (ROOT/'case/parameters.scad').read_text(), re.M)}
BAT = json.loads((ROOT/'manufacturing/battery.json').read_text())
FLOOR = PARAM['bottom_thickness']
UNDER = PARAM['standoff_height'] + PARAM['standoff_shim']
PCB_Z = FLOOR + UNDER
PLATE_Z = PCB_Z + PARAM['pcb_thickness'] + PARAM['plate_to_pcb_gap']
FEET = 2.5
HEADERS = json.loads((ROOT/'manufacturing/header-fit.json').read_text())
RESERVE = BAT['case_reservation_mm']
PROTECTED = BAT['prototype_assumptions']['protected_pack_max_mm']
spare = UNDER - (RESERVE[2] + 4.4 + .5 + .5 + PARAM['damping_thickness'])
controller_floor = UNDER - PARAM['controller_gap'] - PARAM['controller_board_thickness'] - PARAM['damping_thickness']
assert spare >= .4997 and controller_floor >= 1
assert FLOOR == 3.175 and BAT['capacity_mAh'] == 750
reports = []
pair = []
side_shapes = {}
for side, data in DATA.items():
    pcb = Polygon(data[0])
    outer = pcb.buffer(PARAM['outline_expansion'], join_style=2)
    cx, cy = data[3]
    bx, by = data[7]
    rf = box(cx-14, cy-23, cx+14, cy+23)
    switchholes = unary_union([translate(rotate(box(-7,-7,7,7), a, origin=(0,0)), x,y) for x,y,a in data[1]])
    mounts = holes(data[2], 1.1)
    profiles = {'top': outer.difference(mounts).difference(switchholes),
                'bottom': outer.difference(mounts).difference(rf),
                'rf-insert': outer.intersection(rf).buffer(-.25, join_style=2),
                'damping': outer.difference(holes(data[2], 2.6))}
    shapes = {}
    heights = {'top': (PLATE_Z, PARAM['plate_thickness']), 'bottom': (0, FLOOR),
               'rf-insert': (0, FLOOR), 'damping': (FLOOR, PARAM['damping_thickness'])}
    for name, profile in profiles.items():
        z, h = heights[name]
        shape = solid(profile, z, h)
        assert shape.isValid() and len(shape.Solids()) == 1, (side, name)
        export_step(shape, OUT/f'{side}-{name}.step')
        roundtrip = cq.importers.importStep(str(OUT/f'{side}-{name}.step')).val()
        assert abs(shape.Volume()-roundtrip.Volume())/shape.Volume() < 1e-6
        cq.exporters.export(shape, str(OUT/f'{side}-{name}.stl'), tolerance=.08, angularTolerance=.1, opt={"ascii": True})
        edges = Counter()
        vertices = re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', (OUT/f'{side}-{name}.stl').read_text())
        for i in range(0, len(vertices), 3):
            triangle = [tuple(round(float(v),5) for v in p) for p in vertices[i:i+3]]
            assert len(set(triangle)) == 3
            for a,b in zip(triangle, triangle[1:]+triangle[:1]): edges[tuple(sorted((a,b)))] += 1
        assert set(edges.values()) == {2}, (side, name, 'open STL')
        drawing = ezdxf.new()
        drawing.units = 4
        model = drawing.modelspace()
        for ring in [profile.exterior, *profile.interiors]: model.add_lwpolyline(list(ring.coords)[:-1], close=True)
        path = OUT/f'{side}-{name}.dxf'
        drawing.saveas(path)
        normalize_text(path)
        shapes[name] = shape
    assert shapes['top'].intersect(shapes['bottom']).Volume() < 1e-5
    assert shapes['bottom'].intersect(shapes['rf-insert']).Volume() < 1e-5
    assert shapes['top'].intersect(shapes['damping']).Volume() < 1e-5
    assert profiles['top'].intersection(switchholes).area < 1e-6
    battery_envelope = box(bx-RESERVE[0]/2, by-RESERVE[1]/2, bx+RESERVE[0]/2, by+RESERVE[1]/2)
    assert pcb.buffer(-2).covers(battery_envelope)
    assert battery_envelope.distance(rf) >= 10
    battery_x = bx + (-1 if side == 'left' else 1)*(RESERVE[0]-PROTECTED[0])/2
    battery_y = by + (RESERVE[1]-PROTECTED[1])/2
    pack = box(battery_x-PROTECTED[0]/2, battery_y-PROTECTED[1]/2, battery_x+PROTECTED[0]/2, battery_y+PROTECTED[1]/2)
    assert battery_envelope.covers(pack)
    assert all(pack.distance(Point(*p)) >= 3.25 for p in data[2])
    cable = battery_envelope.difference(pack)
    assert cable.area >= 500
    feet = json.loads((ROOT/f'manufacturing/enclosures/e-thin-rigid-sandwich/{side}-feet.json').read_text())['positions_mm']
    assert all(profiles['bottom'].covers(Point(*p).buffer(4.2)) for p in feet)
    assert MultiPoint(feet).convex_hull.contains(pcb.centroid)
    top_engagement = PARAM['top_screw_length'] - (PARAM['plate_thickness']+.5+PARAM['plate_to_pcb_gap']+PARAM['pcb_thickness']+PARAM['standoff_shim'])
    bottom_engagement = PARAM['bottom_screw_length'] - (FLOOR+.5)
    assert 2 <= top_engagement <= 4.5 and 2 <= bottom_engagement <= 4.5
    report = {'side': side, 'quantity': 1, 'battery': BAT['sku'],
              'floor_mm': FLOOR, 'under_pcb_mm': UNDER,
              'desk_to_plate_mm': round(PLATE_Z+PARAM['plate_thickness']+FEET,4),
              'reserved_stack_margin_mm': round(spare,4),
              'controller_floor_above_damping_mm': round(controller_floor,4),
              'header_gap_above_drawing_minimum_mm': round(PARAM['controller_gap']-HEADERS['minimum_body_stack_mm'],4),
              'battery_reserved_mm': RESERVE, 'assumed_protected_pack_mm': PROTECTED,
              'protected_pack_center_mm': [battery_x, battery_y],
              'battery_wire_corridor_mm': [10,2], 'battery_to_RF_mm': round(battery_envelope.distance(rf),4),
              'top_thread_engagement_mm': round(top_engagement,4), 'bottom_thread_engagement_mm': round(bottom_engagement,4),
              'reference_feet_mm': FEET, 'feet_positions_mm': feet, 'desk_fastener_clearance_mm': .4,
              'physical_fit_verified': False, 'parts': {name: {'volume_mm3': shape.Volume(),
              'dimensions_mm': [shape.BoundingBox().xlen, shape.BoundingBox().ylen, shape.BoundingBox().zlen],
              'closed_STL': True, 'STEP_roundtrip': True} for name,shape in shapes.items()}}
    reports.append(report)
    side_shapes[side] = shapes
    dx = 0 if side == 'left' else 195
    installed = [(s.translate((dx,0,FEET)), COLORS.get(name,(90,95,100))) for name,s in shapes.items()]
    installed += [(solid(pcb.difference(mounts), PCB_Z+FEET, 1.6).translate((dx,0,0)),(239,237,225)),
                  (solid(pack, FLOOR+FEET+PARAM['damping_thickness']+.5, PROTECTED[2]).translate((dx,0,0)),(185,145,85)),
                  (solid(cable, FLOOR+FEET+PARAM['damping_thickness']+.5, 1).translate((dx,0,0)),(225,177,90)),
                  (solid(box(cx-9,cy-17,cx+9,cy+17), PCB_Z+FEET-9.6, 1.6).translate((dx,0,0)),(66,109,145))]
    for x,y in data[2]:
        for z,h,r,c in [(FLOOR,PARAM['standoff_height'],2.3,(160,163,162)),(FLOOR+PARAM['standoff_height'],PARAM['standoff_shim'],PARAM['standoff_shim_diameter']/2,(225,225,215)),(PCB_Z+1.6,.5,2.75,(225,225,215)),(PCB_Z+2.1,3,2,(225,225,215))]:
            installed.append((cq.Solid.makeCylinder(r,h,cq.Vector(x+dx,y,z+FEET)),c))
    for x,y in feet: installed.append((cq.Solid.makeCylinder(4,FEET,cq.Vector(x+dx,y,0)),(66,77,82)))
    pair.extend(installed)
    local = [(s.translate((-dx,0,0)),c) for s,c in installed]
    render(local, PRE/f'{side}-assembled.png')
    render([(s.rotate((0,0,0),(0,0,1),-90),c) for s,c in local], PRE/f'{side}-profile.png', True, bounds=((-80,-45),(80,2)))
    slice_plane = solid(box(-110,by-.3,110,by+.3), -1, 55)
    section = [(s.intersect(slice_plane),c) for s,c in local if s.intersect(slice_plane).Volume() > 1e-6]
    render(section, PRE/f'{side}-section.png', True)
for name in profiles:
    assert abs(reports[0]['parts'][name]['volume_mm3']-reports[1]['parts'][name]['volume_mm3']) < .05
render(pair, PRE/'assembled-pair.png')
(OUT/'checks.json').write_text(json.dumps(reports,indent=2)+'\n')
rows = [('Typeractive Liter 403450 battery','750 mAh; protected prototype assumption; No Jack option',2),
        ('nice!nano V2','face up below carrier; BOOST open; use current sleep UF2',2),
        ('Mill-Max 350-10-112-00-006000 male strip','12 round pins; two per controller',4),
        ('MX switches and 1U keycaps','42 each; switches user-owned',42),
        ('clear acrylic top','1.6002 mm; laser cut; 14 mm square latch seats',2),
        ('5052 H32 aluminum floor','3.175 mm; RF opening; deburr and insulate',2),
        ('PMMA RF insert','3.175 mm; flush interior; exterior-only nonconductive seam retention',2),
        ('Würth 970120244 M2 standoff','12 mm; 4 mm flats; through M2 thread; drawing checked',8),
        ('Würth 960020010 lower spacer','2 mm +/-0.1; 4 mm OD; 2.2 mm bore; one per mount',8),
        ('M2 nylon washer','0.5 mm; 5.5 mm OD; one above PCB and one under each screw head',24),
        ('M2 nylon spacer','3 mm; 4 mm OD; 2.2 mm bore',8),
        ('M2 top screw','12 mm; 2.7998 mm nominal engagement',8),
        ('M2 bottom screw','6 mm; 2.325 mm nominal engagement; head+washer <=2.1 mm',8),
        ('non-slip feet','8 mm diameter reference; 2.5 mm installed height; four per half',8),
        ('floor damping sheet','1.6002 mm total; existing flat neoprene profile',2),
        ('foam and dielectric liner','0.5 mm combined below cell; PET liner across conductive floor',2),
        ('insulating cover and air','0.5 mm total above cell; loose nonconductive end tabs, no pouch pressure',2)]
with (OUT/'hardware.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['Part','Specification','Quantity for complete pair']);w.writerows(rows)
print('F: 750 mAh; 14 mm below PCB; 26.3752 mm desk to plate; eight closed solids/STEP round-trips; mirrored pair passes')

with (OUT/'parts.csv').open('w',newline='') as f:
    writer=csv.writer(f,lineterminator='\n')
    writer.writerow(['Part','Quantity','Material','Thickness mm','Files','Dimensions mm'])
    for rec in reports:
        for name,part in rec['parts'].items():
            material={'top':'clear acrylic; laser cut','bottom':'5052 H32 aluminum','rf-insert':'clear PMMA','damping':'neoprene'}[name]
            writer.writerow([rec['side']+'-'+name,1,material,heights[name][1],rec['side']+'-'+name+'.step / .stl / .dxf',json.dumps(part['dimensions_mm'])])
