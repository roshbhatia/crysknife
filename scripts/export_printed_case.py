import json
from pathlib import Path
import subprocess
import re
import shutil
import hashlib
import xml.etree.ElementTree as ET
import zipfile

from shapely.affinity import rotate, translate
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box
from shapely.ops import polygonize, unary_union

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


def section(mesh, height, all_regions=False):
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
    polygons = list(polygonize(segments))
    if all_regions:
        return unary_union([p for p in polygons if not any(
            Polygon(other.exterior).contains(p.representative_point())
            for other in polygons if other != p)])
    return max(polygons, key=lambda polygon: Polygon(polygon.exterior).area)


for side in ('left', 'right'):
    for part in ('plate', 'bottom', 'sleeve'):
        model_path = (OUTPUT if part == 'sleeve' else ROOT/'out/3d')/f'{side}-{part}.3mf'
        source = ROOT/f'case/printed-{part}.scad' if part in ('plate', 'sleeve') else ROOT/'case/sandwich.scad'
        extensions = ('stl', '3mf') if part == 'sleeve' else ('3mf',)
        for extension in extensions:
            target = model_path.with_suffix(f'.{extension}')
            subprocess.run(['openscad', '-o', str(target), '-D', f'side="{side}"',
                            '-D', f'part="{"plate-solid" if part == "plate" else part}"', str(source)], check=True)
        report = check_model(model_path)
        mesh = read_mesh(model_path)
        meshes[f'{side}-{part}'] = mesh
        data = geometries[side]
        solid = section(mesh, 0.8)
        assert all(not solid.intersects(Point(*p).buffer(1.08)) for p in data[2]), 'Blocked M2 hole'
        if part == 'plate':
            assert report['euler_characteristic'] == -48, (side, 'Expected 21 switch holes and four screw holes')
            assert abs(report['dimensions_mm'][2]-(parameters['plate_thickness']+1)) < 0.00001, (side, 'Reinforced plate height changed')
            underside = section(mesh, -0.5, all_regions=True)
            assert not underside.intersects(Polygon(data[0])), 'Underside rim intrudes over the PCB'
            assert all(not underside.intersects(Point(*p).buffer(parameters['washer_diameter']/2)) for p in data[2]), 'Rim blocks mounting spacers'
            report['switch_seat_thickness_mm'] = parameters['plate_thickness']
            report['underside_rim_height_mm'] = 1
            assert len(solid.interiors) == 25, 'Expected 21 switch openings and four mounting holes'
            assert all(not solid.intersects(Point(x, y).buffer(6.98)) for x, y, _ in data[1]), 'Blocked switch seat'
        elif part == 'bottom':
            assert report['euler_characteristic'] == -6, (side, 'Expected four screw holes')
            assert len(solid.interiors) == 4, 'Expected four floor mounting holes'
            assert abs(report['dimensions_mm'][2]-parameters['bottom_thickness']) < 0.00001
        else:
            foot = section(mesh, -sleeve_parameters['sleeve_floor']+0.25)
            assert sleeve_parameters['sleeve_floor']-sleeve_parameters['screw_recess_depth'] >= 1.6-1e-9, 'Bottom skin below recommended wall thickness'
            assert len(foot.interiors) == 0, 'Sleeve bottom must have no through-holes'
            assert all(foot.covers(Point(*p).buffer(3.25)) for p in data[2]), 'Bottom does not cover screw heads'
            recess = section(mesh, -sleeve_parameters['screw_recess_depth']/2)
            assert len(recess.interiors) == 4, 'Expected four blind screw-head recesses'
            assert all(not recess.intersects(Point(*p).buffer(3.25)) for p in data[2]), 'Blocked screw-head recess'
            assert foot.area > Polygon(data[0]).area, 'Sleeve bottom is missing'
            wall = section(mesh, 1.1)
            assert Polygon(wall.interiors[0]).covers(Polygon(data[0]).buffer(parameters['outline_expansion']+sleeve_parameters['sleeve_clearance']-0.01)), 'Sleeve cavity cannot fit bottom plate'
            lip_z = (parameters['bottom_thickness'] + parameters['standoff_height']
                     + parameters['standoff_shim'] + parameters['pcb_thickness']
                     + parameters['plate_to_pcb_gap'] + parameters['plate_thickness']
                     + sleeve_parameters['lip_clearance'])
            lip = section(mesh, lip_z+sleeve_parameters['lip_height']/2, all_regions=True)
            assert not lip.is_empty, 'Retaining lip is missing'
            for x, y, angle in data[1]:
                half = sleeve_parameters['keycap_keepout']/2-0.01
                keepout = translate(rotate(box(-half,-half,half,half), angle, origin=(0,0)), x, y)
                assert not lip.intersects(keepout), 'Lip blocks keycap envelope'
            assert all(not lip.intersects(Point(*p).buffer((parameters['washer_diameter']+1.4)/2)) for p in data[2]), 'Lip blocks top screw access'
            flat_plate = section(meshes[f'{side}-plate'], parameters['plate_thickness']/2, all_regions=True)
            overlap = lip.intersection(flat_plate)
            assert overlap.area > 100, 'Insufficient lip overlap with flat top plate'
            center_y = Polygon(data[0]).centroid.y
            assert overlap.bounds[1] < center_y-15 and overlap.bounds[3] > center_y+15, 'Lip must retain front and rear edges'
            report['retaining_lip_height_mm'] = sleeve_parameters['lip_height']
            report['retaining_lip_overlap_mm'] = sleeve_parameters['lip_overlap']
            report['retaining_lip_vertical_clearance_mm'] = sleeve_parameters['lip_clearance']
            report['retaining_lip_contact_area_mm2'] = round(overlap.area, 3)
            report['keycap_keepout_mm'] = sleeve_parameters['keycap_keepout']
            report['plate_edge_clearance_mm'] = sleeve_parameters['sleeve_clearance']
            report['wall_thickness_mm'] = sleeve_parameters['sleeve_wall']
            report['bottom_thickness_mm'] = sleeve_parameters['sleeve_floor']
            report['bottom_closed'] = True
            report['screw_recess_diameter_mm'] = sleeve_parameters['screw_recess_diameter']
            report['screw_recess_depth_mm'] = sleeve_parameters['screw_recess_depth']
            report['maximum_screw_head_and_washer_height_mm'] = sleeve_parameters['screw_recess_depth']
            report['screw_heads_accessible_after_sleeve_removal'] = True
            report['physical_fit_verified'] = False
        report['m2_holes_open'] = part != 'sleeve'
        if part == 'sleeve':
            report['stl_sha256'] = hashlib.sha256(model_path.with_suffix('.stl').read_bytes()).hexdigest()
            shutil.copy2(model_path, ROOT/f'out/3d/{side}-printed-sleeve.3mf')
        if part in ('bottom', 'plate'):
            shutil.copy2(model_path, OUTPUT/model_path.name)
        reports[f'{side}-{part}'] = report
        print(f'{side}-{part}: connected, closed mesh')
for part in ('plate', 'bottom', 'sleeve'):
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
    for part in ('sleeve', 'case', 'fit'):
        source = ROOT/f'case/printed-{part}.scad' if part not in ('case', 'fit') else ROOT/'case/sandwich.scad'
        arguments = ['openscad', '-o', str(ROOT/f'previews/printed-{part}-{side}.png'),
                     '--preview', '--imgsize=1200,900', '--viewall', '--autocenter',
                     '--colorscheme=Tomorrow', '-D', f'side="{side}"']
        if part in ('case', 'fit'):
            arguments += ['-D', 'part="sleeved-assembly"', '-D', 'exploded=5' if part == 'case' else 'exploded=0']
        subprocess.run(arguments+[str(source)], check=True)
(OUTPUT/'model-checks.json').write_text(json.dumps(reports, indent=2)+'\n')
