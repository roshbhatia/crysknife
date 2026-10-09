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

Both Corney Island and our board switch battery positive to RAW and connect battery negative to GND.
Both reset switches connect RST to GND. Charging and regulation remain on the genuine nice!nano V2 module.
The [published Aurora schematic](https://docs.splitkb.com/doc/aurora_corne_rev1.pdf) independently shows the same battery-switch-to-RAW and reset-to-ground arrangement.
It uses different row/column pins on its two halves, so its firmware cannot replace ours without remapping.

Our schematic/netlist check covers every carrier contact, including the diode matrix, battery path, and reset.
KiCad checks the actual routed copper and ground pours. A source match does not replace those checks.

## Controller, battery, and case

[Community socket documentation](https://github.com/joric/nrfmicro/wiki/Sockets) includes Mill-Max series 315 receivers and separate round pins.
It also describes several other header types and heights. Matching pitch alone does not establish compatibility.
Our selected 315 receivers and 350 male strips have drawing-checked diameters, but their full seated height remains unmeasured.
We did not find a documented build with that exact pair in our face-up underside arrangement.

Our 2000 mAh cells follow [nice!nano charging guidance](https://nicekeyboards.com/docs/nice-nano/getting-started/), including the 500 mA BOOST setting.
They sit below the key field, rather than beneath the controller as in many small-battery builds.
Dimensions, polarity, retention, charging, and radio performance still need measurements.

The custom case uses four standoffs, a 1.6 mm clear acrylic plate, a 1.6 mm neoprene floor, and a 3.175 mm aluminum base.
Our wider lower edge and cutout-clearance guards address the two outer bottom keys.
The neoprene is floor damping. The rigid standoffs do not provide a floating gasket mount.
Published builds do not prove switch latch retention or sound with this material stack.

## Ordering decision

The source comparison supports ordering a small prototype after JLCPCB accepts the exact parts and assembly files.
It does not support calling the keyboard a tested, drop-in product.
Keep the remaining [factory gates](jlcpcb/readiness.json) and [physical tests](physical-tests.md).
Measure the controller stack and test the acrylic coupon before ordering the full case.
