# Printed case prototype

Upload the four STL files for one complete keyboard: one left tray, one right tray, and one plate per half.
The 3MF files contain the same geometry for inspection. Edit the OpenSCAD sources, then regenerate the exports.

## Finish and quote

Live JLC3DP quotes checked on 2026-10-09, USD, one of each part:

| 8001 resin finish | Each tray | Each plate | Four parts | Build time |
| --- | ---: | ---: | ---: | --- |
| Translucent, Fine Sanding | $14.00 | $3.44 | $34.88 | 4 days |
| Transparent, Oil Spraying | $15.86 | $5.09 | $41.90 | 5 days |

The shipping estimate was $10.59, with 8–13 business days in transit.
The address was not confirmed. Tax and supplier review can change the final price.
No coupon was applied. No order was submitted.

The open browser quote uses Translucent with Fine Sanding, quantity one per file.
Thread inserts are disabled. The product description is Plastic Keyboard Enclosure.
This is a guest quote, not a saved account draft.

Fine sanding is the closest available option to a frosted, smooth matte finish.
8001 is hard resin, not a rubber coating. Oil spraying gives a glossy clear finish.
Transparent resin can contain bubbles or surface texture; optical clarity is not guaranteed.
See [8001 resin guidance](https://jlc3dp.com/help/article/photosensitive-8001-resin).

## Assembly

Each tray replaces the metal bottom. The PCB and plate retain their existing four M2 hole centers.
Use metal standoffs, washers, and the existing upper spacers. Do not thread screws into the resin.
Screws enter from the top and bottom. Tighten lightly; excessive force can crack resin.

The floor remains 3.175 mm thick. The PCB has 16 mm of space beneath it, measured from the tray floor.
The cavity leaves 0.6 mm around the PCB. Nominal walls are 1.9 mm thick.
USB has a rounded rear opening. Separate notches give access to reset and power.
Keep the controller face up beneath the PCB, with its USB port toward the rear.
Keep the battery beside the controller. Retain the insulation and damping layer from the assembly guide.
Leave the controller BOOST bridge open.

The plate keeps 14 mm switch openings and 1.6002 mm switch and screw seats.
A 1 mm outer rim raises its overall height to 2.6002 mm for JLC's minimum model size.
The rim clears the nominal keycap envelopes and screw washers.
The tray stops 0.3 mm below the plate; the standoffs set the plate height.

## Validation and limits

All four models are connected, closed meshes. Both plates have 21 switch openings and four M2 holes.
Tray floor holes, PCB cavity clearance, and mirrored geometry pass the export checks.
The original sandwich generator still passes its existing mechanical checks.
The previews show nominal component envelopes, not a physical assembly test.

JLC's quoting page accepted the model sizes and returned prices. Factory acceptance remains pending.
Large flat resin parts can warp. Print tolerance can affect switch clips and screw holes.
Test the switch fit, cable opening, controller stack, battery fit, and finish on the first prototype.
Do not treat this quote as production qualification.

## Regenerate

From the repository's Nix shell:

```sh
python3 scripts/generate_case.py
python3 scripts/export_printed_case.py
```

The sources are `case/printed-tray.scad`, `case/printed-plate.scad`, and `case/parameters.scad`.
Shared plate geometry lives in `case/plate-geometry.scad`.
Exports go here and into `out/3d/`; fresh images go into `previews/`.
Use `part="printed-assembly"` in `case/sandwich.scad` to inspect the assembled stack.
