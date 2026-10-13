"""Export separate enclosure concepts from the unchanged keyboard geometry."""
import json, re, math
from pathlib import Path
import cadquery as cq
from shapely.geometry import Polygon, Point, box
from shapely.affinity import rotate, translate
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'manufacturing/enclosures'
PREVIEW = ROOT / 'previews/enclosures'
PARAM = {k: float(v) for k,v in re.findall(r'^(\w+) = (-?[\d.]+);$', (ROOT/'case/parameters.scad').read_text(), re.M)}
DATA = {s.split('_geometry')[0]: json.loads(s.split(' = ')[1].rstrip(';')) for s in (ROOT/'case/geometry.scad').read_text().splitlines()}
FLOOR = PARAM['bottom_thickness']
UNDER_PCB = PARAM['standoff_height'] + PARAM['standoff_shim']
PCB_Z = FLOOR + UNDER_PCB
PLATE_Z = PCB_Z + PARAM['pcb_thickness'] + PARAM['plate_to_pcb_gap']
assert UNDER_PCB == 16 and PARAM['plate_to_pcb_gap'] == 3.5 and PARAM['controller_gap'] == 8, 'Recheck variant stack after baseline edits'
SEAT = PARAM['plate_thickness']
OPTIONS = ['a-tpu-cnc-plates','b-cnc-rigid-tray','c-printed-tray-plate','d-suspended-hybrid']
COLORS = {'top':(155,209,224),'bottom':(125,135,150),'tray':(134,167,194),'frame':(156,204,219),'gasket':(207,145,75),'rf-insert':(172,219,222),'sleeve':(102,169,172)}

def normalize_text(path):
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')

def export_step(shape,path):
    cq.exporters.export(shape,str(path))
    normalize_text(path)

def polygons(p):
    return [p] if p.geom_type=='Polygon' else [q for q in p.geoms if q.geom_type=='Polygon']

def solid(p,z,h):
    solids=[]
    for poly in polygons(p):
        if poly.area<.01: continue
        w=cq.Workplane('XY').polyline(list(poly.exterior.coords)[:-1]).close()
        for ring in poly.interiors: w=w.polyline(list(ring.coords)[:-1]).close()
        solids.append(w.extrude(h).translate((0,0,z)).val())
    return cq.Compound.makeCompound(solids) if len(solids)>1 else solids[0]

def holes(points,r):
    from shapely.ops import unary_union
    return unary_union([Point(*p).buffer(r,resolution=16) for p in points])

def control_cuts(d,side,shift=0):
    cx,cy=d[3]; rx,ry=d[4]; px,py=d[5]
    # Shared control windows follow sleeve-geometry.scad, with additional cable sweep allowance.
    return [solid(box(cx-10,cy+12,cx+10,cy+52),PCB_Z-8-5+shift,12),
            solid(box(rx-8,ry-5,rx+8,ry+36),PCB_Z-2+shift,24),
            solid(box(px+(-5 if side=='left' else -27),py-8,px+(27 if side=='left' else 5),py+8),PCB_Z-3+shift,24)]

def cut_controls(shape,cuts):
    for c in cuts: shape=shape.cut(c)
    return shape.clean()

