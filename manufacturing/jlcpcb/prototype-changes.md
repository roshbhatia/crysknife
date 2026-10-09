# Prototype draft review — 9 October 2026

Both existing drafts have corrected BOM/CPL files. No order, payment, quote acceptance, or production-file approval was made.

| Draft | Assembled boards | Current total | Build time |
| --- | --- | --- | --- |
| [Left](https://cart.jlcpcb.com/smt-order/?pcbFileNo=ce4fe86abaf54f5793728f9febe7a22f) | 5 | $140.75 | PCB 24 hours; assembly 4–5 days |
| [Right](https://cart.jlcpcb.com/smt-order/?pcbFileNo=5197d9831abd41e9b19388283fb1ec54) | 5 | $140.75 | PCB 24 hours; assembly 4–5 days |

Total: $281.50 before shipping and tax. Manual placement confirmation adds $0.45 per half.
Both drafts retain confirmation enabled, automatic confirmation disabled, and the receiver-seating/polarity remark after reload.
JLC resets the quote form’s automatic-confirmation field to null on reload. Recheck “Do not confirm automatically” before any later cart save.
Both current review tabs have that option selected and an explicit false outgoing value.
No eligible discount was applied. The EasyEDA-only coupon does not apply to these KiCad exports.

Each board has all 47 positions selected, across six component types. The stock check passed.
The PCB configuration remains 2-layer, 1.6 mm FR4, white mask, black silk, ENIG, Standard assembly on both faces.
The outline is approximately 144.862 × 103.224 mm. Two 5 mm rails increase the quoted width to 113.22 mm.

## Changes

- Reset: Panasonic C79175 replaces C79174; same footprint, lighter 1.6 N actuation.
- MX sockets: HanElectricity C41430893 replaces Kailh C5184526. The manufacturer and contact finish differ.
- Controller receivers: HCTL C5156451 replaces Mill-Max C5504443. These are sockets, not controllers.
- Leave both nice!nano BOOST bridges open for nominal 100 mA charging. The ALPS power switch has a 300 mA rating.
- Increase the mechanical controller gap from 5 to 8 mm. The receiver/header stack needs at least approximately 7.434 mm.

`placement-corrections.json` defines supplier-specific origins and angles. The generator applies them to the unchanged KiCad footprints.
Socket pickup origins move to the midpoint of the two solder pads. Local translation is −0.6215 mm X, +3.81 mm Y.
That translation rotates with each native footprint, including the thumb keys. Socket supplier angles are `(180 - native_angle) % 360`. This includes bottom-side mirroring and the corrected body orientation.
Diodes and receivers also need supplier angle changes. Power switches rotate 90 degrees; reset switches rotate 180 degrees.
JST connectors retain their native positions. These rules apply only to the selected supplier models.

## Socket orientation recheck

The initial review missed a 180-degree reversal of the socket body. Pads and hole positions alone did not establish the asymmetric body orientation.
All 42 sockets were corrected, reuploaded, and checked after reload. Translation did not change.
Regular sockets now use 180 degrees. Left S20/S21 use 200/130 degrees; right S20/S21 use 160/230 degrees.
The body outlines now match the PCB reference outlines, including the thumb keys.
See [before](../../previews/jlcpcb/socket-body-before.png) and [after](../../previews/jlcpcb/socket-body-after.png).
The visible red reference text rotates with the component model; its reading direction is not an alignment test.

The [socket manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/d953a8b0b623247f3341ebcfbaa2e88f.pdf?productCode=C41430893) specifies 6.35 mm horizontal and 2.54 mm vertical opening spacing.
Those dimensions match the native footprint. The [diode drawing](https://datasheet.lcsc.com/datasheet/pdf/8abd7fc00ebe41ffb03ad1383c10753b.pdf?productCode=C81598) identifies the band as cathode/pin 1.
All 42 native cathode pads connect to rows; anode pads connect to the corresponding switch nets.
Rendered cathode bands match those pads, including all four angled diodes. Diode rotations remain unchanged.

## Verification and limits

Rendered overlays were inspected on both faces of both halves. Checks covered terminals, socket holes, receiver holes, diode cathodes, and switch actuators.
Close-ups covered angled thumb sockets, receiver rows, JST connectors, power switches, and reset switches.
All 94 saved placements match the generated CPL, including layer, selected part code, position, and angle.
All 42 socket pickup origins also match native solder-pad midpoints. The comparison tolerance is 0.0015 mm for the browser readback.
`placement-readback.json` records the reloaded draft data. Manufacturer drawing checks for the substitutions came from the user's handoff.
This review does not replace JLC's final production-file review or a physical first article.

Copper, schematic, pin mapping, firmware, plate geometry, and controller orientation remain unchanged.
Existing native ERC/DRC results are recorded in `out/validation.json`; they were not rerun for these export-only corrections.
The assembly generator and supplier-placement checks passed. Both metal-bottom meshes pass closed-mesh checks.

Physical mating height, cable clearance, insulation, battery plug polarity, charging completion, low-battery recovery, Bluetooth, and typing remain untested.
Test the matrix over USB before connecting batteries. Keep nice!nano underneath, face up, with USB toward the open rear edge.
The receiver openings face away from the carrier. Seat on the metal shoulders, not the plastic housing.
Keep contacts free of solder/flux. Receiver soldering limit is 260°C for 10 seconds.

## Placement images

| Check | Before | After |
| --- | --- | --- |
| Power switch | [Sideways](../../previews/jlcpcb/left-power-candidate.png) | [Aligned](../../previews/jlcpcb/left-power-rotated.png) |
| Reset switch | [Facing inward](../../previews/jlcpcb/left-reset-zero.png) | [Facing rear edge](../../previews/jlcpcb/left-reset-after.png) |
| Receivers | [Wrong rotation](../../previews/jlcpcb/receiver-before-close.png) | [Left](../../previews/jlcpcb/left-receivers-after.png), [right](../../previews/jlcpcb/right-receivers-after.png) |
| Thumb sockets | [Left original overview](../../previews/jlcpcb/left-user-bottom-before.png) | [Left S20](../../previews/jlcpcb/left-thumb-s20-after.png), [left S21](../../previews/jlcpcb/left-thumb-s21-after.png), [right S20](../../previews/jlcpcb/right-thumb-s20-after.png), [right S21](../../previews/jlcpcb/right-thumb-s21-after.png) |

Final full overlays: [left top](../../previews/jlcpcb/left-top-final.png), [left bottom](../../previews/jlcpcb/left-bottom-final.png), [right top](../../previews/jlcpcb/right-top-final.png), [right bottom](../../previews/jlcpcb/right-bottom-final.png).
Final quotes: [left](../../previews/jlcpcb/left-quote-final.png), [right](../../previews/jlcpcb/right-quote-final.png).
