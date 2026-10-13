"""Export switch-fit coupons with the same latch seats and CNC corner reliefs."""
from pathlib import Path
import cadquery as cq
from generate import OUT, SEAT, solid, export_step, normalize_text
from shapely.geometry import box,Point
import ezdxf
folder=OUT/'coupons';folder.mkdir(parents=True,exist_ok=True)
for process in ('cnc','resin'):
    profile=box(-45,-12,45,12)
    shape=solid(profile,0,SEAT)
    for index,width in enumerate((13.9,14,14.1,14.2)):
        x=-30+20*index
        hole=box(x-width/2,-width/2,x+width/2,width/2)
        tool=cq.Workplane('XY').rect(width,width).extrude(SEAT+.2).translate((x,0,-.1)).val()
        if process=='cnc':
            for sx in (-1,1):
                for sy in (-1,1):
                    cx,cy=x+sx*width/2,sy*width/2
                    tool=tool.fuse(cq.Solid.makeCylinder(.5,SEAT+.2,cq.Vector(cx,cy,-.1)))
                    hole=hole.union(Point(cx,cy).buffer(.5,resolution=12))
        shape=shape.cut(tool);profile=profile.difference(hole)
    if process=='resin':shape=shape.fuse(solid(box(-45,-12,45,12).difference(box(-43.4,-10.4,43.4,10.4)),-1,1))
    assert shape.isValid() and len(shape.Solids())==1
    stem=folder/f'{process}-switch-fit'
    export_step(shape,stem.with_suffix('.step'))
    cq.exporters.export(shape,str(stem.with_suffix('.stl')),tolerance=.08,angularTolerance=.1)
    doc=ezdxf.new();doc.units=4;m=doc.modelspace()
    for ring in [profile.exterior,*profile.interiors]:m.add_lwpolyline(list(ring.coords)[:-1],close=True)
    doc.saveas(stem.with_suffix('.dxf'))
    normalize_text(stem.with_suffix('.dxf'))
print('CNC and reinforced-resin coupons: 13.9 / 14.0 / 14.1 / 14.2 mm openings')
