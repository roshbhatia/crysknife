"""Render installed side profiles at a common scale and report explicit height datums."""
from pathlib import Path
import json,re,csv
import cadquery as cq
from shapely.geometry import Polygon,box
from PIL import Image,ImageDraw,ImageFont
from generate import ROOT,DATA,PARAM,solid,render,COLORS,holes
from lower import FLOOR as THIN_FLOOR,FEET as FEET_HEIGHT,PLATE_Z as THIN_PLATE_Z
assert PARAM['pcb_thickness']==1.6 and PARAM['plate_to_pcb_gap']==3.5, 'Recheck height datums after changing the carrier stack'
OUT=ROOT/'manufacturing/enclosures'
PRE=ROOT/'previews/enclosures/heights';PRE.mkdir(parents=True,exist_ok=True)
fontpath=ROOT/'assets/ioskeley-mono-bold.ttf'
def font(size):return ImageFont.truetype(str(fontpath),size)

class Mesh:
    def __init__(self,path,desk):self.path,self.desk=path,desk
    def tessellate(self,*args):
        vertices=[cq.Vector(float(y),-float(x),float(z)+self.desk) for x,y,z in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',self.path.read_text())]
        return vertices,[tuple(range(i,i+3)) for i in range(0,len(vertices),3)]

baseline_floor=PARAM['bottom_thickness']
base_pcb=baseline_floor+16
base_plate=base_pcb+1.6+3.5
cases=[('e-thin-rigid-sandwich','E  Thin rigid sandwich',FEET_HEIGHT,THIN_FLOOR,16,False),
       ('flat-baseline','Flat 3.175 mm baseline',FEET_HEIGHT,baseline_floor,16,False),
       ('a-tpu-cnc-plates','A  Original TPU sleeve',4.1,baseline_floor,16,True),
       ('b-cnc-rigid-tray','B  CNC rigid tray',FEET_HEIGHT,baseline_floor,16,False),
       ('c-printed-tray-plate','C  Printed rigid tray',FEET_HEIGHT,baseline_floor,16,False),
       ('d-suspended-hybrid','D  Suspension without TPU',FEET_HEIGHT,baseline_floor,18,False),
       ('d-suspended-hybrid-tpu','D  Suspension with TPU',4.1,baseline_floor,18,True)]
records=[]
for key,title,desk,floor,under,tpu in cases:
    option=key.removesuffix('-tpu')
    side='left';data=DATA[side];shapes={}
    if key=='flat-baseline':
        shapes['bottom']=cq.importers.importStep(str(OUT/'a-tpu-cnc-plates/left-pmma-bottom.step')).val()
        shapes['top']=cq.importers.importStep(str(OUT/'e-thin-rigid-sandwich/left-top.step')).val().translate((0,0,baseline_floor-THIN_FLOOR))
    else:
        for path in (OUT/option).glob('left-*.step'):
            name=path.stem[len('left-'):]
            if name=='pmma-bottom' or name=='sleeve' and not tpu:continue
            shapes[name]=cq.importers.importStep(str(path)).val()
    parts=[]
    top=floor+under+1.6+3.5+PARAM['plate_thickness']
    front=min(shape.BoundingBox().ymin for shape in shapes.values())
    front_slab=cq.Workplane('XY').box(250,1,90).translate((0,front+.5,30)).val()
    front_heights=[]
    for name,shape in shapes.items():
        slice=shape.intersect(front_slab)
        if slice.Volume()>1e-7:front_heights.append(slice.BoundingBox().zmax+desk)
        parts.append((shape.translate((0,0,desk)).rotate((0,0,0),(0,0,1),-90),COLORS.get(name,(210,150,80))))
    if key=='a-tpu-cnc-plates':
        path=OUT/'a-tpu-cnc-plates/left-sleeve.stl'
        values=[tuple(map(float,v)) for v in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',path.read_text())]
        miny=min(v[1] for v in values)
        front_heights=[max(v[2]+desk for v in values if v[1]<miny+1)]
        parts.append((Mesh(path,desk),COLORS['sleeve']))
    pcb_z=floor+under
    pcb=solid(Polygon(data[0]).difference(holes(data[2],1.1)),pcb_z,1.6)
    bx,by=data[7];cx,cy=data[3]
    battery=solid(box(bx-30,by-18,bx+30,by+18),floor+PARAM['damping_thickness']+.5,7)
    controller=solid(box(cx-9,cy-17,cx+9,cy+17),pcb_z-9.6,1.6)
    for shape,color in [(pcb,(239,237,225)),(battery,(79,85,98)),(controller,(66,109,145))]:
        parts.append((shape.translate((0,0,desk)).rotate((0,0,0),(0,0,1),-90),color))
    if under==16:
        for x,y in data[2]:
            for z,h,r,col in [(floor,15,2.3,(160,163,162)),(floor+15,1,2.75,(225,225,215)),(pcb_z+1.6,.5,2.75,(225,225,215)),(pcb_z+2.1,3,2,(225,225,215))]:
                support=cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z+desk)).rotate((0,0,0),(0,0,1),-90)
                parts.append((support,col))
    if not tpu:
        if key=='e-thin-rigid-sandwich':points=json.loads((OUT/option/'left-feet.json').read_text())['positions_mm']
        else:
            # Reference contact pads on the exterior floor, not chosen production feet.
            points=json.loads((OUT/'e-thin-rigid-sandwich/left-feet.json').read_text())['positions_mm']
        for x,y in points:
            foot=cq.Solid.makeCylinder(4,desk,cq.Vector(x,y,0))
            parts.append((foot.rotate((0,0,0),(0,0,1),-90),(66,77,82)))
    render(parts,PRE/f'{key}-side.png',True,bounds=((-80,-50),(80,2)))
    record={'id':key,'title':title,'desk_to_front_edge_mm':round(max(front_heights),4),
            'desk_to_plate_top_mm':round(top+desk,4),'example_keycap_top_mm':round(top+desk+10,4),
            'illustrative_keycap_band_mm':[round(top+desk+8,4),round(top+desk+12,4)],
            'foot_or_tpu_desk_contact_mm':desk,'floor_mm':floor,'under_pcb_mm':under,
            'datums':'Desk contact plane at rest; front = highest shell/plate edge in first 1 mm from min Y, excluding keys and screw heads; plate = upper switch-seat surface',
            'caps':'Illustrative H=10 mm above plate; shaded band H=8..12 mm. Not measured or selected Outemu/keycap dimensions.',
            'desk_contact':'TPU sole thickness' if tpu else 'Reference feet at 2.5 mm installed height; no selected foot SKU',
            'physical_height_measured':False}
    records.append(record)
