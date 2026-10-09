# Printed case prototype

Upload four resin parts and two TPU sleeves for one complete keyboard: one tray, one plate, and one sleeve per half.
The 3MF files contain the same geometry for inspection. Edit the OpenSCAD sources, then regenerate the exports.

## Finish and quote

Live JLC3DP quotes checked on 2026-10-09, USD, one of each rigid resin part:

| 8001 resin finish | Each tray | Each plate | Four parts | Build time |
| --- | ---: | ---: | ---: | --- |
| Translucent, Fine Sanding | $14.00 | $3.44 | $34.88 | 4 days |
| Transparent, Oil Spraying | $15.86 | $5.09 | $41.90 | 5 days |

The four resin parts alone had a $10.59 shipping estimate.
The two full-bottom TPU sleeves cost $13.84 each, $27.68 for the pair, with a three-day build time.
The saved cart uses the previous sleeves without retaining lips. Its six-part quote is $62.56: two matte resin trays, two matte resin plates, and two translucent TPU sleeves.
Combined build time is four days. Shipping is estimated at $15.48, with 8–13 business days in transit.
The address was not confirmed. Tax and supplier review can change the final price.
No coupon was applied. No order was submitted.

The account cart contains six parts, quantity one per file.
Replace its two sleeve files with the new lip versions and recalculate before ordering.
The resin parts use Translucent with Fine Sanding. The sleeves use translucent TPU with no surface finish.
Thread inserts are disabled. The sleeves use the Plastic Enclosure product category.
The user saved this quote to the account cart. Current sleeve geometry is newer than that quote.

Fine sanding is the closest available option to a frosted, smooth matte finish.
8001 is hard resin, not a rubber coating. Oil spraying gives a glossy clear finish.
Transparent resin can contain bubbles or surface texture; optical clarity is not guaranteed.
See [8001 resin guidance](https://jlc3dp.com/help/article/photosensitive-8001-resin).

## Removable sleeves

Each translucent 95A TPU sleeve wraps the rigid tray sides and has a full 4.1 mm bottom.
The bottom has no through-holes. Four internal 8 mm blind recesses cover the screw heads.
The sleeve uses no adhesive or additional fasteners.
Walls are 2 mm thick, with 0.5 mm nominal clearance around the rigid tray.
A 4 mm tall inner grip band has 0.2 mm nominal interference against the tray.
The TPU must flex at this band. Retention force and installation effort remain untested.
Use bottom screw heads and washers with a combined height no greater than 2.5 mm.
The recesses leave 1.6 mm of TPU beneath the screw heads, before print tolerance.
Peel off the sleeve to reach the bottom screws.
A 1.6 mm thick retaining lip extends 1.2 mm over the plate edge.
Its underside clears the raised plate rim by 0.3 mm. It does not set PCB or switch height.
The lip and upper sleeve wall clear 20 mm square keycap envelopes and the top screw washers.
The rigid tray and plate shapes remain unchanged.
USB, power, and reset openings are enlarged by 1 mm around the tray openings.

Assemble the rigid keyboard first. Stretch the sleeve around it, then roll the lip over the plate edge.
Peel the lip away to remove the sleeve. Do not lever against the resin with a metal tool.
The lip provides geometric retention. Grip force, print tolerance, and installation effort still need a prototype test.
TPU gives a flexible exterior. FDM leaves print texture, and translucent TPU is not optically clear.
The 95A hardness is firm rubber, not a foam cushion. See [JLC TPU guidance](https://jlc3dp.com/help/article/tpu).

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

All six models are connected, closed meshes. Both plates have 21 switch openings and four M2 holes.
Tray floor holes, PCB cavity clearance, and mirrored geometry pass the export checks.
Sleeve cavity clearance, mirrored geometry, and closed bottoms and blind screw-head recesses also pass.
Lip overlap, front and rear retention, keycap clearance, and top screw access pass nominal geometry checks.
The rigid tray and plate shapes remain unchanged. Shared parameters define the raised plate rim height.
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

The sources are `case/printed-tray.scad`, `case/printed-plate.scad`, `case/printed-sleeve.scad`, `case/printed-parameters.scad`, and `case/parameters.scad`.
Shared shapes live in `case/plate-geometry.scad` and `case/tray-geometry.scad`.
Exports go here and into `out/3d/`; fresh images go into `previews/`.
Use `part="printed-assembly"` in `case/sandwich.scad` to inspect the assembled stack.
