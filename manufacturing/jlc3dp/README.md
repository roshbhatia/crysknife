# TPU sandwich case

Print one sleeve per half. Each sleeve wraps a flat aluminum bottom plate and a flat clear acrylic top plate.
Four M2 standoffs hold the plates and PCB together. The TPU forms the exterior walls and bottom.
The rigid plates carry the screw loads. The sleeve adds no screw holes.

## Files and suppliers

Upload `left-sleeve.stl` and `right-sleeve.stl` to JLC3DP, quantity one each.
Select FDM, TPU Plastic, Translucent, no surface finish, and no thread inserts.
The 3MF files contain the same geometry for inspection.
Buy the flat plates and damping sheets from [SendCutSend](../sendcutsend/README.md).

| Part | Material | Thickness |
| --- | --- | --- |
| Top plate | Clear acrylic | 1.6002 mm |
| Bottom plate | 5052 aluminum | 3.175 mm |
| Floor damping sheet | Neoprene | 1.6002 mm |
| Sleeve walls | 95A TPU | 2 mm |

The printed resin trays and raised resin plates are no longer part of this design.
The saved account cart still contains the previous six-part resin-and-TPU set.
Do not order that set for this version. It needs only two replacement TPU sleeves from JLC3DP.
The previous sleeve price was $13.84 each. That price does not cover the current model.
A new quote and supplier review remain pending. No order was submitted.
Historical quotes remain in `quotes.json` and the quote screenshots.

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
The PCB retains 16 mm of space above the rigid bottom plate.
Keep the controller face up underneath the PCB, with USB toward the rear.
Keep the battery beside it. Retain the dielectric liner and floor damping sheet.
Leave the controller BOOST bridge open.

Both sleeves and both flat plate pairs export as connected, closed meshes.
Checks cover mirror symmetry, screw holes, switch openings, closed sleeve bottoms, and blind screw-head pockets.
Lip overlap, front and rear retention, keycap clearance, and top screw access pass nominal geometry checks.
Both flat plates extend 1.5 mm farther around the PCB than the earlier drawings.
Switch cutouts and mounting holes remain at their original locations.
The controller and battery stack remains unchanged.

The previews show nominal component envelopes. They do not prove physical fit.
Test switch retention, lip fit, cable access, battery clearance, and peel force on the first prototype.
Supplier tolerance can change retention and installation effort.
No supplier review or physical assembly test has accepted this version.

## Regenerate

From the repository's Nix shell:

```sh
python3 scripts/generate_case.py
python3 scripts/export_printed_case.py
```

Edit `case/printed-sleeve.scad`, `case/sandwich.scad`, and `case/parameters.scad`.
Shared shapes live in `case/sleeve-geometry.scad` and `case/plate-geometry.scad`.
Sleeve exports go here. Plate inspection models and sleeve models go into `out/3d/`.
Fresh images go into `previews/`.
Use `part="sleeved-assembly"` in `case/sandwich.scad` to inspect the complete case.