# Installed E assembly, no exploded spacing and no simulated chosen keycaps.
pair=[]
folder=OUT/'e-thin-rigid-sandwich'
for side,data in DATA.items():
    dx=0 if side=='left' else 195
    for path in folder.glob(f'{side}-*.step'):
        name=path.stem[len(side)+1:];shape=cq.importers.importStep(str(path)).val()
        pair.append((shape.translate((dx,0,FEET_HEIGHT)),COLORS.get(name,(160,208,220))))
    floor=THIN_FLOOR;pcb_z=floor+16
    shape=solid(Polygon(data[0]).difference(holes(data[2],1.1)),pcb_z,1.6)
    pair.append((shape.translate((dx,0,FEET_HEIGHT)),(239,237,225)))
    bx,by=data[7];cx,cy=data[3]
    for shape,col in [(solid(box(bx-30,by-18,bx+30,by+18),floor+1.6002+.5,7),(79,85,98)),(solid(box(cx-9,cy-17,cx+9,cy+17),pcb_z-9.6,1.6),(66,109,145))]:pair.append((shape.translate((dx,0,FEET_HEIGHT)),col))
    for x,y in data[2]:
        pair.append((cq.Solid.makeCylinder(2.3,16,cq.Vector(x+dx,y,floor+FEET_HEIGHT)),(160,163,162)))
        pair.append((cq.Solid.makeCylinder(2,3.5,cq.Vector(x+dx,y,pcb_z+1.6+FEET_HEIGHT)),(225,225,215)))
    for x,y in json.loads((folder/f'{side}-feet.json').read_text())['positions_mm']:
        pair.append((cq.Solid.makeCylinder(4,FEET_HEIGHT,cq.Vector(x+dx,y,0)),(66,77,82)))
