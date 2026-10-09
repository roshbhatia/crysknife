# Supplier review requirements

Scope includes JLCPCB assembly and SendCutSend flat case parts for a physical prototype.
No supplier request has been sent, no quote is accepted, and no order has been placed.
Generated files are quote drafts until these requirements receive a documented response.

## JLCPCB request draft

Please quote both separate fridakeys halves from the supplied revision.
Use 2-layer, 1.6 mm FR4, white solder mask, black silkscreen on both faces, and an accepted surface finish.
Please assemble every carrier component: 21 MX hotswap sockets, 21 polarized diodes, two controller receiver strips, power/reset switches, and JST-PH connector per half.
This requires two-face SMT and through-hole assembly.

Please confirm:

- Exact part availability, substitutions, pre-order or consignment requirements, and minimum assembly quantity for each half.
- C5504443 Mill-Max receiver sourcing, wave/selective/manual solder process, parallel alignment, and contact protection.
- The supplied footprint dimensions against each current manufacturer drawing.
- Pickup offsets and rotations in the assembly viewer, especially MX sockets and the bottom battery connector.
- Diode cathode orientation, connector pin 1, power-switch positions, reset locating bosses, and 1 mm finished controller holes.
- Acceptance of the 0.2 mm minimum black artwork features on white mask, without removal of the mouth or title.
- Filled copper and the solid right battery GND pad against the soldering process.
- AOI, bare-board electrical test, and assembly inspection coverage.

Optional service: prepare two supplied genuine nice!nano V2 modules with four matching Mill-Max 350-10-112-00-006000 male header strips.
Please close the 500 mA BOOST bridge on each module and verify orientation, continuity, shorts, insertion, and charging current.
Keep the carrier receiver contacts free of solder.
If this module preparation is unavailable, deliver assembled carriers with empty receiver sockets and state the omitted work clearly.
The builder will plug in the batteries and switches; the PCB factory should not solder switch bodies or lithium cells.

Please return the reviewed placement images, exact BOM/CPL revision, fabrication revision, quantities, price, lead time, and unresolved exceptions.
Catalog support for wave soldering is not acceptance of this particular design.

## SendCutSend request draft

Please review the supplied left/right closed DXF contours at 1:1 millimeter scale.
The case is a flat sandwich without printed parts.
Quote nonconductive 3 mm bottom/spacer/bezel materials and a switch plate close to 1.5 mm, subject to actual stock thickness.
There are six spacer rings per half, one bottom, one plate, and one bezel.
Gasket contours need a material that achieves 1 mm lower and 0.5 mm upper compressed thickness at the agreed clamp load.

Please confirm minimum holes, webs, edge margins, cut tolerance, actual thickness range, and cosmetic face orientation.
Check 14 mm MX switch cutouts and the nominal 2.2 mm M2 clearance holes against the actual switch and hardware.
Do not substitute a thickness without updating and checking the full stack.
The published acrylic cutting tolerance is ±0.009 inches; nominal 3 mm layers do not establish the assembled stack height.

## Acceptance record

Store the supplier response, quote ID, approved files and SHA256 checksums, assembly preview, and exceptions beside the prototype results.
A quote that leaves footprint, rotation, polarity, thickness, or socket preparation unresolved does not close the release gate.
