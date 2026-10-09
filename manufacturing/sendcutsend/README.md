# SendCutSend review files

Each half uses a flat metal bottom plate, rubber sheet, and clear acrylic top plate.
The corners are square. Four M2 standoffs pass through the carrier and join matching holes in the plates.

| File | Material | Thickness | Process |
| --- | --- | --- | --- |
| `*-bottom-flat.dxf` | 5052 H32 aluminum | .063 in / 1.6002 mm | Cut |
| `*-plate.dxf` | Clear acrylic | .063 in / 1.6002 mm | Laser cut |
| `*-damping.dxf` | Neoprene | .063 in / 1.6002 mm | Waterjet cut |
| `switch-fit-coupon.dxf` | Same clear acrylic | Same stock as top plates | Test switch fit first |

All dimensions use millimeters. The metal plates have no bends.
The top plate covers the electronics area. Controllers sit face up beneath the carrier PCBs.
USB, power, and reset remain accessible through the open sides.

Use four round 20 mm M2 standoffs, with a maximum 4 mm body diameter, and four 1 mm nylon shims per half.
The shims sit between the standoffs and the top plate.
Both plates have four matching 2.2 mm holes. The rubber sheet has 4.5 mm clearance holes.
The carrier has 5 mm holes around the standoff bodies.
Use small washers and light screw torque to protect the acrylic.
Check that the screw heads and washers clear the adjacent switch openings.
Choose screw length after measuring the plate, washers, and standoff thread depth.

The rubber lines the metal floor. Add a separate dielectric liner between the metal and electronics.
Secure each battery with foam and an insulating cover. Keep wires clear of screws and edges.

The coupon has four square holes: 13.9, 14.0, 14.1, and 14.2 mm, from left to right.
Test the actual switches, latch retention, and keycap removal with the supplied material.
Set `switch_cutout` in `case/parameters.scad` from that result, then regenerate.
The default is 14 mm. [Acrylic cutting tolerance](https://sendcutsend.com/materials/acrylic/) requires a physical switch-fit check.
[Neoprene stock](https://sendcutsend.com/materials/neoprene/) also requires a thickness check.

Test plate flex, corner stability, controller clearance, and battery fit on the assembled prototype.
These are review files. No supplier quote or production order has been accepted.
