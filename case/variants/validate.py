"""Check assembled CAD intersections and compare mirrored pair geometry."""
from pathlib import Path
import json
import cadquery as cq
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'manufacturing/enclosures'
checks=json.loads((OUT/'checks.json').read_text())
assert len(checks)==8,'Expected four complete left/right pairs'
results=[]
for rec in checks:
 folder=OUT/rec['variant'];side=rec['side']
 shapes={name:cq.importers.importStep(str(folder/f'{side}-{name}.step')).val() for name in rec['parts']}
 def separate(a,b):
  intersection=shapes[a].intersect(shapes[b]).Volume()
  assert intersection<1e-5,(rec['variant'],side,a,b,intersection)
  return round(intersection,7)
 overlaps={}
 if 'tray' in shapes:
  overlaps['plate/tray']=separate('top','tray')
  overlaps['plate/lower gasket']=separate('top','lower-gasket')
 if 'frame' in shapes:
  overlaps['plate/frame']=separate('top','frame')
  overlaps['plate/upper gasket']=separate('top','upper-gasket')
  overlaps['tray/frame']=separate('tray','frame')
  overlaps['sleeve/frame']=separate('sleeve','frame')
  overlaps['sleeve/tray']=separate('sleeve','tray')
  overlaps['sleeve/plate']=separate('sleeve','top')
 for name,shape in shapes.items():assert shape.isValid(),(folder,side,name)
 results.append({'variant':rec['variant'],'side':side,'intersection_volumes_mm3':overlaps})
for option in {r['variant'] for r in checks}:
 left,right=[r for r in checks if r['variant']==option]
 assert left['parts'].keys()==right['parts'].keys()
 for name,p in left['parts'].items():
  q=right['parts'][name]
  assert abs(p['volume_mm3']-q['volume_mm3'])<.05,(option,name,p,q)
print('Eight assemblies: valid CAD, mirrored pair volumes, no rigid/gasket/TPU intersections')
(OUT/'assembly-checks.json').write_text(json.dumps(results,indent=2)+'\n')

from collections import Counter
import struct,re,json
import numpy as np
root=OUT;reports=[]
for p in root.rglob('*.stl'):
 b=p.read_bytes()
 if b.startswith(b'solid'):
  vertices=np.array([tuple(map(float,v)) for v in re.findall(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)',b)]).reshape(-1,3,3)
 else:
  count=struct.unpack_from('<I',b,80)[0]
  assert len(b)==84+50*count,p
  dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
  vertices=np.frombuffer(b,offset=84,count=count,dtype=dtype)['vertices'].astype(float)
 points=np.round(vertices,5)
 edges=Counter()
 for tri in points:
  v=[tuple(a) for a in tri]
  assert len(set(v))==3,(p,'degenerate triangle')
  for a,c in zip(v,v[1:]+v[:1]):edges[tuple(sorted((a,c)))]+=1
 assert set(edges.values())=={2},(p,'open mesh',Counter(edges.values()))
 reports.append({'file':str(p.relative_to(root)),'triangles':len(vertices),'closed':True})
print(len(reports),'STL files have closed manifold triangle edges')
(root/'mesh-checks.json').write_text(json.dumps(reports,indent=2)+'\n')
hybrids=[]
for side in ('left','right'):
    top=cq.importers.importStep(str(OUT/f'b-cnc-rigid-tray/{side}-top.step')).val()
    tray=cq.importers.importStep(str(OUT/f'c-printed-tray-plate/{side}-tray.step')).val()
    overlap=top.intersect(tray).Volume()
    assert overlap<1e-5,(side,'CNC top/printed tray',overlap)
    hybrids.append({'side':side,'top':'b-cnc-rigid-tray','tray':'c-printed-tray-plate','intersection_mm3':round(overlap,7)})
(OUT/'hybrid-checks.json').write_text(json.dumps(hybrids,indent=2)+'\n')
print('CNC top / printed tray hybrid has no CAD overlap on either half')
