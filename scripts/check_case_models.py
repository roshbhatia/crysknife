from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
for side in ('left','right'):
    with zipfile.ZipFile(ROOT/f'build/case/{side}-bottom.3mf') as archive:
        model = ET.fromstring(archive.read('3D/3dmodel.model'))
    assert model.attrib.get('unit','millimeter') == 'millimeter'
    meshes = model.findall('.//m:mesh',NS)
    assert len(meshes) == 1, (side,'Expected one metal body')
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
        assert len(set(indices)) == 3, (side,'Degenerate triangle')
        for a,b in zip(indices,indices[1:]+indices[:1]):
            parent[find(a)] = find(b)
            edges[tuple(sorted((a,b)))] += 1
    assert len({find(v) for v in parent}) == 1, (side,'Disconnected metal bottom')
    assert set(edges.values()) == {2}, (side,'Open or non-manifold metal bottom')
    print(f'{side}: bottom is one connected, closed mesh; {len(triangles)} triangles')
