import json
from pathlib import Path
import subprocess
import re
import shutil
import hashlib
import xml.etree.ElementTree as ET
import zipfile

from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import polygonize

from check_case_models import check_model

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'manufacturing/jlc3dp'
OUTPUT.mkdir(exist_ok=True)
(ROOT/'out/3d').mkdir(exist_ok=True)
reports = {}
parameters = {name: float(value) for name, value in re.findall(
    r'^(\w+) = (-?[\d.]+);$', (ROOT/'case/parameters.scad').read_text(), re.M)}
sleeve_parameters = {name: float(value) for name, value in re.findall(
    r'^(\w+) = (-?[\d.]+);$', (ROOT/'case/printed-sleeve.scad').read_text(), re.M)}
geometries = {line.split('_geometry')[0]: json.loads(line.split(' = ')[1].rstrip(';'))
              for line in (ROOT/'case/geometry.scad').read_text().splitlines()}
meshes = {}


def read_mesh(path):
    with zipfile.ZipFile(path) as archive:
        model = ET.fromstring(archive.read('3D/3dmodel.model'))
    ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    vertices = [[float(v.attrib[k]) for k in ('x', 'y', 'z')]
                for v in model.findall('.//m:vertex', ns)]
    triangles = [[int(t.attrib[k]) for k in ('v1', 'v2', 'v3')]
                 for t in model.findall('.//m:triangle', ns)]
    return vertices, triangles


def section(mesh, height):
    vertices, triangles = mesh
    segments = []
    for triangle in triangles:
        points = []
        for i, j in zip(triangle, triangle[1:]+triangle[:1]):
            a, b = vertices[i], vertices[j]
            if (a[2]-height)*(b[2]-height) < 0:
                fraction = (height-a[2])/(b[2]-a[2])
                points.append(tuple(round(a[k]+fraction*(b[k]-a[k]), 5) for k in (0, 1)))
        if len(points) == 2:
            segments.append(LineString(points))
    return max(polygonize(segments), key=lambda polygon: Polygon(polygon.exterior).area)