class SleeveMesh:
    def __init__(self,path,offset):self.path,self.offset=path,offset
    def tessellate(self,*args):
        vertices=[cq.Vector(float(x)+self.offset,float(y),float(z)-9) for x,y,z in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',self.path.read_text())]
        return vertices,[tuple(range(i,i+3)) for i in range(0,len(vertices),3)]

def render(parts,path,section=False):
    import numpy as np
    vertices=[];triangles=[]
    for shape,color in parts:
        verts,faces=shape.tessellate(.18,.15)
        for ids in faces:
            pts=[verts[i].toTuple() for i in ids]
            projected=[(x,-z,y) for x,y,z in pts] if section else [(.82*x+.57*y,.32*x-.46*y-.9*z,.513*x-.738*y+.56*z) for x,y,z in pts]
            normal=np.cross(np.subtract(pts[1],pts[0]),np.subtract(pts[2],pts[0]))
            length=np.linalg.norm(normal)
            shade=.6+.4*abs(np.dot(normal/length,np.array([.3,-.5,.8]))) if length else 1
            triangles.append((projected,np.array(color)*min(1,shade)))
            vertices.extend(projected)
    v=np.array(vertices);minimum=v[:,:2].min(axis=0);maximum=v[:,:2].max(axis=0)
    w,h=1500,720;scale=min((w-70)/(maximum[0]-minimum[0]),(h-70)/(maximum[1]-minimum[1]))
    pixels=np.full((h,w,3),[246,245,241],dtype=np.uint8);depth=np.full((h,w),-np.inf)
    for pts,color in triangles:
        t=np.array(pts);t[:,:2]=(t[:,:2]-minimum)*scale+35
        x0,y0=np.maximum(0,np.floor(t[:,:2].min(axis=0)).astype(int));x1,y1=np.minimum([w-1,h-1],np.ceil(t[:,:2].max(axis=0)).astype(int))
        if x1<x0 or y1<y0:continue
        x,y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
        a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-9:continue
        u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
        vv=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
        zz=u*a[2]+vv*b[2]+(1-u-vv)*c[2]
        region=depth[y0:y1+1,x0:x1+1];mask=(u>=0)&(vv>=0)&(u+vv<=1)&(zz>region)
        region[mask]=zz[mask];pixels[y0:y1+1,x0:x1+1][mask]=color.astype(np.uint8)
    Image.fromarray(pixels).save(path)

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--variant',choices=OPTIONS)
    args=parser.parse_args()
    records=[]
    for option in ([args.variant] if args.variant else OPTIONS):
        output=OUT/option;output.mkdir(parents=True,exist_ok=True)
        frame_points_left=None
        for side,d in DATA.items():
            pcb=Polygon(d[0]);keys=d[1];bolts=d[2];cx,cy=d[3]
            rf=box(cx-14,cy-23,cx+14,cy+23)
            keyholes=[]
            for x,y,a in keys:
                hole=box(-7,-7,7,7)
                if option!='c-printed-tray-plate':
                    # 1 mm corner reliefs permit milling while retaining straight latch faces.
                    for sx in (-7,7):
                        for sy in (-7,7): hole=hole.union(Point(sx,sy).buffer(.5,resolution=12))
                keyholes.append(translate(rotate(hole,a,origin=(0,0)),x,y))
            from shapely.ops import unary_union
            switchholes=unary_union(keyholes)
            suspended=option.startswith('d-')
            shift=2 if suspended else 0
            pz=PLATE_Z+shift
            expansion=4 if option.startswith('a-') else (14 if suspended else 10)
            outer=pcb.buffer(expansion,join_style=2)
            cuts=control_cuts(d,side,shift)
            top_outer=pcb.buffer(10,join_style=2) if suspended else outer
            top_outline=top_outer.difference(holes(bolts,1.1)).difference(switchholes)
            top=solid(top_outer,pz,SEAT)
            for bx,by in bolts:
                top=top.cut(cq.Solid.makeCylinder(1.1,SEAT+.2,cq.Vector(bx,by,pz-.1)))
            for x,y,a in keys:
                tool=cq.Workplane('XY').rect(14,14).extrude(SEAT+.2).translate((0,0,pz-.1)).val()
                if option!='c-printed-tray-plate':
                    for sx in (-7,7):
                        for sy in (-7,7): tool=tool.fuse(cq.Solid.makeCylinder(.5,SEAT+.2,cq.Vector(sx,sy,pz-.1)))
                tool=tool.rotate((0,0,0),(0,0,1),a).translate((x,y,0))
                top=top.cut(tool)
            top=top.clean()
            parts={'top':top}; profiles={'top':top_outline}
            if option.startswith('a-'):
                # Metal bottom retains a non-metal RF opening matching the existing exclusion.
                bottom_outline=outer.difference(holes(bolts,1.1)).difference(rf)
                parts['bottom']=solid(bottom_outline,0,FLOOR)
                parts['pmma-bottom']=solid(outer.difference(holes(bolts,1.1)),0,FLOOR)
                profiles['bottom']=bottom_outline
                patch=outer.intersection(rf).buffer(-.25)
                parts['rf-insert']=solid(patch,0,FLOOR)
                # Import unchanged TPU exterior; exact original lips and control cutouts.
                # STEP for TPU is intentionally omitted; original watertight STL is the manufacturing model.
                import shutil
                shutil.copy2(ROOT/f'manufacturing/jlc3dp/{side}-sleeve.stl',output/f'{side}-sleeve.stl')
                shutil.copy2(ROOT/f'manufacturing/jlc3dp/{side}-sleeve.3mf',output/f'{side}-sleeve.3mf')
                support='rigid original M2 standoffs; TPU exterior only'
            else:
                cavity=pcb.buffer(4.5,join_style=1,resolution=12)
                # Pockets and walls remain completely outside the existing electronics volume.
                body=solid(outer,0,FLOOR).fuse(solid(outer.difference(cavity),FLOOR,pz-.3-FLOOR))
                # Controlled 2 mm gasket compresses to 1.5 mm on the external ledge.
                gasket_profile=pcb.buffer(8.5,join_style=1).difference(pcb.buffer(5.5,join_style=1))
                groove=solid(gasket_profile,pz-1.5,1.6)
                body=body.cut(groove)
                body=cut_controls(body,cuts)
                gasket=cut_controls(solid(gasket_profile,pz-1.5,1.5),cuts)
                profiles['lower-gasket']=gasket_profile
                parts['lower-gasket']=gasket
                rx,ry=d[4];px,py=d[5]
                profiles['lower-gasket']=gasket_profile.difference(box(rx-8,ry-5,rx+8,ry+36)).difference(box(px+(-5 if side=='left' else -27),py-8,px+(27 if side=='left' else 5),py+8))
                if suspended:
                    # New outer bolts join only tray/frame. Existing PCB holes join only PCB/plate.
                    rim=pcb.buffer(11.5,join_style=1).exterior
                    points=[]
                    for i in range(80):
                        q=rim.interpolate(rim.length*i/80);xy=(q.x,q.y)
                        if top_outer.buffer(1.4).contains(q) or rf.buffer(3).contains(q) or any(c.BoundingBox().xmin-3<q.x<c.BoundingBox().xmax+3 and c.BoundingBox().ymin-3<q.y<c.BoundingBox().ymax+3 for c in cuts):continue
                        if all(q.distance(Point(*p))>40 for p in points):points.append(xy)
                        if len(points)==4:break
                    assert len(points)==4,('frame screws',side)
                    if side=='left':frame_points_left=points
                    else:points=[(-x,y) for x,y in frame_points_left]
                    body=body.fuse(solid(outer.difference(top_outer.buffer(.5,join_style=2)),pz-.3,SEAT+1.8))
                    frame_profile=outer.difference(pcb.buffer(4.5,join_style=1)).difference(holes(points,1.1))
                    parts['frame']=solid(frame_profile,pz+SEAT+1.5,3)
                    upper=cut_controls(solid(gasket_profile,pz+SEAT,1.5),cuts)
                    parts['upper-gasket']=upper;profiles['upper-gasket']=profiles['lower-gasket']
                    body=body.cut(solid(holes(points,1.1),-.1,pz+1))
                    # No floor mounts: entire PCB/plate assembly is carried by gaskets.
                    support='gasket-only plate/PCB module; four external frame bolts; 0.3 mm lower travel stop'
                    Path(output/f'{side}-frame-holes.json').write_text(json.dumps(points,indent=2)+'\n')
                else:
                    body=body.cut(solid(holes(bolts,1.1),-.1,FLOOR+.2))
                    support='original rigid M2 standoffs bypass the external gasket'
                if option!='c-printed-tray-plate':
                    # Metal tray receives a non-metal controller/RF opening through its full height.
                    patch=outer.intersection(rf).buffer(-.25)
                    body=body.cut(solid(rf,-.1,pz+SEAT+6))
                    patch_body=solid(patch,0,FLOOR)
                    patch_wall=patch.difference(cavity)
                    if not patch_wall.is_empty:patch_body=patch_body.fuse(solid(patch_wall,FLOOR,pz-.3-FLOOR))
                    parts['rf-insert']=cut_controls(patch_body,cuts)
                if option=='c-printed-tray-plate':
                    # Thin switch seats plus outside reinforcement retain the existing latch geometry.
                    rim_profile=pcb.buffer(10,join_style=2).difference(pcb.buffer(8.6,join_style=1)).difference(holes(bolts,3.5))
                    top=top.fuse(solid(rim_profile,pz-1,1)).clean();parts['top']=top
                    body=body.cut(solid(rim_profile.buffer(.1),pz-1.1,1.2))
                parts['tray']=body.clean()
                if suspended:
                    height=pz+SEAT+1.5+3
                    sleeve_outer=pcb.buffer(16.5,join_style=2)
                    sleeve_inner=pcb.buffer(14.5,join_style=2)
                    sleeve=solid(sleeve_outer,-4.1,4.1).fuse(solid(sleeve_outer.difference(sleeve_inner),0,height+.3))
                    sleeve=sleeve.fuse(solid(sleeve_outer.difference(pcb.buffer(12.2,join_style=2)),height+.3,1.6))
                    sleeve=sleeve.cut(solid(holes(points,4),-2.5,2.6))
                    sleeve=sleeve.cut(solid(holes(points,3.5),height,3))
                    parts['sleeve']=cut_controls(sleeve,cuts)
            assert outer.covers(pcb)
            cap_envelopes=unary_union([translate(rotate(box(-10,-10,10,10),a,origin=(0,0)),x,y) for x,y,a in keys])
            if suspended:
                assert frame_profile.intersection(cap_envelopes).area<1e-6,('frame/keycap interference',side)
                assert all(not top_outer.buffer(1.1).contains(Point(*p)) for p in points),('frame bolt crosses floating plate',side)
            assert gasket_profile.intersection(pcb).area<1e-7 if not option.startswith('a-') else True
            battery=box(d[7][0]-32,d[7][1]-20,d[7][0]+32,d[7][1]+20)
            assert battery.distance(rf)>=10
            if not option.startswith('a-'):assert cavity.covers(battery)
            # Electronics position and floor material stack retain clearance; suspension adds 2 mm externally.
            spare=16+shift-(13.9+PARAM['damping_thickness'])
            assert spare>=.4997
            report={'variant':option,'side':side,'quantity':1,'support':support,'under_pcb_mm':16+shift,'reserved_stack_spare_mm':round(spare,4),'switch_seat_mm':SEAT,'controller_gap_mm':8,'battery_rf_clearance_mm':battery.distance(rf),'parts':{}}
            for name,shape in parts.items():
                assert shape.isValid() and shape.Volume()>0,(option,side,name)
                if 'gasket' not in name:assert len(shape.Solids())==1,(option,side,name,'disconnected')
                export_step(shape,output/f'{side}-{name}.step')
                cq.exporters.export(shape,str(output/f'{side}-{name}.stl'),tolerance=.08,angularTolerance=.1)
                bb=shape.BoundingBox()
                report['parts'][name]={'dimensions_mm':[round(v,4) for v in (bb.xlen,bb.ylen,bb.zlen)],'volume_mm3':round(shape.Volume(),3),'solids':len(shape.Solids())}
                # Reimport STEP and compare exact CAD volume, rather than claiming a mesh-to-STEP conversion.
                restored=cq.importers.importStep(str(output/f'{side}-{name}.step')).val()
                assert abs(restored.Volume()-shape.Volume())/shape.Volume()<1e-6
            for name,profile in profiles.items():
                # DXF is the XY cutting profile. STEP remains authoritative for pocket depth and reliefs.
                import ezdxf
                doc=ezdxf.new();doc.units=4;m=doc.modelspace()
                for poly in polygons(profile):
                    for ring in [poly.exterior,*poly.interiors]:m.add_lwpolyline(list(ring.coords)[:-1],close=True)
                doc.saveas(output/f'{side}-{name}.dxf')
                normalize_text(output/f'{side}-{name}.dxf')
            records.append(report)
        (output/'checks.json').write_text(json.dumps([r for r in records if r['variant']==option],indent=2)+'\n')
        print(option,'exported left/right CAD',flush=True)
    all_records=[r for option in OPTIONS if (OUT/option/'checks.json').exists() for r in json.loads((OUT/option/'checks.json').read_text())]
    (OUT/'checks.json').write_text(json.dumps(all_records,indent=2)+'\n')
