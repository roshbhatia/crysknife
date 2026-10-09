# SendCutSend review files

Each half uses a bent bottom plate, a flat damping sheet, and a clear top plate.
Six M2 standoffs join the plates. The controller side stays open.

| File | Material | Thickness | Process |
| --- | --- | --- | --- |
| `*-bottom-bent.dxf` | 5052 H32 aluminum | .063 in / 1.6002 mm | Cut; both side flanges bend up 90 degrees |
| `*-plate.dxf` | Clear acrylic | .063 in / 1.6002 mm | Laser cut |
| `*-damping.dxf` | Neoprene | .063 in / 1.6002 mm | Waterjet cut |
| `switch-fit-coupon.dxf` | Same clear acrylic | Same stock as top plates | Test switch fit before cutting the final plates |

The bottom DXFs include two straight bend-center lines on the same layer as the cut contours.
Check that the quote viewer identifies those lines as bends.
The `*-bends.json` files specify direction, radius, deduction, and coordinates.
The blue lines in `*-bend-lines.svg` are review guides. Do not submit those SVGs as cutting files.
All dimensions use millimeters. Confirm both bends point up in the vendor's formed preview.
The [bend table](https://sendcutsend.com/bending-calculator/) supplies the .035 in radius and .096 in deduction.
The [file guide](https://sendcutsend.com/services/cnc-bending/) explains bend-line setup and press-brake limits.

Use six 20 mm M2 standoffs and six 1 mm nylon shims per half.
The shims sit between the standoffs and the top plate.
Both plates have six matching 2.2 mm holes. The damping sheet has 4.5 mm clearance holes.
Use washers and light screw torque to protect the acrylic.
Choose screw length after measuring the plate and washer stack and the standoff thread depth.

The rubber lines the metal floor. It damps the floor; it does not make the top plate float.
Add a dielectric liner between the metal and electronics. Do not assume this rubber grade provides electrical insulation.
Secure the battery with foam and an insulating cover. Keep wires away from screws and bent edges.

The coupon has four square holes, from left to right: 13.9, 14.0, 14.1, and 14.2 mm.
Test the actual Outemu switches, latch retention, and keycap removal with the supplied sheet.
Set `switch_cutout` in `case/parameters.scad` from that result, then regenerate.
The default is 14 mm. [Acrylic cutting tolerance](https://sendcutsend.com/materials/acrylic/) is wider than a typical switch fit allowance.
A physical coupon and supplier confirmation must establish the final hole size and plate thickness.
[Neoprene stock](https://sendcutsend.com/materials/neoprene/) also requires a thickness check.

The model reserves a protected 2000 mAh battery under each PCB.
Controller height, switch seating, battery dimensions, gasket thickness, and bend clearance remain physical test gates.
These are review files. No quote or production order has been accepted.
