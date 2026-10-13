"""Make comparison sheets and pair-quantity bills from the exported concepts."""
from pathlib import Path
import json,csv
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'manufacturing/enclosures';PRE=ROOT/'previews/enclosures'
font_path=ROOT/'assets/ioskeley-mono-bold.ttf'
def font(n):return ImageFont.truetype(str(font_path),n)
options=[('a-tpu-cnc-plates','A  TPU + CNC plates'),('b-cnc-rigid-tray','B  CNC rigid tray'),('c-printed-tray-plate','C  Printed tray + plate'),('d-suspended-hybrid','D  Suspended hybrid')]
from generate import render, solid, DATA, FLOOR, PCB_Z, PLATE_Z, SEAT, COLORS, SleeveMesh, holes
from shapely.geometry import Polygon,box
import cadquery as cq
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--variant',choices=[o[0] for o in options])
parser.add_argument('--reuse-renders',action='store_true')
args=parser.parse_args()
for key,label in [o for o in options if not args.reuse_renders and (args.variant is None or o[0]==args.variant)]:
    pair=[];sections=[]
    for side,data in DATA.items():
        folder=OUT/key;offset=0 if side=='left' else 195;shift=2 if key.startswith('d-') else 0
        for path in sorted(folder.glob(f'{side}-*.step')):
            name=path.stem[len(side)+1:]
            if name=='pmma-bottom':continue
            shape=cq.importers.importStep(str(path)).val()
            colour=COLORS.get(name,(213,164,93))
            exploded=shape.translate((offset,0,8 if name=='top' else (14 if name=='frame' else 0)))
            pair.append((exploded,colour))
            sliced=shape.intersect(cq.Workplane('XY').box(220,.2,90).translate((0,data[2][0][1],20)).val())
            if sliced.Volume()>.0001:sections.append((sliced.translate((offset,0,0)),colour))
        pcb=solid(Polygon(data[0]).difference(holes(data[2],1.1)),PCB_Z+shift,1.6)
        bx,by=data[7];cx,cy=data[3]
        battery=solid(box(bx-30,by-18,bx+30,by+18),FLOOR+1.6002+.5,7)
        controller=solid(box(cx-9,cy-17,cx+9,cy+17),PCB_Z+shift-9.6,1.6)
        for shape,col in [(pcb,(239,237,225)),(battery,(79,85,98)),(controller,(66,109,145))]:pair.append((shape.translate((offset,0,0)),col))
        if not key.startswith('d-'):
            for bx,by in data[2]:pair.append((cq.Solid.makeCylinder(2.3,16,cq.Vector(bx+offset,by,FLOOR)),(169,169,163)))
        if key.startswith('a-'):pair.append((SleeveMesh(folder/f'{side}-sleeve.stl',offset),(102,169,172)))
    render(pair,PRE/f'{key}.png');render(sections,PRE/f'{key}-section.png',True)
    print(label,'rendered',flush=True)
