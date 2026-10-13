# TPU sandwich case

Each half uses a printed resin top, a flat resin bottom, and a TPU sleeve.
Four M2 standoffs hold the plates and PCB together. The TPU forms the exterior walls and closed bottom.
The rigid plates carry the screw loads. The sleeve has no screw holes.

## Files and suppliers

Upload `left-plate.3mf`, `right-plate.3mf`, `left-bottom.3mf`, and `right-bottom.3mf` for SLA printing.
Select 8001 Resin, Translucent, Fine Sanding, and No thread.
Upload `left-sleeve.stl` and `right-sleeve.stl` for FDM printing.
Select TPU Plastic, Translucent, no surface finish, and no thread inserts.
The sleeve 3MF files contain the same geometry for inspection.

| Part | Material | Geometry |
| --- | --- | --- |
| Top | 8001 Resin | 1.6002 mm switch seats; 1 mm underside rim |
| Bottom | 8001 Resin | Flat, 3.175 mm thick |
| Sleeve | TPU | 2 mm walls; closed bottom and retaining lip |

Print one of each part per half.
The top has a 1 mm tall, 1.6 mm wide underside rim, giving a 2.6002 mm overall model height.
The rim stays outside the PCB outline and clears the mounting washers and key openings.
The top face stays flat, with 1.6002 mm switch seats.
The sleeve wraps the plate sandwich without a separate rigid tray.

SendCutSend remains an alternative for [flat acrylic tops, aluminum bottoms, and damping sheets](../sendcutsend/README.md).
Do not buy both rigid plate options for the same keyboard.

## Sleeve

The closed bottom is 4.1 mm thick. Four internal blind pockets cover the bottom screw heads.
Each pocket is 8 mm wide and 2.5 mm deep, leaving 1.6 mm of TPU below it.
Use screw heads and protective washers with a combined height no greater than 2.5 mm.

The widened plates provide an edge border for the retaining lip.
The sleeve leaves 0.5 mm nominal clearance around the plate edges.
A 1.6 mm thick lip extends 1.8 mm over the flat top plate edge.
Its underside sits 0.3 mm above the plate.
The lip and upper wall clear 20 mm square keycap envelopes and the top screw washers.
USB, reset, and power openings remain aligned with the PCB components.

Assemble the rigid sandwich first. Stretch the sleeve around it, then roll the lip over the top plate.
Peel off the sleeve to reach the bottom screws.
The sleeve holds the sandwich between its bottom and upper lip.
There is no inner grip band pressing against exposed electronics.
Keep wires clear of the walls, screws, and control openings.

95A TPU is firm and flexible. FDM leaves print texture; translucent TPU is not optically clear.
See [JLC TPU guidance](https://jlc3dp.com/help/article/tpu).

## Stack and checks

Use the four M2 mounting locations and hardware from the SendCutSend assembly guide.
The PCB retains 14 mm of space above the rigid bottom plate.
Keep the controller face up underneath the PCB, with USB toward the rear.
Keep the battery beside it. Retain the dielectric liner and floor damping sheet.
Leave the controller BOOST bridge open.

Both sleeves, reinforced tops, and flat bottoms export as connected, closed meshes.
Checks cover mirror symmetry, screw holes, switch openings, closed sleeve bottoms, and blind screw-head pockets.
Lip overlap, front and rear retention, keycap clearance, and top screw access pass nominal geometry checks.
Switch cutouts and mounting holes remain at their original locations.
The lower stack uses 12 mm standoffs plus 2 mm nylon spacers for the 750 mAh pack.
The sleeve lip and USB/reset/power openings move down 2 mm.
Old cart models and quotes use the taller stack; replace files before requesting a fresh quote.
This printed resin bottom is monolithic; the metal RF opening belongs to the separate F aluminum floor.

The previews show nominal component envelopes.
Test switch retention, lip fit, cable access, battery clearance, and peel force on the first prototype.
Supplier tolerance can change retention and installation effort.

## Regenerate

From the repository's Nix shell:

```sh
python3 scripts/generate_case.py
python3 scripts/export_printed_case.py
```

Edit `case/printed-plate.scad`, `case/printed-sleeve.scad`, `case/sandwich.scad`, and `case/parameters.scad`.
Shared shapes live in `case/sleeve-geometry.scad` and `case/plate-geometry.scad`.
Supplier plate and sleeve exports go here. Inspection models also go into `out/3d/`.
Fresh images go into `previews/`.
Use `part="sleeved-assembly"` in `case/sandwich.scad` to inspect the complete case.