render(pair,PRE/'e-assembled.png')
# Same pixel/mm scale in all panels. Every solid is in its installed location.
canvas=Image.new('RGB',(1600,1710),'#f6f5f1');draw=ImageDraw.Draw(canvas)
draw.text((20,12),'ASSEMBLED HEIGHTS  |  no exploded gaps  |  common scale',font=font(25),fill='#24333c')
draw.text((20,46),'Caps: +10 mm example; shaded +8..12 mm band is illustrative, not chosen switch/keycap dimensions.',font=font(15),fill='#624a23')
scale=1430/160*.5
for i,record in enumerate(records):
    x=i%2*800;y=85+i//2*400
    draw.text((x+20,y),record['title'],font=font(23),fill='#24333c')
    im=Image.open(PRE/f"{record['id']}-side.png");im=im.resize((750,360));canvas.paste(im,(x+5,y+28))
    # Renderer origin (35,35), world v=-z minimum=-50. Reduce image by one half.
    desk_y=y+28+(35+50*(1430/160))*.5
    lo=record['illustrative_keycap_band_mm'][0];hi=record['illustrative_keycap_band_mm'][1]
    draw.rectangle((x+100,desk_y-hi*scale,x+570,desk_y-lo*scale),outline='#ab7839',width=2)
    for xx in range(x+100,x+570,12):draw.line((xx,desk_y-record['example_keycap_top_mm']*scale,xx+6,desk_y-record['example_keycap_top_mm']*scale),fill='#ab7839',width=2)
    draw.line((x+60,desk_y,x+600,desk_y),fill='#34434d',width=2)
    draw.text((x+60,desk_y+3),'desk datum',font=font(13),fill='#34434d')
    for xx,height,color in [(x+620,record['desk_to_front_edge_mm'],'#536b7b'),(x+655,record['desk_to_plate_top_mm'],'#257779'),(x+690,record['example_keycap_top_mm'],'#ab7839')]:
        yy=desk_y-height*scale;draw.line((xx,desk_y,xx,yy),fill=color,width=2)
        for end in (desk_y,yy):draw.line((xx-4,end,xx+4,end),fill=color,width=2)
    text=f"front {record['desk_to_front_edge_mm']:.2f} | plate {record['desk_to_plate_top_mm']:.2f} | cap example {record['example_keycap_top_mm']:.2f} mm"
    draw.text((x+20,y+327),text,font=font(15),fill='#24333c')
    draw.text((x+20,y+351),'CAD dimensions; foot compression and actual cap height require measurement',font=font(12),fill='#58636b')
canvas.save(PRE/'assembled-comparison.png')
(OUT/'height-review.json').write_text(json.dumps(records,indent=2)+'\n')
with (OUT/'height-review.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['Variant','Desk-to-front mm','Desk-to-plate-top mm','Example cap top H=10 mm','Desk contact mm','Physical height measured'])
    for r in records:w.writerow([r['title'],r['desk_to_front_edge_mm'],r['desk_to_plate_top_mm'],r['example_keycap_top_mm'],r['foot_or_tpu_desk_contact_mm'],False])
print('Seven installed-height profiles and common-scale comparison exported')
