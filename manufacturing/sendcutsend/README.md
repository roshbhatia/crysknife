# SendCutSend review files

Each half uses a flat metal bottom plate, rubber sheet, and clear acrylic top plate.
The corners are square. Four M2 screws pass through the top plate and carrier, then thread into standoffs below the PCB.

| File | Material | Thickness | Process |
| --- | --- | --- | --- |
| `*-bottom-flat.dxf` | 5052 H32 aluminum | .125 in / 3.175 mm | Laser cut, deburr, black anodize |
| `*-plate.dxf` | Clear acrylic | .063 in / 1.6002 mm | Laser cut |
| `*-damping.dxf` | Neoprene | .063 in / 1.6002 mm | Waterjet cut |
| `switch-fit-coupon.dxf` | Same clear acrylic | Same stock as top plates | Test switch fit first |

All dimensions use millimeters. The metal plates have no bends.
The top plate covers the electronics area. Controllers sit face up beneath the carrier PCBs.
USB, power, and reset remain accessible through the open sides.
The two outer bottom key cutouts have at least 4 mm of PCB clearance and 6.5 mm of acrylic edge clearance.

Use this stack at each of the four mounting positions:

| Part, from bottom to top | Dimension | Quantity per half |
| --- | --- | --- |
| Female/female metal M2 standoff | 15 mm length, 4 mm across flats, 5 mm thread depth | 4 |
| Nylon M2 washer below PCB | 0.5 mm thick, 5.5 mm outer diameter | 8, stacked in pairs |
| Carrier PCB | 1.6 mm thick, 2.2 mm hole | 1 |
| Nylon M2 washer above PCB | 0.5 mm thick, 5.5 mm outer diameter | 4 |
| Unthreaded nylon M2 spacer | 3 mm long, 4 mm outer diameter, 2.2 mm bore | 4 |
| Clear top plate | 1.6002 mm thick, 2.2 mm hole | 1 |

[RS PRO 224-0440](https://uk.rs-online.com/web/p/standoffs/2240440) provides the specified metal standoff dimensions.
[Würth 960030010](https://www.we-online.com/components/products/datasheet/960030010.pdf) provides the nylon spacer dimensions.
[Vital Parts WASH028](https://www.vital-parts.co.uk/nylon-washers/29530-wash028) provides the 0.5 mm nylon washers.
Use M2 × 12 mm screws from the top and M2 × 6 mm screws from the bottom, with one 0.5 mm protective washer under each head.
Nominal thread engagement is 3.8 mm above and 2.325 mm below. Confirm the supplied thread depths and lengths before assembly.
Both plates and the PCB have 2.2 mm screw holes. The floor rubber has 5.2 mm body-clearance holes.
The lower standoffs stop beneath the PCB; their bodies no longer pass through it.
Use light screw torque to protect the acrylic. Check that washers clear nearby switches.

The rubber lines the metal floor. Add a separate dielectric liner between the metal and electronics.
Secure each battery with foam and an insulating cover. Keep wires clear of screws and edges.

The coupon has four square holes: 13.9, 14.0, 14.1, and 14.2 mm, from left to right.
Test the actual switches, latch retention, and keycap removal with the supplied material.
Set `switch_cutout` in `case/parameters.scad` from that result, then regenerate.
The default is 14 mm. [Acrylic cutting tolerance](https://sendcutsend.com/materials/acrylic/) requires a physical switch-fit check.
[Neoprene stock](https://sendcutsend.com/materials/neoprene/) also requires a thickness check.

Test plate flex, corner stability, controller clearance, and battery fit on the assembled prototype.
These are review files. No supplier quote or production order has been accepted.

## Material and finish choices

Checked against the supplier catalog on October 8, 2026.
The suggested finish is black anodizing over deburred aluminum, with clear acrylic above it.
This keeps the PCB artwork visible and gives the base a finished surface.

| Choice | Result for this design |
| --- | --- |
| Current .125 in aluminum base | About 107 g per half. Roughly 7.8 times the base bending stiffness of .063 in stock at the same outline and alloy. |
| Optional .063 in aluminum base | Light; about 54 g per half before finishing and hardware. Regenerate models before changing stock. |
| .063 in clear acrylic top | Matches the modeled switch latch thickness. Cut the fit coupon first. |
| .063 in plain neoprene floor | A removable damping layer. It does not suspend the switch plate. |
| .118 in polycarbonate top | Requires redesigned switch retention, screw holes, and routed internal corners. It cannot replace the current plate directly. |

Mass estimates use the exported bottom area and a nominal aluminum density of 2.7 g/cm³.
Stiffness is a thickness-cubed estimate, not a load test or a typing-feel prediction.
The model uses `bottom_thickness = 3.175` for the thicker base.
Keep the acrylic at 1.6002 mm; thicker stock can prevent switch latches from engaging.

[Anodizing](https://sendcutsend.com/services/anodizing/) supports this aluminum stock.
Its minimum hanging hole is 1.6 mm; the four 2.2 mm mounting holes exceed that value before coating.
The supplier must confirm the rack location and finished hole clearance.
[Deburring](https://sendcutsend.com/services/deburring-services/) is preselected for anodized sheet parts.
It can leave tabs, scratches, and sharp edges. Check exposed edges when the parts arrive.
[Tumbling](https://sendcutsend.com/services/tumbling/) can soften edges on .125 in stock, but cannot guarantee an edge radius.
Combining tumbling and anodizing requires a custom quote. The standard finish choice uses deburring and anodizing.

[Clear acrylic](https://sendcutsend.com/materials/acrylic/) is available at .063 in, with a published cutting tolerance of ±.009 in.
[Neoprene](https://sendcutsend.com/materials/neoprene/) is waterjet cut at .063 in with the same published cutting tolerance.
[Polycarbonate](https://sendcutsend.com/materials/polycarbonate/) starts at .118 in and uses CNC routing.
Catalog availability does not mean these uploaded parts have been accepted.

Use four small silicone desk feet per half and metal M2 standoffs with protective washers.
Source these separately unless the supplier confirms the exact hardware.
Do not use foam compression or screw torque to adjust battery clearance.
The floor rubber can reduce vibration, but the rigid standoffs make this a sandwich mount, not a floating gasket mount.
Compare sound, flex, grip, and keycap removal on the prototype before choosing the final material stack.
