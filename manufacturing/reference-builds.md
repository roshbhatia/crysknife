# Reference keyboards

Checked on October 8, 2026. The core circuit follows a common wireless Corne setup.
Corney Island is the closest source match. Its matrix GPIO assignments and power connections match ours exactly.
Other builds support the component choices, but do not validate our exact assembly or case.

| Reference | Shared hardware or technology | Relevant difference |
| --- | --- | --- |
| [Corney Island](https://github.com/ceoloide/corney-island/blob/b7cadab700a4a198a7217d05b6692b787136d043/ergogen/config.yaml) | Ergogen, nice!nano, MX preset, hotswap footprints, battery connector, side power/reset, identical matrix GPIO assignments | Reversible controller jumpers and separate controller cover. Source comparison, not a physical test of our board. |
| [Aurora Corne](https://github.com/splitkb/aurora/tree/6d308f78f806c23072477cb6270ab36dbea230a7/Aurora%20Corne) | Corne plate files and sandwich construction | Different outline and controller positions. Its plates cannot fit our layout directly. |
| [Corne V4 Pro Micro Edition](https://github.com/klouderone/CorneV4ProMicroEdition/tree/7364dfbecb6512b7caeae3d0680cc4e3bdaa93d0) | nice!nano V2, MX hotswap, 1N4148 diodes, machined sockets, power/reset, battery connection | Different controller mount, case, switch parts, and manual assembly. Its QMK instructions do not replace our ZMK firmware. |
| [Josukey](https://github.com/Narkoleptika/josukey/tree/15bfa535a9876d95c239333d4debe53209aa4b46) | Ergogen, nice!nano V2 ZMK overlay, hotswap, JST-PH, battery-to-RAW switch, reset-to-ground | Five-column Choc board with different GPIO assignments. It is a firmware and circuit reference, not an MX plate reference. |
| [ThinkCorney](https://github.com/infused-kim/kb_think_corney/tree/68dcfd41f26583129f97856944a912d72ae558c0) | Ergogen, nice!nano, wireless Corne geometry | Choc/TrackPoint design. The author marks it under development and not ready for production. |
| [Wireless Corne MX build](https://github.com/JoshuaMarkle/corne/blob/b60afe5e0c9b399c32bcc3f23d6e5b25a2765334/doc/Build-Guide.md) | Built 42-key MX keyboard, nice!nano V2, ZMK, hotswap and socketed controllers | Different controller orientation and battery wiring. The published build does not identify our exact header pair. |
| [Corne build guide](https://github.com/devpew/corne-build-guide/tree/771b2b90264cf9ef86a9b828392396274da66fba) | Author reports MX and Choc builds, removable controllers and batteries below the case | Reports poor switch retention and blocked charging ports in purchased cases. These justify our fit coupon and port checks. |

## Circuit comparison

The pinned Corney Island configuration assigns columns to Pro Micro GPIO labels 21, 20, 19, 18, 15, and 14.
Rows use 5, 6, 7, and 8. Our Ergogen parameters use the same ten assignments.
Our ZMK row/column configuration and compiled nice!nano GPIO map match those assignments.
The [controller comparison](controller-reference.json) records all 24 contact positions and pin functions.

| Carrier net | Pro Micro GPIO label |
| --- | --- |
| C0, C1, C2, C3, C4, C5 | 21, 20, 19, 18, 15, 14 |
| R0, R1, R2, R3 | 5, 6, 7, 8 |

The right ZMK overlay reverses column scan order and adds a six-column offset.
This maps the mirrored board to the correct key positions. Each firmware layer contains all 42 bindings.
Use our left/right firmware files; a stock Corne shield can assign different GPIOs.

The pinned wireless Corney Island YAML was fetched again and compared with our current parameters.
Its SHA-256 is `e34803e8275f70fe0089129523e149a12f667e97664d6c479095e28163a3eed0`.
The controller audit also checked the compiled ZMK GPIO mapping against the pinned nice!nano library.

Both Corney Island and our board switch battery positive to RAW and connect battery negative to GND.
Both reset switches connect RST to GND. Charging and regulation remain on the genuine nice!nano V2 module.
The [published Aurora schematic](https://docs.splitkb.com/doc/aurora_corne_rev1.pdf) independently shows the same battery-switch-to-RAW and reset-to-ground arrangement.
It uses different row/column pins on its two halves, so its firmware cannot replace ours without remapping.

Our schematic/netlist check covers every carrier contact, including the diode matrix, battery path, and reset.
KiCad checks the actual routed copper and ground pours. A source match does not replace those checks.
The checks compare all 117 carrier pins per half with the exported schematic netlist, including intentionally unused pins.
Each key has its own diode, with the cathode connected to its row. The firmware scans column to row.
Routing preserves the original footprint pads, holes, layers, and net assignments.
Trace paths differ because our spacing, outline, and controller mounting differ from the reference boards.

The final [KiCad run](https://github.com/roshbhatia/crysknife/actions/runs/37887225267) passed at source `8644c1a3f2dc836ab49acee8cc40efbe70545180`.
Both halves have zero ERC issues, DRC errors, and unconnected copper items.
Each has 53 footprint-library warnings. These reflect local library identifiers, not waived copper violations.
The audit found and fixed a 0.22 mm gap between reset via drills; the corrected gap is 0.30 mm.
Both ground pours are filled, with disconnected islands removed and a controller exclusion on both copper faces.
The checked board hashes and export revision are recorded in [validation.json](../out/validation.json).

## Controller, battery, and case

[Community socket documentation](https://github.com/joric/nrfmicro/wiki/Sockets) includes Mill-Max series 315 receivers and separate round pins.
It also describes several other header types and heights. Matching pitch alone does not establish compatibility.
Our selected HCTL receivers and Mill-Max 350 male strips have drawing-checked diameters, but their full seated height remains unmeasured.
We did not find a documented build with that exact pair in our face-up underside arrangement.

Our 2000 mAh cells follow [nice!nano charging guidance](https://nicekeyboards.com/docs/nice-nano/getting-started/), with BOOST left OPEN for nominal 100 mA because the carrier power switch is rated 300 mA.
They sit below the key field, rather than beneath the controller as in many small-battery builds.
Dimensions, polarity, retention, charging, and radio performance still need measurements.

The custom case uses four standoffs with either printed resin plates or acrylic and aluminum plates.
A removable TPU sleeve provides the walls, floor, and retaining lip.
Our wider lower edge and cutout-clearance guards address the two outer bottom keys.
The neoprene is floor damping. The rigid standoffs do not provide a floating gasket mount.
Published builds do not prove switch latch retention or sound with this material stack.