canvas=Image.new('RGB',(1600,1000),'#f6f5f1');draw=ImageDraw.Draw(canvas)
for i,(key,label) in enumerate(options):
 x=(i%2)*800;y=(i//2)*500
 draw.text((x+25,y+12),label,font=font(25),fill='#24333c')
 im=Image.open(PRE/f'{key}.png');im.thumbnail((785,450));canvas.paste(im,(x+5,y+46))
canvas.save(PRE/'comparison.png')
# Dimensioned support explanation. Horizontal placement is schematic; vertical coordinates follow CAD.
canvas=Image.new('RGB',(1600,950),'#f6f5f1');d=ImageDraw.Draw(canvas)
for i,(key,label) in enumerate(options):
 x=(i%2)*800;y=(i//2)*475
 d.text((x+22,y+12),label,font=font(24),fill='#24333c')
 suspended=i==3;pz=24.275+(2 if suspended else 0);base=y+365;scale=9
 def block(a,b,z,h,c):d.rectangle((x+a,base-(z+h)*scale,x+b,base-z*scale),fill=c,outline='#26333c',width=2)
 # Floor and complete reserved cavity; gasket lives beside that cavity.
 block(55,440,0,3.175,'#879db1')
 block(115,375,3.175,1.6002,'#626367')
 block(145,345,5.2752,7,'#69747e')
 block(75,425,pz-5.1,1.6,'#e5e3d9')
 block(60,440,pz,1.6002,'#a6d9df')
 if i==0:
  block(45,55,-4.1,pz+7.3,'#74aaa8');block(445,455,-4.1,pz+7.3,'#74aaa8');block(45,455,-4.1,4.1,'#74aaa8')
 if not suspended:
  block(92,110,3.175,16,'#8c8d89');block(92,110,pz-3.5,3.5,'#8c8d89')
 else:block(92,110,pz-3.5,3.5,'#8c8d89')
 if i>0:
  block(35,58,3.175,pz-3.475,'#879db1');block(442,465,3.175,pz-3.475,'#879db1')
  block(42,58,pz-1.5,1.5,'#d19d61');block(442,458,pz-1.5,1.5,'#d19d61')
 if suspended:
  block(42,58,pz+1.6002,1.5,'#d19d61');block(442,458,pz+1.6002,1.5,'#d19d61')
  block(25,65,pz+3.1002,3,'#a6d9df');block(435,475,pz+3.1002,3,'#a6d9df')
  block(25,35,3.175,pz-.0748,'#879db1');block(465,475,3.175,pz-.0748,'#879db1')
  for bx in (30,470):d.line((x+bx,base+14,x+bx,base-(pz+6.1002)*scale-4),fill='#35434d',width=4)
 d.text((x+495,y+65),'plate 1.6002 mm',font=font(17),fill='#24333c')
 d.text((x+495,y+103),'PCB gap 3.5 mm',font=font(17),fill='#24333c')
 d.text((x+495,y+141),f'below PCB {18 if suspended else 16} mm',font=font(17),fill='#24333c')
 d.text((x+495,y+179),f'stack spare {2.4998 if suspended else .4998} mm',font=font(17),fill='#24333c')
 if i>0:
  d.text((x+495,y+217),'gasket 2 -> 1.5 mm',font=font(17),fill='#986936')
  d.text((x+495,y+255),'25% nominal squeeze',font=font(17),fill='#986936')
 text='load: plate -> posts -> floor' if not suspended else 'load: plate -> rubber -> shell'
 d.text((x+30,y+414),text,font=font(18),fill='#24333c')
 d.text((x+30,y+443),'schematic; thin layers enlarged' if not suspended else 'outer bolts bypass floating module; stop gap 0.3 mm',font=font(14),fill='#4a545b')
canvas.save(PRE/'support-sections.png')
rows=[
 ['common','Assembled carrier PCB','Existing left/right PCB files; supplier-specific placement approval',2,'required'],
 ['common','nice!nano V2','Genuine controller; BOOST open',2,'required'],
 ['common','Male headers','Mill-Max 350-10-112-00-006000; 12 round pins per strip',4,'required'],
 ['common','Battery','Protected Adafruit 2011; 3.7 V 2000 mAh; verify plug polarity',2,'required'],
 ['common','MX switches','Existing MX footprint; verify actual latch retention',42,'required'],
 ['common','Keycaps','1U; nominal 20 mm keepout',42,'required']
]
rigid=[('M2 female/female standoff','15 mm; 4 mm flats; 5 mm thread depth',8),('Nylon M2 spacer','3 mm long; 4 mm OD; 2.2 mm bore',8),('Nylon M2 washer','0.5 mm; 5.5 mm OD; includes stacked lower shims and head protection',40),('M2 top screw','12 mm',8),('M2 bottom screw','6 mm',8)]
for key,_ in options:
 def add(part,spec,qty,condition='required'):rows.append([key,part,spec,qty,condition])
 if key.startswith('d-'):
  add('Nylon M2 spacer','3 mm long; 4 mm OD; 2.2 mm bore',8)
  add('Nylon M2 washer','0.5 mm; includes PCB gap shims and head protection',40)
  add('M2 module screw','10 mm; joins only plate/PCB',8)
  add('M2 frame screw','35 mm; head/washer height <=2.5 mm',8)
  add('M2 thin nut','1.6 mm high; eight module nuts plus eight outer frame nuts',16)
 else:
  for part,spec,qty in rigid:add(part,spec,qty)
 if not key.startswith('a-'):
  add('Lower gasket cut set','Closed-cell silicone foam; 2.0 +/-0.1 mm free; 3 mm wide; no added adhesive layer',2)
  if key.startswith('d-'):add('Upper gasket cut set','Same foam; 1.5 mm installed height',2)
 add('Floor damping','Existing 1.6002 mm pad; keep full cavity allowance',2)
 add('Dielectric/battery cover','Nonconductive liner within existing protection allowance; no extra cavity layers',2)
 add('Battery foam/retainer','Within existing battery protection envelope; no cell pressure',2)
 if key.startswith(('a-','b-','d-')):add('RF insert retention','Underside-only nonconductive seam bond; flush inner floor',2,'metal bottom/tray only')
 if not key.startswith('a-'):add('Silicone feet','Four per half; external to tray',8,'without TPU sleeve')
with (OUT/'hardware.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['Option','Part','Specification','Quantity for left/right pair','Condition']);w.writerows(rows)
records=json.loads((OUT/'checks.json').read_text())
with (OUT/'parts.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['Option','File stem','Quantity','X mm','Y mm','Z mm','Condition'])
 for rec in records:
  for name,p in rec['parts'].items():
   condition='cut 2 mm sheet; STEP shows installed 1.5 mm' if 'gasket' in name else 'required'
   if name=='pmma-bottom':condition='replaces metal bottom and RF insert'
   if rec['variant'].startswith('a-') and name in ('bottom','rf-insert'):condition='metal-bottom choice only'
   if rec['variant'].startswith('d-') and name=='sleeve':condition='optional custom TPU exterior'
   w.writerow([rec['variant'],rec['side']+'-'+name,1,*p['dimensions_mm'],condition])
  if rec['variant'].startswith('a-'):w.writerow([rec['variant'],rec['side']+'-sleeve',1,158.180136,117.523056,31.875199,'original TPU sleeve'])
print('Comparison, support sections, hardware and pair quantities exported')