for side in ('left', 'right'):
    for part in ('plate', 'tray', 'sleeve'):
        for extension in ('stl', '3mf'):
            subprocess.run(['openscad', '-o', str(OUTPUT/f'{side}-{part}.{extension}'),
                            '-D', f'side="{side}"', str(ROOT/f'case/printed-{part}.scad')], check=True)
        report = check_model(OUTPUT/f'{side}-{part}.3mf')
        mesh = read_mesh(OUTPUT/f'{side}-{part}.3mf')
        meshes[f'{side}-{part}'] = mesh
        data = geometries[side]
        solid = section(mesh, 0.8)
        assert all(not solid.intersects(Point(*p).buffer(1.08)) for p in data[2]), 'Blocked M2 hole'
        if part == 'plate':
            assert report['euler_characteristic'] == -48, (side, 'Expected 21 switch holes and four screw holes')
            assert abs(report['dimensions_mm'][2]-2.6002) < 0.00001, (side, 'Rim height changed')
            assert len(solid.interiors) == 25, 'Expected 21 switch openings and four mounting holes'
            assert all(not solid.intersects(Point(x, y).buffer(6.98)) for x, y, _ in data[1]), 'Blocked switch seat'
        elif part == 'tray':
            assert report['euler_characteristic'] == -8, (side, 'Expected four screw holes and one USB opening')
            assert len(solid.interiors) == 4, 'Expected four floor mounting holes'
            pcb_z = parameters['bottom_thickness'] + parameters['standoff_height'] + parameters['standoff_shim']
            wall = section(mesh, pcb_z-3)
            assert len(wall.interiors) == 1, 'Expected open PCB cavity'
            cavity = Polygon(wall.interiors[0])
            assert cavity.covers(Polygon(data[0]).buffer(0.59)), 'PCB wall clearance below 0.6 mm'
            report['pcb_wall_clearance_mm'] = 0.6
            report['under_pcb_clearance_mm'] = pcb_z-parameters['bottom_thickness']
        else:
            assert report['euler_characteristic'] == 0, (side, 'Expected only the USB through-opening')
            foot = section(mesh, -sleeve_parameters['sleeve_floor']+0.25)
            assert sleeve_parameters['sleeve_floor']-sleeve_parameters['screw_recess_depth'] >= 1.6-1e-9, 'Bottom skin below recommended wall thickness'
            assert len(foot.interiors) == 0, 'Sleeve bottom must have no through-holes'
            assert all(foot.covers(Point(*p).buffer(3.25)) for p in data[2]), 'Bottom does not cover screw heads'
            recess = section(mesh, -sleeve_parameters['screw_recess_depth']/2)
            assert len(recess.interiors) == 4, 'Expected four blind screw-head recesses'
            assert all(not recess.intersects(Point(*p).buffer(3.25)) for p in data[2]), 'Blocked screw-head recess'
            assert foot.area > Polygon(data[0]).area, 'Sleeve bottom is missing'
            wall = section(mesh, 1.1)
            assert Polygon(wall.interiors[0]).covers(Polygon(data[0]).buffer(parameters['outline_expansion']+sleeve_parameters['sleeve_clearance']-0.01)), 'Sleeve cavity cannot fit tray'
            report['tray_clearance_mm'] = sleeve_parameters['sleeve_clearance']
            report['wall_thickness_mm'] = sleeve_parameters['sleeve_wall']
            report['bottom_thickness_mm'] = sleeve_parameters['sleeve_floor']
            report['bottom_closed'] = True
            report['screw_recess_diameter_mm'] = sleeve_parameters['screw_recess_diameter']
            report['screw_recess_depth_mm'] = sleeve_parameters['screw_recess_depth']
            report['maximum_screw_head_and_washer_height_mm'] = sleeve_parameters['screw_recess_depth']
            report['grip_band_interference_mm'] = sleeve_parameters['grip_interference']
            report['screw_heads_accessible_after_sleeve_removal'] = True
            report['physical_fit_verified'] = False
        report['m2_holes_open'] = part != 'sleeve'
        report['stl_sha256'] = hashlib.sha256((OUTPUT/f'{side}-{part}.stl').read_bytes()).hexdigest()
        shutil.copy2(OUTPUT/f'{side}-{part}.3mf', ROOT/f'out/3d/{side}-printed-{part}.3mf')
        reports[f'{side}-{part}'] = report
        print(f'{side}-{part}: connected, closed mesh')
for part in ('plate', 'tray', 'sleeve'):
    layers = {}
    for side in ('left', 'right'):
        layers[side] = {}
        for x, y, z in meshes[f'{side}-{part}'][0]:
            layers[side].setdefault(round(z, 5), []).append((-x if side == 'left' else x, y))
    assert layers['left'].keys() == layers['right'].keys(), f'{part}: different mesh heights'
    for height in layers['left']:
        left = MultiPoint(layers['left'][height])
        right = MultiPoint(layers['right'][height])
        assert left.hausdorff_distance(right) < 0.0001, f'{part}: exports are not mirrored halves'
for side in ('left', 'right'):
    for part in ('tray', 'plate', 'sleeve', 'case'):
        source = ROOT/f'case/printed-{part}.scad' if part != 'case' else ROOT/'case/sandwich.scad'
        arguments = ['openscad', '-o', str(ROOT/f'previews/printed-{part}-{side}.png'),
                     '--preview', '--imgsize=1200,900', '--viewall', '--autocenter',
                     '--colorscheme=Tomorrow', '-D', f'side="{side}"']
        if part == 'case':
            arguments += ['-D', 'part="printed-assembly"', '-D', 'exploded=5']
        subprocess.run(arguments+[str(source)], check=True)
(OUTPUT/'model-checks.json').write_text(json.dumps(reports, indent=2)+'\n')
