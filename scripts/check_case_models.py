from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def check_model(path):
    with zipfile.ZipFile(path) as archive:
        model = ET.fromstring(archive.read('3D/3dmodel.model'))
    assert model.attrib.get('unit','millimeter') == 'millimeter'
    meshes = model.findall('.//m:mesh',NS)
    assert len(meshes) == 1, (path, 'Expected one body')
    mesh = meshes[0]
    parent = {}
    edges = Counter()

    def find(v):
        parent.setdefault(v,v)
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    triangles = mesh.findall('m:triangles/m:triangle',NS)
    assert triangles
    for triangle in triangles:
        indices = [int(triangle.attrib[k]) for k in ('v1','v2','v3')]
        assert len(set(indices)) == 3, (path, 'Degenerate triangle')
        for a,b in zip(indices,indices[1:]+indices[:1]):
            parent[find(a)] = find(b)
            edges[tuple(sorted((a,b)))] += 1
    assert len({find(v) for v in parent}) == 1, (path, 'Disconnected body')
    assert set(edges.values()) == {2}, (path, 'Open or non-manifold body')
    vertices = [[float(v.attrib[k]) for k in ('x', 'y', 'z')]
                for v in mesh.findall('m:vertices/m:vertex', NS)]
    return {'triangles': len(triangles), 'connected': True, 'closed': True,
            'euler_characteristic': len(parent)-len(edges)+len(triangles),
            'dimensions_mm': [max(v[i] for v in vertices)-min(v[i] for v in vertices) for i in range(3)]}


if __name__ == '__main__':
    for side in ('left', 'right'):
        result = check_model(ROOT/f'build/case/{side}-bottom.3mf')
        print(f"{side}: bottom is one connected, closed mesh; {result['triangles']} triangles")
