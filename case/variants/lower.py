"""Export a reversible thin-floor rigid sandwich without lowering electronics clearance."""
from pathlib import Path
import json,csv
import cadquery as cq
import ezdxf
from shapely.geometry import Polygon,box,Point
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
from generate import ROOT,DATA,PARAM,solid,holes,export_step,normalize_text
OUT=ROOT/'manufacturing/enclosures/e-thin-rigid-sandwich'
OUT.mkdir(parents=True,exist_ok=True)
FLOOR=1.6002
FEET=2.5
UNDER=PARAM['standoff_height']+PARAM['standoff_shim']
PCB_Z=FLOOR+UNDER
PLATE_Z=PCB_Z+PARAM['pcb_thickness']+PARAM['plate_to_pcb_gap']
if __name__ == '__main__':
    reports=[]
    left_feet=None
    for side,data in DATA.items():
        pcb=Polygon(data[0]);outer=pcb.buffer(PARAM['outline_expansion'],join_style=2)
        mounts=holes(data[2],PARAM['bolt_diameter']/2)
        cutouts=unary_union([translate(rotate(box(-7,-7,7,7),angle,origin=(0,0)),x,y) for x,y,angle in data[1]])
        cx,cy=data[3];rf=box(cx-14,cy-23,cx+14,cy+23)
        profiles={'top':outer.difference(mounts).difference(cutouts),
                  'bottom':outer.difference(mounts).difference(rf),
                  'rf-insert':outer.intersection(rf).buffer(-.25)}
        parts={name:solid(profile,PLATE_Z if name=='top' else 0,PARAM['plate_thickness'] if name=='top' else FLOOR) for name,profile in profiles.items()}
        assert UNDER==16
        assert UNDER-(13.9+PARAM['damping_thickness'])>=.4997
        assert UNDER-PARAM['controller_gap']-PARAM['controller_board_thickness']-PARAM['damping_thickness']>=4.79
        assert profiles['top'].intersection(cutouts).area<1e-7
        assert parts['bottom'].intersect(solid(rf,-.1,FLOOR+.2)).Volume()<1e-5
        for name,shape in parts.items():
            assert shape.isValid() and len(shape.Solids())==1,(side,name)
            export_step(shape,OUT/f'{side}-{name}.step')
            cq.exporters.export(shape,str(OUT/f'{side}-{name}.stl'),tolerance=.08,angularTolerance=.1)
            roundtrip=cq.importers.importStep(str(OUT/f'{side}-{name}.step')).val()
            assert abs(shape.Volume()-roundtrip.Volume())/shape.Volume()<1e-6
            doc=ezdxf.new();doc.units=4;m=doc.modelspace()
            profile=profiles[name]
            for ring in [profile.exterior,*profile.interiors]:m.add_lwpolyline(list(ring.coords)[:-1],close=True)
            path=OUT/f'{side}-{name}.dxf';doc.saveas(path);normalize_text(path)
        if side=='left':
            candidates=[]
            x0,y0,x1,y1=outer.bounds
            for x in range(int(x0)+5,int(x1)-4,2):
                for y in range(int(y0)+5,int(y1)-4,2):
                    point=Point(x,y)
                    if profiles['bottom'].covers(point.buffer(4.2)) and point.distance(rf)>=6 and all(point.distance(Point(*b))>=7.3 for b in data[2]):candidates.append(point)
            centre=pcb.centroid
            left_feet=[]
            for sx,sy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                quadrant=[p for p in candidates if (p.x-centre.x)*sx>0 and (p.y-centre.y)*sy>0]
                point=max(quadrant,key=lambda p:p.distance(centre));left_feet.append((point.x,point.y))
            from shapely.geometry import MultiPoint
            assert MultiPoint(left_feet).convex_hull.contains(centre),'Foot polygon must contain PCB centroid'
            assert all(MultiPoint(left_feet).convex_hull.buffer(4).covers(Point(x,y)) for x,y,_ in data[1]),'Foot contact footprint must support switch centres'
        feet=left_feet if side=='left' else [(-x,y) for x,y in left_feet]
        assert all(profiles['bottom'].covers(Point(*p).buffer(4.2)) for p in feet)
        (OUT/f'{side}-feet.json').write_text(json.dumps({'positions_mm':feet,'reference_diameter_mm':8,'installed_height_mm':FEET,'actual_foot_selected':False},indent=2)+'\n')
        top_engagement=12-(PARAM['plate_thickness']+.5+3.5+1.6+1)
        bottom_engagement=4-(FLOOR+.5)
        assert 1.5<=bottom_engagement<=5
        reports.append({'side':side,'floor_mm':FLOOR,'feet_mm':FEET,'under_pcb_mm':UNDER,
                        'plate_top_from_desk_mm':PLATE_Z+PARAM['plate_thickness']+FEET,
                        'reserved_stack_spare_mm':UNDER-(13.9+PARAM['damping_thickness']),
                        'controller_floor_gap_above_pad_mm':UNDER-8-1.6-PARAM['damping_thickness'],
                        'lower_screw_mm':4,'lower_thread_engagement_mm':bottom_engagement,
                        'upper_thread_engagement_mm':top_engagement,'maximum_bottom_head_washer_mm':2.1,
                        'desk_clearance_under_fastener_mm':FEET-2.1,
                        'pcb_xy_and_switch_geometry_unchanged':True,'physical_fit_verified':False,
                        'parts':{n:{'volume_mm3':s.Volume(),'dimensions_mm':[s.BoundingBox().xlen,s.BoundingBox().ylen,s.BoundingBox().zlen]} for n,s in parts.items()}})
    for name in parts:assert abs(reports[0]['parts'][name]['volume_mm3']-reports[1]['parts'][name]['volume_mm3'])<.05
    (OUT/'checks.json').write_text(json.dumps(reports,indent=2)+'\n')
    rows=[('clear acrylic top plate','1.6002 mm; unchanged 14 mm square seats',2),
          ('5052 H32 aluminum bottom','1.6002 mm; preserve RF opening; deburr both faces',2),
          ('PMMA RF insert','1.6002 mm; flush inner floor; exterior seam retention',2),
          ('M2 metal female/female standoff','15 mm; 4 mm flats; minimum 5 mm thread depth',8),
          ('M2 nylon spacer','3 mm; 4 mm OD; 2.2 mm bore',8),
          ('M2 nylon washer','0.5 mm; 5.5 mm OD; includes shims and head protection',40),
          ('M2 top screw','12 mm; verify 3.7998 mm engagement',8),
          ('M2 bottom screw','4 mm; verify 1.8998 mm engagement; head plus washer <=2.1 mm',8),
          ('non-slip foot','2.5 mm installed height; 4 per half; control compression/desk clearance',8),
          ('floor damping pad','existing 1.6002 mm profile; no new internal layer',2),
          ('battery retention and dielectric cover','within existing allowance; no cell pressure or exposed contacts',2),
          ('RF insert retention','underside-only nonconductive seam bond; no extra interior thickness',2)]
    with (OUT/'hardware.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Part','Specification','Quantity for complete pair']);w.writerows(rows)
    print('E: plate top 26.8004 mm above desk; 16 mm internal clearance retained; pair exported')
